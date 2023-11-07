from xlsx_import.group_hierarchy import Lesson
from cattrs import unstructure
from pymongo import MongoClient

client = MongoClient("localhost:27017")

db = client["mirea_schedule"]

lessons = db["lesson"]
lesson_schema = {
    "lesson_num": int,
    "time": str,
    "day": str,
    "week_type": bool,
    "classroom": str,
    "teacher_name": str,
    "lesson_type": str,
    "discipline": str
}

class_groups = db["class_group"]
class_group_schema = {
    "group_name": str,
    "class_schedules": [str],  # stores the object_id strings of class_schedule
}


def remove_all_groups_and_lessons():
    cursor = lessons.find()
    for record in cursor:
        print(record)

    cursor = class_groups.find()
    for record in cursor:
        print(record)
    lessons.delete_many({})
    class_groups.delete_many({})
    print('hi')
    cursor = lessons.find()
    for record in cursor:
        print(record)

    cursor = class_groups.find()
    for record in cursor:
        print(record)


def update_group(group_name: str, schedule: list[Lesson]):
    lesson_doc = [unstructure(x) for x in schedule]

    lessons.insert_many(lesson_doc)

    class_group_doc = {
        "group_name": group_name,
        "class_schedules": [str(x['id'] for x in lesson_doc)]
    }

    class_groups.insert_one(class_group_doc)
