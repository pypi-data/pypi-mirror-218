import datetime
import arrow

if __name__ == '__main__':

    print('test date shift from iso')

    shift_weekday_enum = 4
    shift_week_amount = -4

    now = arrow.now()
    now_iso = now.isocalendar()
    then = now
    today_wkday = now_iso.weekday
    shift_days = now_iso.weekday - shift_weekday_enum
    then = then.shift(days=+shift_days)
    then = then.shift(weeks=+shift_week_amount).naive


    print(f'. exclude_date {then}')