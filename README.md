# changeIssueContributor

## Introduction 
This Python script updates user information for Jira issues. Specifically, it updates the assignee, reporter, request participants, and watchers from old usernames to new ones. It uses the Jira REST API to search for issues with the old usernames and updates the issues with the new usernames.

## Getting Started
To use this script, you need to have Python installed on your system and install the jira module by running the following command in your terminal:
>pip install jira

## How to Use
1. Clone this repository to your local machine.
2. Open the terminal and navigate to the directory where you cloned the repository.
3. Run the following command to start the script:
>python changeIssueContributor.py
4. Follow the instructions in the terminal to input your Jira server URL, API key, old and new user accounts, and JQL request.
5. The script will then search for issues that meet the JQL request and update the assignee, reporter, request participant, and/or watcher fields with the new user account.