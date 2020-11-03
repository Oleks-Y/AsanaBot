import asana
import json
from Models.Task import TaskToCreate


# from Task import TaskToCreate

class AsanaWorker:
    """ By default tasks create to one wokspace and project and assigned to owner of token"""

    def __init__(self, token: str, defaultProject: str):
        self.token = token
        self.client = asana.Client.access_token(token)
        self.configure_project_default(defaultProject)

    def configure_project_default(self, defaultProject: str):
        me: dict = self.client.users.me()
        self.workspace_gid = me["workspaces"][0]["gid"]
        self.me_gid = me["gid"]
        projects = self.client.projects.get_projects({"workspace": self.workspace_gid})
        for p in projects:
            # self.project_gid = p["gid"]
            if p["name"] == defaultProject:
                self.project_gid = p["gid"]

    def create_task_with_name(self, name):
        task_to_create = TaskToCreate(name=name,
                                      project_gid=self.project_gid,
                                      workspace_gid=self.workspace_gid,
                                      assignee_gid=self.me_gid)
        task_to_create.fillByDefault()

        return self.client.tasks.create_task(task_to_create.to_dict())

    def create_task_with_name_and_asignee(self, name, assignee_gid):
        task_to_create = TaskToCreate(name=name,
                                      project_gid=self.project_gid,
                                      workspace_gid=self.workspace_gid,
                                      assignee_gid=assignee_gid)
        task_to_create.fillByDefault()

        return self.client.tasks.create_task(task_to_create.to_dict())

    def attach_file_to_task(self, file, task_gid, filename):
        self.client.attachments.create_attachment_for_task(task_gid, file, file_name=filename)

    def getUserId(self, username: str):
        users = self.client.users.get_users({"workspace": self.workspace_gid})
        for user in users:
            if user["name"] == username:
                return user["gid"]


if __name__ == '__main__':
    asana = AsanaWorker("1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a")
    print(asana.getUserId("Alex"))
