from app.models import Results, Athletes, Meets, NationalRecords
from app.variables import DISTANCES, DISTANCES_IND, COURSES, TYPES, YEARS, GENDERS
from app.utils import get_athlete_id, generate_json_response

from flask import Blueprint, request, render_template, jsonify

bp_app = Blueprint('app', __name__)


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
        records_nb = int(request.form['records_nb']) if request.form['records_nb'] != '' else 5
        top_results = Results.get_top_results(event_gender=event_gender, distance=distance, course=course,
                                              year=year, records_nb=records_nb)
        return render_template('rankings.html', top_results=top_results, distances=DISTANCES, courses=COURSES,
                               years=YEARS, genders=GENDERS, types=TYPES, year=year, event_gender=event_gender,
                               course=course, distance=distance, records_nb=records_nb)
    top_results = dict()
    return render_template('rankings.html', distances=DISTANCES, courses=COURSES, years=YEARS, genders=GENDERS,
                           types=TYPES, top_results=top_results)


@bp_app.route('/meets/<meet_code>', methods=['GET', 'POST'])
def meets(meet_code):
    if request.method == 'POST' and request.form.get('show'):
        event_gender = request.form['event_gender']
        distance = request.form['distance']
        results = Results.get_results(meet_code=meet_code, distance=distance, event_gender=event_gender)
        return render_template('meets.html', distances=DISTANCES, genders=GENDERS, results=results, distance=distance,
                               event_gender=event_gender)
    elif meet_code.lower() == 'all':
        return render_template('meets_list.html', meets=Meets.get_meets())
    else:
        return render_template('meets.html', distances=DISTANCES, genders=GENDERS, results=dict())


@bp_app.route('/records.html', methods=['GET', 'POST'])
def records():
    if request.method == 'POST' and request.form.get('show'):
        event_gender = request.form['event_gender']
        distance = request.form['distance']
        records = NationalRecords.get_records(gender=event_gender, distance=distance)
        return render_template('records.html', records=records, distances=DISTANCES, genders=GENDERS,
                               event_gender=event_gender, distance=distance)
    return render_template('records.html', distances=DISTANCES, genders=GENDERS, types=TYPES, records=dict())


@bp_app.route('/charts1.html', methods=['GET', 'POST'])
def charts1():
    athletes = Athletes.get_athletes()
    if request.method == 'POST' and request.form.get('show'):
        athlete_name = request.form['athlete_name']
        distance = request.form['distance']
        results = Results.get_athlete_results(athlete_name=athlete_name, distance=distance)
        return render_template('charts1.html', results_lc=results['results_lc'], results_sc=results['results_sc'],
                               max_lc=results['max_lc'], max_sc=results['max_sc'], athlete_name=athlete_name,
                               distance=distance, athletes=athletes, distances=DISTANCES_IND)

    return render_template('charts1.html', athletes=athletes, distances=DISTANCES_IND)


@bp_app.route('/charts2.html', methods=['GET', 'POST'])
def charts2():
    athletes = Athletes.get_athletes()
    if request.method == 'POST' and request.form.get('show'):
        athlete_name_1 = request.form['athlete_name_1']
        athlete_name_2 = request.form['athlete_name_2']
        distance = request.form['distance']
        results_1 = Results.get_athlete_results(athlete_name=athlete_name_1, distance=distance)
        results_2 = Results.get_athlete_results(athlete_name=athlete_name_2, distance=distance)
        return render_template('charts2.html', results_lc_1=results_1['results_lc'],
                               results_sc_1=results_1['results_sc'], max_lc_1=results_1['max_lc'],
                               max_sc_1=results_1['max_sc'], results_lc_2=results_2['results_lc'],
                               results_sc_2=results_2['results_sc'], max_lc_2=results_2['max_lc'],
                               max_sc_2=results_2['max_sc'], athlete_name_1=athlete_name_1,
                               athlete_name_2=athlete_name_2, distance=distance, athletes=athletes,
                               distances=DISTANCES_IND)

    return render_template('charts2.html', athletes=athletes, distances=DISTANCES_IND, results_1={}, results_2={})


@bp_app.route('/athletes.html', methods=['GET', 'POST'])
def athletes():
    athletes = Athletes.get_athletes()
    athlete_name = request.args.get('athlete_name')
    if athlete_name:
        try:
            athlete_id = Athletes.get_athlete_id(athlete_name)
        except TypeError:
            athlete_id = get_athlete_id(athlete_name)
        results = Results.get_best_results(athlete_id)
        athlete_info, swrid = Athletes.get_athlete_info(athlete_id)
        return render_template('athletes.html', results=results, athlete=athlete_info, swrid=swrid, athletes=athletes)
    return render_template('athletes.html', athletes=athletes)


@bp_app.route('/api.html')
def api():
    return render_template('api.html')


# API VIEWS
@bp_app.route('/api/records', methods=['GET'])
def api_records():
    event_gender = request.args.get('event_gender')
    distance = request.args.get('distance')
    if not event_gender or not distance:
        return jsonify(msg='Wrong API call')
    else:
        records = NationalRecords.get_records(gender=event_gender, distance=distance)
        return generate_json_response(records)


@bp_app.route('/api/rankings', methods=['GET'])
def api_rankings():
    year = request.args.get('year') if request.args.get('year') else 'ALL'
    event_gender = request.args.get('event_gender')
    course = request.args.get('course')
    distance = request.args.get('distance')
    records_nb = int(request.args.get('records_nb')) if request.args.get('records_nb') else 5
    if not event_gender or not course or not distance:
        return jsonify(msg='Wrong API call')
    else:
        results = Results.get_top_results(event_gender=event_gender, distance=distance, course=course,
                                          year=year, records_nb=records_nb)
        return generate_json_response(results)


@bp_app.route('/api/meets', methods=['GET'])
def api_meets():
    meet_code = request.args.get('meet_code')
    event_gender = request.args.get('event_gender')
    distance = request.args.get('distance')
    if not event_gender and not distance and not meet_code:
        return generate_json_response(Meets.get_meets())
    if not event_gender or not distance or not meet_code:
        return jsonify(msg='Wrong API call')
    else:
        results = Results.get_results(meet_code=meet_code, distance=distance, event_gender=event_gender)
        return generate_json_response(results)


@bp_app.route('/api/athletes', methods=['GET'])
def api_athletes():
    athlete_id = request.args.get('athlete_id')
    if not athlete_id:
        return generate_json_response(Athletes.get_all_athletes())
    else:
        results = Results.get_best_results(athlete_id=athlete_id)
        return generate_json_response(results)


@bp_app.route('/api/athletes_results', methods=['GET'])
def api_athletes_results():
    athlete_name = Athletes.get_athlete_name(request.args.get('athlete_id'))
    distance = request.args.get('distance')
    print(athlete_name)
    if not athlete_name or not distance:
        return jsonify(msg='Wrong API call')
    else:
        results = Results.get_athlete_results(athlete_name=athlete_name, distance=distance)
        return generate_json_response(results)


@bp_app.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html')
