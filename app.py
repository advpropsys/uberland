import streamlit as st
import folium
from streamlit_folium import st_folium
import pydeck as pdk
import polyline
import pandas as pd
import googlemaps
import datetime
import random
from core.router import get_direction, DirectionConfig
from dotenv import load_dotenv
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))


st.set_page_config(layout="wide")

if "markers" not in st.session_state:
    print("markers1")
    st.session_state["markers"] = []
    
if "markers1" not in st.session_state:
    st.session_state["markers1"] = []


st.write("# UberLand perfect transit")
st.write("### :orange[ Team: taxi drivers (Ryan Gosling)]")


prices=pd.read_csv('/Users/apsys/Downloads/prices.csv')

df=pd.DataFrame(columns=['name','path'])
df=df.append({'name':'name','path':list(map(lambda x: x[::-1],polyline.decode('jzvmEyr{y[pAFAr@Am@j@?fCRpCt@\\Dd@Cn@Mh@QjA}@p@w@v@{Al@m@t@i@x@c@z@]|@W\\I~AQn@CF@jAN`AFrG`AnATnB^|@T|Bt@b@Px@b@hAp@p@f@`DvEt@d@l@r@zBbDbB~Br@zALd@dAdBx@jArAvAxAnAvDlCf@b@~BpBzCnCnA|A~@hAz@rAvAjCx@dB~@|BpBrFz@bD^hBRtAh@lDt@`D~BjKv@dD|@lDlB|Hx@pD`BfHZpB^dDRrCDdEBzGAvAKxCEhB?dBK~BIp@]jBm@fCm@hB]x@sBzDoAjCe@nAo@jCs@rCw@rCg@bBk@bCa@dCStBGvA?pDHrC\\bG\\tDT~BJ`B@fBIjCYxCy@jEk@bCWvAMlAI~@QnCBfDPtBd@dE\\`EHfBC|DUrD_@zD_@tD_@vBiAxEmA~FoBfImA~EOx@iA~Eg@pBgAlDaA~CYhAa@|B_@bCWtBMrBGfDI~DSvKGjAMdBUlB]lCs@dDm@bCo@vCsA|EcAnD}@hD_AxD_A~E{@bEkA`FwAtFeAdD[z@oAvCoCbGeBxDkAfCuAxBw@tAyAfCoBnDiDxEoE`GwAzB}@|AgAhCg@|Ak@vBWnAeBdJo@xEW|Be@tE_@vD]~CQ`AWfA}@lC{AbDk@`Ai@r@gBnBmCjCqBdBk@l@{@|@{@nAsCbFmAbBoD~DgB|Bu@dAq@hAe@~@m@zAeBfF}@lBgAtBq@tAyAzDgBbFk@xBs@hD}@fEgBtIoAhG]jCYxDGlDDdDFrAj@fGZdGJrBFrB?rBMlE[zDoAtKc@`C[xCg@rESdDO|EE`CCxEJrLRbDNxA`@|CR`AXrBLdBDjA?rBStH@|GC|FIfMDnAAdBAhAKxBOxAUnBO`Aa@bBy@pCy@|Bg@fA_@n@oAjBm@x@w@|@yAtAkAz@{XdQiW`P_GrDkCdB{B~AcClBcB|AgFnFmEpEg@b@_@XwA|Ak@f@u@n@iA`AoBtBoG~GwDzDo@f@IF]\\}FbG{EnFuAlBiDnFoAhCkAxCgBhD_@v@e@r@Qh@aDbGqHhNmB`DwFvKqBpDcBdDq@|@INiAvAiAfAaBhAkAf@gCfAq@T_Cr@}DbAi@J[@m@FgBHyBDiDMeDYcE{@mCUsBCuADaBFkB`@oAd@a@Vo@`@gAr@oA`Aq@j@o@h@yAfBs@rARNaB\\ECOj@Id@Ib@Mp@UtACTAJKFa@PMFUH_C\\KDYPYJM@OAEXm@lE')))}, ignore_index=True)
df['color']=[(255,255,153)]*len(df)


