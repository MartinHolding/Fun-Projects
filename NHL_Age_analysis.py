#Standard imports
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import glob

#Load in the regular season data and add the season column so I can better track player age
bio_files = glob.glob('Bio_Info_*.csv')

df_list= []
endYear = 2015
for filename in bio_files:
  print(filename)
  data = pd.read_csv(filename)
  data['Season'] = endYear
  df_list.append(data)
  endYear += 1

bio_data = pd.concat(df_list)

#Get a summary of the data

print(bio_data.head())

## ----------Lets start by looking at the age of the players grouped by team and across seasons ----------- ## 

#First, since bio doesn't give us the players current age, we need to calculate it by hand

#Loop through dobs in biodata and convert to int for subtraction and back to str for extraction and back to int
#for storage. There must be a simpler way of doing this....
ages = []
seasons = ['2015_Season', '2016_Season', '2017_Season', '2018_Season', '2019_Season', '2020_Season']
ages_df = pd.DataFrame(columns= seasons)

todays_date = 20152509 # store as int so I can subtract this from player DOB

#Use df.at[row, col] to add each age to each column. 
#Will need to do a double loop to iterate over all players and also increment the year by adding 10000
row_idx = 0
col_idx = 0
for season in seasons:
    for birthday in bio_data.DOB:
        dob_int = int(birthday.replace("-", "")) #remove '-' character
        age_int = todays_date-dob_int
        age = int(str(age_int)[:2]) #Only interested in the age in years (the first 2 characters)
        ages.append(age)
        ages_df.at[row_idx, season] = age
        row_idx += 1 
        
    todays_date += 10000 #add extra year to date
    col_idx += 1
    row_idx = 0

#create a dataframe of playoff performances for each team and season
playoff_df = pd.read_csv('Playoff Positions 2015-2020.csv')

#turn playoff performance into categorical
category_map = {'DNQ': 0, 'First Round': 1, 'Second Round': 2, 'Conf. Finals': 3, 
                'Cup Final': 4, 'Champions': 5}
playoff_df_cat = playoff_df.copy()
playoff_df_cat = playoff_df_cat.astype('category')

playoff_df_cat.replace(category_map, inplace=True)
playoff_df_cat = playoff_df_cat.drop(labels = 'Division', axis = 1)
playoff_df_cat_transpose = playoff_df_cat.T


years =[2015, 2016, 2017, 2018, 2019, 2020]
ax1 = plt.subplot()
sns.set(style="darkgrid")
ax1 = sns.lineplot(data = playoff_df_cat_transpose)
#create a new data frame of the ages in each season
#bio_data["Age"] = ages


#Now I can make a violin chart of the ages of players across the teams
ax = plt.subplot()
ax = sns.violinplot(x=bio_data["Team"], y=bio_data["Age"])
plt.title('Age of players across all seasons')
plt.ylabel('Age (years)')
plt.xticks(rotation=90)
plt.xlabel('Team')
plt.show()

#Could do with more space its a bit crowded..lets try and subplot by division..

atl_div = ['BOS', 'TBL', 'TOR', 'FLA', 'MTL', 'BUF', 'OTT', 'DET']
met_div = ['WSH', 'PHI', 'PIT', 'CAR', 'CBJ', 'NYI', 'NYR', 'NJD']
cen_div = ['STL', 'COL', 'DAL', 'WIN', 'NSH', 'MIN', 'CHI' ]
pac_div = ['VGK', 'EDM', 'CGY', 'VAN', 'ARI', 'ANA', 'LAK', 'SJS']

atl_data = np.array([]) #initilize empty arrays
met_data = np.array([])
cen_data = np.array([])
pac_data = np.array([])
index_cnt = 0

for team in bio_data["Team"]:
    if(team in atl_div):
       atl_data = np.append(atl_data, team)
       atl_data = np.append(atl_data, int(bio_data["Age"][index_cnt]))
    elif(team in met_div):
       met_data = np.append(met_data, team)
       met_data = np.append(met_data, int(bio_data["Age"][index_cnt]))
    elif(team in cen_div):
       cen_data = np.append(cen_data, team)
       cen_data = np.append(cen_data, int(bio_data["Age"][index_cnt]))
    elif(team in pac_div):
       pac_data = np.append(pac_data, team)
       pac_data = np.append(pac_data, int(bio_data["Age"][index_cnt]))
    index_cnt += 1       

#reshape the array as it comes out as a 1D vector. Shape into Nx2 matrix 
atl_data_reshape = atl_data.reshape(int(len(atl_data)/2), 2)
met_data_reshape = met_data.reshape(int(len(met_data)/2), 2)
cen_data_reshape = cen_data.reshape(int(len(cen_data)/2), 2)
pac_data_reshape = pac_data.reshape(int(len(pac_data)/2), 2)

#convert to dataframes and cast age to int so I can plot. Comes up as a string right now for some reason
atl_df = pd.DataFrame(atl_data_reshape, columns=['Team', 'Age'])
met_df = pd.DataFrame(met_data_reshape, columns=['Team', 'Age'])
cen_df = pd.DataFrame(cen_data_reshape, columns=['Team', 'Age'])
pac_df = pd.DataFrame(pac_data_reshape, columns=['Team', 'Age'])

atl_df['Age'] = pd.to_numeric(atl_df['Age'], downcast='integer')
met_df['Age'] = pd.to_numeric(met_df['Age'], downcast='integer')
cen_df['Age'] = pd.to_numeric(cen_df['Age'], downcast='integer')
pac_df['Age'] = pd.to_numeric(pac_df['Age'], downcast='integer')

#Now I can plot them on subplots for each division
figure, axes = plt.subplots(nrows=2, ncols=2)

sns.violinplot(x=atl_df['Team'], y=atl_df['Age'], ax=axes[0,0])
axes[0,0].title.set_text('Atlantic Division')
plt.xlabel('Team')
plt.ylabel('Age (Years)')

sns.violinplot(x=met_df['Team'], y=met_df['Age'], ax=axes[0,1])
axes[0,1].title.set_text('Metropolitan Division')

sns.violinplot(x=cen_df['Team'], y=cen_df['Age'], ax=axes[1,0])
axes[1,0].title.set_text('Central Division')

sns.violinplot(x=pac_df['Team'], y=pac_df['Age'], ax=axes[1,1])
axes[1,1].title.set_text('Pacific Division')

plt.tight_layout(pad=2.0)
plt.show()

