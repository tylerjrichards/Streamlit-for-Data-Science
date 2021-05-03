import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_airplane = load_lottieurl('https://assets4.lottiefiles.com/packages/lf20_jhu1lqdz.json')
st_lottie(lottie_airplane, speed=1, height=200, key="initial")

st.title('Major US Airline Job Application')
st.write('by Tyler Richards')
st.subheader('Question 1: Airport Distance')
'''
The first exercise asks us 'Given the table of airports and 
locations (in latitude and longitude) below, 
write a function that takes an airport code as input and 
returns the airports listed from nearest to furthest from 
the input airport.' There are three steps here:

1. Load Data
2. Implement Distance Algorithm
3. Apply distance formula across all airports other than the input
4. Return sorted list of airports Distance
'''

#load necessary data
airport_distance_df = pd.read_csv('ex1_table.csv')

with st.echo():
	airport_distance_df = pd.read_csv('ex1_table.csv')

'''
From some quick googling, I found that the haversine distance is 
a good approximation for distance. At least good enough to get the 
distance between airports! Haversine distances can be off by up to .5%, 
because the earth is not actually a sphere. It looks like the latitudes 
and longitudes are in degrees, so I'll make sure to have a way to account 
for that as well. The haversine distance formula is labeled below, 
followed by an implementation in python
'''
st.image('haversine.png')

with st.echo():
	from math import radians, sin, cos, atan2, sqrt
	def haversine_distance(long1, lat1, long2, lat2, degrees=False):
	    #degrees vs radians
	    if degrees == True:
	        long1 = radians(long1)
	        lat1 = radians(lat1)
	        long2 = radians(long2)
	        lat2 = radians(lat2)
	    
	    #implementing haversine
	    a = sin((lat2-lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((long2-long1) / 2)**2
	    c = 2*atan2(sqrt(a), sqrt(1-a))
	    distance = 6371 * c #radius of earth in kilometers
	    return(distance)

#execute haversine function definition
from math import radians, sin, cos, atan2, sqrt
def haversine_distance(long1, lat1, long2, lat2, degrees=False):
    #degrees vs radians
    if degrees == True:
        long1 = radians(long1)
        lat1 = radians(lat1)
        long2 = radians(long2)
        lat2 = radians(lat2)
    
    #implementing haversine
    a = sin((lat2-lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((long2-long1) / 2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c #radius of earth in kilometers
    return(distance)

'''
Now, we need to test out our function! The 
distance between the default points is 
18,986 kilometers, but feel free to try out
your own points of interest. 
'''
long1 = st.number_input('Longitude 1', value = 2.55)
long2 = st.number_input('Longitude 2', value = 172.00)
lat1 = st.number_input('Latitude 1', value = 49.01)
lat2 = st.number_input('Latitude 2', value = -43.48)

test_distance = haversine_distance(long1 = long1, long2 = long2,
		lat1 = lat1, lat2 = lat2, degrees=True)
st.write('Your distance is: {} kilometers'.format(test_distance))

