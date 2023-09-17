import streamlit as st
import folium
from streamlit_folium import st_folium
import pydeck as pdk
import polyline
from dotenv import load_dotenv

load_dotenv() 

st.set_page_config(layout="wide")

if "markers" not in st.session_state:
    st.session_state["markers"] = []
    
if "markers1" not in st.session_state:
    st.session_state["markers1"] = []


st.write("# UberLand perfect transit")
st.write("### :orange[ Team: taxi drivers]")

m = folium.Map(location=[-33.81619, 151.00325],tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWR2cHJvcDExIiwiYSI6ImNsbWx3ZW02ZjBoMjEyaXBna2MyOGx2eDkifQ.XGZz3RDWSKBebpjuqsMJMg", attr='none', zoom_start=16)
m1 = folium.Map(location=[-33.81619, 151.00325],tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWR2cHJvcDExIiwiYSI6ImNsbWx3ZW02ZjBoMjEyaXBna2MyOGx2eDkifQ.XGZz3RDWSKBebpjuqsMJMg", attr='none', zoom_start=16)

view_state = pdk.ViewState(
    latitude=-33.81619,
    longitude=151.00325,
    zoom=10
)
import pandas as pd

df=pd.DataFrame(columns=['name','path'])
df=df.append({'name':'name','path':list(map(lambda x: x[::-1],polyline.decode('jzvmEyr{y[pAFAr@Am@j@?fCRpCt@\\Dd@Cn@Mh@QjA}@p@w@v@{Al@m@t@i@x@c@z@]|@W\\I~AQn@CF@jAN`AFrG`AnATnB^|@T|Bt@b@Px@b@hAp@p@f@`DvEt@d@l@r@zBbDbB~Br@zALd@dAdBx@jArAvAxAnAvDlCf@b@~BpBzCnCnA|A~@hAz@rAvAjCx@dB~@|BpBrFz@bD^hBRtAh@lDt@`D~BjKv@dD|@lDlB|Hx@pD`BfHZpB^dDRrCDdEBzGAvAKxCEhB?dBK~BIp@]jBm@fCm@hB]x@sBzDoAjCe@nAo@jCs@rCw@rCg@bBk@bCa@dCStBGvA?pDHrC\\bG\\tDT~BJ`B@fBIjCYxCy@jEk@bCWvAMlAI~@QnCBfDPtBd@dE\\`EHfBC|DUrD_@zD_@tD_@vBiAxEmA~FoBfImA~EOx@iA~Eg@pBgAlDaA~CYhAa@|B_@bCWtBMrBGfDI~DSvKGjAMdBUlB]lCs@dDm@bCo@vCsA|EcAnD}@hD_AxD_A~E{@bEkA`FwAtFeAdD[z@oAvCoCbGeBxDkAfCuAxBw@tAyAfCoBnDiDxEoE`GwAzB}@|AgAhCg@|Ak@vBWnAeBdJo@xEW|Be@tE_@vD]~CQ`AWfA}@lC{AbDk@`Ai@r@gBnBmCjCqBdBk@l@{@|@{@nAsCbFmAbBoD~DgB|Bu@dAq@hAe@~@m@zAeBfF}@lBgAtBq@tAyAzDgBbFk@xBs@hD}@fEgBtIoAhG]jCYxDGlDDdDFrAj@fGZdGJrBFrB?rBMlE[zDoAtKc@`C[xCg@rESdDO|EE`CCxEJrLRbDNxA`@|CR`AXrBLdBDjA?rBStH@|GC|FIfMDnAAdBAhAKxBOxAUnBO`Aa@bBy@pCy@|Bg@fA_@n@oAjBm@x@w@|@yAtAkAz@{XdQiW`P_GrDkCdB{B~AcClBcB|AgFnFmEpEg@b@_@XwA|Ak@f@u@n@iA`AoBtBoG~GwDzDo@f@IF]\\}FbG{EnFuAlBiDnFoAhCkAxCgBhD_@v@e@r@Qh@aDbGqHhNmB`DwFvKqBpDcBdDq@|@INiAvAiAfAaBhAkAf@gCfAq@T_Cr@}DbAi@J[@m@FgBHyBDiDMeDYcE{@mCUsBCuADaBFkB`@oAd@a@Vo@`@gAr@oA`Aq@j@o@h@yAfBs@rARNaB\\ECOj@Id@Ib@Mp@UtACTAJKFa@PMFUH_C\\KDYPYJM@OAEXm@lE')))}, ignore_index=True)
df['color']=[(255,255,153)]*len(df)

layer = pdk.Layer(
    type='PathLayer',
    data=df,
    pickable=True,
    get_color='color',
    width_scale=40,
    width_min_pixels=2,
    get_path='path',
    get_width=5
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={'text': '{name}'})
st.pydeck_chart(r)

fg = folium.FeatureGroup(name="Markers")
fg1 = folium.FeatureGroup(name="Markers1")

for marker in st.session_state["markers"]:
    fg.add_child(marker)
for marker in st.session_state["markers1"]:
    fg1.add_child(marker)
    
    
left, right = st.columns(2)

with left:
    st.write('Pickup location')
    st_data = st_folium(m, width=720, feature_group_to_add=fg)
    
with right:
    st.write('Target location')
    st_data1 = st_folium(m1, width=720, feature_group_to_add=fg1, key='1')




#---------


pickup_loc=[]
targets=[]

if st_data["last_clicked"]:
    pickup_loc.append(st_data["last_clicked"]) # pickup location
    if len(pickup_loc)<1:
        st.session_state['markers'].append(folium.Marker(
        list(st_data["last_clicked"].values())
        ))

if st_data1["last_clicked"]:
    targets.append(st_data1["last_clicked"]) # target location
    st.session_state['markers1'].append(folium.Marker(
        list(st_data1["last_clicked"].values())
    ))



