#!/usr/bin/env python

'''
Pre Upload Name Checker - P.U.N.C.
Kurt Strecker
v 0.1 - beta version ready for on set testing
updated 01/04/2018
'''

import csv
import re
import os
import argparse

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

    def __str__(self):
        # return "{}, {}, {}, {}".format(self.sku, self.feature_color, self.alt_colors_clean, self.shot_suffix)
        return '{} - {}'.format(self.sku, self.generated_filenames)

def generate_expected_filenames(csv_path, turn_in_date):

    session_skus = []
    session_files = []

    with open(csv_path) as csv_data:
        csvfile = csv.reader(csv_data)
        csv_list = [row for row in csvfile]

        for shot_sku in csv_list[3:]:
            if shot_sku[7] != '':
                if shot_sku[18] == turn_in_date:
                    session_skus.append(SKU(shot_sku))
                # commented-out after date format was standardized
                # elif shot_sku[18] == '12/27/2017':
                #     session_skus.append(SKU(shot_sku))
                else:
                    pass


        # for sku in session_skus:
        #     print(sku)

        for sku in session_skus:
            if sku.generated_filenames:
                for filename in sku.generated_filenames:
                    session_files.append(filename)
        return set(session_files)



def read_filenames_from_path(path):
    filenames = []
    for file in os.listdir(path):
        if file[0] != '.':
            filenames.append(file)
    return set(filenames)

def read_filenames_recursively(path):
    filenames = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name[0] != '.':
                if name[-4:].upper() != '.MOV':
                    filenames.append(name)
    return set(filenames)

def parse_the_args():
    parser = argparse.ArgumentParser(
        usage='''Validates file names in a Turn In folder based on a TURN IN SHEET csv

        Instructions: type 'python punc.py' into the terminal window, followed by a space. Then ...
        1. Drag the Turn In date folder onto the terminal window
        2. Drag the downloaded CSV File onto the terminal window
        3. Type the TURN IN date to check, formatted DD/MM/YYYY, no quotes required. EX: 03/14/2018
        '''
    )
    parser.add_argument('path', type=str, help='the path to the TURN IN directory you wish to validate')
    parser.add_argument('csv', type=str, help='the path to the downloaded CSV file')
    parser.add_argument('date', type=str, help='the turn-in date to validate, formatted DD/MM/YYYY')

    args = parser.parse_args()
    return args.path, args.csv, args.date

if __name__ == '__main__':
    turnin_folder_path, csv_path, turn_in_date = parse_the_args()

    #print('\nChecking filenames in - '+turnin_folder_path, '\nCSV FILE - '+csv_path, '\nChecking against TURN-IN DATE - '+turn_in_date+'\n')

    print('''
    Checking filenames in - {}
    CSV File - {}
    Turn In Date  - {}
    '''.format(turnin_folder_path, csv_path, turn_in_date))

    expected_filenames = generate_expected_filenames(csv_path, turn_in_date)

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