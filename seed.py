import json
import uuid
from calyvim.models import Board, Task, State, User, Priority, Label, Sprint
from django.utils.text import slugify
from django.utils.timezone import make_aware
from django.utils.timezone import datetime


data = json.load(open("formester.json"))

board = Board.objects.get(id="256f727f-102c-456b-a8a1-d51709176caf")

for item in data:
    state, created = State.objects.get_or_create(name=item["State"], board=board)
    created_by = User.objects.filter(display_name=item["Created By"]).first()

    if not created_by:
        try:
            created_by = User.objects.create(username=slugify(item["Created By"]), display_name=item["Created By"], email=f"{slugify(item['Created By'])}@acornglobus.com", first_name=item["Created By"])
        except Exception as e:
            print(item["Created By"])
            print("Failed &&&&", item["ID"], e)

    priority = None
    if item["Priority"] is not None:
        priority, created = Priority.objects.get_or_create(name=item["Priority"], board=board)

    assignee = None
    if item["Assignee"]:
        assignee_names = item["Assignee"].split(",")
        assignee = User.objects.filter(display_name=assignee_names[0]).first()

    sprint = None
    if item["Cycle Name"]:
        sprint = Sprint.objects.filter(name=item["Cycle Name"], board=board).first()
        if not sprint:
            start_date = make_aware(datetime.strptime(item["Cycle Start Date"], "%a, %d %b %Y"))
            end_date = make_aware(datetime.strptime(item["Cycle End Date"], "%a, %d %b %Y"))
            sprint = Sprint.objects.create(name=item["Cycle Name"], board=board, start_date=start_date, end_date=end_date)

    is_archived = False
    archived_at = None
    if item["Archived At"]:
        is_archived = True
        archived_at = datetime.strptime(item["Archived At"].strip(), "%a, %d %b %Y %H:%M:%S")

    created_at = datetime.strptime(item["Created At"], "%a, %d %b %Y %H:%M:%S %Z%z")

    completed_at = None
    if item["Completed At"]:
        completed_at = datetime.strptime(item["Created At"], "%a, %d %b %Y %H:%M:%S %Z%z")

    task_id = int(item["ID"].split("-")[-1])
    print('Calling for', task_id, "and ID", item["ID"])

    try:
        task = Task(board=board, summary=item["Name"],description=item["Description"],description_raw=item["Description"],state=state,priority=priority,created_by=created_by,assignee=assignee,sprint=sprint,created_at=created_at,archived_at=archived_at,is_archived=is_archived,completed_at=completed_at,number=task_id,name=item["ID"])
        task.save()
        label_names = item["Labels"].split(",")
        for label_name in label_names:
            label, created = Label.objects.get_or_create(name=label_name, board=board)
            task.labels.add(label)
        print("Task SUCCESS", task.name)
    except Exception as e:
        print("Failed *****", item["ID"], e)
