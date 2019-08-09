"""
This file implements all the auxiliar functions, used to manipulate the time data,
such as converting time from "HH:MM" to minutes format and vice versa, and doing
basic operations to them
"""

import os
import sys
# from datetime import date, timedelta
import datetime
import time
import calendar
import operator

from functools import reduce


def convert_to_int(input_time):
    """
    This function gets the time string and return the hrs and minutes as integers
    """
    hrs = int(input_time[0:input_time.index(':')])
    mins = int(input_time[input_time.index(':') + 1 :])
    return(hrs, mins)

def change_to_minutes(input_time):
    """
    This function converts the time from hrs:mins to minutes
    """
    hrs, mins = convert_to_int(input_time)
    return 60 * hrs + mins

def change_to_hours(minutes):
    """
    This function converts the time from minutes to hrs:mins format
    """
    mins = minutes % 60
    hrs = (minutes - mins) // 60
    return "{:02d}:{:02d}".format(hrs, mins)

def time_is_greater(time_one, time_two):
    """
    This function checks if the time_one is greater than the time_two
    """
    return change_to_minutes(time_one) > change_to_minutes(time_two)

def mult_time(input_time, factor):
    """
    This function is responsible to multiply the hour value
    """
    minutes = change_to_minutes(input_time)
    return change_to_hours(factor * minutes)

def sum_times(time_one, time_two, *args):
    """
    This function is responsible to add as many times as the user passes
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    total_sum = time_minutes_one + time_minutes_two
    for arg in args:
        total_sum += change_to_minutes(arg)
    return change_to_hours(total_sum)

def sum_times_list(input_list):
    """
    This function sums all the times inside a given list
    """
    total_sum = '00:00'
    for input_time in input_list:
        total_sum = sum_times(total_sum, input_time)
    return total_sum

def sub_times(time_one, time_two):
    """
    This function is responsible to subtract two times
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    return change_to_hours(time_minutes_two - time_minutes_one)

def total_worked_time(time_one=None, time_two=None, time_three=None, time_four=None, input_list=None):
    """
    This function is responsible for calculating the total time worked on a day
    """
    if input_list:
        time_one = input_list[0]
        time_two = input_list[1]
        time_three = input_list[2]
        time_four = input_list[3]
    return sum_times(sub_times(time_one, time_two), sub_times(time_three, time_four))

