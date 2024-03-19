#!/usr/bin/env python
# coding: utf-8

# In[5]:


#sample code to get direct forks of a giithub repository


import requests
import json
from datetime import datetime

access_token = 'Github_access_token'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
main_project_owner = 'apache'
main_project_repo = 'mynewt'
end_of_incubation_date = datetime.strptime('2017-06-21', '%Y-%m-%d')

def get_all_direct_forks(username, repo, end_date):
    forks_list = []
    has_next_page = True
    cursor = None
    
    while has_next_page:
        graphql_query = """
        query ($owner: String!, $name: String!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            forks(first: 100, after: $cursor) {
              edges {
                node {
                  name
                  owner {
                    login
                  }
                  createdAt
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
        }
        """
        variables = {
            'owner': username,
            'name': repo,
            'cursor': cursor
        }
        
        response = requests.post('https://api.github.com/graphql', headers=headers, json={'query': graphql_query, 'variables': variables})
        data = response.json()
        
        fork_data = data['data']['repository']['forks']
        for edge in fork_data['edges']:
            createdAt = datetime.strptime(edge['node']['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
            if createdAt < end_date:
                forks_list.append({
                    'owner': edge['node']['owner']['login'],
                    'name': edge['node']['name'],
                    'createdAt': edge['node']['createdAt']
                })
        
        has_next_page = fork_data['pageInfo']['hasNextPage']
        cursor = fork_data['pageInfo']['endCursor']

    return forks_list

forks_list = get_all_direct_forks(main_project_owner, main_project_repo, end_of_incubation_date)
print(f"Total Direct Forks Created Before {end_of_incubation_date.strftime('%Y-%m-%d')}: {len(forks_list)}")



# In[14]:


import requests
import csv
from datetime import datetime

# Configuration
access_token = 'Github_access_token'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def get_fork_count(repo_url, end_date):
    # Extract owner and repo name from URL
    split_url = repo_url.rstrip('/').split('/')
    owner, repo = split_url[-2], split_url[-1]
    forks_list = []
    has_next_page = True
    cursor = None

    while has_next_page:
        graphql_query = """
        query ($owner: String!, $name: String!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            forks(first: 100, after: $cursor) {
              edges {
                node {
                  createdAt
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
        }
        """
        variables = {'owner': owner, 'name': repo, 'cursor': cursor}
        response = requests.post('https://api.github.com/graphql', json={'query': graphql_query, 'variables': variables}, headers=headers)
        data = response.json()

        if 'errors' in data:
            print(f"Error fetching data for {repo_url}: {data['errors']}")
            break

        forks_data = data['data']['repository']['forks']['edges']
        for fork in forks_data:
            created_at = datetime.strptime(fork['node']['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
            if created_at <= end_date:
                forks_list.append(fork['node'])

        has_next_page = data['data']['repository']['forks']['pageInfo']['hasNextPage']
        cursor = data['data']['repository']['forks']['pageInfo']['endCursor']

    return len(forks_list)
            
def process_csv(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Number of Direct Forks Before End of Incubation']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            repo_url = row['corrected_pj_github_url']
            end_date_str = row['end_date'] or datetime.now().strftime('%Y-%m-%d')
            try:
                # Try to parse the date assuming format '11/8/2008'
                end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
            except ValueError:
                # If the above fails, parse the date assuming format 'YYYY-MM-DD'
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            fork_count = get_fork_count(repo_url, end_date)
            row['Number of Direct Forks Before End of Incubation'] = fork_count
            writer.writerow(row)
            print(f"Processed {row['listid']}: {fork_count} forks added.")


# Paths to your input and output CSV files
input_csv_path = 'Dataset_main.csv'
output_csv_path = 'output5.csv'

process_csv(input_csv_path, output_csv_path)


# In[ ]:




