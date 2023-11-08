import sys
from argparse import ArgumentError, ArgumentParser, BooleanOptionalAction
from xlsx_import.excel_reader import get_groups_timetable
from xlsx_import.config import filesize
import os
from mirea_db.db import Database
import asyncio


class InputArgumentError(Exception):
    pass


def parse_args(argv):
    try:
        argparser = ArgumentParser(exit_on_error=False)
        argparser.add_argument('-f', '--filepath', type=str, default="",
                               help="Path to students schedule in xlsx format")
        argparser.add_argument('-l' '--link', type=str, required=True,
                               help="Link to a MongoDB Database")
        args = argparser.parse_args(argv[1:])
    except ArgumentError as e:
        raise InputArgumentError(f"\nНеверно указан параметр."
                                 f"\nНеправильный параметр: {e.argument_name} "
                                 f"\nОшибка, связанная с ним: {e}")
    return args


async def check_timetable(filepath: str, link: str, web_parse: bool = None):
    if not web_parse and filepath == "":
        raise InputArgumentError(f"Необходимо указать параметр пути или необходимости парсинга.")
    if web_parse is None:
        raise NotImplementedError()  # TODO: написать логику парсера
    current_filesize = os.path.getsize(filepath)
    if current_filesize != filesize:
        open("xlsx_import/config.py", "w").write(f"filesize = {current_filesize}\n")

        db.remove_all_lessons()````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

    if current_filesize == filepath:
        return None

    schedule_list = get_groups_timetable(filepath)
    db.update_group(schedule_list)

    return schedule_list


if __name__ == "__main__":
    p_args = parse_args(sys.argv)
    db = Database(link=p_args.link)
    groups = asyncio.run(check_timetable(p_args.filepath, p_args.link))

# import pymongo
#
# client = pymongo.MongoClient("localhost:27017")
# db = client["mirea_schedule"]
# lessons = db["lesson"]
# class_groups = db["class_group"]
#
# cursor = lessons.find()
# for record in cursor:
#     print(record)
#
# cursor = class_groups.find()
# for record in cursor:
#     print(record)
#
