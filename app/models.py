import pandas as pd

from app.database import db
from sqlalchemy import and_, asc
from app.utils import calc_fina_points
from sqlalchemy.orm import class_mapper
from app.variables import AGE_GROUPS_IND, AGE_GROUPS_REL, CUSTOM_DICT


def convert_sqlalch_obj_to_dict(query_results):
    results = list()
    for result in query_results:
        columns = [c.key for c in class_mapper(result.__class__).columns]
        result_dict = dict((c, getattr(result, c)) for c in columns)
        results.append(result_dict)

    return results


class Meets(db.Model):
    __tablename__ = 'meets'
    meet_code = db.Column('meet_code', db.String, primary_key=True)
    meet_name = db.Column('meet_name', db.String, primary_key=True)
    meet_city = db.Column('meet_city', db.String, primary_key=True)
    meet_date = db.Column('meet_date', db.Date, primary_key=True)
    meet_year = db.Column('meet_year', db.String, primary_key=True)

    def __init__(self, meet_code, meet_name, meet_city, meet_date, meet_year):
        self.meet_code = meet_code
        self.meet_name = meet_name
        self.meet_city = meet_city
        self.meet_date = meet_date
        self.meet_year = meet_year

    @staticmethod
    def get_meets():
        meets_query = db.session.query(Meets).all()
        meets = convert_sqlalch_obj_to_dict(meets_query)
        return meets


class NationalRecords(db.Model):
    __tablename__ = 'national_records'
    athlete_id = db.Column('athlete_id', db.String)
    athlete_name = db.Column('athlete_name', db.String)
    club_name = db.Column('club_name', db.String)
    course = db.Column('course', db.String, primary_key=True)
    meet_city = db.Column('meet_city', db.String)
    date = db.Column('date', db.Date)
    distance = db.Column('distance', db.String)
    swimtime = db.Column('swimtime', db.String)
    age_group = db.Column('age_group', db.String, primary_key=True)
    gender = db.Column('gender', db.String, primary_key=True)
    result_type = db.Column('result_type', db.String, primary_key=True)

    def __init__(self, athlete_id, athlete_name, club_name, course, meet_city, date,
                 distance, swimtime, age_group, result_type):
        self.athlete_id = athlete_id
        self.athlete_name = athlete_name
        self.club_name = club_name
        self.course = course
        self.meet_city = meet_city
        self.date = date
        self.distance = distance
        self.swimtime = swimtime
        self.age_group = age_group
        self.result_type = result_type

    @staticmethod
    def get_records(gender: str, distance: str):
        if distance not in ['4x50 FREE', '4x50 MEDLEY']:
            result_type = 'INDIVIDUAL'
        else:
            result_type = 'RELAY'
            distance = distance[2:]
        records_lc = db.session.query(NationalRecords).filter(and_(NationalRecords.gender == gender,
                                                                   NationalRecords.distance == distance,
                                                                   NationalRecords.course == 'LCM',
                                                                   NationalRecords.result_type == result_type)).all()
        records_sc = db.session.query(NationalRecords).filter(and_(NationalRecords.gender == gender,
                                                                   NationalRecords.distance == distance,
                                                                   NationalRecords.course == 'SCM',
                                                                   NationalRecords.result_type == result_type)).all()
        records = {'LONG COURSE METERS': convert_sqlalch_obj_to_dict(records_lc),
                   'SHORT COURSE METERS': convert_sqlalch_obj_to_dict(records_sc)}
        return records


