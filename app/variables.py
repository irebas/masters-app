DISTANCES = ['50 FREE', '100 FREE', '200 FREE', '400 FREE', '800 FREE', '1500 FREE', '50 BACK', '100 BACK', '200 BACK',
             '50 BREAST', '100 BREAST', '200 BREAST', '50 FLY', '100 FLY', '200 FLY', '100 MEDLEY', '200 MEDLEY',
             '400 MEDLEY', '4x50 FREE', '4x50 MEDLEY']
DISTANCES_IND = [x for x in DISTANCES if x not in ['4x50 FREE', '4x50 MEDLEY']]

COURSES = ['SCM', 'LCM']
TYPES = ['INDIVIDUAL', 'RELAY']
YEARS = ['ALL', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013']
GENDERS = ['M', 'F', 'X']
AGE_GROUPS = ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74',
              '75-79', '80-84', '85-89', '90-94', '95-99']
AGE_GROUPS_IND = ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74',
                  '75-79', '80-84', '85-89', '90-94', '95-99']
AGE_GROUPS_REL = ['100-119', '120-159', '160-199', '200-239', '240-279', '280-319']
CUSTOM_DICT = {'50 FREE': 1, '100 FREE': 2, '200 FREE': 3, '400 FREE': 4, '800 FREE': 5, '1500 FREE': 6,
               '50 BACK': 7, '100 BACK': 8, '200 BACK': 9, '50 BREAST': 10, '100 BREAST': 11, '200 BREAST': 12,
               '50 FLY': 13, '100 FLY': 14, '200 FLY': 15, '100 MEDLEY': 16, '200 MEDLEY': 17, '400 MEDLEY': 18,
               '50 FREE SPLIT': 19, '100 FREE SPLIT': 20, '50 BREAST SPLIT': 21, '50 FLY SPLIT': 22}
