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
    def __init__(self, sku, feature_color, alt_colors, views, date):
        self.sku = sku
        self.feature_color = feature_color
        self.alt_colors = alt_colors
        self.views = views
        self.date = date

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.sku, self.feature_color, self.alt_colors, self.views, self.date)

with open('oct_sample_data.csv') as csv_data:
    csvfile = csv.reader(csv_data)
    csv_list = [row for row in csvfile]

    test_sku = SKU(csv_list[100][7], csv_list[100][10], csv_list[100][11], csv_list[100][25:33], csv_list[100][34])
    print(test_sku)
    #headers_numbered = enumerate(csv_list[2])

    # A1, A2, A3, A4 = '', '', '', ''

    # for row in csv_list:
    #     if row[27] != '':
    #         row[27] = 'A1'

    #     if row[28] != '':
    #         row[28] = 'A2'

    #     if row[29] != '':
    #         row[29] = 'A3'

    #     if row[30] != '':
    #         row[30] = 'A4'

    #     if row[34]:
    #         print row[34], row[7].strip(), row[10:12], row[27:31]

    # print csv_list[665][34], csv_list[665][7].strip(), csv_list[665][27:31]