class WR(db.Model):
    __tablename__ = 'world_records'
    id = db.Column('id', db.Integer, primary_key=True)
    distance = db.Column('distance', db.String)
    course = db.Column('course', db.String)
    gender = db.Column('gender', db.String)
    fullname = db.Column('fullname', db.String)
    nationality = db.Column('nationality', db.String)
    swimtime = db.Column('swimtime', db.String)
    meet_name = db.Column('meet_name', db.String)
    meet_date = db.Column('meet_date', db.Date)

    def __init__(self, distance, course, gender, fullname, nationality, swimtime, meet_name, meet_date):
        self.distance = distance
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
    date = db.Column('date', db.Date)
    distance = db.Column('distance', db.String)
    event_gender = db.Column('event_gender', db.String)
    age_group = db.Column('age_group', db.String)
    athlete_name = db.Column('athlete_name', db.String)
    athlete_id = db.Column('athlete_id', db.String)
    birthdate = db.Column('birthdate', db.String)
    birth_year = db.Column('birth_year', db.String)
    gender = db.Column('gender', db.String)
    nation = db.Column('nation', db.String)
    swrid = db.Column('swrid', db.String)
    license_nb = db.Column('license_nb', db.String)
    club_name = db.Column('club_name', db.String)
    place = db.Column('place', db.Integer)
    swimtime = db.Column('swimtime', db.String)
    result_type = db.Column('result_type', db.String)
    row_id = db.Column('row_id', db.String, primary_key=True)

    def __init__(self, meet_code, meet_name, meet_year, meet_city, course, date, distance, event_gender, age_group,
                 athlete_name, athlete_id, birthdate, birth_year, gender, nation, swrid, license_nb, club_name,
                 place, swimtime, result_type, row_id):
        self.meet_code = meet_code
        self.meet_name = meet_name
        self.meet_year = meet_year
        self.meet_city = meet_city
        self.course = course
        self.date = date
        self.distance = distance
        self.event_gender = event_gender
        self.age_group = age_group
        self.athlete_name = athlete_name
        self.athlete_id = athlete_id
        self.birthdate = birthdate
        self.birth_year = birth_year
        self.gender = gender
        self.nation = nation
        self.swrid = swrid
        self.license_nb = license_nb
        self.club_name = club_name
        self.place = place
        self.swimtime = swimtime
        self.result_type = result_type
        self.row_id = row_id

    @staticmethod
    def get_results(meet_code: str, distance: str, event_gender: str):
        results = dict()
        if distance not in ['4x50 FREE', '4x50 MEDLEY']:
            result_type = 'INDIVIDUAL'
            age_groups = AGE_GROUPS_IND
        else:
            result_type = 'RELAY'
            distance = distance[2:]
            age_groups = AGE_GROUPS_REL
        for age_group in age_groups:
            results_ag = db.session.query(Results).filter(and_(Results.event_gender == event_gender,
                                                               Results.distance == distance,
                                                               Results.age_group == age_group,
                                                               Results.meet_code == meet_code,
                                                               Results.result_type == result_type,
                                                               Results.place != -1)).order_by(asc(Results.place))

            results[age_group] = convert_sqlalch_obj_to_dict(results_ag)
        return results

    @staticmethod
    def get_top_results(event_gender: str, course: str, distance: str, year: str, records_nb: int):
        top_results = dict()
        if distance not in ['4x50 FREE', '4x50 MEDLEY']:
            result_type = 'INDIVIDUAL'
            age_groups = AGE_GROUPS_IND
        else:
            result_type = 'RELAY'
            distance = distance[2:]
            age_groups = AGE_GROUPS_REL
        year = '2%' if year == 'ALL' else year
        for age_group in age_groups:
            results_ag = db.session.query(Results).filter(and_(Results.event_gender == event_gender,
                                                               Results.course == course,
                                                               Results.distance == distance,
                                                               Results.result_type == result_type,
                                                               Results.age_group == age_group,
                                                               Results.meet_year.like(year),
                                                               Results.place != -1)).order_by(asc(Results.swimtime)
                                                                                              ).all()
            results_ag = results_ag[:records_nb]
            top_results[age_group] = convert_sqlalch_obj_to_dict(results_ag)
        return top_results

    @staticmethod
    def get_best_results(athlete_id: str):
        sql = db.session.query(Results,
                               WR.swimtime.label('world_record')).join(WR, and_(WR.distance == Results.distance,
                                                                                WR.gender == Results.gender,
                                                                                WR.course == Results.course),
                                                                       isouter=True).filter(and_(
                                                                                    Results.athlete_id == athlete_id,
                                                                                    Results.place != -1,
                                                                                    Results.result_type.in_(
                                                                                        ['INDIVIDUAL', 'RELAY_SPLIT']))
                                                                  ).statement
        df = pd.read_sql(sql=sql, con=db.session.get_bind())
        # window function - get best time partitioned by course, stroke and athlete_id
        df['stroke_rank'] = df.groupby(['course', 'distance', 'athlete_id',
                                        'result_type'])['swimtime'].rank(method='first', ascending=True)
        df = df.loc[(df['stroke_rank'] == 1)]
        # assign sort mapping
        df.reset_index(inplace=True, drop=True)
        df['distance'] = [x if y == 'INDIVIDUAL' else f'{x} SPLIT' for x, y in zip(df['distance'], df['result_type'])]
        df['sort_rank'] = df['distance'].map(CUSTOM_DICT)
        # calculate fina points
        df['fina_points'] = [calc_fina_points(x, y) for x, y in zip(df['swimtime'], df['world_record'])]
        df.sort_values(by=['sort_rank', 'course'], inplace=True, ascending=[True, True])
        df = df[['athlete_id', 'athlete_name', 'distance', 'course', 'meet_code', 'meet_name', 'meet_city',
                 'date', 'swimtime', 'fina_points']]
        results = df.to_dict('records')
        return results

    @staticmethod
    def get_athlete_results(athlete_name: str, distance: str):
        sql = db.session.query(Results.swimtime, Results.athlete_id, Results.athlete_name, Results.date,
                               Results.meet_city, Results.course, Results.distance,
                               WR.swimtime.label('world_record')).join(WR, and_(WR.distance == Results.distance,
                                                                                WR.gender == Results.gender,
                                                                                WR.course == Results.course),
                                                                       isouter=True).filter(and_(
                                                                                Results.athlete_name == athlete_name,
                                                                                Results.distance == distance,
                                                                                Results.result_type == 'INDIVIDUAL',
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
        results_all = {'results_lc': results_lc, 'results_sc': results_sc, 'max_lc': max_lc, 'max_sc': max_sc}
        return results_all

    def __repr__(self):
        return self.athlete_id


class Athletes(db.Model):
    __tablename__ = 'athletes'
    athlete_id = db.Column('athlete_id', db.String, primary_key=True)
    athlete_name = db.Column('athlete_name', db.String)
    birth_year = db.Column('birth_year', db.String)
    club_name = db.Column('club_name', db.String)
    last_entry = db.Column('last_entry', db.Date)
    swrid = db.Column('swrid', db.String)

    def __init__(self, athlete_id, athlete_name, birth_year, club_name, last_entry, swrid):
        self.athlete_id = athlete_id
        self.athlete_name = athlete_name
        self.birth_year = birth_year
        self.club_name = club_name
        self.last_entry = last_entry
        self.swrid = swrid

    @staticmethod
    def get_athletes():
        athletes = [r.athlete_name for r in db.session.query(Athletes)]
        athletes.sort()
        return athletes

    @staticmethod
    def get_all_athletes():
        return convert_sqlalch_obj_to_dict(db.session.query(Athletes))

    @staticmethod
    def get_athlete_name(athlete_id: str):
        athlete_name = db.session.query(Athletes.athlete_name).filter(Athletes.athlete_id == athlete_id).first()[0]
        return athlete_name

    @staticmethod
    def get_athlete_id(athlete_name: str):
        athlete_id = db.session.query(Athletes.athlete_id).filter(Athletes.athlete_name == athlete_name).first()[0]
        return athlete_id

    @staticmethod
    def get_athlete_info(athlete_id):
        athlete = db.session.query(Athletes).filter(Athletes.athlete_id == athlete_id).first()
        if type(athlete.swrid) != str:
            swrid = 'NA'
        else:
            swrid = f'https://www.swimrankings.net/index.php?page=athleteDetail&athleteId={athlete.swrid}'

        return athlete, swrid

    def __repr__(self):
        return self.fullname
