def parse_date_from_file(name,user):
    """Parses the date from the name of a saved file"""
    date = name
    date = date[date.find(user) + len(user) + 1:date.find(".txt")]
    date = date.split("-")
    final = date[-1].split("_")
    date.pop()
    for i in range(len(final) - 1):
        date.append(final[i])

    for i in range(len(date)):
        date[i]=int(date[i])
    return date
def what_time_is_it():
    from datetime import datetime
    """The output for this function is [year,month,day,hour,minute] as integers"""
    a = datetime.now().strftime("%Y %m %d %H %M").split()
    b = []
    for i in a:
        b.append(int(i))
    return b
def calculatetimepassed(initial, final):

    """Please note that the input and output is in the form [year,month,day,hour,minute]. This calculates how much
    time has passed since date 'initial' and date 'final'. """

    yearf = final[0]
    monthf = final[1]
    dayf = final[2]
    hourf = final[3]
    minutef = final[4]
    yeari = initial[0]
    monthi = initial[1]
    dayi = initial[2]
    houri = initial[3]
    minutei = initial[4]

    if minutef - minutei < 0:
        hourf = hourf - 1
        minutef += 60
    # 'mi' is the minutes passed
    mi = minutef - minutei

    if hourf - houri < 0:
        dayf = dayf - 1
        hourf += 24

    h = hourf - houri

    if dayf - dayi < 0:
        monthf = monthf - 1
        dayf += 30

    d = dayf - dayi

    if monthf - monthi < 0:
        yearf = yearf - 1
        monthf += 12

    m = monthf - monthi

    y = yearf - yeari
    return [y,m,d, h, mi]


def convert_to_days(date):
    # The input is in the format : [year,month,day,hour,minute]
    # This function will convert the amount of time passed into days
    # Each coeffiecent on the terms convert the unit to days:
    totaldays = date[2] + 30 * date[1] + 365 * date[0] + date[3] / 24 + date[4] / 1440
    """It is very important to remember that the input and output is in the format [year,month,day,hour,minute]"""
    return totaldays


def convert_to_hours(date):
    # The input is in the format : [year,month,day,hour,minute]
    # This function will convert the amount of time passed into hours
    # Each coeffiecent on the terms convert the coressponding unit to hours:

    return(date[0]*8760+date[1]*720	+ date[2]*24 + date[3] + date[4]/60)




