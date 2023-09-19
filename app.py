import streamlit as st
import folium
from streamlit_folium import st_folium
import pydeck as pdk
import polyline
import pandas as pd
import googlemaps
import datetime
import itertools
import random
from core.router import get_direction, DirectionConfig
from dotenv import load_dotenv
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import g4f

provider=g4f.Provider.You

load_dotenv()

try:
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))


    st.set_page_config(layout="wide")

    if "markers" not in st.session_state:
        st.session_state["markers"] = []
        
    if "markers1" not in st.session_state:
        st.session_state["markers1"] = []


    st.write("# UberLand perfect transit")
    st.write("### :orange[ Team: taxi drivers (Ryan Gosling)]")


    prices=pd.read_csv('data/prices.csv')


    # The line `m = folium.Map(...)` is creating a Folium map object. It sets the initial location of the
    # map to (-33.87318,151.20701), which corresponds to the latitude and longitude of a specific
    # location. It also specifies the map tiles to be used from the Mapbox API and sets the zoom level of
    # the map to 16.
    m = folium.Map(location=(-33.87318,151.20701), tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWR2cHJvcDExIiwiYSI6ImNsbWx3ZW02ZjBoMjEyaXBna2MyOGx2eDkifQ.XGZz3RDWSKBebpjuqsMJMg", attr='none', zoom_start=16)
    m1 = folium.Map(location=(-33.87318,151.20701), tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWR2cHJvcDExIiwiYSI6ImNsbWx3ZW02ZjBoMjEyaXBna2MyOGx2eDkifQ.XGZz3RDWSKBebpjuqsMJMg", attr='none', zoom_start=16)

    def pdk_graph(df1):
        """
        The function `pdk_graph` takes a DataFrame `df1` as input and creates a PyDeck graph visualization
        based on the data in the DataFrame.
        
        :param df1: The parameter `df1` is a DataFrame that contains the data for creating the path layer in
        the PyDeck graph. It should have the following columns: path, color, name
        :return: a PyDeck chart object.
        """
        view_state = pdk.ViewState(
            latitude=df1.iloc[0]['path'][0][1],
            longitude=df1.iloc[0]['path'][0][0],
            zoom=11
        )

        layer = pdk.Layer(
            type='PathLayer',
            data=df1,
            pickable=True,
            get_color='color',
            width_scale=5,
            width_min_pixels=2,
            get_path='path',
            get_width=5
        )

        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={'text': '{name}'})
        return st.pydeck_chart(r)


    fg = folium.FeatureGroup(name="Markers")
    fg1 = folium.FeatureGroup(name="Markers1")

    for marker in st.session_state["markers"]:
        fg.add_child(marker)
    for marker in st.session_state["markers1"]:
        fg1.add_child(marker)

    pickup_coords=None
    target_coords=None
    country = None
    target_cost_transport = None
    
        
    left, right = st.columns(2)
    with left:
        pickup = st.text_input('Write pickup point')
        # googlemaps.places_autocomplete('new', session_token='AIzaSyBKgD8C__tyR3fnWy3HsommzNnEZ7EETVw',  types='(cities)')
        st.write('Pickup location')
        st_data = st_folium(m, center = st.session_state["center"],width=720, feature_group_to_add=fg)
        
    with right:
        target = st.text_input('Write target point')
        st.write('Target location')
        st_data1 = st_folium(m1, center=st.session_state["center1"], width=720, feature_group_to_add=fg1, key='1')

    pickup_loc=[]

    if pickup:
            pickup_place=gmaps.places_autocomplete(pickup)[0]['place_id']
            country=gmaps.place(pickup_place, fields=['formatted_address'])['result']["formatted_address"].split(',')[-1]
            st.write(country)
            pickup_coords=list(gmaps.place(pickup_place)['result']['geometry']['location'].values())
            pickup_loc.append(pickup_coords)
            if "markers" in st.session_state:
                st.session_state['markers'].append(folium.Marker(
                pickup_coords, popup='Pickup')
            )
            

    targets=[]

    if target:
            target_place=gmaps.places_autocomplete(target)[0]['place_id']
            target_coords=list(gmaps.place(target_place)['result']['geometry']['location'].values())
            st.write(target_coords)
            targets.append(target_coords)
            st.session_state['markers1'].append(folium.Marker(
                target_coords, popup='Target')
            )
    
    if (pickup_coords):
        st.session_state['center'] = pickup_coords
    else:
        st.session_state['center'] = (-33.87318,151.20701)
    if (target_coords):
        st.session_state['center1'] = target_coords
    else:
        st.session_state['center1'] = (-33.87318,151.20701)

    st.write('Directions Config')

    left, right = st.columns(2)
    with left:
        toll_state = st.checkbox('Avoid tolls 💸')
        high_state = st.checkbox('Avoid highways 🛣️')
        ferry_state = st.checkbox('Avoid ferries ⛴️')
        indoor_state = st.checkbox('Avoid indoor 🐹')
        elderly_state = st.checkbox('Elderly 👵🏿')
        
    with right:
        
        if country: 
            try:
                target_cost_transport = prices['sorting_1'][prices['odd 2'] == str(country).lstrip().rstrip()].to_list()[0]
            except:
                target_cost_transport = 1

        # budget_state = st.text_input("Budget 💷")
        # transit_mode = st.selectbox("Transport",["bus"]) #  c nizhney tak nado https://stackoverflow.com/questions/58053077/get-distance-from-google-cloud-maps-directions-api
        max_walk_time = float(st.text_input("Max walk time ⌚️",10))*60
        departute_time = datetime.datetime.now()




    if st_data["last_clicked"]:
        # pickup_loc.append(st_data["last_clicked"]) # pickup location
        if len(pickup_loc)<2:
                st.session_state['markers'].append(folium.Marker(
                list(st_data["last_clicked"].values())
                ))
        else:
            st.session_state['markers'].append(folium.Marker(
                pickup_coords, popup='Pickup')
            )

    if st_data1["last_clicked"]:
        targets.append(list(st_data1["last_clicked"].values())) # target location
        st.session_state['markers1'].append(folium.Marker(
            list(st_data1["last_clicked"].values())
        ))


    directions = None    
    
    if len(pickup_loc)>0 and len(targets)>0:
        
        length = float(2000)
        number_of_stops = int(5)
        research_alpha_bus = length/number_of_stops
        # st.write(targets[:-2])
        st.write(tuple(pickup_loc[0]))
        st.write(tuple(targets[-1]))
        directions = DirectionConfig(from_loc=tuple(pickup_loc[0]), 
                                    waypoints=targets[:-2],
                                    to_loc=tuple(targets[-1]),
                                    departute_time=departute_time,
                                    max_walk_time=max_walk_time,
                                    transit_mode=["bus","subway","train"],
                                    elderly=elderly_state,
                                    transport_fee=float(target_cost_transport),
                                    taxi_fee=float(target_cost_transport),
                                    research_alpha_bus=research_alpha_bus,
                                    avoid=['avoidToll' if toll_state else ""]
                                    )
    statistics = None

    if statistics:
        st.metric("CO2 emissions reduced by","0.3kg",-1.2)

    r,e,a = st.tabs(["Route","Eco Route","Alternative"])

    data = None
    if directions:
            data = get_direction(directions)
    with r:
        if data:
            steps = data[0].steps
            st.metric("CO2 emissions reduced by",'10%',-data[0].co2)
            df_r=pd.DataFrame(columns=['name','path','color'])
            for step in steps:
                st.write(step)
                if type(step.polyline) is list:
                    c=random.randrange(1,255)
                    c1=random.randrange(1,255)
                    st.write(step.polyline)
                    merged = list(itertools.chain(*[step.polyline]))
                    # st.write(list(map(lambda x: x.points,merged)))
                    for i in merged:
                        polys = polyline.decode(str(i.points))
                        df_r.loc[len(df_r)] = pd.Series({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,c1,c)} )
                    
                else: 
                    polys = polyline.decode(str(step.polyline.points))
                    df_r.loc[len(df_r)] = pd.Series({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,random.randrange(1,255),random.randrange(1,255))})
            
            pdk_graph(df_r)
            st.write("Arrival time:",(datetime.datetime.now()+datetime.timedelta(seconds=data[0].total_duration)).strftime("%H:%M, %d.%m"))
            st.write("Total Cost:", str(round(data[0].total_cost,2)), "USD")
            st.write("Total Taxi Cost:", str(round(data[0].total_taxi_cost, 2)), "USD")
            st.write("CO2 emissions:", str(round(data[0].co2, 2)))
            
except Exception as e:
    # response = g4f.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": f"so you got this error {e}, describe this error to end user (dont tell anything about code error or something)"}],
    #         provider=provider,
    #         proxy='zPM6ju8G:inyA2RYN@91.204.182.244:63522'
    #     )
    st.write(e)
    


