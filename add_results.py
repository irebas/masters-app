import os
import sqlite3
import pandas as pd
import xml.etree.ElementTree as ET


class Results:

    def __init__(self, competition_code):
        self.competition_code = competition_code
        file_name = f'splash_files/{competition_code}.lef'
        tree = ET.parse(file_name)
        self.root = tree.getroot()

    def get_events_ranks(self):
        df_events = pd.DataFrame()
        df_ranks = pd.DataFrame()
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
                        age_group = f'{agegroup.attrib["agemin"]}-{agegroup.attrib["agemax"]}'
                        try:
                            for ranking in agegroup.find('RANKINGS'):
                                d_rank = {'eventid': eventid, 'resultid': ranking.attrib['resultid'],
                                          'place': ranking.attrib['place'], 'age_group': age_group}
                                df_ranks = pd.concat([df_ranks, pd.DataFrame(data=[d_rank])])
                        except (TypeError, KeyError):
                            pass

                except (TypeError, KeyError):
                    pass

        df_events_ranks = df_ranks.merge(df_events, on='eventid', how='left')
        return df_events_ranks

    def get_athletes_results(self):
        df_athletes = pd.DataFrame()
        df_results = pd.DataFrame()
        df_results_rel = pd.DataFrame()
        d_athletes_names = dict()

        club_tags = self.root.findall("./MEETS/MEET/CLUBS/CLUB")

        for club in club_tags:
            club_name = club.attrib['name']
            for athlete in club.findall('ATHLETES/ATHLETE'):
                d_athlete = athlete.attrib
                try:
                    d_athlete['birth_year'] = athlete.attrib['birthdate'][:4]
                except KeyError:
                    d_athlete['birth_year'] = '9999'
                athlete_id = athlete.attrib['athleteid']
                try:
                    athlete_fullname = athlete.attrib['lastname'] + ' ' + athlete.attrib['firstname']
                except KeyError:
                    athlete_fullname = athlete.attrib['nameprefix'] + ' ' + athlete.attrib['firstname']

                # dictionary used for assigning fullnames to ids in relays
                d_athletes_names[athlete_id] = athlete_fullname
                df_athletes = pd.concat([df_athletes, pd.DataFrame(data=[d_athlete])])
                for result in athlete.findall('RESULTS/RESULT'):
                    d_result = dict((k, result.attrib[k]) for k in ['swimtime', 'resultid'])
                    d_result['athleteid'] = athlete_id
                    d_result['fullname'] = athlete_fullname
                    d_result['club_name'] = club_name
                    df_results = pd.concat([df_results, pd.DataFrame(data=[d_result])])

            for relay in club.findall('RELAYS/RELAY'):
                for result in relay.findall('RESULTS/RESULT'):
                    d_result = dict((k, result.attrib[k]) for k in ['swimtime', 'resultid'])
                    # add relay members as fullname
                    relay_team_list = []
                    for relay_position in result.findall('RELAYPOSITIONS/RELAYPOSITION'):
                        try:
                            athlete_id = relay_position.attrib['athleteid']
                            athlete_fullname = d_athletes_names[athlete_id]
                        except KeyError:
                            athlete_fullname = 'NA'
                        relay_team_list.append(athlete_fullname)
                    relay_team = ', '.join(relay_team_list)
                    d_result['athleteid'] = pd.NA
                    d_result['fullname'] = relay_team
                    d_result['club_name'] = club_name
                    df_results_rel = pd.concat([df_results_rel, pd.DataFrame(data=[d_result])])

        df_results['type'] = 'INDIVIDUAL'
        df_results_rel['type'] = 'RELAY'
        # merge invdividual results with relay results
        df_results_all = pd.concat([df_results, df_results_rel])
        # merge results with athletes, ranks with events and get final dataframe
        df_athletes_results = df_results_all.merge(df_athletes, on='athleteid', how='left')
        return df_athletes_results

    @staticmethod
    def get_df_final(df_events_ranks, df_athletes_results, competition_code):
        df_final = df_athletes_results.merge(df_events_ranks, on='resultid', how='left')
        # add columns to dataframe
        df_final['competition_code'] = competition_code
        df_final['stroke'] = df_final['distance'] + ' ' + df_final['stroke']
        # old results don't have those fields
        if 'swrid' not in df_final.columns:
            df_final['swrid'] = pd.NA
        if 'license' not in df_final.columns:
            df_final['license'] = pd.NA
        # get only selected columns
        df_final = df_final[['competition_code', 'date', 'stroke', 'event_gender', 'age_group', 'fullname', 'firstname',
                             'lastname', 'birthdate', 'birth_year', 'gender', 'nation', 'swrid', 'license', 'club_name',
                             'place', 'swimtime', 'type']]
        df_final.reset_index(inplace=True, drop=True)

        return df_final


def get_all_results(competition_code):
    df_athletes_results = Results(competition_code).get_athletes_results()
    df_events_ranks = Results(competition_code).get_events_ranks()
    df_all_results = Results.get_df_final(df_athletes_results, df_events_ranks, competition_code)
    return df_all_results


def main():
    # 'LMP_GLI_2016', 'ZMP_OLS_2016'
    competition_codes = ['LMP_WAW_2017', 'ZMP_GLI_2017', 'LMP_POZ_2018',
                         'ZMP_OLS_2018', 'LMP_GLI_2019', 'ZMP_LOD_2019', 'ZMP_POZ_2021', 'ZMP_POZ_2022']
    with sqlite3.connect('masters.db') as conn:
        for code in competition_codes:
            df_all_results = get_all_results(code)
            df_all_results.to_sql('results', conn, if_exists='append', index=False)
            print(f'{code} appended successfully!')


def get_files_list(root: str) -> list:
    files_list = list()
    for path, subdirs, files in os.walk(root):
        for file in files:
            if file.endswith('.csv') or file.endswith('.txt'):
                files_list.append(os.path.join(path, file))

    return files_list


if __name__ == '__main__':
    main()
