from Models.Asana import AsanaWorker

asa = AsanaWorker("1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a")
task_gid= asa.create_task_with_name("Meow")["gid"]
asa.attach_file_to_task(open("TestAttachment.txt", "rb").read(), task_gid)
