import requests
from DatabaseWorker import DatabaseWorker
import colorama
import asana
import json
from dataclasses import dataclass
from aiogram import Bot

TOKEN = "1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a"
ENDPOINT_URL = "https://app.asana.com/api/1.0/events"
HEADRES = headers = {
    'Authorization': 'Bearer 1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a'
}


@dataclass()
class Update:
    type: str
    text: str
    updated_by: str
    sorce: str


def getDefaultInfo() -> tuple:
    client = asana.Client.access_token(TOKEN)
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
    result = client.tasks.get_tasks({"project": project_gid}, opt_pretty=True)
    tasks_gids = []
    for task in result:
        tasks_gids.append(task["gid"])
        print(colorama.Fore.GREEN + "Fetched task:" + json.dumps(task, indent=3))
    return tasks_gids


def getNewEventsComments():
    updated: list[Update] = []
    task_gids = getDefaultInfo()
    # get sync tokens
    # if sync token not exist:
    # doing first request, check for error respponce status, get sync token, and create second request
    tasks_with_sync: dict[str, str] = {}
    databse = DatabaseWorker()
    for task_gid in task_gids:
        sync_token = databse.getToken(task_gid)
        # беремо токени синхронізації
        if sync_token is None:
            # token is new
            # токена синхронізації ще немає в бд
            tasks_with_sync[task_gid] = sync_token
        tasks_with_sync[task_gid] = sync_token
    # reqursts here
    for task_gid in tasks_with_sync.keys():
        sync = tasks_with_sync[task_gid]
        if sync is None:
            # токена синхронізації ще немає в бд
            # тоді ми робимо перший запит без нього, реквест матиме код 412,
            # в ньому буде токена синхронізації,
            # зберігаємо його в бд і робимо з ним наступні запити
            res_not_sync = requests.get(
                "{ENDPOINT_URL}/?resource={task_gid}".format(ENDPOINT_URL=ENDPOINT_URL, task_gid=task_gid),
                headers=HEADRES)
            if res_not_sync.status_code == 401:
                print(colorama.Back.RED + colorama.Fore.BLACK + "Trouble with token")
            if res_not_sync.status_code != 412:
                print(colorama.Back.RED + colorama.Fore.BLACK + "Now, we are fucked")
                print(colorama.Fore.RED + "Program must crash here")
            sync = res_not_sync.json()["sync"]
            databse.setToken(task_gid, sync)
        res = requests.get(
            "{ENDPOINT_URL}/?resource={task_gid}&sync={sync}".format(ENDPOINT_URL=ENDPOINT_URL, task_gid=task_gid,
                                                                     sync=sync), headers=HEADRES)
        if res.status_code == 401:
            print(colorama.Back.RED + colorama.Fore.BLACK + "Trouble with token")
        if res.status_code == 412:
            print(colorama.Back.RED + colorama.Fore.BLACK + "Now, we are fucked")
            print(colorama.Fore.RED + "Program must crash here")
        new_sync = res.json().get("sync", "")

        if res.status_code == 200:
            event = res.json()
            for update in event.get("data", []):
                resource = update.get("resource", {})
                source = ""
                if resource.get("type", "") == "comment" and resource.get("type", "") == "system":
                    try:
                        source = update.get("parent", {}).get("name", "")
                    except:
                        source = ""
                    updated.append(Update(type=resource["type"], text=resource["text"],
                                          updated_by=resource.get("created_by", {}).get("name", ""),
                                          sorce=source))
                elif update.get("change", None) and update.get("change", {}).get("new_value", {}).get("name",
                                                                                                      "") == "Status":
                    updated.append(Update(type="status",
                                          text=update.get("change", {}).get("new_value", {}).get("enum_value", {}).get(
                                              "name", ""),
                                          updated_by=update.get("change", {}).get("new_value", {}).get( "created_by", {}).get("name", ""),
                                          sorce=resource.get("name", "")))
        print("Update : " + res.text)
        databse.updateToken(task_gid, new_sync)
    return updated


if __name__ == '__main__':
    updated = getNewEventsComments()
    bot = Bot(token="1344620215:AAFEo5hC3D5Io-tua33KvfF5G28AtUJ0jhg")
    
