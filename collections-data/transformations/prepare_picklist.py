#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

import pandas


"""
Script for preparing picklist data. Writes output to picklist.csv and
picklistitem.csv.
Run from commandline, like this:

    prepare_picklist.py filename
"""

if __name__ == '__main__':

    help_text = 'Transform picklist values for import to Specify'
    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument(
        '-i',
        dest='infile',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='path to file with picklist data')

    parser.add_argument(
        '-n', '--names',
        type=str,
        nargs='*',
        help='names of picklist(s) to use')

    arguments = parser.parse_args()


    picklist_columns = ['picklist_sourceid', 'name']
    picklistitem_columns = [
        'picklistitem_sourceid', 'picklist_sourceid', 'title', 'value']

    value_lists = pandas.read_csv(arguments.infile, dtype='unicode')
    value_lists[value_lists.IsRecommended=='yes']
        
    if len(value_lists) > 0:
        value_lists['dwValueListName'] = (
            'dw' + value_lists.ValueListName.fillna(''))
        picklist = pandas.DataFrame()
        picklist['name'] = pandas.unique(value_lists.dwValueListName)
        picklist['picklist_sourceid'] = range(1, len(picklist) + 1)

        if arguments.names:
            value_lists = value_lists[
                value_lists.ValueListName.isin(arguments.names)]
        value_lists = value_lists.merge(
            picklist[['name', 'picklist_sourceid']], how='left',
            left_on='dwValueListName', right_on='name')
    
    picklistitem = pandas.DataFrame()
    picklistitem['picklist_sourceid'] = value_lists.picklist_sourceid
    picklistitem['name'] = value_lists.ValueListName
    picklistitem['title'] = value_lists.ValueListName
    picklistitem['value'] = value_lists.Value
    picklistitem['picklistitem_sourceid'] = range(1, len(picklistitem) + 1)

    picklist[picklist_columns].to_csv('picklist.csv', index=False)
    picklistitem[picklistitem_columns].to_csv('picklistitem.csv', index=False)
