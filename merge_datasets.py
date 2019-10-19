'''
Author: Shubham Patil (sbp5931@rit.edu)
'''

import math
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="BDA")

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


date_parser_mass = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
# date_parser_mary = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S %p')

mass_raw = pd.read_csv("Massachusetts.csv", parse_dates = ['OCCURRED_ON_DATE'], date_parser = date_parser_mass)
mary_raw = pd.read_csv("Maryland.csv", parse_dates = ['Start_Date_Time']) # date_parser = date_parser_mary

# Random 1000 samples
mass_raw = mass_raw.sample(n=10)
mary_raw = mary_raw.sample(n=10)

mass_final = pd.DataFrame()
mary_final = pd.DataFrame()

mass_final['IncidentNumber'] = mass_raw['INCIDENT_NUMBER'].apply(lambda x: x[1:10])
mary_final['IncidentNumber'] = mary_raw['Incident ID']

mass_final['OffenseCode'] = mass_raw['OFFENSE_CODE']
mary_final['OffenseCode'] = mary_raw['Offence Code']


mass_final['OffenseDescription'] = mass_raw['OFFENSE_DESCRIPTION']
mary_final['OffenseDescription'] = mary_raw['Crime Name3']

mass_final['OffenseCodeGroup'] = mass_raw['OFFENSE_CODE_GROUP']
mary_final['OffenseCodeGroup'] = mary_raw['Crime Name2']


mass_final['StreetName'] = mass_raw['STREET']
mary_final['StreetName'] = mary_raw['Street Name']

mass_datetime = mass_raw['OCCURRED_ON_DATE']
mary_datetime = mary_raw['Start_Date_Time']
mass_final['OccurredOnDate'] = mass_datetime.dt.date
mary_final['OccurredOnDate'] = mary_datetime.dt.date
mass_final['OccurredOnTime'] = mass_datetime.dt.time
mary_final['OccurredOnTime'] = mary_datetime.dt.time


mass_final['PoliceDistrictName'] = mass_raw['DISTRICT']
mary_final['PoliceDistrictName'] = mary_raw['Police District Number']

def geocode_reverse(lat, lng):
    if math.isnan(lat) or math.isnan(lng):
        return None
    else:
        return geolocator.reverse(f"{lat}, {lng}").address

mass_final['Address'] = mass_raw.apply(lambda x: geocode_reverse(x['Lat'], x['Long']), axis=1)
mary_final['Address'] = mary_raw.apply(lambda x: geocode_reverse(x['Latitude'], x['Longitude']), axis=1)

mass_final['Zipcode'] = mass_final['Address'].apply(lambda x: x.split(",")[-2] if x is not None else x)
mary_final['Zipcode'] = mary_final['Address'].apply(lambda x: x.split(",")[-2] if x is not None else x)
mass_final['City'] = mass_final['Address'].apply(lambda x: x.split(",")[-5:-4] if x is not None else x)
mary_final['City'] = mary_final['Address'].apply(lambda x: x.split(",")[-5:-4] if x is not None else x)
print(pd.concat([mass_final,mary_final], axis=1))
#print(mary_final['Address'].apply(lambda x: x.split(",") if x is not None else x))
