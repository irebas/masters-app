from datetime import datetime
import json
from flask import Response


def calc_fina_points(swimtime: str, world_record: str) -> int:
    if world_record:
        t1 = datetime.strptime(swimtime, '%H:%M:%S.%f')
        t2 = datetime.strptime(world_record, '%H:%M:%S.%f')
        swimtime_ms = t1.minute * 6000 + t1.second * 100 + t1.microsecond / 10000
        world_record_ms = t2.minute * 6000 + t2.second * 100 + t2.microsecond / 10000
        fina_points = int(1000 * ((world_record_ms / swimtime_ms) ** 3))
    else:
        fina_points = 0

    return fina_points


def get_athlete_id(athlete_name: str):
    x = athlete_name.rfind(' ')
    last_letter = athlete_name[x - 1:x]
    gender = 'F' if last_letter == 'a' else 'M'
    athlete_id = f"{athlete_name[:3]}{athlete_name[(athlete_name.find(',') + 2):(athlete_name.find(',') + 2) + 3].upper()}{athlete_name[-5:-1]}{gender}"

    return athlete_id


def generate_json_response(data):
    json_string = json.dumps(data, ensure_ascii=False, default=str, indent=2)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response
