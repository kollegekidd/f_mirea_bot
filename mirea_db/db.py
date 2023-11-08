from xlsx_import.group_hierarchy import Lesson
from cattrs import unstructure
from pymongo import MongoClient


class Database:

    def __init__(self, link: str):
        self.link = link
        self.lessons = self._get_lessons_table()

    def __database_connect(self):
        client = MongoClient(self.link)

        return client["mirea_schedule"]

    def _get_lessons_table(self):
        client = self.__database_connect()
        return client["lesson"]

    def remove_all_lessons(self):
        self.lessons.delete_many({})

    def update_group(self, schedule: list[Lesson]):
        lesson_doc = [unstructure(x) for x in schedule]

        self.lessons.insert_many(lesson_doc)

    def find_lessons_by_group_and_day(self, group_name: str, week_type: bool | int, day: str):
        lesson_list = self.lessons.find({"group_name": group_name,
                                         "week_type": bool(week_type),
                                         "day": day})
        return [x for x in lesson_list]

    find_lessons_by_group_and_day("ФКБО-01-23", 0, "Понедельник")
