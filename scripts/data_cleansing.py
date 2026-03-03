import pandas as pd
import numpy as np

df = pd.read_csv("datasets/plants.csv", encoding = "latin1")

#drop duplicates of plant entry
df = df.drop_duplicates(subset=df.columns[0], keep='first')

#fix spelling mistake in watering column

df.loc[df["Watering"] == "Regular watering", "Watering"] = "Regular Watering"

#drop duplicates of the same values in every column (to avoid having plants with ident ical attributes)
df = df.drop_duplicates(subset=df.columns[1:], keep='first')

#save csv containing only unique values to separate file
#IMPORTANT - this file will be used as final file of accessable plants
#file used in - loading images, training knn classification, generating results to user
df.to_csv('datasets/plants_unique.csv', index=False)

#initialize new dataframe for numerical values: -1 for lowest/worst, 1 for highest/best
df_numerical = pd.DataFrame()

trait_dict ={
    #from fast learing to slow
    'growth':[
        "fast",
        "moderate",
        "slow"
    ],
    #from universal - extravert to indiviudal small friend group
    'soil':[
        "loamy",
        "moist",
        "well-drained",
        "sandy",
        "acidic"
    ],
    #from loves sun to hate it
    'sun':[
        'full sunlight',
        'partial sunlight',
        'indirect sunlight'
    ],
    #from loves water to doesnt
    'watering':[
        "Keep soil consistently moist",
        "Keep soil evenly moist",
        "Keep soil moist",
        "Keep soil slightly moist",
        "Regular, moist soil",
        "Regular Watering",
        "Regular, well-drained soil",
        "Water weekly",
        "Water when soil feels dry",
        "Water when topsoil is dry",
        "Water when soil is dry",
        "Let soil dry between watering"
    ],
    #from good diet to bad
    'fertilization':[
        "Balanced",
        "Organic",
        "No",
        "Low-nitrogen",
        "Acidic"
    ]
}

column_names = df.columns[1:]

mapping = dict(zip(column_names, trait_dict.keys()))

df_numerical['Plant Name'] = df['Plant Name']

#create column for each trait and assign appropariate values for each plant using map
for column_name, trait_list in zip(column_names, trait_dict.keys()):
    trait = trait_dict[trait_list]
    level = np.round(np.linspace(1,-1,len(trait)), 5) #numerical value assosiated with the trait
    num_map = dict(zip(trait, level))
    df_numerical[column_name] = df[column_name].map(num_map)


#save dataframe containing numerical values to another file - will be used for training knn
df_numerical.to_csv('datasets/numerical_plants.csv', index=False)