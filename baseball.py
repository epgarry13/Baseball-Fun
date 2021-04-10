from baseball_scraper import statcast, playerid_lookup, statcast_pitcher, pitching_stats, statcast_batter
from datetime import date, timedelta
import pandas as pd
import json

#still need to set minimum number of at bats

#TODO find unlucky players
#TODO find hot streak players
#TODO find unlucky teams going against lucky pitchers

today = date.today()
data = statcast(str(today-timedelta(5)),str(today-timedelta(1)))
#batterData = statcast_batter(str(today-timedelta(5)), str(today-timedelta(1)))

la = data[data['launch_angle'].notna()]
la = la.groupby(['batter']).mean('launch_angle')['launch_angle'].to_frame(name = 'launch_angle').reset_index() # average launch angle by batter

ls = data[data['launch_speed'].notna()]
ls = ls.groupby(['batter']).mean('launch_speed')['launch_speed'].to_frame(name = 'launch_speed').reset_index() # average launch speed by batter

bv = data[data['babip_value'].notna()]
bv = bv.groupby(['batter']).mean('babip_value')['babip_value'].to_frame(name = 'babip_value').reset_index() # average babip_value by batter

df = la.merge(ls, how='left', on='batter')
df = df.merge(bv, how='left', on='batter')

df_temp = df.sort_values('launch_speed',ascending = False)

temptemp = df.head(40) #for testing

# Populate table based on top 20 average launch speeds over the last 4 days
arr=[]
new_arr = []
new_item = {}
min = 10000
for index, row in temptemp.iterrows():
    temp = statcast_batter(str(today-timedelta(5)), str(today-timedelta(1)), player_id=int(row['batter']))
    
    #update min
    if len(arr) < 20 : # only want top 20
        new_item = {}
        batterTable = statcast_batter(str(today-timedelta(5)), str(today-timedelta(1)), player_id=int(row['batter']))
        playerName = batterTable['player_name'].iloc[0]      
        tempdict = {}
        tempdict['launch_speed'] = row['launch_speed']
        tempdict['launch_angle'] = row['launch_angle']
        tempdict['babip_value'] = row['babip_value']
        new_item[playerName] = tempdict
        arr.append(new_item)

        #update min if necessary
        if min > row['launch_speed']:               
            min = row['launch_speed']
            nameMin = playerName

 
    elif row['launch_speed'] > min: # need to remove lowest launch speed to make room

        new_item = {}
        tempdict = {}
        batterTable = statcast_batter(str(today-timedelta(5)), str(today-timedelta(1)), player_id=int(row['batter']))
        playerName = batterTable['player_name'].iloc[0]      
        tempdict['launch_speed'] = row['launch_speed']
        tempdict['launch_angle'] = row['launch_angle']
        tempdict['babip_value'] = row['babip_value']
        new_item[playerName] = tempdict
        arr.append(new_item)

        new_arr = []
        for player in arr:
            if list(player.keys())[0] != nameMin:
                new_arr.append(player)

if new_arr == []:
    arr = json.dumps(arr)
    print(arr)
else:
    new_arr = json.dumps(new_arr)
    print(new_arr)







# dict = {'hello': {'hello2': 'hello', 'hello3': 'hello'}}
# print(list(dict.keys()))

# for col in data.columns:
#     print(col)