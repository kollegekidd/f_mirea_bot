import datetime

group_dict = {
                1: "ФКБО-01-20",
                2: "ФКБО-01-21",
                3: "ФКБО-01-22",
                4: "ФКБО-01-23",
                5: "ФВБО-01-20",
                6: "ФВБО-01-21",
                7: "ФВБО-01-22",
                8: "ФВБО-01-23",
                9: "ФЭБО-01-20",
                10: "ФЭБО-01-21",
                11: "ФЭБО-01-22",
                12: "ФЭБО-01-23",
                13: "ФКБВ-01-20",
                14: "ФКБВ-01-21",
                15: "ФКБВ-01-22",
                16: "ФКБВ-01-23",
                17: "ФРМО-01-22",
                18: "ФРМО-01-23",
                19: "ФКМО-01-22",
                20: "ФКМО-01-23"
              }

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


def is_even_week(start_date):
    current_date = datetime.datetime.today()
    start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()

    week_difference = (current_date - start_date).days // 7 + 1
    print(week_difference)
    week_even = week_difference % 2 == 0

    return week_even


def get_current_day():
    return datetime.datetime.now().weekday()


def contains_alphabet_character(text):
    alphabet = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    return any(letter in alphabet for letter in text) if text is not None else False


def remove_redundant_spaces(substring):
    return " ".join(substring.split())
