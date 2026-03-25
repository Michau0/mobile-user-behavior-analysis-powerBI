import pandas as pd
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv('../data/user_behavior_dataset.csv')

# Load the dataset
df = pd.read_csv('../data/user_behavior_dataset.csv')

# Cleaning the dataset
duplicates_count = df.duplicated().sum() #check for duplicates and drop them if found

if duplicates_count > 0:
    print(f"found {duplicates_count} duplicates. Removing...")
    df = df.drop_duplicates()
else:
    print("No duplicates found.")

nulls = df.isnull().sum() #check for null values and fill them if found

if nulls.sum() > 0:
    print("Filling null values with mean...")
    df = df.fillna(df.mean())
else:
    print("No null values found.")

na_values = df.isna().sum() #check for NA values and fill them if found

if na_values.sum() > 0:
    print("Filling NA values with mean...")
    df = df.fillna(df.mean())
else:
    print("No NA values found.")


print("Unique values in Operating System column: ", df['Operating System'].unique())
print("Unique values in Device Model column: ", df['Device Model'].unique())

df.to_csv('../data/mobile_usage_cleaned.csv', index=False)

df = pd.read_csv('../data/mobile_usage_cleaned.csv')

df['Brand'] = df['Device Model'].apply(lambda x: x.split()[0])


# screen time to minutes for better analysis
df['Data_Per_SOT_Minute'] = df['Data Usage (MB/day)'] / (df['Screen On Time (hours/day)'] * 60)

# adding a new feature: battery drain per hour of screen time
df['Battery_Per_SOT_Hour'] = df['Battery Drain (mAh/day)'] / df['Screen On Time (hours/day)']

# categorizing users into age groups
def age_group(age):
    if age < 25: return 'Gen Z'
    elif age < 40: return 'Millennials'
    elif age < 55: return 'Gen X'
    else: return 'Boomers'

df['Age_Group'] = df['Age'].apply(age_group)

# final dataset ready for analysis
df.to_csv('../data/mobile_data_ready.csv', index=False)