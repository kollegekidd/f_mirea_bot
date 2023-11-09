from xlsx_import.group_hierarchy import Lesson
from cattrs import unstructure
from pymongo import MongoClient


class Database:

    def __init__(self, link: str):
        self.link = link
        self.client = MongoClient(self.link)["mirea_schedule"]
        self.lessons = self._get_lessons_table()
        self.tg_users = self._get_users_table()

    def _get_lessons_table(self):
        return self.client["lesson"]

    def _get_users_table(self):
        return self.client["tg_user"]

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

    def fill_user(self, user_id: int, user_group: int, user_preference: int = 0):
        self.tg_users.insert_one({
            "user_id": user_id,
            "user_group": user_group,
            "user_preference": user_preference
        })

    def change_user_variable(self, user_id: int, variable_name: str, value):
        current_user = self.tg_users.find_one({"user_id": user_id})
        current_user.update_one({"$set": {variable_name: value}})

    def check_user_existence(self, user_id: int):
        return True if self.tg_users.count_documents({"user_id": user_id}) > 0 else False
