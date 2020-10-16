#Standard imports
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

#Load in the regular season data 

bio_data = pd.read_csv('Bio Info All.csv') #player bio

#Get a summary of the data

print(bio_data.head())

## ----------Lets start by looking at the age of the players grouped by team and across seasons ----------- ## 

#First, since bio doesn't give us the players current age, we need to calculate it by hand
todays_date = 20202509 # store as int so I can subtract this from player DOB

#Loop through dobs in biodata and convert to int for subtraction and back to str for extraction and back to int
#for storage. There must be a simpler way of doing this....
ages = []
for birthday in bio_data.DOB:
    dob_int = int(birthday.replace("-", "")) #remove '-' character
    age_int = todays_date-dob_int
    age = int(str(age_int)[:2]) #Only interested in the age in years (the first 2 characters)
    ages.append(age)


#Add ages back into bio dataframe 
bio_data["Age"] = ages

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

