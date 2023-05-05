from __future__ import annotations
from jira import JIRA
import csv


# searches issues with 'assignee = old'
# overwrites old assignee in issues with new 
def updateAssignee(old, new, jql='issue in watchedIssues() or not issue in watchedIssues()'):
   if isActiveUser(old) and isActiveUser(new):
      issues = jira.search_issues(f'assignee = {old} and ({jql})')
      for issue in issues:
         jira.assign_issue(issue, new)
   else:
      print(f"User {old} or {new} not found")


# searches issues with 'reporter = old'
# overwrites old reporter in issues with new
def updateReporter(old, new, jql='issue in watchedIssues() or not issue in watchedIssues()'):
   if isActiveUser(old) and isActiveUser(new):
      issues = jira.search_issues(f'reporter = {old} and ({jql})')
      for issue in issues:
         issue.update(reporter={'name': new}) 
   else:
      print(f"User {old} or {new} not found")


# searches issues with 'Request participants in (old)'
# adds new request participant to issues
# field id of request participants might alter in different instances of Jira/JSM
def updateRequestParticipant(old, new, jql='issue in watchedIssues() or not issue in watchedIssues()'):
   new_user = jira.user(new) # create jira.user object
   if isActiveUser(old) and isActiveUser(new):
      issues = jira.search_issues(f'"Request participants" in ({old}) and ({jql})')
      for issue in issues:
         rp_list = issue.fields.customfield_10601 # save all current request participants in list
         rp_list.append(new_user)
         new_rp = [{"name": str(user.name)} for user in rp_list] # create list with names of users
         issue.update(fields={"customfield_10601": new_rp}) # update request participant field
   else:
      print(f"User {old} or {new} not found")


# removes old account as watcher
# adds new account as watcher
def updateWatcher(old, new, jql='issue in watchedIssues() or not issue in watchedIssues()'):
   if isActiveUser(old) and isActiveUser(new):
      issues = jira.search_issues(f'watcher = {old} and ({jql})')
      for issue in issues:
         # jira.remove_watcher(issue, old)
         jira.add_watcher(issue, new)
   else:
      print(f"User {old} or {new} not found")


# überprüfen ob Nutzer vorhanden ist
def isActiveUser(user):
   return bool(jira.search_users(user))


# input: dictionary with key = old user and value = new user as Strings
# input: JQL request as string
# updates reporter and assignee from old to new user
# adds new user as rp if old user is rp
# adds new user as watcher if old user is watcher
def updateAllUsers(dict, jql=None):
   for k in dict:
      updateAssignee(old=k, new=newAccountOf[k], jql=jql)
      updateReporter(old=k, new=newAccountOf[k], jql=jql)
      updateRequestParticipant(old=k, new=newAccountOf[k], jql=jql)
      updateWatcher(old=k, new=newAccountOf[k], jql=jql)


###################################################

# input: server url as string
# input: API-Key as string
server = input("Please enter the URL of your Jira Instance (i.e. 'https://service.convales.de'): ")
url = f"{server}/rest/api/2/search"
API_KEY = input("Please enter your API-Key: ")

# connect to server with PAT
options = {'server': server}
jira = JIRA(options, token_auth=API_KEY)

# read csv file with old and new users (2 columns)
# csv file must use ';' as delimiter
file_path = input("Enter the path to the csv file: ")
newAccountOf = {}

with open(file_path, newline='') as csvfile:
   reader = csv.reader(csvfile, delimiter=';', quotechar='|')
   for row in reader:
      newAccountOf[row[0]] = row[1]

# JQL request
wantJQL = (True if input("Do you want to enter a JQL request? (y/n): ") == 'y' else False)
if wantJQL:
   jql = input("Enter JQL (i.e. 'key = ITMIS-32448'): ")
   updateAllUsers(newAccountOf, jql)
else:
   updateAllUsers(newAccountOf)