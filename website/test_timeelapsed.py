from datetime import datetime
import pytz
import time

def convert_time_format(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if hour == 0 and minutes != 0 and seconds != 0:
        if minutes == 1:
            return "%d minute and %d seconds." % (minutes, seconds)
        else:
            return "%d minutes and %d seconds." % (minutes, seconds)
    elif hour == 0 and minutes == 0 and seconds != 0:
        return "%d seconds." % (seconds)
    elif hour == 0 and minutes != 0 and seconds == 0:
        if minutes == 1:
            return "%d minute." % (minutes)
        else:
            return "%d minutes." % (minutes)
    elif hour != 0 and minutes == 0 and seconds == 0:
        return "%d hours." % (hour)
    elif hour != 0 and minutes != 0 and seconds == 0:
        if minutes == 1:
            return "%d hours and %d minute." % (hour, minutes)
        else:
            return "%d hours and %d minutes." % (hour, minutes)
    elif hour != 0 and minutes == 0 and seconds != 0:
        return "%d hours and %d seconds." % (hour, seconds)
    else:
        if minutes == 1:
            return "%d hours, %d minute, and %d seconds." % (hour, minutes, seconds)
        else:
            return "%d hours, %d minute, and %d seconds." % (hour, minutes, seconds)

def check_time_for_mineral(seconds):

    finish_mining_time = convert_time_format(seconds)
    for i in range(seconds):
        current_mining_time = convert_time_format(i)
        return f"{finish_mining_time}"
        time.sleep(1)