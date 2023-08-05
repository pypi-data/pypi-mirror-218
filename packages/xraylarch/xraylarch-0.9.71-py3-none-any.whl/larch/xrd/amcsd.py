#!/usr/bin/env python
"""
AMCIFDB: American Mineralogical CIF database as sqlite3 database/python

Usage:
   amcifdb = AMCIFDB('amcif.db')

add a CIF file:
  amcifdb.add_ciffile('NewFile.cif')

generatt the text of a CIF file from index:
  cif_text = amcifdb.get_ciftext(300)

OK, that looks like 'well, why not just save the CIF files'?

And the answers are that there are simple methods for:
   a) getting the XRD Q points
   b) getting structure factors
   c) getting atomic clustes as for feff files
   d) saving Feff.inp files


"""

import sys
import os
import re
import time
import json
from string import ascii_letters
from base64 import b64encode, b64decode
from collections import namedtuple
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import numpy as np

from sqlalchemy import MetaData, create_engine, func, text, and_, Table
from sqlalchemy import __version__ as sqla_version
from sqlalchemy.sql import select as sqla_select
from sqlalchemy.orm import sessionmaker

try:
    from pymatgen.io.cif import CifParser
    HAS_CIFPARSER = True
except IOError:
    HAS_CIFPARSER = False

from xraydb.chemparser import chemparse

from .amcsd_utils import (make_engine, isAMCSD, put_optarray, get_optarray)
from .xrd_cif import XRDCIF, elem_symbol
from .cif2feff import cif2feffinp
from ..utils import isotime
from ..site_config import user_larchdir
from .. import logger
from larch.utils.strutils import version_ge

CifPublication = namedtuple('CifPublication', ('id', 'journalname', 'year',
                                            'volume', 'page_first',
                                            'page_last', 'authors'))

_CIFDB = None
AMCSD_TRIM = 'amcsd_cif1.db'
AMCSD_FULL = 'amcsd_cif2.db'
SOURCE_URLS = ('https://docs.xrayabsorption.org/databases/',
               'https://millenia.cars.aps.anl.gov/xraylarch/downloads/')

CIF_TEXTCOLUMNS = ('formula', 'compound', 'pub_title', 'formula_title', 'a',
                   'b', 'c', 'alpha', 'beta', 'gamma', 'cell_volume',
                   'crystal_density', 'atoms_sites', 'atoms_x', 'atoms_y',
                   'atoms_z', 'atoms_occupancy', 'atoms_u_iso',
                   'atoms_aniso_label', 'atoms_aniso_u11', 'atoms_aniso_u22',
                   'atoms_aniso_u33', 'atoms_aniso_u12', 'atoms_aniso_u13',
                   'atoms_aniso_u23', 'qdat','url', 'hkls')


def select(*args):
    """wrap sqlalchemy select for version 1.3 and 2.0"""
    # print("SELECT ", args, type(args))
    # print(sqla_version, version_ge(sqla_version, '1.4.0'))
    if version_ge(sqla_version, '1.4.0'):
        return sqla_select(*args)
    else:
        return sqla_select(tuple(args))


def get_nonzero(thing):
    try:
        if len(thing) == 1 and abs(thing[0]) < 1.e-5:
            return None
    except:
        pass
    return thing

def clean_elemsym(sym):
    sx = (sym + ' ')[:2]
    return ''.join([s.strip() for s in sx if s in ascii_letters])


def parse_cif_file(filename):
    """parse ciffile, extract data for 1st listed structure,
    and do some basic checks:
        must have formula
        must have spacegroup
    returns dat, formula, json-dumped symm_xyz
    """
    if not HAS_CIFPARSER:
        raise ValueError("CifParser from pymatgen not available. Try 'pip install pymatgen'.")

    cif = CifParser(filename)
    cifkey = list(cif._cif.data.keys())[0]
    dat = cif._cif.data[cifkey].data

    formula = None
    for formname in ('_chemical_formula_sum', '_chemical_formula_moiety'):
        if formname in dat:
            formula = dat[formname]
    if formula is None and '_atom_site_type_symbol' in dat:
        comps = {}
        complist = dat['_atom_site_type_symbol']
        for c in complist:
            if c not in comps:
                nx = complist.count(c)
                comps[c] = '%s%d' % (c, nx) if nx != 1 else c
        formula = ''.join(comps.values())

    if formula is None:
        raise ValueError(f'Cannot read chemical formula from file {filename:s}')

    # get spacegroup and symmetry
    sgroup_name = dat.get('_symmetry_space_group_name_H-M', None)
    if sgroup_name is None:
        for key, val in dat.items():
            if 'space_group' in key and 'H-M' in key:
                sgroup_name = val

    symm_xyz = dat.get('_space_group_symop_operation_xyz', None)
    if symm_xyz is None:
        symm_xyz = dat.get('_symmetry_equiv_pos_as_xyz', None)
    if symm_xyz is None:
        raise ValueError(f'Cannot read symmetries from file {filename:s}')

    symm_xyz = json.dumps(symm_xyz)
    return dat, formula, symm_xyz


