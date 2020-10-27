import asana
import json
from Models.Task import TaskToCreate


class AsanaWorker:
    """ By default tasks create to one wokspace and project and assigned to owner of token"""

    def __init__(self, token: str):
        self.token = token
        self.client = asana.Client.access_token(token)
        self.configure_project_default()

    def configure_project_default(self):
        me: dict = self.client.users.me()
        self.workspace_gid = me["workspaces"][0]["gid"]
        self.me_gid = me["gid"]
        projects = self.client.projects.get_projects({"workspace": self.workspace_gid})
        for p in projects:
            self.project_gid = p["gid"]

    def create_task_with_name(self, name):
        task_to_create = TaskToCreate(name=name,
                                      project_gid=self.project_gid,
                                      workspace_gid=self.workspace_gid,
                                      assignee_gid=self.me_gid)
        task_to_create.fillByDefault()

        return self.client.tasks.create_task(task_to_create.to_dict())
    def attach_file_to_task(self, file, task_gid, filename):
        self.client.attachments.create_attachment_for_task(task_gid, file, file_name=filename)


# if __name__ == '__main__':
    # client = asana.Client.access_token("1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a")
    # me: dict = client.users.me()
    # workspace_gid = me["workspaces"][0]["gid"]
    # me_gid = me["gid"]
    # projects = client.projects.get_projects({"workspace": workspace_gid})
    # project_gid = ""
    # for p in projects:
    #     project_gid = p["gid"]
    # # get some tasks
    # # tasks = client.tasks.get_tasks({"workspace":workspace_gid, "assignee":me_gid}, opt_pretty=True)
    # # task_to_create = {
    # #     "approval_status": "pending",
    # #     "assignee": me_gid,
    # #     "assignee_status": "upcoming",
    # #     "completed": False,
    # #     "due_at": "2019-09-15T02:06:58.147Z",
    # #     "liked": True,
    # #     "name": "Some new tasks to вщ",
    # #     "notes": "Mittens really likes the stuff from Humboldt.",
    # #     "resource_subtype": "default_task",
    # #     "start_on": "2019-09-14",
    # #     "workspace": workspace_gid,
    # #     "projects": [
    # #         project_gid
    # #     ],
    # # }
    # task_to_create = TaskToCreate("New Task", workspace_gid=workspace_gid, project_gid=project_gid, assignee_gid=me_gid)
    # d = task_to_create.to_dict()
    #
    # client.tasks.create_task(d)
