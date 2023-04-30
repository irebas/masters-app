import numpy as np
import pandas as pd

from app.database import db
from sqlalchemy import and_, desc, asc
from app.utils import calc_fina_points

AGE_GROUPS_IND = ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74',
                  '75-79', '80-84', '85-89', '90-94', '95-99']
AGE_GROUPS_REL = ['100-119', '120-159', '160-199', '200-239', '240-279', '280-319']


class Meets(db.Model):
    __tablename__ = 'meets'
    meet_code = db.Column('meet_code', db.String, primary_key=True)
    meet_name = db.Column('meet_name', db.String, primary_key=True)
    meet_city = db.Column('meet_city', db.String, primary_key=True)
    meet_date = db.Column('meet_date', db.String, primary_key=True)
    meet_year = db.Column('meet_year', db.String, primary_key=True)

    def __init__(self, meet_code, meet_name, meet_city, meet_date, meet_year):
        self.meet_code = meet_code
        self.meet_name = meet_name
        self.meet_city = meet_city
        self.meet_date = meet_date
        self.meet_year = meet_year

    @staticmethod
    def get_meets():
        meets = db.session.query(Meets).all()

        return meets

class WR(db.Model):
    __tablename__ = 'world_records'
    stroke = db.Column('stroke', db.String, primary_key=True)
    course = db.Column('course', db.String, primary_key=True)
    gender = db.Column('gender', db.String, primary_key=True)
    fullname = db.Column('fullname', db.String)
    nationality = db.Column('nationality', db.String)
    swimtime = db.Column('swimtime', db.String)
    meet_name = db.Column('meet_name', db.String)
    meet_date = db.Column('meet_date', db.String)

    def __init__(self, stroke, course, gender, fullname, nationality, swimtime, meet_name, meet_date):
        self.stroke = stroke
        self.course = course
        self.gender = gender
        self.fullname = fullname
        self.nationality = nationality
        self.swimtime = swimtime
        self.meet_name = meet_name
        self.meet_date = meet_date