class CifStructure():
    """representation of a Cif Structure
    """

    def __init__(self, ams_id=None, publication=None, mineral=None,
                 spacegroup=None, hm_symbol=None, formula_title=None,
                 compound=None, formula=None, pub_title=None, a=None,
                 b=None, c=None, alpha=None, beta=None, gamma=None, hkls=None,
                 cell_volume=None, crystal_density=None, atoms_sites='<missing>',
                 atoms_aniso_label='<missing>', atoms_x=None, atoms_y=None,
                 atoms_z=None, atoms_occupancy=None, atoms_u_iso=None,
                 atoms_aniso_u11=None, atoms_aniso_u22=None,
                 atoms_aniso_u33=None, atoms_aniso_u12=None,
                 atoms_aniso_u13=None, atoms_aniso_u23=None):

        self.ams_id = ams_id
        self.publication = publication
        self.mineral = mineral
        self.spacegroup = spacegroup
        self.hm_symbol = hm_symbol
        self.formula_title = formula_title
        self.compound = compound
        self.formula = formula
        self.pub_title = pub_title
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.hkls = hkls
        self.cell_volume = cell_volume
        self.crystal_density = crystal_density
        self.atoms_sites = atoms_sites
        self.atoms_aniso_label = atoms_aniso_label
        self.atoms_x = atoms_x
        self.atoms_y = atoms_y
        self.atoms_z = atoms_z
        self.atoms_occupancy = get_nonzero(atoms_occupancy)
        self.atoms_u_iso = get_nonzero(atoms_u_iso)
        self.atoms_aniso_u11 = get_nonzero(atoms_aniso_u11)
        self.atoms_aniso_u22 = get_nonzero(atoms_aniso_u22)
        self.atoms_aniso_u33 = get_nonzero(atoms_aniso_u33)
        self.atoms_aniso_u12 = get_nonzero(atoms_aniso_u12)
        self.atoms_aniso_u13 = get_nonzero(atoms_aniso_u13)
        self.atoms_aniso_u23 = get_nonzero(atoms_aniso_u23)
        self.natoms = 0
        self._xrdcif = None
        self._ciftext = None
        if atoms_sites not in (None, '<missing>'):
            self.natoms = len(atoms_sites)

    def __repr__(self):
        if self.ams_id is None or self.formula is None:
            return '<CifStructure empty>'
        return f'<CifStructure, ams_id={self.ams_id:d}, formula={self.formula:s}>'

    def get_mineralname(self):
        minname = self.mineral.name
        if minname == '<missing>':
            minname =self.formula_title
        if minname == '<missing>':
            minname = 'missing'
        return minname


    @property
    def ciftext(self):
        if self._ciftext is not None:
            return self._ciftext

        out = ['data_global']
        if self.formula_title != '<missing>':
            out.append(f"_amcsd_formula_title '{self.formula_title:s}'")

        if self.mineral.name != '<missing>':
            out.append(f"_chemical_name_mineral '{self.mineral.name:s}'")
        out.append('loop_')
        out.append('_publ_author_name')
        for a in self.publication.authors:
            out.append(f"'{a:s}'")

        out.append(f"_journal_name_full '{self.publication.journalname}'")
        out.append(f"_journal_volume {self.publication.volume}")
        out.append(f"_journal_year {self.publication.year}")
        out.append(f"_journal_page_first {self.publication.page_first}")
        out.append(f"_journal_page_last {self.publication.page_last}")
        out.append('_publ_section_title')
        out.append(';')
        out.append(f"{self.pub_title:s}")
        out.append(';')
        out.append(f"_database_code_amcsd {self.ams_id:07d}")
        if self.compound != '<missing>':
            out.append(f"_chemical_compound_source '{self.compound}'")
        out.append(f"_chemical_formula_sum '{self.formula}'")
        out.append(f"_cell_length_a {self.a}")
        out.append(f"_cell_length_b {self.b}")
        out.append(f"_cell_length_c {self.c}")
        out.append(f"_cell_angle_alpha {self.alpha}")
        out.append(f"_cell_angle_beta {self.beta}")
        out.append(f"_cell_angle_gamma {self.gamma}")
        out.append(f"_cell_volume {self.cell_volume}")
        out.append(f"_exptl_crystal_density_diffrn  {self.crystal_density}")
        out.append(f"_symmetry_space_group_name_H-M '{self.hm_symbol}'")
        out.append('loop_')
        out.append('_space_group_symop_operation_xyz')
        for xyzop in json.loads(self.spacegroup.symmetry_xyz):
            out.append(f"  '{xyzop:s}'")

        atoms_sites = self.atoms_sites
        if atoms_sites not in (None, 'None', '0', '<missing>'):
            out.append('loop_')
            out.append('_atom_site_label')
            out.append('_atom_site_fract_x')
            out.append('_atom_site_fract_y')
            out.append('_atom_site_fract_z')


            natoms = len(atoms_sites)
            atoms_x = self.atoms_x
            atoms_y = self.atoms_y
            atoms_z = self.atoms_z
            atoms_occ = self.atoms_occupancy
            atoms_u_iso = self.atoms_u_iso
            if atoms_occ is not None:
                out.append('_atom_site_occupancy')
            if atoms_u_iso is not None:
                out.append('_atom_site_U_iso_or_equiv')
            for i in range(natoms):
                adat = f"{atoms_sites[i]}   {atoms_x[i]}  {atoms_y[i]}  {atoms_z[i]}"
                if atoms_occ is not None:
                    adat +=  f"  {atoms_occ[i]}"
                if atoms_u_iso is not None:
                    adat +=  f"  {atoms_u_iso[i]}"
                out.append(adat)

            aniso_label = self.atoms_aniso_label
            if aniso_label not in (None, '0', '<missing>'):
                out.append('loop_')
                out.append('_atom_site_aniso_label')
                out.append('_atom_site_aniso_U_11')
                out.append('_atom_site_aniso_U_22')
                out.append('_atom_site_aniso_U_33')
                out.append('_atom_site_aniso_U_12')
                out.append('_atom_site_aniso_U_13')
                out.append('_atom_site_aniso_U_23')
                natoms = len(aniso_label)
                u11 = self.atoms_aniso_u11
                u22 = self.atoms_aniso_u22
                u33 = self.atoms_aniso_u33
                u12 = self.atoms_aniso_u12
                u13 = self.atoms_aniso_u13
                u23 = self.atoms_aniso_u23

                for i in range(natoms):
                    out.append(f"{aniso_label[i]}   {u11[i]}  {u22[i]}  {u33[i]}  {u12[i]}  {u13[i]}  {u23[i]}")

        out.append('')
        out.append('')
        self._ciftext = '\n'.join(out)
        return self.ciftext

    def get_structure_factors(self, wavelength=None, energy=None, qmin=0.1, qmax=9):
        _xrdcif = XRDCIF(text=self.ciftext)
        return  _xrdcif.structure_factors(wavelength=wavelength,
                                          energy=energy,
                                          hkls=self.hkls,
                                          qmin=qmin,
                                          qmax=qmax)


    def get_feffinp(self, absorber, edge=None, cluster_size=8.0, absorber_site=1,
                    with_h=False, version8=True):
        pub = self.publication
        journal = f"{pub.journalname} {pub.volume}, pp. {pub.page_first}-{pub.page_last} ({pub.year:d})"
        authors = ', '.join(pub.authors)
        titles = [f'Structure from AMCSD, AMS_ID: {self.ams_id:d}',
                  f'Mineral Name: {self.mineral.name:s}']

        if not self.formula_title.startswith('<missing'):
            titles.append(f'Formula Title: {self.formula_title}')

        titles.extend([f'Journal: {journal}', f'Authors: {authors}'])
        if not self.pub_title.startswith('<missing'):
            for i, line in enumerate(self.pub_title.split('\n')):
                titles.append(f'Title{i+1:d}: {line}')

        return cif2feffinp(self.ciftext, absorber, edge=edge,
                           cluster_size=cluster_size, with_h=with_h,
                           absorber_site=absorber_site,
                           extra_titles=titles, version8=version8)

    def save_feffinp(self, absorber, edge=None, cluster_size=8.0, absorber_site=1,
                      filename=None, version8=True):
        feff6text = self.get_feffinp(absorber, edge=edge, cluster_size=cluster_size,
                                      absorber_site=absorber_site, version8=version8)
        if filename is None:
            min_name = self.mineral.name.lower()
            if min_name in ('', '<missing>', 'None'):
                name = f'{absorber:s}_{edge:s}_CIF{self.ams_id:06d}'
            else:
                name = f'{absorber:s}_{edge:s}_{min_name:s}_CIF{self.ams_id:06d}'

            bfolder = os.path.join(user_larchdir, 'feff6', name)
            if not os.path.exists(bfolder):
                os.makedirs(bfolder)

            filename = os.path.join(bfolder, 'feff.inp')
        with open(filename, 'w', encoding=sys.getdefaultencoding()) as fh:
            fh.write(feff6text)
        return filename

