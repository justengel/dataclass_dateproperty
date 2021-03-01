

def run_basic_example():
    import time
    import datetime
    from dataclass_property import dataclass, field, fields
    from dataclass_dateproperty import datetime_property, time_property, date_property, Weekdays, weekdays_property

    now = datetime.datetime.now()
    time.sleep(0.1)

    @dataclass
    class Alarm:
        timer = datetime_property(default_factory=datetime.datetime.now)
        weekdays: Weekdays = field(default_factory=Weekdays(monday=True).copy)
        sunday: bool = weekdays_property('sunday')
        monday: bool = weekdays_property('monday')
        tuesday: bool = weekdays_property('tuesday')
        wednesday: bool = weekdays_property('wednesday')
        thursday: bool = weekdays_property('thursday')
        friday: bool = weekdays_property('friday')
        saturday: bool = weekdays_property('saturday')

    a = Alarm()
    fs = [f.name for f in fields(a)]
    assert 'timer' in fs, fs
    assert 'weekdays' in fs
    assert 'sunday' in fs
    assert 'monday' in fs
    assert 'tuesday' in fs
    assert 'wednesday' in fs
    assert 'thursday' in fs
    assert 'friday' in fs
    assert 'saturday' in fs

    assert a.timer > now
    assert a.weekdays.sunday is False
    assert a.weekdays.monday is True
    assert a.weekdays.tuesday is False
    assert a.sunday is False
    assert a.monday is True
    assert a.tuesday is False

    a = Alarm(timer=now, sunday=True)
    assert a.timer == now
    assert a.weekdays.sunday is True
    assert a.weekdays.monday is True
    assert a.weekdays.tuesday is False
    assert a.sunday is True
    assert a.monday is True
    assert a.tuesday is False


if __name__ == '__main__':
    run_basic_example()
