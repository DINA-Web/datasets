#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

import numpy
import pandas


"""
Script for preparing geography data. Writes output to geography.csv.
Run from commandline, like this:

    prepare_geography.py treedef_filename basetree_filename [--sweden filename]
"""


def append_country_geography(frame, country_frame, country):
    country_id = frame.ID[frame.Name==country].values[0]
    country_frame.ID = (
        country_frame.ID.astype(int) + max(frame.ID.astype('int')))
    country_frame.ParentID = (
        country_frame.ID.astype(int).fillna(0) +
        max(frame.ID.astype(int)))
    country_frame.loc[country_frame.Name==country, 'ID'] = country_id
    frame = pandas.concat([frame, country_frame])
    frame.drop_duplicates(subset='ID', inplace=True)
    return frame


if __name__ == '__main__':

    help_text = 'Transform geography data import to Specify'
    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument(
        dest='treedefitems',
        type=argparse.FileType('r'),
        help='path to file with tree definition items')

    parser.add_argument(
        dest='basetree',
        type=argparse.FileType('r'),
        help='path to file with the base tree')

    parser.add_argument(
        '--denmark',
        dest='denmark',
        type=argparse.FileType('r'),
        metavar='filename',
        help='path to file with geography for Denmark')

    parser.add_argument(
        '--finland',
        dest='finland',
        type=argparse.FileType('r'),
        metavar='filename',
        help='path to file with geography for Finland')

    parser.add_argument(
        '--norway',
        dest='norway',
        type=argparse.FileType('r'),
        metavar='filename',
        help='path to file with geography for Norway')

    parser.add_argument(
        '--sweden',
        dest='sweden',
        type=argparse.FileType('r'),
        metavar='filename',
        help='path to file with geography for Sweden')


    arguments = parser.parse_args()

    rank_names = {
        'L0 earth' : 'Earth',
        'L1 continent': 'Continent',
        'L2 region': 'Region',
        'L3 area': 'Area',
        'L4 country': 'Country',
        'L5 province': 'State',
        'L6 district': 'County'}

    output_columns = [
        'geography_sourceid',
        'parent_sourceid',
        'name',
        'geographytreedefitem_sourceid']

    treedefitems = pandas.read_csv(arguments.treedefitems, dtype='unicode')

    basetree = pandas.read_csv(arguments.basetree, dtype='unicode')

    # Add root node
    root_id = min(basetree.ID.astype(int) - 1)
    basetree.loc[basetree.ParentID.isnull(), 'ParentID'] = root_id
    
    number_to_add = 1 - root_id
    basetree.ID = basetree.ID.astype(int) + number_to_add
    basetree.ParentID = basetree.ParentID.astype(int) + number_to_add
    
    basetree = basetree.append({
        'ID': root_id + number_to_add,
        'ParentID': numpy.nan,
        'Name': 'Earth',
        'Category': 'L0 earth'}, ignore_index=True)

    basetree = basetree[['ID', 'ParentID', 'Name', 'Category']]

    if arguments.denmark:
        geo_den = pandas.read_csv(arguments.denmark, dtype='unicode')
        geo_den = geo_den[['ID', 'ParentID', 'Name', 'Category']]
        basetree = append_country_geography(basetree, geo_den, 'Denmark')

    if arguments.finland:
        geo_fin = pandas.read_csv(arguments.finland, dtype='unicode')
        geo_fin = geo_fin[['ID', 'ParentID', 'Name', 'Category']]
        basetree = append_country_geography(basetree, geo_fin, 'Finland')

    if arguments.norway:
        geo_nor = pandas.read_csv(arguments.norway, dtype='unicode')
        geo_nor = geo_nor[['ID', 'ParentID', 'Name', 'Category']]
        basetree = append_country_geography(basetree, geo_nor, 'Norway')

    if arguments.sweden:
        geo_swe = pandas.read_csv(arguments.sweden, dtype='unicode')
        geo_swe = geo_swe[['ID', 'ParentID', 'Name', 'Category']]
        basetree = append_country_geography(basetree, geo_swe, 'Sweden')

    basetree['Category'] = basetree['Category'].replace(rank_names)

    treedefitems_merge = treedefitems[[
            'geographytreedefitem_sourceid',
            'name']].rename(columns={'name': 'Category'})
    geography = basetree.merge(
        treedefitems_merge, how='inner', on='Category')

    geography.rename(columns={
        'Name': 'name',
        'ID': 'geography_sourceid',
        'ParentID': 'parent_sourceid'}, inplace=True)

    geography.geography_sourceid = geography.geography_sourceid.astype(int)
    geography.sort_values(by='geography_sourceid', inplace=True)

    geography.parent_sourceid = (
        geography.parent_sourceid.dropna().astype(int).astype(str))
    geography[output_columns].to_csv('geography.csv', index=False, float='%g')
