import sys
from argparse import ArgumentError, ArgumentParser
from xlsx_import.excel_reader import get_groups_timetable
from xlsx_import.config import filesize
import os
from mirea_db.db import update_group, remove_all_groups_and_lessons
import asyncio


class InputArgumentError(Exception):
    pass


def parse_args(argv):
    try:
        argparser = ArgumentParser(exit_on_error=False)
        argparser.add_argument('-f', '--filepath', type=str)
        argparser.add_argument('-wp', '--web-parse', type=bool, default=False)
        args = argparser.parse_args(argv[1:])
    except ArgumentError as e:
        raise InputArgumentError(f"\nНеверно указан параметр."
                                 f"\nНеправильный параметр: {e.argument_name} "
                                 f"\nОшибка, связанная с ним: {e}")
    return args


async def check_timetable(filepath: str, web_parse: bool = False):
    if web_parse is False and filepath is None:
        raise InputArgumentError(f"Необходимо указать параметр -f пути или -wp необходимости парсинга с сайта.")
    if web_parse is True:
        pass  # TODO: написать логику парсера
    current_filesize = os.path.getsize(filepath)
    if current_filesize != filesize:
        open("xlsx_import/config.py", "w").write(f"filesize = {current_filesize}\n")

        remove_all_groups_and_lessons()

    if current_filesize == filepath:
        return None

    schedule = get_groups_timetable(filepath)
    for item in schedule:
        update_group(item.group_name, item.schedule)

    return schedule


if __name__ == "__main__":
    p_args = parse_args(sys.argv)
    groups = asyncio.run(check_timetable(p_args.filepath))

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
