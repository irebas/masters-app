import pandas as pd
from flask import Blueprint, request, url_for, redirect, render_template, flash
bp_app = Blueprint('app', __name__)
from app.models import Results, Athletes, Meets, NationalRecords

DISTANCES = ['50 FREE', '100 FREE', '200 FREE', '400 FREE', '800 FREE', '1500 FREE', '50 BACK', '100 BACK', '200 BACK',
             '50 BREAST', '100 BREAST', '200 BREAST', '50 FLY', '100 FLY', '200 FLY', '100 MEDLEY', '200 MEDLEY',
             '400 MEDLEY', '4x50 FREE', '4x50 MEDLEY']
DISTANCES_IND = [x for x in DISTANCES if x not in ['4x50 FREE', '4x50 MEDLEY']]

COURSES=['SCM', 'LCM']
TYPES=['INDIVIDUAL', 'RELAY']
YEARS=['ALL', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013']
GENDERS = ['M', 'F', 'X']
AGE_GROUPS = ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74',
              '75-79', '80-84', '85-89', '90-94', '95-99']

@bp_app.route('/')
@bp_app.route('/index.html')
def home():
    return render_template('index.html')


@bp_app.route('/rankings.html', methods=['GET', 'POST'])
def rankings():
    if request.method == 'POST' and request.form.get('show'):
        year = request.form['year']
        event_gender = request.form['event_gender']
        course = request.form['course']
        distance = request.form['distance']
        top_results = Results.get_top_results(event_gender=event_gender,
                                              distance=distance,
                                              course=course,
                                              year=year)
        return render_template('rankings.html', top_results=top_results, distances=DISTANCES, courses=COURSES,
                               years=YEARS, genders=GENDERS, types=TYPES, year=year, event_gender=event_gender,
                               course=course, distance=distance)
    top_results = dict()
    return render_template('rankings.html', distances=DISTANCES, courses=COURSES,
                           years=YEARS, genders=GENDERS, types=TYPES, top_results=top_results)


@bp_app.route('/meets.html', methods=['GET', 'POST'])
def meets():
    meets = Meets.get_meets()
    return render_template('meets.html', meets=meets)

@bp_app.route('/records.html', methods=['GET', 'POST'])
def records():
    if request.method == 'POST' and request.form.get('show'):
        event_gender = request.form['event_gender']
        distance = request.form['distance']
        records = NationalRecords.get_records(gender=event_gender, distance=distance)
        # records = Results.get_records(event_gender=event_gender, distance=distance)
        return render_template('records.html', records=records, distances=DISTANCES, genders=GENDERS,
                               event_gender=event_gender, distance=distance)

    records = dict()
    return render_template('records.html', distances=DISTANCES, genders=GENDERS, types=TYPES, records=records)


@bp_app.route('/charts1.html', methods=['GET', 'POST'])
def charts1():
    athletes = Athletes.get_athletes()
    if request.method == 'POST' and request.form.get('show'):
        athlete_name = request.form['athlete_name']
        distance = request.form['distance']
        results_lc, results_sc, max_lc, max_sc = Results.get_athlete_results(athlete_name=athlete_name, distance=distance)
        print(results_sc)
        return render_template('charts1.html', results_lc=results_lc, results_sc=results_sc, max_lc=max_lc,
                               max_sc=max_sc, athlete_name=athlete_name, distance=distance, athletes=athletes,
                               distances=DISTANCES_IND)

    return render_template('charts1.html', athletes=athletes, distances=DISTANCES_IND)

@bp_app.route('/charts2.html', methods=['GET', 'POST'])
def charts2():
    athletes = Athletes.get_athletes()
    if request.method == 'POST' and request.form.get('show'):
        athlete_name_1 = request.form['athlete_name_1']
        athlete_name_2 = request.form['athlete_name_2']
        distance = request.form['distance']
        results_lc_1, results_sc_1, max_lc_1, max_sc_1 = Results.get_athlete_results(athlete_name=athlete_name_1,
                                                                                     distance=distance)
        results_lc_2, results_sc_2, max_lc_2, max_sc_2 = Results.get_athlete_results(athlete_name=athlete_name_2,
                                                                                     distance=distance)
        return render_template('charts2.html', results_lc_1=results_lc_1, results_sc_1=results_sc_1, max_lc_1=max_lc_1,
                               max_sc_1=max_sc_1, results_lc_2=results_lc_2, results_sc_2=results_sc_2,
                               max_lc_2=max_lc_2, max_sc_2=max_sc_2, athlete_name_1=athlete_name_1,
                               athlete_name_2=athlete_name_2, distance=distance, athletes=athletes,
                               distances=DISTANCES_IND)

    return render_template('charts2.html', athletes=athletes, distances=DISTANCES_IND)


@bp_app.route('/athletes.html', methods=['GET', 'POST'])
def athletes():
    results = []
    athletes = Athletes.get_athletes()
    # athlete_info = {'fullname': '', 'club': '', 'birthday': '', ''}
    if request.method == 'GET':
        if request.form.get('show'):
            athlete_name = request.form['athlete_name']
            df_results = Results.get_best_results(athlete_name)
            results = df_results.to_dict('records')
            athlete_info, swrid = Athletes.get_athlete_info(athlete_name)
            return render_template('athletes.html', results=results, athlete=athlete_info,
                                   swrid=swrid, athletes=athletes)

    return render_template('athletes.html', athletes=athletes)


@bp_app.route('/test.html', methods=['GET', 'POST'])
def test():
    pass


@bp_app.app_errorhandler(404)
def page_not_found(e):
    return "Aaaa"
    # return render_template('404.html'), 404


# https://codersdiaries.com/blog/flask-project-structure