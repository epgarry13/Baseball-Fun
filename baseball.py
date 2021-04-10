from baseball_scraper import statcast, playerid_lookup, statcast_pitcher, pitching_stats, statcast_batter
from datetime import date, timedelta
import pandas as pd
import json

#still need to set minimum number of at bats

#TODO find unlucky players -- get BA/ABs over same period as exit velo and launch_angle data
#TODO find hot streak players
#TODO find unlucky teams going against lucky pitchers

today = date.today()
data = statcast(str(today-timedelta(5)),str(today-timedelta(1)))

#CHECK OUTPUT
# print(data[data['batter'] == 405395.0]['launch_speed'])
# print(data[data['batter'] == 405395.0]['launch_angle'])
# print(data[data['batter'] == 405395.0]['babip_value'])




la = data[data['launch_angle'].notna()]
la = la.groupby(['batter']).mean('launch_angle')['launch_angle'].to_frame(name = 'launch_angle').reset_index() # average launch angle by batter

ls = data[data['launch_speed'].notna()]
ls = ls.groupby(['batter']).mean('launch_speed')['launch_speed'].to_frame(name = 'launch_speed').reset_index() # average launch speed by batter

lsa = data[data['launch_speed_angle'].notna()]
lsa = lsa.groupby(['batter']).mean('launch_speed_angle')['launch_speed_angle'].to_frame(name = 'launch_speed_angle').reset_index()  #launch speed angle

woba = data[data['estimated_woba_using_speedangle'].notna()]
woba = woba.groupby(['batter']).mean('estimated_woba_using_speedangle')['estimated_woba_using_speedangle'].to_frame(name = 'estimated_woba_using_speedangle').reset_index() # WOBA

df = la.merge(ls, how='left', on='batter')
df = df.merge(lsa, how='left', on='batter')
df = df.merge(woba, how='left', on='batter')

#sortedDF = df.sort_values('launch_speed',ascending = False)


# Populate json object based on top 20 average launch speeds over the last 4 days
arr=[]
new_arr = []
new_item = {}
for index, row in df.iterrows():
    new_item = {}
    batterTable = statcast_batter(str(today-timedelta(5)), str(today-timedelta(1)), player_id=int(row['batter']))
    playerName = batterTable['player_name'].iloc[0]      
    tempdict = {}
    tempdict['launch_speed'] = row['launch_speed']
    tempdict['launch_angle'] = row['launch_angle']
    tempdict['launch_speed_angle'] = row['launch_speed_angle']
    tempdict['estimated_woba_using_speedangle'] = row['estimated_woba_using_speedangle']
    new_item[playerName] = tempdict
    arr.append(new_item)


if new_arr == []:
    arr = json.dumps(arr, indent=2)
    print(arr)
else:
    new_arr = json.dumps(new_arr, indent=2)
    print(new_arr)




# for col in data.columns:
#     print(col)