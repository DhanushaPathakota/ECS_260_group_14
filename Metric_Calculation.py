#!/usr/bin/env python
# coding: utf-8

# In[60]:


import requests
import pandas as pd

github_pat = 'Github_access_token'

# Load the initial CSV file into a DataFrame
df = pd.read_csv('Dataset_main.csv')

# Add a new column to store the count of contributors
df['contributors_count'] = 0

def extract_owner_repo(url):
    # Extract owner and repo name from GitHub URL
    parts = url.split('/')
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo

def get_contributor_count(owner, repo):
    # Fetch contributors list from GitHub API
    contributors_url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    headers = {'Authorization': f'token {github_pat}'}
    response = requests.get(contributors_url, headers=headers)
    
    # Initialize count
    count = 0
    
    if response.status_code == 200:
        contributors = response.json()
        count += len(contributors)
        
        # Check for pagination (more than one page of contributors)
        if 'next' in response.links.keys():
            while 'next' in response.links.keys():
                next_page = response.links['next']['url']
                response = requests.get(next_page, headers=headers)
                if response.status_code == 200:
                    contributors = response.json()
                    count += len(contributors)
    else:
        print(f"Failed to fetch contributors for {owner}/{repo}. Status code: {response.status_code}")
    
    return count

# Update DataFrame with the number of contributors
for index, row in df.iterrows():
    owner, repo = extract_owner_repo(row['corrected_pj_github_url'])
    contributors_count = get_contributor_count(owner, repo)
    df.at[index, 'contributors_count'] = contributors_count
    print(f"Contributors count for {row['pj_alias']} (Repo: {repo}): {contributors_count}")

# Save the updated DataFrame to a new CSV
df.to_csv('contributors_added.csv', index=False)
print("CSV file has been updated with contributors count.")


# In[63]:


import pandas as pd

# Load your dataset
df = pd.read_csv('contributors_added.csv')

# Calculate percentiles
small_cutoff = df['contributors_count'].quantile(0.33)
medium_cutoff = df['contributors_count'].quantile(0.66)

# Get the minimum and maximum values for each category
small_min = df['contributors_count'].min()
small_max = small_cutoff
medium_min = small_cutoff + 1
medium_max = medium_cutoff
large_min = medium_cutoff + 1
large_max = df['contributors_count'].max()

# Function to categorize project size
def categorize_size(count, small_cutoff, medium_cutoff):
    if count <= small_cutoff:
        print(f"Project size range: Small ({small_min}-{small_max})")
        return 'Small'
    elif count <= medium_cutoff:
        print(f"Project size range: Medium ({medium_min}-{medium_max})")
        return 'Medium'
    else:
        print(f"Project size range: Large ({large_min}-{large_max})")
        return 'Large'

# Apply the function to create a new column
df['project_size'] = df['contributors_count'].apply(lambda x: categorize_size(x, small_cutoff, medium_cutoff))

# Save the updated DataFrame
df.to_csv('project_sizes.csv', index=False)


# In[ ]:




