import csv

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

    def __init__(self, sku, feature_color, alt_colors, views, date):
        self.sku = sku
        self.feature_color = feature_color.replace(' ', '')
        self.alt_colors = alt_colors
        self.views = views
        self.view_names = [
            ['R', False],
            ['ASTL', False],
            ['A1', False],
            ['A2', False],
            ['A3', False],
            ['A4', False],
            ['C2', False],
            ['C3', False],
            ['V', False],
        ]
        self.shot_views = []
        self.file_names = []
        self.date = date

        self.set_variant_naming()
        self.set_shot_views()

    def set_variant_naming(self):
        for idx, shot_view in enumerate(self.views):
            if shot_view != '':
                self.view_names[idx][1] = True

    def set_shot_views(self):
        for view in self.view_names:
            if view[1] is True:
                self.shot_views.append(view[0])

    def generate_filenames(self):
        for view in self.shot_views[:-1]:
            output = ''
            if view == 'R':
                if self.feature_color != '':
                    output = '{}_{}.tiff'.format(self.sku, self.feature_color)
                else:
                    output = '{}.tiff'.format(self.sku)

            else:
                output = '{}_{}.tiff'.format(self.sku, view)

            self.file_names.append(output)
        return self.file_names

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.sku, self.feature_color, self.alt_colors, self.shot_views, self.date)

session_files = []

with open('csv.csv') as csv_data:
    csvfile = csv.reader(csv_data)
    csv_list = [row for row in csvfile]

    for shot_sku in csv_list:
        test_sku = SKU(shot_sku[7], shot_sku[10], shot_sku[11], shot_sku[25:34], shot_sku[34])
        file_names = test_sku.generate_filenames()
        if file_names:
            for name in file_names:
                session_files.append(name)

for name in session_files:
    print(name)
