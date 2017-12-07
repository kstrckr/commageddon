import csv
import re
import os

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

def generate_expected_filenames(csv_path):

    session_skus = []
    session_files = []

    with open(csv_path) as csv_data:
        csvfile = csv.reader(csv_data)
        csv_list = [row for row in csvfile]

        for shot_sku in csv_list[3:]:
            if shot_sku[7] != '':
                session_skus.append(SKU(shot_sku))

        # for sku in session_skus:
        #     print(sku)

        for sku in session_skus:
            if sku.generated_filenames:
                for filename in sku.generated_filenames:
                    session_files.append(filename)
        print(len(session_files))
        return set(session_files)

        

expected_files = generate_expected_filenames('nynov.csv')
print(len(expected_files))

# for file in expected_files:
#     print(file)




def read_filenames_from_path(path):
    filenames = []
    for file in os.listdir(path):
        if file[0] != '.':
            filenames.append(file)
    return set(filenames)

# expected_filenames = generate_expected_filenames('nynov.csv')
# todays_filenames = read_filenames_from_path('/Volumes/kycreative/_TEAM/Kurt/commageddon/files')

# missing_files = todays_filenames - expected_filenames

# print(len(todays_filenames), len(missing_files))
# for file in expected_filenames:
#     print(file)