import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests

password_attempt = st.text_input('Please Enter The Password')
if password_attempt != 'example_password':
	st.write('Incorrect Password!')
	st.stop()

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

airport_distance_df = pd.read_csv('airport_location.csv')

with st.echo():
	#load necessary data
	airport_distance_df = pd.read_csv('airport_location.csv')

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
st.write('Your distance is: {} kilometers'.format(int(test_distance)))

'''
We have the Haversine distance implemented, and we also have
proven to ourselves that it works reasonably well.
Our next step is to implement this in a function!
'''

def get_distance_list(airport_dataframe, airport_code):
    df = airport_dataframe.copy() 
    row = df[df.loc[:,'Airport Code'] == airport_code] 
    lat = row['Lat'] 
    long = row['Long'] 
    df = df[df['Airport Code'] != airport_code] 
    df['Distance'] = df.apply(lambda x: haversine_distance(lat1=lat, long1=long, 
    	lat2 = x.Lat, long2 = x.Long, degrees=True), axis=1)
    return(df.sort_values(by='Distance').reset_index()['Airport Code']) 

with st.echo():
	def get_distance_list(airport_dataframe, airport_code):
	    df = airport_dataframe.copy() #creates a copy of our dataframe for our function to use
	    row = df[df.loc[:,'Airport Code'] == airport_code] #selects the row from our airport code input
	    lat = row['Lat'] #get latitude
	    long = row['Long'] #get longitude
	    df = df[df['Airport Code'] != airport_code] #filter out our airport, implement haversine distance
	    df['Distance'] = df.apply(lambda x: haversine_distance(lat1=lat, long1=long, 
	    	lat2 = x.Lat, long2 = x.Long, degrees=True), axis=1)
	    return(df.sort_values(by='Distance').reset_index()['Airport Code']) #return values sorted

'''
To use this function, select an airport from the airports provided in the dataframe
and this application will find the distance between each one, and 
return a list of the airports closest to furthest.
'''

selected_airport = st.selectbox('Airport Code', airport_distance_df['Airport Code'])
distance_airports = get_distance_list(
	airport_dataframe=airport_distance_df, airport_code=selected_airport)
st.write('Your closest airports in order are {}'.format(list(distance_airports)))

'''
This all seems to work just fine! There are a few ways I would improve this if I was working on 
this for a longer period of time.  
1. I would implement the [Vincenty Distance](https://en.wikipedia.org/wiki/Vincenty%27s_formulae) 
instead of the Haversine distance, which is much more accurate but cumbersome to implement.  
2. I would vectorize this function and make it more efficient overall. 
Because this dataset is only 7 rows long, it wasn't particularly important, 
but if this was a crucial function that was run in production we would want to vectorize it for speed. 
'''

st.subheader('Question 2: Representation')

'''
For this transformation, there are a few things 
that I would start with. First, I would have to define 
what a unique trip actually was. In order to do this, I would 
group by the origin, the destination, and the departure date 
(for the departure date, often customers will change around 
this departure date, so we should group by the date plus or 
minus at least 1 buffer day to capture all the correct dates).   
Additionally, we can see that often users search from an entire city, 
and then shrink that down into a specific airport. So we should also 
consider a group of individual queries from cities and airports in the 
same city, as the same search, and do the same for destination.    
From that point, we should add these important columns to each unique search.
'''

example_df = pd.DataFrame(columns=['userid', 'number_of_queries', 'round_trip', 'distance', 'number_unique_destinations',
                     'number_unique_origins', 'datetime_first_searched','average_length_of_stay',
                     'length_of_search'])
example_row = {'userid':98593, 'number_of_queries':5, 'round_trip':1,
                   'distance':893, 'number_unique_destinations':5,
                     'number_unique_origins':1, 'datetime_first_searched':'2015-01-09',
                   'average_length_of_stay':5, 'length_of_search':4}
st.write(example_df.append(example_row, ignore_index=True))
'''
For answering the second part of the question, we should take the euclidian distance 
on two normalized vectors. There are two solid options for comparing two 
entirely numeric rows, the euclidian distance (which is just the straight line 
difference between two values), and the manhattan distance (think of this as the 
distance traveled if you had to use city blocks to travel diagonally across manhattan). 
Because we have normalized data, and the data is not high dimensional or sparse, I 
would recommend using the euclidian distance to start off. This distance would tell 
us how similar two trips were.
'''
