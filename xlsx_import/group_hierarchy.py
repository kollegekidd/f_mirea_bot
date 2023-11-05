from attrs import define
from functions import remove_redundant_spaces

lessons_timetable = {1: '09-00:10-30',
                     2: '10-40:12-10',
                     3: '12-30:14-00',
                     4: '14-10:15-40',
                     5: '15-45:17-15',
                     6: '17-20:18-50',
                     7: '19-00:20-30'}

days_dict = {1: "Понедельник",
             2: "Вторник",
             3: "Среда",
             4: "Четверг",
             5: "Пятница",
             6: "Суббота"}


@define
class Lesson:
    lesson_num: int
    time: str
    day: str
    week_type: bool
    classroom: str
    teacher_name: str
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

        else:
            lesson_type = "Военная кафедра"

        return Lesson(
            lesson_num,
            lessons_timetable[lesson_num],
            days_dict[day_number],
            even,
            remove_redundant_spaces(classroom) if classroom is not None else "",
            remove_redundant_spaces(teacher_name) if teacher_name is not None else "",
            remove_redundant_spaces(lesson_type),
            remove_redundant_spaces(discipline)
        )


@define
class Schedule:
    sessions: list[Lesson]


@define
class Group:
    group_name: str
    schedule: Schedule
