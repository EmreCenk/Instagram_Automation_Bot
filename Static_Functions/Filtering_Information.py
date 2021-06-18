from Static_Functions import working_with_dates as dt
from Static_Functions.Processing_Stats import findlist
from Static_Functions.working_with_dates import parse_date_from_file
from Static_Functions.Writing_Analysis_Files import path
import os

def filter_stat(stat):
    update = ""
    for i in stat:
        try:
            x = int(i)
            update += str(i)

        except:
            pass

    multiplier=1
    if "m" in stat:
        if "." in stat:
           multiplier=100000
        else:
            multiplier=1000000
    elif "k" in stat:
        if "." in stat:
            multiplier=100
        else:
            multiplier=1000


    stat = int(update)*multiplier
    return stat


def name_of_record(user,index=-1):
    """Returns string with the name of the users record with index 'index'."""


    pathtogo = path[0:-1]
    pathtogo = pathtogo + user
    # CHECKING TO SEE IF A FILE OF THIS PERSON EXISTS:
    try:
        os.chdir(pathtogo)
        files = os.listdir()
        date = files[index]

    except FileNotFoundError:
        date = ""
    return date

def divide_dm(message, separator=" "):
    """Takes a string as input. Returns an array that has divided the message onto smaller pieces according to the
    message character limit (999 in this case). """
    message=message.split(separator)

    c_len=0 #current length of mini message
    mini_message="" #Divided part of the message
    general_message=[]

    for word in message:
        if c_len+len(word)+len(separator)>=1000:
            c_len=len(word)+len(separator)
            general_message.append(mini_message)
            mini_message=word+separator
        else:
            mini_message+=word+separator
            c_len+=len(word)+len(separator)
    if mini_message!="":
        general_message.append(mini_message)
    return general_message


def get_records(user,how_many_days=7):
    """    RETURNS: [ARRAY_OF_FOLLOWERS,ARRAY_OF_FOLLOWING,ARRAY_OF_PEOPLE_WHO_HAVENT_FOLLOWED_BACK]   """


    name = name_of_record(user, -1)  # getting the latest report

    time_now = dt.what_time_is_it()
    time_then = parse_date_from_file(name, user)  # Get the date of the record as an array

    time_passed = dt.calculatetimepassed(time_then, time_now)

    time_passed = dt.convert_to_days(time_passed)  # find how much time has passed in terms of days

    if time_passed <= how_many_days:
        final = findlist(name, user)
    else:
        final=False


    return final