#!/usr/bin/env python

'''
Pre Upload Name Checker - P.U.N.C.
Kurt Strecker

updated 01/07/2018
v 0.1.2 - beta version ready for on set testing
update notes 1.1
    1. added optional -s flag at end of terminal arguments to enable seraching CSV by shoot date
    2. simplified argument for command line date lookup to accept MM/DD or even just MMDD for faster typing
    3. added some additional reportout information for missing files

update notes 1.2
    1. added a -a flag, to be followed by a date, to check for Shoot date AND a different Turn in date

update notes 1.3
    1. added a function clean_turn_in_date() to fix an formatting errors for Turn In Date column of the turn in sheet 
    to deal with inconsistancies eg: sometimes it's input as 01/05/2017 and sometimes 1/5/2017
    2. added a function to clean shoot-dates clean_shoot_date() to account for photographer variation in shoot date entries
    ex 1-15, 1/15, and 01/15 are all commonly seen.
'''

import csv
import re
import os
import argparse
import datetime

# (0, 'CATEGORY')
# (1, 'Pictures')
# (2, 'STATUS')
# (3, 'GROUP ID')
# (4, 'COORD')
# (5, 'Look #')
# (6, 'Vendor')
# (7, 'SKU or META')
# (8, 'Style #')
# (9, 'Description')
# (10, 'Feature Color')
# (11, 'Alt Colors')
# (12, 'Alt View #1')
# (13, 'Alt View #2')
# (14, 'Alt View #3')
# (15, 'Alt View #4')
# (16, 'Detail Full/Crop')
# (17, 'STUDIO Comments')
# (18, 'Turn-in Date')
# (19, 'Web Book Date')
# (20, 'Pub Date')
# (21, 'Shop the Look List')
# (22, 'MERCH OPS/PROD Comments (VIDEO)')
# (23, 'Type/Age Range')
# (24, 'Photo Studio Comments')
# (25, 'R')
# (26, 'STL')
# (27, 'A1')
# (28, 'A2')
# (29, 'A3')
# (30, 'A4')
# (31, 'C2')
# (32, 'C3')
# (33, 'V')
# (34, 'SHOOT DATE')
# (35, 'STATUS')
# (36, '# Feature Colors Shot')
# (37, '# Alt Colors Shot')
# (38, ' PHOTO NOTES')
# (39, 'RT OP')
# (40, 'STATUS')
# (41, 'V  OP')
# (42, 'VIDEO STATUS')
# (43, 'IMAGING AND VIDEO NOTES')
# (44, 'IMAGE UPL')
# (45, 'IMAGE RUN TIME')
# (46, 'VIDEO UPL')
# (47, 'VIDEO RUN TIME')
# (48, '')

# Feature(R): SKU
# STL: SKU_ASTL
# All additional alts: SKU_A1, SKU_A2, etc
# C2/C3: SKU_COLOR, SKU_COLORTWO, etc

class SKU():

    '''Base SKU class, handles building file names for each SKU'''
    # pylint: disable=too-many-instance-attributes

    def __init__(self, csv_line):

        self.sku = csv_line[7]
        self.feature_color = re.sub(r'[^\w]', '', csv_line[10].upper())
        self.alt_colors_raw = csv_line[11].split(',')
        self.alt_colors_clean = []
        self.alt_views = csv_line[12:16]
        self.turnin_date = csv_line[18]
        self.shot_views = csv_line[25:34]
        self.shot_suffix = [
            ['R'],
            ['ASTL'],
            ['A1'],
            ['A2'],
            ['A3'],
            ['A4'],
            ['C2'],
            ['C3'],
            ['V'],
        ]
        self.feature_colors_shot = csv_line[36]
        # self.alt_colors_shot = int(csv_line[37])
        self.shoot_date = csv_line[34]
        self.generated_shots = []
        self.generated_filenames = []

        self.clean_alt_colors()
        self.sync_shot_suffixes()
        self.generate_shotlist()
        self.generate_filenames()
        # self.clean_turn_in_date()

    def sync_shot_suffixes(self):
        for idx, shot in enumerate(self.shot_views):
            self.shot_suffix[idx].append(shot)

    def clean_alt_colors(self):
        for color in self.alt_colors_raw:
            clean_color = re.sub(r'[^\w]', '', color.upper())
            self.alt_colors_clean.append(clean_color)

    def generate_shotlist(self):
        filename_source = []
        if self.feature_color != '':
            filename_source.append(self.feature_color)
        for color in self.alt_colors_clean:
            if color != '':
                filename_source.append(color)
        for shot in self.shot_suffix:
            if shot[1] != '':
                filename_source.append(shot[0])
        self.generated_shots = filename_source
            
    def generate_filenames(self):
        for shot in self.generated_shots:
            output = ''
            if shot == 'R':
                pass
            elif shot == 'C2':
                pass
            elif shot == 'C3':
                pass
            elif shot == 'V':
                pass
            else:
                output = '{}_{}.tif'.format(self.sku, shot)
            if output != '':
                self.generated_filenames.append(output)

    # def clean_turn_in_date(self):
    #     dirty_date = self.turnin_date
    #     clean_date = datetime.datetime.strptime(dirty_date, '%d/%m/%Y').strftime('%d/%m/%Y')
    #     self.turnin_date = clean_date

    def __str__(self):
        # return "{}, {}, {}, {}".format(self.sku, self.feature_color, self.alt_colors_clean, self.shot_suffix)
        return '{} - {}'.format(self.sku, self.generated_filenames)

