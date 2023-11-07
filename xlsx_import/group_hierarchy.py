from attrs import define
from xlsx_import.functions import remove_redundant_spaces, lessons_timetable, days_dict


class VariableError(Exception):
    pass


@define
class Lesson:
    lesson_num: int
    time: str
    day: str
    week_type: bool
    classroom: str | None
    teacher_name: str | None
    lesson_type: str
    discipline: str

    @classmethod
    def from_list(cls, lesson_num: int, day_number: int, classroom: str | None, teacher_name: str | None,
                  lesson_type: str | None, discipline: str):

        even = True if lesson_num % 2 == 0 else False

        lesson_num = lesson_num // 2 + 1 if lesson_num % 2 != 0 else lesson_num // 2

        if lesson_type is not None:
            if "ЛБ" in lesson_type:
                lesson_type = "Лабораторная"
            if "П" in lesson_type:
                lesson_type = "Семинар"
            if "Л" in lesson_type:
                lesson_type = "Лекция"

        if lesson_type is None:
            lesson_type = "Военная кафедра"

        return Lesson(
            lesson_num,
            lessons_timetable[lesson_num],
            days_dict[day_number],
            even,
            remove_redundant_spaces(classroom) if classroom else None,
            remove_redundant_spaces(teacher_name) if teacher_name else None,
            remove_redundant_spaces(lesson_type),
            remove_redundant_spaces(discipline)
        )


@define
class Group:
    group_name: str
    schedule: list[Lesson]
