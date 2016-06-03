#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

import numpy
import pandas


"""
Script for preparing taxon data. Writes output to taxon.csv.
Run from commandline, like this:

    prepare_taxon.py treedef_filename taxon_filename
"""

if __name__ == '__main__':

    help_text = 'Transform taxon data import to Specify'
    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument(
        dest='treedefitems',
        type=argparse.FileType('r'),
        help='path to file with tree definition items')

    parser.add_argument(
        dest='taxondata',
        type=argparse.FileType('r'),
        help='path to file with the taxon data')

    arguments = parser.parse_args()

    rank_names = {
        'root' : 'Life',
        'Division': 'Phylum',
        'SpecificEpithet': 'Species',
        'InfraspecificEpithet': 'Subspecies'}

    output_columns = [
        'taxon_sourceid',
        'parent_sourceid',
        'name',
        'taxontreedefitem_sourceid']

    treedefitems = pandas.read_csv(arguments.treedefitems, dtype='unicode')

    taxondata = pandas.read_csv(arguments.taxondata, dtype='unicode')

    # Add root node
    root_id = min(taxondata.ID.astype(int) - 1)
    taxondata.loc[taxondata.ParentID.isnull(), 'ParentID'] = root_id

    number_to_add = 1 - root_id
    taxondata.ID = taxondata.ID.astype(int) + number_to_add
    taxondata.ParentID = taxondata.ParentID.astype(int) + number_to_add
    
    taxondata = taxondata.append({
        'ID': root_id + number_to_add,
        'ParentID': numpy.nan,
        'Name': 'Life',
        'Category': 'Life'}, ignore_index=True)

    taxondata = taxondata[['ID', 'ParentID', 'Name', 'Category']]

    taxondata['Category'] = taxondata['Category'].replace(rank_names)

    treedefitems_merge = treedefitems[[
            'taxontreedefitem_sourceid',
            'name']].rename(columns={'name': 'Category'})
    taxon = taxondata.merge(
        treedefitems_merge, how='inner', on='Category')

    taxon.rename(columns={
        'Name': 'name',
        'ID': 'taxon_sourceid',
        'ParentID': 'parent_sourceid'}, inplace=True)

    taxon.taxon_sourceid = taxon.taxon_sourceid.astype(int)
    taxon.sort_values(by='taxon_sourceid', inplace=True)

    taxon[output_columns].to_csv(
        'taxon.csv', index=False, float_format='%g')