m = folium.Map(location=(-33.87318,151.20701), tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWR2cHJvcDExIiwiYSI6ImNsbWx3ZW02ZjBoMjEyaXBna2MyOGx2eDkifQ.XGZz3RDWSKBebpjuqsMJMg", attr='none', zoom_start=16)
m1 = folium.Map(location=(-33.87318,151.20701), tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWR2cHJvcDExIiwiYSI6ImNsbWx3ZW02ZjBoMjEyaXBna2MyOGx2eDkifQ.XGZz3RDWSKBebpjuqsMJMg", attr='none', zoom_start=16)

def pdk_graph(df1):
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
pdk_graph(df)

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
    st_data = st_folium(m, width=720, feature_group_to_add=fg)
    
with right:
    target = st.text_input('Write target point')
    st.write('Target location')
    st_data1 = st_folium(m1, width=720, feature_group_to_add=fg1, key='1')
    
pickup_loc=[]

if pickup:
        pickup_place=gmaps.places_autocomplete(pickup)[0]['place_id']
        country=gmaps.place(pickup_place)['result']['address_components'][-2].get('long_name')
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

st.write('Directions Config')

left, right = st.columns(2)
with left:
    toll_state = st.checkbox('Avoid tolls 💸')
    high_state = st.checkbox('Avoid highways 🛣️')
    ferry_state = st.checkbox('Avoid ferries ⛴️')
    indoor_state = st.checkbox('Avoid indoor 🐹')
    fewer_walk_state = st.checkbox('Fewer walking 🩼👩🏿‍🦼')
    fewer_transfers_state = st.checkbox('Fewer transfers 🔂')
    elderly_state = st.checkbox('Elderly 👵🏿')
    
with right:
    
    if country: 
        target_cost_transport = prices['sorting_1'][prices['odd 2'] == country].to_list()[0]

    budget_state = st.text_input("Budget 💷")
    transit_mode = st.selectbox("Transport",["bus"]) #  c nizhney tak nado https://stackoverflow.com/questions/58053077/get-distance-from-google-cloud-maps-directions-api
    max_walk_time = float(st.text_input("Max walk time ⌚️"))*60
    max_transfers = st.text_input('Max transfers')
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


directions = None    
 
if len(pickup_loc)>0 and len(targets)>0:
    st.write(pickup_loc,targets)
    directions = DirectionConfig(tuple(pickup_loc[0]), 
                                 targets,
                                 tuple(targets[-1]),
                                 departute_time,
                                 max_walk_time,
                                 transit_mode,
                                 elderly_state,
                                 float(target_cost_transport),
                                 float(target_cost_transport),
                                 )
    
    
if st_data1["last_clicked"]:
    targets.append(st_data1["last_clicked"]) # target location
    st.session_state['markers1'].append(folium.Marker(
        list(st_data1["last_clicked"].values())
    ))
    
statistics = None

if statistics:
    st.metric("CO2 emissions reduced by","0.3kg",-1.2)

r,e,a = st.tabs(["Route","Eco Route","Alternative"])

data = None
if directions:
        data = get_direction(directions)
        st.write(data)
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
                for i in step.polyline:
                    polys = polyline.decode(str(i.points))
                    df_r=df_r.append({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,c1,c)}, ignore_index=True)
            else: 
                polys = polyline.decode(str(step.polyline.points))
                df_r=df_r.append({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,random.randrange(1,255),random.randrange(1,255))}, ignore_index=True)
        
        pdk_graph(df_r)
        st.write("Arrival time:",(datetime.datetime.now()+datetime.timedelta(seconds=data[0].total_duration)).strftime("%H:%M"))
        st.write("Total Cost:", str(data[0].total_cost), "USD")
        st.write("Total Taxi Cost:", str(data[0].total_taxi_cost), "USD")


