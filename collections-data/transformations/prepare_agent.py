#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

import pandas


"""
Script for preparing agent-data for import to Specify. Run from commandline,
like this:

    prepare_agent.py infile
"""

if __name__ == '__main__':
    
    valid_output_columns = [
        'agent_sourceid',
        'createdbyagent_sourceid',
        'modifiedbyagent_sourceid',
        'parentorganization_sourceid',
        'abbreviation',
        'agenttype',
        'dateofbirth',
        'dateofbirthprecision',
        'dateofdeath',
        'dateofdeathprecision',
        'datetype',
        'email',
        'firstname',
        'guid',
        'initials',
        'interests',
        'jobtitle',
        'lastname',
        'middleinitial',
        'remarks',
        'suffix',
        'timestampcreated',
        'timestampmodified',
        'title',
        'url',
        'version']
    
    help_text = 'Transform agent-data for import to Specify'
    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument(
        '-i',
        dest='infile',
        type=argparse.FileType('r'),
        help='path to input file')


    arguments = parser.parse_args()

    frame = pandas.read_csv(arguments.infile.name)
    frame.columns = frame.columns.str.lower()

    output_columns = list(
        set(frame.columns).intersection(valid_output_columns))

    frame[output_columns].to_csv('agent.csv', index=False)

