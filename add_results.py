import unidecode
import os
import sqlite3
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime

def get_split_times(times_list: list):
    times = []
    times.append(times_list[0])
    times.append(get_time_diff(times_list[0], times_list[1]))
    times.append(get_time_diff(times_list[1], times_list[2]))
    times.append(get_time_diff(times_list[2], times_list[3]))

    return times


def get_time_diff(t1: str, t2: str) -> str:
    t1 = datetime.strptime(t1,'%H:%M:%S.%f').time()
    t2 = datetime.strptime(t2, '%H:%M:%S.%f').time()
    t1_ms = t1.microsecond / 10000 + t1.second * 100 + t1.minute * 6000
    t2_ms = t2.microsecond / 10000 + t2.second * 100 + t2.minute * 6000
    if t2_ms > t1_ms:
        t_fin_ms = t2_ms - t1_ms
        minutes = int(t_fin_ms / 6000)
        seconds = int((t_fin_ms - minutes * 6000) / 100)
        milliseconds = int((t_fin_ms - minutes * 6000 - seconds * 100))
        t_str = f'{minutes}:{seconds}.{milliseconds}'
        timestamp = datetime.strptime(t_str, '%M:%S.%f').time()
        t_fin = str(timestamp)[:11]
    else:
        t_fin = "00:00:00.00"

    return t_fin


def calc_age_group(birth_year: str, meet_year: str) -> str:
    age = int(meet_year) - int(birth_year)
    if 20 <= age <= 24:
        age_group = '20-24'
    elif 25 <= age <= 29:
        age_group = '25-29'
    elif 30 <= age <= 34:
        age_group = '30-34'
    elif 35 <= age <= 39:
        age_group = '35-39'
    elif 40 <= age <= 44:
        age_group = '40-44'
    elif 45 <= age <= 49:
        age_group = '45-49'
    elif 50 <= age <= 54:
        age_group = '50-54'
    elif 55 <= age <= 59:
        age_group = '55-59'
    elif 60 <= age <= 64:
        age_group = '60-64'
    elif 65 <= age <= 69:
        age_group = '65-69'
    elif 70 <= age <= 74:
        age_group = '70-74'
    elif 75 <= age <= 79:
        age_group = '75-79'
    elif 80 <= age <= 84:
        age_group = '80-84'
    elif 85 <= age <= 89:
        age_group = '85-89'
    elif 90 <= age <= 94:
        age_group = '90-94'
    elif 95 <= age <= 99:
        age_group = '95-99'
    elif age >= 100:
        age_group = '99+'
    else:
        age_group = 'NA'

    return age_group