class AMCSD():
    """
    Database of CIF structure data from the American Mineralogical Crystal Structure Database

       http://rruff.geo.arizona.edu/AMS/amcsd.php

    """
    def __init__(self, dbname=None, read_only=False):
        "connect to an existing database"
        if dbname is None:
            parent, _ = os.path.split(__file__)
            dbname = os.path.join(parent, AMCSD_TRIM)
        if not os.path.exists(dbname):
            raise IOError("Database '%s' not found!" % dbname)

        if not isAMCSD(dbname):
            raise ValueError("'%s' is not a valid AMCSD Database!" % dbname)

        self.connect(dbname, read_only=read_only)

        ciftab = self.tables['cif']
        for colname in CIF_TEXTCOLUMNS:
            if colname not in ciftab.columns and not read_only:
                self.session.execute(text(f'alter table cif add column {colname} text'))
                self.close()
                self.connect(dbname, read_only=read_only)
                time.sleep(0.1)
                self.insert('version', tag=f'with {colname}', date=isotime(),
                            notes=f'added {colname} column to cif table')


    def connect(self, dbname, read_only=False):
        self.dbname = dbname
        self.engine = make_engine(dbname)
        self.conn = self.engine.connect()
        kwargs = {'bind': self.engine, 'autoflush': True, 'autocommit': False}
        self.session = sessionmaker(**kwargs)()
        if read_only:
            def readonly_flush(*args, **kwargs):
                return
            self.session.flush = readonly_flush

        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.tables = self.metadata.tables
        self.cif_elems = None

    def close(self):
        "close session"
        self.session.flush()
        self.session.close()

    def query(self, *args, **kws):
        "generic query"
        return self.session.query(*args, **kws)

    def insert(self, tablename, **kws):
        if isinstance(tablename, Table):
            table = tablename
        else:
            table = self.tables[tablename]
        stmt = table.insert().values(kws)
        out = self.session.execute(stmt)
        self.session.commit()
        self.session.flush()

    def update(self, tablename, whereclause=False, **kws):
        if isinstance(tablename, Table):
            table = tablename
        else:
            table = self.tables[tablename]

        stmt = table.update().where(whereclause).values(kws)
        out = self.session.execute(stmt)
        self.session.commit()
        self.session.flush()

    def execall(self, query):
        return self.session.execute(query).fetchall()

    def execone(self, query):
        results = self.session.execute(query).fetchone()
        if results is None or len(results) < 1:
            return None
        return results

    def get_all(self, tablename):
        return self.execall(self.tables[tablename].select())


    def get_version(self, long=False, with_history=False):
        """
        return sqlite3 database and python library version numbers

        Parameters:
            long (bool): show timestamp and notes of latest version [False]
            with_history (bool): show complete version history [False]

        Returns:
            string: version information
        """
        out = []
        rows = self.get_all('version')
        if not with_history:
            rows = rows[-1:]
        if long or with_history:
            for row in rows:
                out.append(f"AMCSD Version: {row.tag} [{row.date}] '{row.notes}'")
            out.append(f"Python Version: {__version__}")
            out = "\n".join(out)
        elif rows is None:
            out = f"AMCSD Version: unknown, Python Version: {__version__}"
        else:
            out = f"AMCSD Version: {rows[0].tag}, Python Version: {__version__}"
        return out

    def _get_tablerow(self, table, name, add=True):
        tab = self.tables[table]
        if '"' in name:
            name = name.replace('"', '\"')
        rows = self.execall(tab.select().where(tab.c.name==name))
        if len(rows) == 0:
            if not add:
                return None
            self.insert(tab, name=name)
            rows = self.execall(tab.select().where(tab.c.name==name))
        return rows[0]

    def get_spacegroup(self, hm_name):
        """get row from spacegroups table by HM notation.  See add_spacegroup()
        """
        tab = self.tables['spacegroups']
        rows = self.execall(tab.select().where(tab.c.hm_notation==hm_name))
        if len(rows) >0:
            return rows[0]
        return None


    def add_spacegroup(self, hm_name, symmetry_xyz, category=None):
        """add entry to spacegroups table, including HM notation and CIF symmetry operations
        """
        sg = self.get_spacegroup(hm_name)
        if sg is not None and sg.symmetry_xyz == symmetry_xyz:
            return sg

        args = {'hm_notation': hm_name, 'symmetry_xyz': symmetry_xyz}
        if category is not None:
            args['category'] = category
        self.insert('spacegroups', **args)
        return self.get_spacegroup(hm_name)

    def get_publications(self, journalname=None, year=None, volume=None,
                        page_first=None, page_last=None, id=None):
        """get rows from publications table by journalname, year (required)
        and optionally volume, page_first, or page_last.
        """
        tab = self.tables['publications']

        args = []
        if journalname is not None:
            args.append(func.lower(tab.c.journalname)==journalname.lower())
        if year is not None:
            args.append(tab.c.year==int(year))
        if volume is not None:
            args.append(tab.c.volume==str(volume))
        if page_first is not None:
            args.append(tab.c.page_first==str(page_first))
        if page_last is not None:
            args.append(tab.c.page_last==str(page_last))
        if id is not None:
            args.append(tab.c.id==id)

        rows = self.execall(tab.select().where(and_(*args)))
        if len(rows) > 0:
            out = []
            authtab = self.tables['authors']
            patab = self.tables['publication_authors']
            for row in rows:
                q = select(authtab.c.name).where(and_(authtab.c.id==patab.c.author_id,
                                                      patab.c.publication_id==row.id))
                authors = tuple([i[0] for i in self.execall(q)])
                out.append(CifPublication(row.id, row.journalname, row.year,
                                          row.volume, row.page_first,
                                          row.page_last, authors))
            return out
        return None


    def add_publication(self, journalname, year, authorlist, volume=None,
                        page_first=None, page_last=None, with_authors=True):

        args = dict(journalname=journalname, year=year)
        if volume is not None:
            args['volume']  = volume
        if page_first is not None:
            args['page_first'] = page_first
        if page_last is not None:
            args['page_last'] = page_last

        self.insert('publications', **args)
        self.session.flush()
        pub = self.get_publications(journalname, year, volume=volume,
                                    page_first=page_first,
                                    page_last=page_last)[0]

        if with_authors:
            for name in authorlist:
                auth = self._get_tablerow('authors', name, add=True)
                self.insert('publication_authors',
                            publication_id=pub.id, author_id=auth.id)
        return pub

    def add_cifdata(self, cif_id, mineral_id, publication_id,
                    spacegroup_id, formula=None, compound=None,
                    formula_title=None, pub_title=None, a=None, b=None,
                    c=None, alpha=None, beta=None, gamma=None, url='',
                    cell_volume=None, crystal_density=None,
                    atoms_sites=None, atoms_x=None, atoms_y=None,
                    atoms_z=None, atoms_occupancy=None, atoms_u_iso=None,
                    atoms_aniso_label=None, atoms_aniso_u11=None,
                    atoms_aniso_u22=None, atoms_aniso_u33=None,
                    atoms_aniso_u12=None, atoms_aniso_u13=None,
                    atoms_aniso_u23=None, with_elements=True):

        self.insert('cif', id=cif_id, mineral_id=mineral_id,
                    publication_id=publication_id,
                    spacegroup_id=spacegroup_id,
                    formula_title=formula_title, pub_title=pub_title,
                    formula=formula, compound=compound, url=url, a=a, b=b,
                    c=c, alpha=alpha, beta=beta, gamma=gamma,
                    cell_volume=cell_volume,
                    crystal_density=crystal_density,
                    atoms_sites=atoms_sites, atoms_x=atoms_x,
                    atoms_y=atoms_y, atoms_z=atoms_z,
                    atoms_occupancy=atoms_occupancy,
                    atoms_u_iso=atoms_u_iso,
                    atoms_aniso_label=atoms_aniso_label,
                    atoms_aniso_u11=atoms_aniso_u11,
                    atoms_aniso_u22=atoms_aniso_u22,
                    atoms_aniso_u33=atoms_aniso_u33,
                    atoms_aniso_u12=atoms_aniso_u12,
                    atoms_aniso_u13=atoms_aniso_u13,
                    atoms_aniso_u23=atoms_aniso_u23)

        if with_elements:
            for element in chemparse(formula).keys():
                self.insert('cif_elements', cif_id=cif_id, element=element)
        return self.get_cif(cif_id)


    def add_ciffile(self, filename, cif_id=None, url='', debug=False):

        if not HAS_CIFPARSER:
            raise ValueError("CifParser from pymatgen not available. Try 'pip install pymatgen'.")
        try:
            dat, formula, symm_xyz = parse_cif_file(filename)
        except:
            raise ValueError(f"unknown error trying to parse CIF file: {filename}")

        # compound
        compound = '<missing>'
        for compname in ('_chemical_compound_source',
                         '_chemical_name_systematic',
                         '_chemical_name_common'):
            if compname in dat:
                compound = dat[compname]


        # spacegroup
        sgroup_name = dat.get('_symmetry_space_group_name_H-M', None)
        if sgroup_name is None:
            for key, val in dat.items():
                if 'space_group' in key and 'H-M' in key:
                    sgroup_name = val

        sgroup = self.get_spacegroup(sgroup_name)
        if sgroup is not None and sgroup.symmetry_xyz != symm_xyz:
            for i in range(1, 11):
                tgroup_name = sgroup_name + f' %var{i:d}%'
                sgroup = self.get_spacegroup(tgroup_name)
                if sgroup is None or sgroup.symmetry_xyz == symm_xyz:
                    sgroup_name = tgroup_name
                    break
        if sgroup is None:
            sgroup = self.add_spacegroup(sgroup_name, symm_xyz)

        min_name = '<missing>'
        for mname in ('_chemical_name_mineral',
                       '_chemical_name_common'):
            if mname in dat:
                min_name = dat[mname]
        mineral = self._get_tablerow('minerals', min_name)

        # get publication data (including ISCD style of 'citation' in place of 'journal' )
        pubdict = dict(journalname=dat.get('_journal_name_full', None),
                       year=dat.get('_journal_year', None),
                       volume=dat.get('_journal_volume', None),
                       page_first=dat.get('_journal_page_first', None),
                       page_last=dat.get('_journal_page_last', None))

        for key, alt, dval in (('journalname', 'journal_full', 'No Journal'),
                               ('year', None, -1),
                               ('volume', 'journal_volume', 0),
                               ('page_first', None, 0),
                               ('page_last', None, 0)):
            if pubdict[key] is None:
                if alt is None:
                    alt = key
                alt = '_citation_%s' % alt
                pubdict[key] = dat.get(alt, [dval])[0]
        authors = dat.get('_publ_author_name', None)
        if authors is None:
            authors = dat.get('_citation_author_name', ['Anonymous'])

        pubs = self.get_publications(**pubdict)
        if pubs is None:
            pub = self.add_publication(pubdict['journalname'],
                                       pubdict['year'], authors,
                                       volume=pubdict['volume'],
                                       page_first=pubdict['page_first'],
                                       page_last=pubdict['page_last'])
        else:
            pub = pubs[0]

        density = dat.get('_exptl_crystal_density_meas', None)
        if density is None:
            density = dat.get('_exptl_crystal_density_diffrn', -1.0)

        if cif_id is None:
            cif_id = dat.get('_database_code_amcsd', None)
            if cif_id is None:
                cif_id = dat.get('_cod_database_code', None)
            if cif_id is None:
                cif_id = self.next_cif_id()
        cif_id = int(cif_id)

        # check again for this cif id (must match CIF AMS id and formula
        tabcif = self.tables['cif']
        this = self.execone(select(tabcif.c.id, tabcif.c.formula
                               ).where(tabcif.c.id==int(cif_id)))
        if this is not None:
            _cid, _formula = this
            if formula.replace(' ', '') == _formula.replace(' ', ''):
                return cif_id
            else:
                cif_id = self.next_cif_id()

        if debug:
            print("##CIF Would add Cif Data !" )
            print(cif_id, mineral.id, pub.id, sgroup.id)
            print("##CIF formuala / compound: ", formula, compound)
            print("titles: ",
                  dat.get('_amcsd_formula_title', '<missing>'),
                  dat.get('_publ_section_title', '<missing>'))
            print("##CIF atom sites :", json.dumps(dat['_atom_site_label']))
            print("##CIF locations : ",
                  put_optarray(dat, '_atom_site_fract_x'),
                  put_optarray(dat, '_atom_site_fract_y'),
                  put_optarray(dat, '_atom_site_fract_z'),
                  put_optarray(dat, '_atom_site_occupancy'),
                  put_optarray(dat, '_atom_site_U_iso_or_equiv'))
            print("##CIF aniso label : ",
                  json.dumps(dat.get('_atom_site_aniso_label', '<missing>')))
            print("##CIF aniso : ",
                  put_optarray(dat, '_atom_site_aniso_U_11'),
                  put_optarray(dat, '_atom_site_aniso_U_22'),
                  put_optarray(dat, '_atom_site_aniso_U_33'),
                  put_optarray(dat, '_atom_site_aniso_U_12'),
                  put_optarray(dat, '_atom_site_aniso_U_13'),
                  put_optarray(dat, '_atom_site_aniso_U_23'))
            print('##CIF cell data: ', dat['_cell_length_a'],
                  dat['_cell_length_b'],
                  dat['_cell_length_c'],
                  dat['_cell_angle_alpha'],
                  dat['_cell_angle_beta'],
                  dat['_cell_angle_gamma'])
            print("##CIF volume/ density ", dat.get('_cell_volume', -1),  density)
            print("##CIF  url : ", type(url), url)

        self.add_cifdata(cif_id, mineral.id, pub.id, sgroup.id,
                         formula=formula, compound=compound,
                         formula_title=dat.get('_amcsd_formula_title', '<missing>'),
                         pub_title=dat.get('_publ_section_title', '<missing>'),
                         atoms_sites=json.dumps(dat['_atom_site_label']),
                         atoms_x=put_optarray(dat, '_atom_site_fract_x'),
                         atoms_y=put_optarray(dat, '_atom_site_fract_y'),
                         atoms_z=put_optarray(dat, '_atom_site_fract_z'),
                         atoms_occupancy=put_optarray(dat, '_atom_site_occupancy'),
                         atoms_u_iso=put_optarray(dat, '_atom_site_U_iso_or_equiv'),
                         atoms_aniso_label=json.dumps(dat.get('_atom_site_aniso_label', '<missing>')),
                         atoms_aniso_u11=put_optarray(dat, '_atom_site_aniso_U_11'),
                         atoms_aniso_u22=put_optarray(dat, '_atom_site_aniso_U_22'),
                         atoms_aniso_u33=put_optarray(dat, '_atom_site_aniso_U_33'),
                         atoms_aniso_u12=put_optarray(dat, '_atom_site_aniso_U_12'),
                         atoms_aniso_u13=put_optarray(dat, '_atom_site_aniso_U_13'),
                         atoms_aniso_u23=put_optarray(dat, '_atom_site_aniso_U_23'),
                         a=dat['_cell_length_a'],
                         b=dat['_cell_length_b'],
                         c=dat['_cell_length_c'],
                         alpha=dat['_cell_angle_alpha'],
                         beta=dat['_cell_angle_beta'],
                         gamma=dat['_cell_angle_gamma'],
                         cell_volume=dat.get('_cell_volume', -1),
                         crystal_density=density,
                         url=url)
        return cif_id

    def get_cif(self, cif_id, as_strings=False):
        """get Cif Structure object """
        tab = self.tables['cif']

        cif = self.execone(tab.select().where(tab.c.id==cif_id))
        if cif is None:
            return

        tab_pub  = self.tables['publications']
        tab_auth = self.tables['authors']
        tab_pa   = self.tables['publication_authors']
        tab_min  = self.tables['minerals']
        tab_sp   = self.tables['spacegroups']
        mineral  = self.execone(tab_min.select().where(tab_min.c.id==cif.mineral_id))
        sgroup   = self.execone(tab_sp.select().where(tab_sp.c.id==cif.spacegroup_id))
        hm_symbol = sgroup.hm_notation
        if '%var' in hm_symbol:
            hm_symbol = hm_symbol.split('%var')[0]

        pub = self.get_publications(id=cif.publication_id)[0]

        out = CifStructure(ams_id=cif_id, publication=pub,
                           mineral=mineral, spacegroup=sgroup,
                           hm_symbol=hm_symbol)

        for attr in ('formula_title', 'compound', 'formula', 'pub_title'):
            setattr(out, attr, getattr(cif, attr, '<missing>'))
        for attr in ('a', 'b', 'c', 'alpha', 'beta', 'gamma',
                     'cell_volume', 'crystal_density'):
            val = getattr(cif, attr, '-1')
            if not as_strings:
                if val is not None:
                    if '(' in val:
                        val = val.split('(')[0]
                    if ',' in val and '.' not in val:
                        val = val.replace(',', '.')
                    try:
                        val = float(val)
                    except:
                        pass
            setattr(out, attr, val)

        for attr in ('atoms_sites', 'atoms_aniso_label'):
            val = getattr(cif, attr, '<missing>')
            val = '<missing>' if val in (None, '<missing>') else json.loads(val)
            setattr(out, attr, val)

        if out.atoms_sites not in (None, '<missing>'):
            out.natoms = len(out.atoms_sites)
            for attr in ('atoms_x', 'atoms_y', 'atoms_z', 'atoms_occupancy',
                         'atoms_u_iso', 'atoms_aniso_u11', 'atoms_aniso_u22',
                         'atoms_aniso_u33', 'atoms_aniso_u12',
                         'atoms_aniso_u13', 'atoms_aniso_u23'):
                try:
                    val =  get_optarray(getattr(cif, attr))
                    if val == '0':
                        val = None
                    elif not as_strings:
                        tmp = []
                        for i in range(len(val)):
                            v = val[i]
                            if v in ('?', '.'):
                                v = 2.
                            else:
                                v = float(v)
                            tmp.append(v)
                        val = tmp
                    setattr(out, attr, val)
                except:
                    print(f"could not parse CIF entry for {cif_id} '{attr}': {val} ")

        out.qval = None
        if cif.qdat is not None:
            out.qval = np.unpackbits(np.array([int(b) for b in b64decode(cif.qdat)],
                                              dtype='uint8'))
        out.hkls = None
        if hasattr(cif, 'hkls'):
           if cif.hkls is not None:
               tmp = np.array([int(i) for i in b64decode(cif.hkls)])
               out.hkls = tmp.reshape(len(tmp)//3, 3)

        return out

    def next_cif_id(self):
        """next available CIF ID > 200000 that is not in current table"""
        max_id = 200_000
        tabcif = self.tables['cif']
        for row in self.execall(select(tabcif.c.id).where(tabcif.c.id>200000)):
            if row[0] > max_id:
                max_id = row[0]
        return max_id + 1


    def all_minerals(self):
        names = []
        for row in self.get_all('minerals'):
            if row.name not in names:
                names.append(row.name)
        return names

    def all_authors(self):
        names = []
        for row in self.get_all('authors'):
            if row.name not in names:
                names.append(row.name)
        return names

    def all_journals(self):
        names = []
        for row in self.get_all('publications'):
            if row.journalname not in names:
                names.append(row.journalname)
        return names

    def get_cif_elems(self):
        if self.cif_elems is None:
            out = {}
            for row in self.get_all('cif_elements'):
                cifid = int(row.cif_id)
                if cifid not in out:
                    out[cifid] = []
                if row.element not in out[cifid]:
                    out[cifid].append(row.element)

            self.cif_elems = out
        return self.cif_elems


    def find_cifs(self, id=None, mineral_name=None, author_name=None,
                  journal_name=None, contains_elements=None,
                  excludes_elements=None, strict_contains=False,
                  full_occupancy=False, max_matches=1000):
        """return list of CIF Structures matching mineral, publication, or elements
        """
        if id is not None:
            thiscif = self.get_cif(id)
            if thiscif is not None:
                return [thiscif]

        tabcif = self.tables['cif']
        tabmin = self.tables['minerals']
        tabpub = self.tables['publications']
        tabaut = self.tables['authors']
        tab_ap = self.tables['publication_authors']
        tab_ce = self.tables['cif_elements']

        matches = []
        t0 = time.time()
        if mineral_name is None:
            mineral_name = ''
        mineral_name = mineral_name.strip()

        if mineral_name not in (None, '') and ('*' in mineral_name or
                                               '^' in mineral_name or
                                               '$' in mineral_name):
            pattern = mineral_name.replace('*', '.*').replace('..*', '.*')
            matches = []
            for row in self.get_all('minerals'):
                if re.search(pattern, row.name, flags=re.IGNORECASE) is not None:
                    query = select(tabcif.c.id).where(tabcif.c.mineral_id==row.id)
                    for m in [row[0] for row in self.execall(query)]:
                        if m not in matches:
                           matches.append(m)

            if journal_name not in (None, ''):
                pattern = journal_name.replace('*', '.*').replace('..*', '.*')
                new_matches = []
                for c in matches:
                    pub_id = self.execone(select(tabcif.c.publication_id
                                             ).where(tabcif.c.id==c))
                    this_journal = self.execone(select(tabpub.c.journalname
                                                   ).where(tabpub.c.id==pub_id))
                    if re.search(pattern,  this_journal, flags=re.IGNORECASE) is not None:
                        new_matches.append[c]
                matches = new_matches


        else: # strict mineral name or no mineral name
            args = []
            if mineral_name not in (None, ''):
                args.append(func.lower(tabmin.c.name)==mineral_name.lower())
                args.append(tabmin.c.id==tabcif.c.mineral_id)

            if journal_name not in (None, ''):
                args.append(func.lower(tabpub.c.journalname)==journal_name.lower())
                args.append(tabpub.c.id==tabcif.c.publication_id)

            if author_name not in (None, ''):
                args.append(func.lower(tabaut.c.name)==author_name.lower())
                args.append(tabcif.c.publication_id==tab_ap.c.publication_id)
                args.append(tabaut.c.id==tab_ap.c.author_id)

            query = select(tabcif.c.id)
            if len(args) > 0:
                query = select(tabcif.c.id).where(and_(*args))
            matches = [row[0] for row in self.execall(query)]
            matches = list(set(matches))
        #
        cif_elems = self.get_cif_elems()
        if contains_elements is not None:
            for el in contains_elements:
                new_matches = []
                for row in matches:
                    if row in cif_elems and el in cif_elems[row]:
                        new_matches.append(row)
                matches = new_matches

            if strict_contains:
                excludes_elements = elem_symbol[:]
                for c in contains_elements:
                    if c in excludes_elements:
                        excludes_elements.remove(c)
        if excludes_elements is not None:
            bad = []
            for el in excludes_elements:
                for row in matches:
                    if el in cif_elems[row] and row not in bad:
                        bad.append(row)
            for row in bad:
                matches.remove(row)


        if full_occupancy:
            good = []
            for cif_id in matches:
                cif = self.execone(tabcif.select().where(tabcif.c.id==cif_id))
                occ = get_optarray(getattr(cif, 'atoms_occupancy'))
                if occ in ('0', 0, None):
                    good.append(cif_id)
                else:
                    try:
                        min_wt = min([float(x) for x in occ])
                    except:
                        min_wt = 0
                    if min_wt > 0.96:
                        good.append(cif_id)
            matches = good

        if len(matches) > max_matches:
            matches = matches[:max_matches]
        return [self.get_cif(cid) for cid in matches]

    def set_hkls(self, cifid, hkls):
        hkldat = b64encode(bytes(hkls[:].flatten().tolist()))
        ctab = self.tables['cif']
        self.update(ctab, whereclause=(ctab.c.id == cifid), hkls=hkldat)

def get_amcsd(download_full=True, timeout=30):
    """return instance of the AMCSD CIF Database

    Returns:
        AMCSD database
    Example:

    """
    global _CIFDB
    if _CIFDB is not None:
        return _CIFDB

    dbfull = os.path.join(user_larchdir, AMCSD_FULL)
    if os.path.exists(dbfull):
        _CIFDB = AMCSD(dbfull)
        return _CIFDB
    t0 = time.time()
    if download_full:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        for src in SOURCE_URLS:
            url = f"{src:s}/{AMCSD_FULL:s}"
            req = requests.get(url, verify=True, timeout=timeout)
            if req.status_code == 200:
                break
        if req.status_code == 200:
            with open(dbfull, 'wb') as fh:
                fh.write(req.content)
            print("Downloaded  %s : %.2f sec" % (dbfull, time.time()-t0))
            time.sleep(0.25)
            _CIFDB = AMCSD(dbfull)
            return _CIFDB
    # finally download of full must have failed
    return AMCSD()

def get_cif(ams_id):
    """
    get CIF Structure by AMS ID
    """
    db = get_amcsd()
    return db.get_cif(ams_id)

def find_cifs(mineral_name=None, journal_name=None, author_name=None,
              contains_elements=None, excludes_elements=None,
              strict_contains=False, full_occupancy=False):

    """
    return a list of CIF Structures matching a set of criteria:

     mineral_name:  case-insensitive match of mineral name
     journal_name:
     author_name:
     containselements:  list of atomic symbols required to be in structure
     excludes_elements:  list of atomic symbols required to NOT be in structure
     strict_contains:    `contains_elements` is complete -- no other elements


    """
    db = get_amcsd()
    return db.find_cifs(mineral_name=mineral_name,
                        journal_name=journal_name,
                        author_name=author_name,
                        contains_elements=contains_elements,
                        excludes_elements=excludes_elements,
                        strict_contains=strict_contains,
                        full_occupancy=full_occupancy)
