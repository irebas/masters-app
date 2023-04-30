from datetime import datetime

def calc_fina_points(swimtime: str, world_record: str) -> int:
    if world_record:
        t1 = datetime.strptime(swimtime, '%H:%M:%S.%f')
        t2 = datetime.strptime(world_record, '%H:%M:%S.%f')
        swimtime_ms = t1.minute * 6000  + t1.second * 100 + t1.microsecond / 10000
        world_record_ms = t2.minute * 6000 + t2.second * 100 + t2.microsecond / 10000
        fina_points = int(1000 * ((world_record_ms / swimtime_ms) ** 3))
    else:
        fina_points = 0

    return fina_points
