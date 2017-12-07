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
        self.feature_colors_shot = csv_line[36]
        self.alt_colors_shot = int(csv_line[37])
        self.shoot_date = csv_line[34]
        self.generated_filenames = []

        self.clean_alt_colors()
        self.generate_filenames()

    def clean_alt_colors(self):
        for color in self.alt_colors_raw:
            clean_color = re.sub(r'[\w]', '', clean_color)
            self.alt_colors_clean.append(clean_color)

    def generate_filenames(self):
        for view in self.shot_views[:-1]:
            output = ''
            if view == 'R':
                if self.feature_color != '':
                    output = '{}_{}.tif'.format(self.sku, self.feature_color)
                else:
                    output = '{}.tif'.format(self.sku)

            elif view == 'C2'or view == 'C3':
                pass

            else:
                output = '{}_{}.tif'.format(self.sku, view)

            if output:
                self.file_names.append(output)
        #return self.file_names

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.sku, self.feature_color, self.alt_colors, self.shot_views, self.date)


def generate_expected_filenames(csv_path):

    session_skus = []
    session_files = []

    with open(csv_path) as csv_data:
        csvfile = csv.reader(csv_data)
        csv_list = [row for row in csvfile]

        for shot_sku in csv_list[3:]:
            session_skus.append(SKU(shot_sku[7], shot_sku[10], shot_sku[11], shot_sku[25:34], shot_sku[34]))

        for sku in session_skus:
            # if sku.file_names:
            #     for filename in sku.file_names:
            #         session_files.append(filename)
            print('{} - {}'.format(sku.sku, sku.file_names))
        # return set(session_files)

def read_filenames_from_path(path):
    filenames = []
    for file in os.listdir(path):
        if file[0] != '.':
            filenames.append(file)
    return set(filenames)

expected_filenames = generate_expected_filenames('nynov.csv')
todays_filenames = read_filenames_from_path('/Volumes/kycreative/_TEAM/Kurt/commageddon/files')

# missing_files = todays_filenames - expected_filenames

# print(len(todays_filenames), len(missing_files))
# for file in expected_filenames:
#     print(file)