# pylint: disable=no-member
# pylint: disable=protected-access
# pylint: disable=broad-except
def get_absolute_resource_path(relative_path):
    """
    Function to handle the pyinstaller added data relative path
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        try:
            base_path = os.path.dirname(sys.modules['src'].__file__)
        except Exception:
            base_path = ''

        if not os.path.exists(os.path.join(base_path, relative_path)):
            base_path = 'src'

    path = os.path.join(base_path, relative_path)

    if not os.path.exists(path):
        return None

    return path

def get_dict_values_list(input_dict, key):
    """
    Method get a list of values from all occurences of a key on a dictionary
    """
    values_list = []
    for i, j in input_dict.items():
        for k in j.keys():
            values_list.append(input_dict[i][k][key])
    return values_list

def count_dict_value(input_dict, key, value):
    """
    Method to count the occurence of a value in the input dict
    """
    values_list = get_dict_values_list(input_dict, key)
    return int(values_list.count(value))

def csv_to_dict(csv_file):
    """
    Method to convert the csv file to a dict
    """
    dict_from_csv = {}
    with open(get_absolute_resource_path("resources/dictionaries/{}".format(csv_file))) as data_file:
        for row in data_file:
            row = row.strip().split(',')
            dict_from_csv.setdefault(int(row[0]), {})[int(row[1])] = {row[2] : row[3], row[4] : row[5],
                                                                      row[6] : row[7], row[8] : row[9],
                                                                      row[10] : row[11], row[12] : row[13],
                                                                      row[14] : row[15]}
    return dict_from_csv

def dict_to_csv(input_dict):
    """
    Method to convert the dict to csv file
    """
    print(input_dict)

def count_csv_values_from(csv_file, index, value):
    """
    Method to return the amount of values from a specified index
    """
    temp_list = []
    for i in range(0, csv_file.shape[0]):
        if csv_file.iloc[i][index] == value:
            temp_list.append(csv_file.iloc[i][index])
    return len(temp_list)

def get_current_week_data(csv_file, week):
    """
    Method to return a pandas archive containing only the current week data
    """
    current_week_data = csv_file[csv_file['week'] == week]
    return current_week_data

def get_current_month_data(csv_file, month):
    """
    Method to return a pandas archive containing only the current month data
    """
    current_month_data = csv_file[csv_file['month'] == month]
    return current_month_data

def parse_log_data_by(csv_file, day=None, week=None, month=None, year=None):
    """
    Method to parse the csv_data from work log data, returning a new pandas data with the required information
    """
    if day:
        return csv_file[csv_file['day'] == day]
    elif week:
        return csv_file[csv_file['week'] == week]
    elif month:
        return csv_file[csv_file['month'] == month]
    else:
        return csv_file[csv_file['year'] == year]


def  get_total_time_from(csv_file, week=None, month=None):
    """
    Method to return the total time by month or week
    """
    temp_list = []
    if week:
        search_type = 'week'
        value = week
    elif month:
        search_type = 'month'
        value = month
    else:
        for i in range(0, csv_file.shape[0]):
            if csv_file.iloc[i]['total_time']:
                temp_list.append(csv_file.iloc[i]['total_time'])
        return sum_times_list(temp_list)
    temp_df = csv_file[csv_file[search_type] == value]
    for i in range(0, temp_df.shape[0]):
        if temp_df.iloc[i]['total_time']:
            temp_list.append(temp_df.iloc[i]['total_time'])
    return sum_times_list(temp_list)

def get_month_from_week(year, week):
    """
    Method to get the month from a passed week number
    The returned month number will be the one most present on the week range
    """
    temp_date = datetime.date(year, 1, 1)
    delta = datetime.timedelta(days=(week-1)*7)
    first = temp_date + delta
    last = temp_date + delta + datetime.timedelta(days=6)
    if 4 < last.day < 7:
        return last.month
    return first.month

def get_ij_status(list_of_times):
    """
    Method to return all status from one day
    """
    work_one_ij = change_to_minutes(sub_times(list_of_times[0], list_of_times[1]))
    lunch_ij = change_to_minutes(sub_times(list_of_times[1], list_of_times[2]))
    work_two_ij = change_to_minutes(sub_times(list_of_times[2], list_of_times[3]))

    work_one_ij_status = "background-color : green" if 0 < work_one_ij <= 360 else "background-color : red"
    lunch_ij_status = "background-color : green" if 0 < lunch_ij <= 120 else "background-color : red"
    work_two_ij_status = "background-color : green" if 0 < work_two_ij <= 360 else "background-color : red"

    return work_one_ij_status, lunch_ij_status, work_two_ij_status

def get_work_time_status(times_list):
    """
    Method to check the total work time status from all week days
    """
    if '00:00' in times_list:
        return "color : gray"
    total_time = change_to_minutes(total_worked_time(input_list=times_list))
    if 300 < total_time < 480:
        return "color : orange"
    if total_time == 480:
        return "color : green"
    if 600 > total_time > 480:
        return "color : blue"
    return "color : red"

def get_week_days_list(year, week):
    """
    Method to return a list of lists containing the days af a given week
    """
    startdate = time.asctime(time.strptime('{} {} 1'.format(year, week-1), '%Y %W %w'))
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    days = [[(startdate + datetime.timedelta(days=i)).year, (startdate + datetime.timedelta(days=i)).month,
             (startdate + datetime.timedelta(days=i)).day] for i in range(0, 7)]
    return days

def get_month_days_list(year, month):
    """
    Method to return a list of lists containg the days of a given month
    """
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    return days

def get_from_dict(data_dict, map_list, extra_key=None):
    """
    Method to return the values from a dict path specified on a list
    """
    input_list = map_list.copy()
    if extra_key:
        input_list.append(extra_key)
    return reduce(operator.getitem, input_list, data_dict)

def set_in_dict(data_dict, map_list, extra_key, value):
    """
    Method to set the values from a dict path specified on a list
    """
    # get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value
    get_from_dict(data_dict, map_list)[extra_key] = value
