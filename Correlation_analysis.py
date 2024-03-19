#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('Successful_projects_with_project_size.csv') 

df_success = df[df['status'] == 1]


def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


metrics = ['Number_of_Forks', 'merge_to_fork_ratio', 'Fork_Frequency', 'Merge_Frequency']
for metric in metrics:
    df_success = remove_outliers(df_success, metric)


scaler = StandardScaler()
df_success[metrics] = scaler.fit_transform(df_success[metrics])

for metric in metrics:
    sns.scatterplot(x=df_success[metric], y=df_success['Incubation_Period(days)'])
    plt.title(f'Relationship between Normalized {metric} and Incubation Time')
    plt.xlabel(f'Normalized {metric}')
    plt.ylabel('Incubation Time (days)')
    plt.show()


# In[90]:


import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('Successful_projects_with_project_size.csv')  


df_success = df[df['status'] == 1]

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


metrics = ['Number_of_Forks', 'merge_to_fork_ratio', 'Fork_Frequency', 'Merge_Frequency']
for metric in metrics:
    df_success = remove_outliers(df_success, metric)


scaler = StandardScaler()
df_success[metrics] = scaler.fit_transform(df_success[metrics]


spearman_corr, spearman_p = spearmanr(df_success['merge_to_fork_ratio'], df_success['Incubation_Period(days)'])
print("Spearman's correlation coefficient:", spearman_corr)
print("P-value:", spearman_p)

spearman_corr, spearman_p = spearmanr(df_success['Number_of_Forks'], df_success['Incubation_Period(days)'])
print("Spearman's correlation coefficient:", spearman_corr)
print("P-value:", spearman_p)

spearman_corr, spearman_p = spearmanr(df_success['Fork_Frequency'], df_success['Incubation_Period(days)'])
print("Spearman's correlation coefficient:", spearman_corr)
print("P-value:", spearman_p)

spearman_corr, spearman_p = spearmanr(df_success['Merge_Frequency'], df_success['Incubation_Period(days)'])
print("Spearman's correlation coefficient:", spearman_corr)
print("P-value:", spearman_p)


# In[88]:


# Group projects by size
sizes = df_success['project_size'].unique()

# Calculate correlations for each project size
for size in sizes:
    print("Project Size:", size)
    df_size = df_success[df_success['project_size'] == size]
    
    # Calculate Spearman's rank correlation coefficient
    try:
        spearman_corr, spearman_p = spearmanr(df_size['merge_to_fork_ratio'], df_size['Incubation_Period(days)'])
        print("Spearman's correlation coefficient for merge_to_fork_ratio:", spearman_corr)
        print("P-value:", spearman_p)
    except ValueError:
        print("Spearman's correlation coefficient for merge_to_fork_ratio: Constant input array")
    
    try:
        spearman_corr, spearman_p = spearmanr(df_size['Number_of_Forks'], df_size['Incubation_Period(days)'])
        print("Spearman's correlation coefficient for Number_of_Forks:", spearman_corr)
        print("P-value:", spearman_p)
    except ValueError:
        print("Spearman's correlation coefficient for Number_of_Forks: Constant input array")
    
    try:
        spearman_corr, spearman_p = spearmanr(df_size['Fork_Frequency'], df_size['Incubation_Period(days)'])
        print("Spearman's correlation coefficient for Fork_Frequency:", spearman_corr)
        print("P-value:", spearman_p)
    except ValueError:
        print("Spearman's correlation coefficient for Fork_Frequency: Constant input array")
    
    try:
        spearman_corr, spearman_p = spearmanr(df_size['Merge_Frequency'], df_size['Incubation_Period(days)'])
        print("Spearman's correlation coefficient for Merge_Frequency:", spearman_corr)
        print("P-value:", spearman_p)
    except ValueError:
        print("Spearman's correlation coefficient for Merge_Frequency: Constant input array")
    
    print("\n")

