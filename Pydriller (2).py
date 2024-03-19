#!/usr/bin/env python
# coding: utf-8


pip install pydriller


from pydriller import Repository
from datetime import datetime

import csv
import sys


def extract_merge_commits(url):
    # Extract merge commits from the given repository URL(s).
    # Prints the repository path and hash of each merge commit.

    # Check if the input is a single URL or a list of URLs
    if isinstance(url, str):
        urls = [url]  # Make it a list if it's a single URL
    elif isinstance(url, list):
        urls = url
    else:
        print("Invalid URL input type. It should be a string or a list of strings.")
        sys.exit(1)
        
    for repo_url in urls:
        # Analyzing the repository
        for commit in Repository(path_to_repo=repo_url, only_no_merge=False).traverse_commits():
            # Filtering merge commits, which are identified by having more than one parent
            if len(commit.parents) > 1:
                print(f"Repository: {repo_url}, Merge Commit Hash: {commit.hash}")



def analyze_merge_commits(repo_path):
    # Analyzes and prints detailed information about merge commits in the given repository.

    for commit in Repository(path_to_repo=repo_path).traverse_commits():
        if commit.merge:  # Filter for merge commits
            print(f"Repository: {repo_path}")
            print(f"Commit Hash: {commit.hash}")
            print(f"Message: {commit.msg}")
            print(f"Author: {commit.author.name}, Email: {commit.author.email}")
            print(f"Committer: {commit.committer.name}, Email: {commit.committer.email}")
            print(f"Author Date: {commit.author_date}, Timezone: {commit.author_timezone}")
            print(f"Committer Date: {commit.committer_date}, Timezone: {commit.committer_timezone}")
            print(f"Branches: {commit.branches}")
            print(f"In Main Branch: {commit.in_main_branch}")
            print(f"Modified Files:")
            for modified_file in commit.modified_files:
                print(f"    - {modified_file.filename}, Change Type: {modified_file.change_type.name}")
                print(f"      Added Lines: {modified_file.added_lines}, Deleted Lines: {modified_file.deleted_lines}")
            print("-----------------------------------------------------")




# Example
urls = ["https://github.com/apache/daffodil"]

extract_merge_commits(urls)



# Example repository path
repo_path = "https://github.com/apache/daffodil"

analyze_merge_commits(repo_path)




def analyze_repositories_from_csv(csv_file_path):
    # Reads repository paths from a CSV file and analyzes merge commits for each repository.

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:  # Assuming there's only one row
            for repo_path in row:
                if repo_path:
                    print(f"Analyzing repository: {repo_path}")
                    analyze_merge_commits(repo_path)
                    print("=====================================================")
            break  # Stop after the first row



# Path to CSV file Example
csv_file_path = "pj_github_url.csv"  # path of the CSV file

analyze_repositories_from_csv(csv_file_path)



import re

def analyze_merge_commit_number(repo_path):
    # Extracts the URL or branch each merge from.
    # Counts merges per committer and total merges each project.
    
    committer_merge_count = {}
    total_merges = 0

    # Regular expression patterns
    url_pattern = re.compile(r'https://[\S]+')
    branch_pattern = re.compile(r"Merge branch '([^']+)' into [\S]+")
    remote_branch_pattern = re.compile(r"Merge remote-tracking branch '([^']+)' into [\S]+")
    pull_request_pattern = re.compile(r"Merge pull request #[\d]+ from ([^/]+/[^/\s]+)")

    for commit in Repository(path_to_repo=repo_path).traverse_commits():
        if commit.merge:
            total_merges += 1
            committer = commit.committer.email
            committer_merge_count[committer] = committer_merge_count.get(committer, 0) + 1

            # Attempt to extract information from commit message
            urls = url_pattern.findall(commit.msg)
            if urls:
                extracted_info = ', '.join(urls)
            else:
                branch_match = branch_pattern.search(commit.msg)
                remote_branch_match = remote_branch_pattern.search(commit.msg)
                pull_request_match = pull_request_pattern.search(commit.msg)
                
                if branch_match:
                    extracted_info = branch_match.group(1)
                elif remote_branch_match:
                    extracted_info = remote_branch_match.group(1)
                elif pull_request_match:
                    extracted_info = pull_request_match.group(1)  # Extracting user/repo from pull request
                else:
                    extracted_info = "No URL or specific branch information found"

            # Print detailed information
            print(f"Repository: {repo_path}")
            print(f"Commit Hash: {commit.hash}")
            print(f"Message: {commit.msg}")
            print(f"Extracted Info: {extracted_info}")
            print(f"Branches: {', '.join(commit.branches)}")
            print(f"Committer: {commit.committer.name}, Email: {committer}")
            print("-----------------------------------------------------")

    # Print summary
    print(f"Total merges in {repo_path}: {total_merges}")
    for committer, count in committer_merge_count.items():
        print(f"{committer} has made {count} merge(s)")




# Example
repo_path = "https://github.com/apache/daffodil"
analyze_merge_commit_number(repo_path)


def analyze_repositories_from_csv_1(csv_file_path):

    # Reads repository paths from a CSV file and analyzes merge commits for each repository.
    # Extracts the URL or branch each merge from.
    # Counts merges per committer and total merges each project.
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:  # Assuming there's only one row
            for repo_path in row:
                if repo_path:
                    print(f"Analyzing repository: {repo_path}")
                    analyze_merge_commit_number(repo_path)
                    print("=====================================================")
            break  # Stop after the first row



# Path to CSV file Example
csv_file_path = "pj_github_url.csv"  # Change to the actual path of your CSV file

analyze_repositories_from_csv_1(csv_file_path)


