#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Get all the pull requests merged before the end of incubation time

import requests
from datetime import datetime

def get_merged_pull_requests(owner, repo, token):
    base_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {token}'}
    params = {'state': 'closed', 'per_page': 100, 'page': 1}  
    merged_pull_requests = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        pull_requests = response.json()

        if not pull_requests:
            break

        for pr in pull_requests:
            if pr.get('merged_at'):
                merged_pull_requests.append(pr)

        # Check for pagination
        if 'Link' in response.headers:
            links = response.headers['Link']
            if 'rel="next"' not in links:
                break
            params['page'] += 1
        else:
            break

    return merged_pull_requests

def main():
    owner = 'apache'
    repo = 'Airflow'
    token = 'Github-access-token'

    end_of_incubation_date = datetime.strptime('2018-12-19T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')

    merged_pull_requests = get_merged_pull_requests(owner, repo, token)

    print(f"Total Merged Pull Requests in {owner}/{repo}: {len(merged_pull_requests)}")


    unique_source_repos = set()

    print("PR URLs Merged Before the Given Date:")
    for pr in merged_pull_requests:
        merge_date = pr.get('merged_at', "Not Available")
        merged_at = datetime.strptime(merge_date, '%Y-%m-%dT%H:%M:%SZ')

    
        if merged_at <= end_of_incubation_date:
            print(pr['html_url'])

 
            if pr.get('head') and pr['head'].get('repo') and 'full_name' in pr['head']['repo']:
                source_repo = pr['head']['repo']['full_name']

          
                owner, repo_name = source_repo.split('/')

               
                if '/' not in repo_name:
                    unique_source_repos.add(owner)
            else:
               
                author_name = pr.get('user', {}).get('login', 'Author Not Available')
                unique_source_repos.add(author_name)

    print("\nPR URLs Associated with Unique Source Repositories:")
    for owner_name in unique_source_repos:
        print(f"Owner: {owner_name}")
        for pr in merged_pull_requests:
            merge_date = pr.get('merged_at', "Not Available")
            merged_at = datetime.strptime(merge_date, '%Y-%m-%dT%H:%M:%SZ')

            if pr.get('head') and pr['head'].get('repo') and 'full_name' in pr['head']['repo']:
                source_repo = pr['head']['repo']['full_name']
                owner, repo_name = source_repo.split('/')

                if owner == owner_name and merged_at <= end_of_incubation_date:
                    print(f"  {pr['html_url']}")
    print(len(unique_source_repos))
    print(unique_source_repos)

if __name__ == "__main__":
    main()


# In[1]:


#Get the count of merged forks of a repository

import requests
from datetime import datetime

def get_merged_pull_requests(owner, repo, token):
    base_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {token}'}
    params = {'state': 'closed', 'per_page': 100, 'page': 1}  # Initialize 'page' parameter
    merged_pull_requests = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        pull_requests = response.json()

        if not pull_requests:
            break

        for pr in pull_requests:
            if pr.get('merged_at'):
                merged_pull_requests.append(pr)

        # Check for pagination
        if 'Link' in response.headers:
            links = response.headers['Link']
            if 'rel="next"' not in links:
                break
            params['page'] += 1
        else:
            break

    return merged_pull_requests

def main():
    owner = 'apache'
    repo = 'commons-rdf'
    token = 'Github-access-token'

    end_of_incubation_date = datetime.strptime('2016-11-18T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')

    merged_pull_requests = get_merged_pull_requests(owner, repo, token)

    print(f"Total Merged Pull Requests in {owner}/{repo}: {len(merged_pull_requests)}")

    unique_source_repos = set()

    print("PR URLs Merged Before the Given Date:")
    for pr in merged_pull_requests:
        merge_date = pr.get('merged_at', "Not Available")
        merged_at = datetime.strptime(merge_date, '%Y-%m-%dT%H:%M:%SZ')

        if merged_at <= end_of_incubation_date:
            print(pr['html_url'])

          
            if pr.get('head') and pr['head'].get('repo') and 'full_name' in pr['head']['repo']:
                source_repo = pr['head']['repo']['full_name']

            
                owner, repo_name = source_repo.split('/')

         
                if '/' not in repo_name:
                    unique_source_repos.add(owner)
            else:
         
                author_name = pr.get('user', {}).get('login', 'Author Not Available')
                unique_source_repos.add(author_name)

    print("\nPR URLs Associated with Unique Source Repositories:")
    for owner_name in unique_source_repos:
        print(f"Owner: {owner_name}")
        for pr in merged_pull_requests:
            merge_date = pr.get('merged_at', "Not Available")
            merged_at = datetime.strptime(merge_date, '%Y-%m-%dT%H:%M:%SZ')

            if pr.get('head') and pr['head'].get('repo') and 'full_name' in pr['head']['repo']:
                source_repo = pr['head']['repo']['full_name']
                owner, repo_name = source_repo.split('/')

                if owner == owner_name and merged_at <= end_of_incubation_date:
                    print(f"  {pr['html_url']}")
    print(len(unique_source_repos))
    print(unique_source_repos)

if __name__ == "__main__":
    main()


# In[9]:


import requests
from datetime import datetime
import pandas as pd

def get_merged_pull_requests(owner, repo, token):
    base_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {token}'}
    params = {'state': 'closed', 'per_page': 100, 'page': 1}
    merged_pull_requests = []

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        pull_requests = response.json()

        if not pull_requests:
            break

        for pr in pull_requests:
            if pr.get('merged_at'):
                merged_pull_requests.append(pr)

        if 'Link' in response.headers:
            links = response.headers['Link']
            if 'rel="next"' not in links:
                break
            params['page'] += 1
        else:
            break

    return merged_pull_requests

def main():

    csv_file = 'Dataset_main.csv'
    df = pd.read_csv(csv_file)


    df['contributed_forks'] = None

    for index, row in df.iterrows():
        owner = 'apache'  
        repo = row['corrected_pj_github_url'].split('/')[-1]
        token = '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'  # Replace with your GitHub token

        end_of_incubation_date = datetime.strptime(row['end_date'], '%m/%d/%Y')

        try:
            merged_pull_requests = get_merged_pull_requests(owner, repo, token)
            print(f"Processing {owner}/{repo}...")

      
            unique_source_repos = set()

            for pr in merged_pull_requests:
                merge_date = pr.get('merged_at', "Not Available")
                merged_at = datetime.strptime(merge_date, '%Y-%m-%dT%H:%M:%SZ')

                if merged_at <= end_of_incubation_date:

                    if pr.get('head') and pr['head'].get('repo') and 'full_name' in pr['head']['repo']:
                        source_repo = pr['head']['repo']['full_name']

             
                        owner, repo_name = source_repo.split('/')

                        if '/' not in repo_name:
                            unique_source_repos.add(owner)
                    else:
               
                        author_name = pr.get('user', {}).get('login', 'Author Not Available')
                        unique_source_repos.add(author_name)

  
            df.at[index, 'contributed_forks'] = len(unique_source_repos)

            print(f"Number of Unique Source Repositories (Merged Before {end_of_incubation_date}): {len(unique_source_repos)}")
            
        except Exception as e:
            print(f"Error fetching pull requests for {owner}/{repo}. {e}")

    df.to_csv('output_cont.csv', index=False)

if __name__ == "__main__":
    main()