def clean_turn_in_date(input_date):
    return datetime.datetime.strptime(input_date, '%m/%d/%Y').strftime('%m/%d/%Y')

def clean_shoot_date(input_date):
    date_pattern = re.compile(r'(?P<month>[\d]{1,2})\W+(?P<day>[\d]{1,2})')
    parsed_date = date_pattern.match(input_date)
    month, day = parsed_date.groups()
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    output = '{}-{}'.format(month, day)
    return output

def generate_expected_filenames(csv_path, lookup_date, lookup_by_shootdate, and_shoot_date):

    session_skus = []
    session_files = []

    with open(csv_path) as csv_data:
        csvfile = csv.reader(csv_data)
        csv_list = [row for row in csvfile]

        for shot_sku in csv_list[3:]:
            if shot_sku[7] != '':
                shot_sku[18] = clean_turn_in_date(shot_sku[18])
                if shot_sku[34] != '':
                    shot_sku[34] = clean_shoot_date(shot_sku[34])
                if not lookup_by_shootdate and not and_shoot_date:
                    if shot_sku[18][:5].replace('/','') == lookup_date[:4]:
                        session_skus.append(SKU(shot_sku))
                    # commented-out after date format was standardized
                    # elif shot_sku[18] == '12/27/2017':
                    #     session_skus.append(SKU(shot_sku))
                    else:
                        pass
                elif not and_shoot_date:
                    cleaned_sku_shoot_date = shot_sku[34].replace('-','').replace('/','')
                    if cleaned_sku_shoot_date == lookup_date[:4]:
                        session_skus.append(SKU(shot_sku))
                
                else:
                    cleaned_sku_shoot_date = shot_sku[34].replace('-','').replace('/','')
                    if shot_sku[18][:5].replace('/','') == lookup_date[:4] and cleaned_sku_shoot_date == and_shoot_date[:4]:
                        session_skus.append(SKU(shot_sku))


        # for sku in session_skus:
        #     print(sku)

        for sku in session_skus:
            if sku.generated_filenames:
                sku_shoot_date = sku.shoot_date
                sku_turnin_date = sku.turnin_date
                for filename in sku.generated_filenames:
                    #filename_output = '{} \n\t\t\tTurn-In {} \n\t\t\tShot On {} \n'.format(filename, sku_turnin_date[:5], sku.shoot_date.replace('-','/'))
                    session_files.append(filename)
        return set(session_files)



def read_filenames_from_path(path):
    filenames = []
    for file in os.listdir(path):
        if file[0] != '.':
            filenames.append(file)
    return set(filenames)

def read_filenames_recursively(path, mode=False):
    filenames = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file[0] != '.':
                if file[-4:].upper() != '.MOV':
                    filenames.append(file)
    return set(filenames)

def parse_the_args():
    parser = argparse.ArgumentParser(
        usage='''Validates file names in a Turn In folder based on a TURN IN SHEET csv

        Instructions: drag the beta_punc_v01.py file into the terminal window, followed by a space. Then ...
        1. Drag the Turn In date folder onto the terminal window - no quotes required
        2. Drag the downloaded CSV File onto the terminal window - no quotes required
        3. Type the TURN IN date to check, formatted MM/DD/YYYY, MM/DD, or even just MMDD. no quotes required. EX: 03/14/2018 or 03/14 or 0314 - no quotes requried
        '''
    )
    parser.add_argument('path', type=str, help='the path to the TURN IN directory you wish to validate')
    parser.add_argument('csv', type=str, help='the path to the downloaded CSV file')
    parser.add_argument('date', type=str, help='the turn-in date to validate, formatted MM/DD/YYYY')
    parser.add_argument('-s', action='store_true')
    parser.add_argument('-a', '--andshootdate', type=str)

    args = parser.parse_args()
    return args.path, args.csv, args.date.replace('/',''), args.s, args.andshootdate

if __name__ == '__main__':
    turnin_folder_path, csv_path, lookup_date, lookup_mode, and_shoot_date = parse_the_args()

    #print('\nChecking filenames in - '+turnin_folder_path, '\nCSV FILE - '+csv_path, '\nChecking against TURN-IN DATE - '+lookup_date+'\n')

    print('''
    Checking filenames in - {}
    CSV File - {}
    Turn In Date  - {}
    Lookup by Shoot Date - {}
    Lookup by Shoto Date AND Turn In Date - {}
    '''.format(turnin_folder_path, csv_path, lookup_date[:4], lookup_mode, and_shoot_date))

    expected_filenames = generate_expected_filenames(csv_path, lookup_date, lookup_mode, and_shoot_date)

    # todays_filenames = read_filenames_from_path('./files')
    todays_filenames = read_filenames_recursively(turnin_folder_path)

    missing_files = expected_filenames - todays_filenames
    extra_files = todays_filenames - expected_filenames

    print('''    {} Files expected according to the Turn In Sheet
    {} Files checked in Turn In folder
    {} Missing files
    {} Possibly extra files found in Turn In folder
    '''.format(len(expected_filenames), len(todays_filenames), len(missing_files), len(extra_files)))

    print('\tmissing files:')
    for file in missing_files:
        print('\t\t'+file)
    print('\n\tpotentially extra files:')
    for file in extra_files:
        print('\t\t'+file)