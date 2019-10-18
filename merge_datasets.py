'''
Author: Shubham Patil (sbp5931@rit.edu)
'''

import math
import pandas as pd

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Shubham")

pd.set_option('display.max_columns', None)

mass_raw = pd.read_csv("Massachusetts.csv", parse_dates = True)
mary_raw = pd.read_csv("Maryland.csv", parse_dates = True)

# Random 1000 samples
mass_raw = mass_raw.sample(n=10)
mary_raw = mary_raw.sample(n=100)

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

mass_datetime = pd.to_datetime(mass_raw['OCCURRED_ON_DATE'])
mary_datetime = pd.to_datetime(mary_raw['Start_Date_Time'])
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
mary_final['ZipCode'] = mary_raw['Police District Number']

print(Geocoder('AIzaSyC9azed9tLdjpZNjg2_kVePWvMIBq154eA').reverse_geocode(42.28995318, -71.06076101))
print(geocoder.google([42.28995318, -71.06076101], method='reverse'))

print(geolocator.reverse(52.509669, 13.376294))
print(mass_final)
# print(mary_final)
