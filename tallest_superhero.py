import requests


def get_heroes(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_height_in_cm(height):
    split_height = height.split()

    value = float(split_height[0])
    unit = split_height[1]
    if unit == 'meters':
        value *= 100
        unit = 'cm'
    elif unit != 'cm':
        unit = None

    return value, unit


def get_filter_heroes(heroes: list, gender: str, has_work: bool):
    suitable_heroes = []

    for hero in heroes:
        appearance = hero.get("appearance", {})
        # Проверка пола
        if appearance.get("gender") != gender:
            continue

        work = hero.get("work", {})
        # Проверка наличия работы
        occupation = work.get("occupation", "")
        hero_has_work = bool(occupation and occupation.strip() and occupation != "-")
        if hero_has_work != has_work:
            continue

        height = appearance.get("height")[1]
        # Определение роста героя в сантиметрах
        value, unit = get_height_in_cm(height)
        if unit is None or value == 0:
            continue

        suitable_heroes.append((value, hero["name"]))

    return suitable_heroes


def get_tallest_hero(gender: str, has_work: bool):
    url = "https://akabab.github.io/superhero-api/api/all.json"
    heroes = get_heroes(url)

    suitable_heroes = get_filter_heroes(heroes, gender, has_work)

    if not suitable_heroes:
        return None
    
    sorted_heroes = sorted(suitable_heroes, key=lambda x: x[0], reverse=True)

    return sorted_heroes[0][1]

if __name__ == "__main__":
    print(get_tallest_hero("Male", True))  # Пример вызова функции для поиска самого высокого мужского героя с работой
    print(get_tallest_hero("Male", False))  # Пример вызова функции для поиска самого высокого мужского героя без работы
    print(get_tallest_hero("Female", True))  # Пример вызова функции для поиска самой высокой женской героини с работой
    print(get_tallest_hero("Female", False))  # Пример вызова функции для поиска самой высокой женской героини без работы
