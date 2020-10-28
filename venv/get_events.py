import asana
import json
import requests


client = asana.Client.access_token("1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a")
# get workspace  gid
# get project gid

me: dict = client.users.me()
workspace_gid = me["workspaces"][0]["gid"]
me_gid = me["gid"]
projects = client.projects.get_projects({"workspace": workspace_gid})
project_gid = ""
for p in projects:
    project_gid = p["gid"]
    break
result = client.tasks.get_tasks({"project":project_gid}, opt_pretty=True)
tasks_gids = []
for task in result:
    tasks_gids.append(task["gid"])
    print(json.dumps(task, indent=3))
results = []
endpoint_url = "https://app.asana.com/api/1.0/events"
# need to get sync tokens from database
#
for task in tasks_gids:
    requests.get(url)
# get gid of all tasks in project
# get events of all tasks