class Results:

    def __init__(self, file_name):
        tree = ET.parse(file_name)
        self.root = tree.getroot()
        self.meet_year = file_name[-8:-4]
        self.meet_date = self.root.find("./MEETS/MEET/AGEDATE").attrib['value']

    def get_events_ranks(self):
        df_events = pd.DataFrame()
        df_ranks = pd.DataFrame()
        meet_name = self.root.find("./MEETS/MEET").attrib['name']
        meet_city = self.root.find("./MEETS/MEET").attrib['city']
        course = self.root.find("./MEETS/MEET").attrib['course']
        session_tags = self.root.findall("./MEETS/MEET/SESSIONS/SESSION")
        for session in session_tags:
            date = session.attrib['date']
            event_tags = session.findall('EVENTS/EVENT')
            for event in event_tags:
                eventid = event.attrib['eventid']
                try:
                    event_gender = event.attrib['gender']
                except KeyError:
                    event_gender = 'X'
                d_event = {'date': date, 'eventid': eventid, 'event_gender': event_gender,
                           'distance': event.find('SWIMSTYLE').attrib['distance'],
                           'stroke': event.find('SWIMSTYLE').attrib['stroke']}
                df_events = pd.concat([df_events, pd.DataFrame(data=[d_event])])
                try:
                    for agegroup in event.findall('AGEGROUPS/AGEGROUP'):
                        age_group_lxf = f'{agegroup.attrib["agemin"]}-{agegroup.attrib["agemax"]}'
                        try:
                            for ranking in agegroup.find('RANKINGS'):
                                d_rank = {'eventid': eventid, 'resultid': ranking.attrib['resultid'],
                                          'place': ranking.attrib['place'], 'age_group_lxf': age_group_lxf}
                                df_ranks = pd.concat([df_ranks, pd.DataFrame(data=[d_rank])])
                        except (TypeError, KeyError):
                            pass

                except (TypeError, KeyError):
                    pass

        df_events_ranks = df_ranks.merge(df_events, on='eventid', how='left')
        df_events_ranks['meet_name'] = meet_name
        df_events_ranks['meet_city'] = meet_city
        df_events_ranks['course'] = course

        return df_events_ranks

    def get_athletes_results(self):
        df_athletes = pd.DataFrame()
        df_results = pd.DataFrame()
        df_results_rel = pd.DataFrame()
        df_results_rel_ind = pd.DataFrame()
        d_athletes_all = dict()
        d_athletes_names = dict()

        club_tags = self.root.findall("./MEETS/MEET/CLUBS/CLUB")

        for club in club_tags:
            try:
                club_name = club.attrib['name']
            except KeyError:
                club_name = 'Niezrzeszony'
            for athlete in club.findall('ATHLETES/ATHLETE'):
                d_athlete = athlete.attrib
                swrid = d_athlete['swrid'] if 'swrid' in d_athlete else np.NaN
                try:
                    d_athlete['birth_year'] = athlete.attrib['birthdate'][:4]
                except KeyError:
                    d_athlete['birth_year'] = '9999'
                d_athlete['age_group_calc'] = calc_age_group(d_athlete['birth_year'], self.meet_year)
                athleteid = athlete.attrib['athleteid']
                try:
                    lastname = unidecode.unidecode(athlete.attrib['lastname'].strip())
                except KeyError:
                    lastname = unidecode.unidecode(athlete.attrib['nameprefix'].strip())
                firstname = unidecode.unidecode(athlete.attrib['firstname'].strip()).title()
                fullname = f"{lastname.upper()}, {firstname}"
                athlete_id = f"{lastname.upper()}, {firstname} ({d_athlete['birth_year']})"
                # dictionary used for assigning fullnames to ids in relays
                d_athletes_names[athleteid] = athlete_id
                # remove second condition later!
                if athlete_id not in d_athletes_all:
                    d_athletes_all[athlete_id] = {'athlete_id': athlete_id, 'fullname': fullname,
                                                  'birthday': d_athlete['birth_year'], 'club': club_name,
                                                  'last_entry': self.meet_date, 'swrid': swrid}
                df_athletes = pd.concat([df_athletes, pd.DataFrame(data=[d_athlete])])
                for result in athlete.findall('RESULTS/RESULT'):
                    d_result = dict((k, result.attrib[k]) for k in ['swimtime', 'resultid'])
                    d_result['athleteid'] = athleteid
                    d_result['fullname'] = fullname
                    d_result['club_name'] = club_name
                    d_result['athlete_id'] = athlete_id
                    df_results = pd.concat([df_results, pd.DataFrame(data=[d_result])])

            for relay in club.findall('RELAYS/RELAY'):
                for result in [x for x in relay.findall('RESULTS/RESULT') if x.attrib['swimtime'] != '00:00:00.00']:
                    d_result = dict((k, result.attrib[k]) for k in ['swimtime', 'resultid'])
                    # add relay members as fullname
                    relay_team_list = []
                    splits_list = []
                    for split in result.findall('SPLITS/SPLIT'):
                        splits_list.append(split.attrib['swimtime'])
                    splits_list.append(result.attrib['swimtime'])

                    split_times = get_split_times(splits_list) if len(splits_list) == 4 else 4 * ['00:00:00.00']

                    k = 0
                    for relay_position in result.findall('RELAYPOSITIONS/RELAYPOSITION'):
                        k = k + 1
                        try:
                            athleteid = relay_position.attrib['athleteid']
                            athlete_id = d_athletes_names[athleteid]
                            # tu trzeba teraz dodać te zesplitowane czasy ludzi
                            d_result_rel_ind = dict()
                            d_result_rel_ind['swimtime'] = split_times[k - 1]
                            d_result_rel_ind['resultid'] = result.attrib['resultid']
                            d_result_rel_ind['athleteid'] = athleteid
                            d_result_rel_ind['fullname'] = athlete_id
                            d_result_rel_ind['club_name'] = club_name
                            d_result_rel_ind['athlete_id'] = athlete_id
                            d_result_rel_ind['type'] = 'INDIVIDUAL' if k == 1 else 'RELAY SPLIT'
                            d_result_rel_ind['relay_order'] = k
                            df_results_rel_ind = pd.concat([df_results_rel_ind, pd.DataFrame(data=[d_result_rel_ind])])
                        except KeyError:
                            athlete_id = 'NA'
                        relay_team_list.append(athlete_id)
                    relay_team = ', '.join(relay_team_list)
                    d_result['athleteid'] = pd.NA
                    d_result['fullname'] = relay_team
                    d_result['club_name'] = club_name
                    df_results_rel = pd.concat([df_results_rel, pd.DataFrame(data=[d_result])])

        df_results['type'] = 'INDIVIDUAL'
        df_results_rel['type'] = 'RELAY'
        df_results['relay_order'] = 0
        df_results_rel['relay_order'] = 0
        # merge invdividual results with relay results
        df_results_all = pd.concat([df_results, df_results_rel, df_results_rel_ind])
        # merge results with athletes, ranks with events and get final dataframe
        df_athletes_results = df_results_all.merge(df_athletes, on='athleteid', how='left')
        return df_athletes_results, d_athletes_all

    @staticmethod
    def get_df_final(df_athletes_results, df_events_ranks, meet_code):
        df_events_ranks.to_csv('test123.csv')
        df_athletes_results.to_csv('test456.csv')
        df_final = df_athletes_results.merge(df_events_ranks, on='resultid', how='left')
        # add columns to dataframe
        df_final['meet_code'] = meet_code
        df_final['stroke'] = df_final['distance'] + ' ' + df_final['stroke']
        # old results don't have those fields
        if 'swrid' not in df_final.columns:
            df_final['swrid'] = pd.NA
        if 'license' not in df_final.columns:
            df_final['license'] = pd.NA
        # exclude non masters people and assign proper age group
        df_final['age_group'] = [x for x in df_final['age_group_calc']]
        df_final = df_final[df_final['age_group'] != 'NA']
        df_final.reset_index(inplace=True, drop=True)
        custom_dict = {0: 'NA', 1: 'BACK', 2: 'BREAST', 3: 'FLY', 4: 'FREE'}
        df_final['relay_stroke'] = df_final['relay_order'].map(custom_dict)
        df_final['stroke'] = ['NA' if pd.isna(x) else x for x in df_final['stroke']]
        for r in range(len(df_final)):

            if df_final.loc[r, 'type'] == 'RELAY':
                df_final.loc[r, 'age_group'] = df_final.loc[r, 'age_group_lxf']
            elif df_final.loc[r, 'type'] == 'RELAY SPLIT' and 'MEDLEY' in df_final.loc[r, 'stroke']:
                df_final.loc[r, 'stroke'] = df_final.loc[r, 'stroke'].replace('MEDLEY', df_final.loc[r, 'relay_stroke'])

        df_final['row_id'] = df_final['meet_code'] + '_' + df_final['resultid']
        df_final['meet_year'] = [x[-4:] for x in df_final['meet_code']]
        # get only selected columns
        df_final = df_final[['meet_code', 'meet_name', 'meet_city', 'meet_year', 'course', 'date', 'stroke',
                             'event_gender', 'age_group', 'fullname', 'firstname', 'lastname', 'birthdate',
                             'birth_year', 'gender', 'nation', 'swrid', 'license', 'club_name', 'place', 'swimtime',
                             'type', 'athlete_id', 'row_id']]
        df_final.to_csv('test.csv')
        df_final.reset_index(inplace=True, drop=True)
        # df_athletes = df_final.drop_duplicates(['athlete_id'])[['athlete_id', 'fullname', 'birthdate',
        #                                                         'birth_year', 'club_name', 'meet_year', 'swrid']]
        return df_final


