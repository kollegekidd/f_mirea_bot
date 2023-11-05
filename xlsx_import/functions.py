import datetime


def is_even_week(start_date):
    current_date = datetime.datetime.today()
    start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()

    week_difference = (current_date - start_date).days // 7 + 1
    print(week_difference)
    week_even = week_difference % 2 == 0

    return week_even


def contains_alphabet_character(text):
    alphabet = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    return any(letter in alphabet for letter in text) if text is not None else False


def remove_redundant_spaces(substring):
    return " ".join(substring.split())
