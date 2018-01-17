import re
import datetime

#{1,2}
#(?P<day>[0-2]{1,2})/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{2,4})

#match.group('day')
#match.group('month')
#match.group('year')

#date_search = re.compile(r'(?P<month>[\d]{1,2})/(?P<day>[\d]{1,2})/(?P<year>[\d]{2,4})')

def standardize_date_datetime(input_date):
    return datetime.datetime.strptime(input_date, "%m/%d/%Y").strftime("%m/%d/%Y")

def standardize_date(input_date):
    date_search = re.compile(r'(?P<month>[\d]{1,2})/(?P<day>[\d]{1,2})/(?P<year>[\d]{2,4})')
    parsed_date = date_search.search(input_date)
    month, day, year = parsed_date.groups()

    if len(month) == 1:
        output_month = '0' + month
    else:
        output_month = month
    
    if len(day) == 1:
        output_day = '0' + day
    else:
        output_day = day

    if len(year) == 2:
        output_year = '20' + year
    else:
        output_year = year

    print('{}/{}/{}'.format(output_month, output_day, output_year))