def get_all_results(file_name):
    df_events_ranks = Results(file_name).get_events_ranks()
    df_athletes_results, d_athletes_all = Results(file_name).get_athletes_results()
    meet_code = file_name[-16:-4]
    df_all_results = Results.get_df_final(df_athletes_results=df_athletes_results,
                                          df_events_ranks=df_events_ranks,
                                          meet_code=meet_code)
    return df_all_results, d_athletes_all


def main():
    files_list = get_files_list(r'splash_files\Valid\MP')
    with sqlite3.connect('masters.db') as conn:
        for file in files_list:
            df_all_results, d_athletes_all = get_all_results(file)
            athletes_all_ids = list(d_athletes_all.keys())
            print(f'Athletes in competition: {len(athletes_all_ids)}')
            # iterate over existing records
            cur = conn.cursor()
            cur.execute('SELECT * FROM athletes')
            rows = cur.fetchall()
            print(f'Athletes in database: {len(rows)}')
            d_athletes_db = dict()
            for r in rows:
                if r[0] in athletes_all_ids:
                    if d_athletes_all[r[0]]['last_entry'] > r[4]:
                        club = d_athletes_all[r[0]]['club']
                        last_entry = d_athletes_all[r[0]]['last_entry']
                    else:
                        club = r[3]
                        last_entry = r[4]
                    swrid = d_athletes_all[r[0]]['swrid'] if not pd.isna(d_athletes_all[r[0]]['swrid']) else r[5]
                else:
                    club = r[3]
                    last_entry = r[4]
                    swrid = r[5]
                d_athletes_db[r[0]] = {'athlete_id': r[0], 'fullname': r[1], 'birthday': r[2], 'club': club,
                                       'last_entry': last_entry, 'swrid': swrid}

            # add new rows
            a = 0
            for k in d_athletes_all:
                if k not in d_athletes_db.keys():
                    d_athletes_db[d_athletes_all[k]['athlete_id']] = d_athletes_all[k]
                    a = a + 1

            print(f'New athletes: {a}')
            l_athletes_all = list(d_athletes_db.values())
            df_athletes_all = pd.DataFrame(data=l_athletes_all)
            df_athletes_all.to_sql('athletes', conn, if_exists='replace', index=False)
            df_all_results.to_sql('results', conn, if_exists='append', index=False)
            print(f'{file} appended successfully!')


def get_files_list(root: str) -> list:
    files_list = list()
    for path, subdirs, files in os.walk(root):
        for file in files:
            if file.endswith('.lef'):
                files_list.append(os.path.join(path, file))

    return files_list


if __name__ == '__main__':
    main()