class Results(db.Model):
    __tablename__ = 'results'
    meet_code = db.Column('meet_code', db.String)
    meet_name = db.Column('meet_name', db.String)
    meet_year = db.Column('meet_year', db.String)
    meet_city = db.Column('meet_city', db.String)
    course = db.Column('course', db.String)
    date = db.Column('date', db.String)
    stroke = db.Column('stroke', db.String)
    event_gender = db.Column('event_gender', db.String)
    age_group = db.Column('age_group', db.String)
    fullname = db.Column('fullname', db.String)
    firstname = db.Column('firstname', db.String)
    lastname = db.Column('lastname', db.String)
    birthdate = db.Column('birthdate', db.String)
    birth_year = db.Column('birth_year', db.String)
    gender = db.Column('gender', db.String)
    nation = db.Column('nation', db.String)
    swrid = db.Column('swrid', db.String)
    license = db.Column('license', db.String)
    club_name = db.Column('club_name', db.String)
    place = db.Column('place', db.String)
    swimtime = db.Column('swimtime', db.String)
    type = db.Column('type', db.String)
    athlete_id = db.Column('athlete_id', db.String)
    row_id = db.Column('row_id', db.String, primary_key=True)

    def __init__(self, meet_code, meet_name, meet_year, meet_city, course, date, stroke, event_gender, age_group,
                 fullname, firstname, lastname, birthdate, birth_year, gender, nation, swrid, license, club_name,
                 place, swimtime, type, athlete_id, row_id):
        self.meet_code = meet_code
        self.meet_name = meet_name
        self.meet_year = meet_year
        self.meet_city = meet_city
        self.course = course
        self.date = date
        self.stroke = stroke
        self.event_gender = event_gender
        self.age_group = age_group
        self.fullname = fullname
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.birth_year = birth_year
        self.gender = gender
        self.nation = nation
        self.swrid = swrid
        self.license = license
        self.club_name = club_name
        self.place = place
        self.swimtime = swimtime
        self.type = type
        self.athlete_id = athlete_id
        self.row_id = row_id

    @staticmethod
    def get_records(event_gender: str, distance: str):
        records = dict()
        if distance not in ['4x50 FREE', '4x50 MEDLEY']:
            type_ = 'INDIVIDUAL'
        else:
            type_ = 'RELAY'
            distance = distance[2:]
        records = db.session.query(Results).filter(and_(Results.event_gender == event_gender,
                                                        Results.nation == 'POL',
                                                        Results.stroke == distance,
                                                        Results.type == type_,
                                                        Results.place != -1)).statement
        df = pd.read_sql(sql=records, con=db.session.get_bind())
        df['rank'] = df.groupby(['course', 'stroke', 'age_group'])['swimtime'].rank(method='first',
                                                                                            ascending=True)
        df = df.loc[(df['rank'] == 1)]
        df.sort_values(by='age_group', inplace=True, ascending=True)
        df = df[['athlete_id', 'fullname', 'club_name', 'course', 'meet_city', 'date', 'swimtime', 'age_group', 'type']]
        df_lc = df.loc[(df['course']) == 'LCM']
        df_sc = df.loc[(df['course']) == 'SCM']
        df_lc.reset_index(inplace=True, drop=True)
        df_sc.reset_index(inplace=True, drop=True)
        print(df_sc)
        records_lc = df_lc.to_dict('records')
        records_sc = df_sc.to_dict('records')

        records = {'LONG COURSE METERS': records_lc, 'SHORT COURSE METERS': records_sc}

        return records

    @staticmethod
    def get_top_results(event_gender: str, course: str, stroke: str, year: str):
        top_results = dict()
        if stroke not in ['4x50 FREE', '4x50 MEDLEY']:
            type_ = 'INDIVIDUAL'
            age_groups = AGE_GROUPS_IND
        else:
            type_ = 'RELAY'
            stroke = stroke[2:]
            age_groups = AGE_GROUPS_REL
        year = '2%' if year == 'ALL' else year
        for age_group in age_groups:
            results_ag = db.session.query(Results).filter(and_(Results.event_gender == event_gender,
                                                               Results.course == course,
                                                               Results.stroke == stroke,
                                                               Results.type == type_,
                                                               Results.age_group == age_group,
                                                               Results.meet_year.like(year),
                                                               Results.place != -1)).order_by(asc(Results.swimtime))
            top_results[age_group] = results_ag

        return top_results

    @staticmethod
    def get_best_results(athlete_id: str):
        sql = db.session.query(Results,
                               WR.swimtime.label('world_record')).join(WR, and_(WR.stroke == Results.stroke,
                                                                                WR.gender == Results.event_gender,
                                                                                WR.course == Results.course),
                                             isouter=True).filter(and_(Results.athlete_id == athlete_id,
                                                                       Results.place != -1)).statement
        df = pd.read_sql(sql=sql, con=db.session.get_bind())
        # window function - get best time partitioned by course, stroke and athlete_id
        df['stroke_rank'] = df.groupby(['course', 'stroke', 'athlete_id'])['swimtime'].rank(method='first', ascending=True)
        df = df.loc[(df['stroke_rank'] == 1)]
        # assign sort mapping
        df.reset_index(inplace=True, drop=True)
        custom_dict = {'50 FREE': 0, '100 FREE': 2, '200 FREE': 3, '400 FREE': 4, '800 FREE': 5, '1500 FREE': 6,
                       '50 BACK': 7, '100 BACK': 8, '200 BACK': 9, '50 BREAST': 10, '100 BREAST': 11, '200 BREAST': 12,
                       '50 FLY': 13, '100 FLY': 14, '200 FLY': 15, '100 MEDLEY': 16, '200 MEDLEY': 17}
        df['sort_rank'] = df['stroke'].map(custom_dict)
        # calculate fina points
        df['fina_points'] = [calc_fina_points(x, y) for x,y in zip(df['swimtime'], df['world_record'])]
        df.sort_values(by=['sort_rank', 'course'], inplace=True, ascending=[True, True])
        df = df[['athlete_id', 'fullname', 'stroke', 'course', 'meet_name', 'meet_city',
                 'date', 'swimtime', 'fina_points']]
        return df

    @staticmethod
    def get_athlete_results(athlete_id: str, event: str):
        sql = db.session.query(Results.swimtime, Results.athlete_id, Results.date, Results.meet_city, Results.course,
                               Results.stroke,
                               WR.swimtime.label('world_record')).join(WR, and_(WR.stroke == Results.stroke,
                                                                                WR.gender == Results.event_gender,
                                                                                WR.course == Results.course),
                                             isouter=True).filter(and_(Results.athlete_id == athlete_id,
                                                                       Results.stroke == event,
                                                                       Results.place != -1)).statement

        df = pd.read_sql(sql=sql, con=db.session.get_bind())
        df['fina_points'] = [calc_fina_points(x, y) for x, y in zip(df['swimtime'], df['world_record'])]
        df.sort_values(by=['date'], inplace=True, ascending=True)
        df_lc = df.loc[df['course'] == 'LCM']
        df_lc.reset_index(inplace=True, drop=True)
        df_sc = df.loc[df['course'] == 'SCM']
        df_sc.reset_index(inplace=True, drop=True)
        max_lc = df_lc['swimtime'].min()
        max_sc = df_sc['swimtime'].min()
        results_lc = df_lc.to_dict('records')
        results_sc = df_sc.to_dict('records')
        return results_lc, results_sc, max_lc, max_sc

    def __repr__(self):
        return self.fullname


class Athletes(db.Model):
    __tablename__ = 'athletes'
    athlete_id = db.Column('athlete_id', db.String, primary_key=True)
    fullname = db.Column('fullname', db.String)
    birthday = db.Column('birthday', db.String)
    club = db.Column('club', db.String)
    last_entry = db.Column('last_entry', db.String)
    swrid = db.Column('swrid', db.String)

    def __init__(self, athlete_id, fullname, birthday, club, last_entry, swrid):
        self.athlete_id = athlete_id
        self.fullname = fullname
        self.birthday = birthday
        self.club = club
        self.last_entry = last_entry
        self.swrid = swrid

    @staticmethod
    def get_athletes():
        athletes = [r.athlete_id for r in db.session.query(Athletes)]
        athletes.sort()
        return athletes

    @staticmethod
    def get_athlete_info(athlete_id):
        athlete = db.session.query(Athletes).filter(Athletes.athlete_id == athlete_id).first()
        print(type(athlete.swrid))
        if type(athlete.swrid) != str:
            swrid = 'NA'
        else:
            swrid = f'https://www.swimrankings.net/index.php?page=athleteDetail&athleteId={athlete.swrid}'

        return athlete, swrid

    def __repr__(self):
        return self.fullname


