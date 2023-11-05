from googlesearch import search

keyword = 'рту мирэа в г фрязино расписание семестра учебного года для всех форм обучения'


def get_page_link():
    results = search(keyword, num_results=1)
    for link in results:
        return link

print(get_page_link())
