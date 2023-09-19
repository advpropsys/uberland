import streamlit as st
import pandas as pd
import polyline  
import itertools
import random
import datetime
import collections


def flatten(x):
    if isinstance(x, collections.abc.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

            
def data_step(data,x, pdk_graph):
            steps = data[x].steps
            st.metric("CO2 emissions","co2",-round(data[x].co2,2))
            df_r=pd.DataFrame(columns=['name','path','color'])
            for idx, step in enumerate(steps):
                tmp=step.html_instructions.replace("\n","")
                if tmp=="" or tmp==None:
                    tmp="Take Uber"
                st.write(f'{idx}. {tmp}, \nEmissions: {round(step.emissions,2)}')
                if type(step.polyline) is list:
                    c=random.randrange(1,255)
                    c1=random.randrange(1,255)
                    merged = flatten([step.polyline])
                    for i in merged:
                        if type(i) is list:
                            for j in i:
                                if type(j) is list:
                                    for z in j:
                                        polys = polyline.decode(str(z.points))
                                        df_r.loc[len(df_r)] = pd.Series({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,c1,c)} )
                                else:
                                    polys = polyline.decode(str(j.points))
                                    df_r.loc[len(df_r)] = pd.Series({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,c1,c)} )
                        else:
                            polys = polyline.decode(str(i.points))
                            df_r.loc[len(df_r)] = pd.Series({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,c1,c)} )
                    
                else: 
                    polys = polyline.decode(str(step.polyline.points))
                    df_r.loc[len(df_r)] = pd.Series({'name':step.html_instructions,'path':list(map(lambda x: x[::-1],polys)),'color':(255,random.randrange(1,255),random.randrange(1,255))})
            
            pdk_graph(df_r)
            st.write("Arrival time:",(datetime.datetime.now()+datetime.timedelta(seconds=data[x].total_duration)).strftime("%H:%M, %d.%m"))
            st.write("Total Cost:", str(round(data[x].total_cost,2)), "USD")
            st.write("Total Taxi Cost:", str(round(data[x].total_taxi_cost, 2)), "USD")
            st.write("CO2 emissions:", str(round(data[x].co2, 2)))