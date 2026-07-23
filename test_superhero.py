from unittest.mock import patch

from tallest_superhero import get_height_in_cm, get_filter_heroes, get_tallest_hero


# Тесты get_height_in_cm

def test_height_cm():
    assert get_height_in_cm("180 cm") == (180.0, "cm")


def test_height_meters():
    assert get_height_in_cm("2 meters") == (200.0, "cm")


def test_height_unknown_unit():
    assert get_height_in_cm("180 kg") == (180.0, None)


# Тестовые данные

heroes = [
    {
        "name": "Hero1",
        "appearance": {
            "gender": "Male",
            "height": ["5 ft", "170 cm"]
        },
        "work": {
            "occupation": "Teacher"
        }
    },
    {
        "name": "Hero2",
        "appearance": {
            "gender": "Male",
            "height": ["7 ft", "200 cm"]
        },
        "work": {
            "occupation": "-"
        }
    },
    {
        "name": "Hero3",
        "appearance": {
            "gender": "Female",
            "height": ["6 ft", "190 cm"]
        },
        "work": {
            "occupation": "Doctor"
        }
    },
        {
        "name": "Hero4",
        "appearance": {
            "gender": "Male",
            "height": ["6 ft", "180 cm"]
        },
        "work": {
            "occupation": "Detective"
        }
    }
]

# Тесты get_filter_heroes

def test_filter_male_with_work():
    result = get_filter_heroes(heroes, "Male", True)
    assert result == [(170.0, "Hero1"), (180.0, "Hero4")]


def test_filter_male_without_work():
    result = get_filter_heroes(heroes, "Male", False)
    assert result == [(200.0, "Hero2")]


def test_filter_female_with_work():
    result = get_filter_heroes(heroes, "Female", True)
    assert result == [(190.0, "Hero3")]


def test_filter_no_result():
    result = get_filter_heroes(heroes, "Female", False)
    assert result == []


def test_ignore_zero_height():
    test_data = [
        {
            "name": "Hero",
            "appearance": {
                "gender": "Male",
                "height": ["-", "0 cm"]
            },
            "work": {
                "occupation": "Teacher"
            }
        }
    ]

    assert get_filter_heroes(test_data, "Male", True) == []


def test_ignore_unknown_unit():
    test_data = [
        {
            "name": "Hero",
            "appearance": {
                "gender": "Male",
                "height": ["-", "180 kg"]
            },
            "work": {
                "occupation": "Teacher"
            }
        }
    ]

    assert get_filter_heroes(test_data, "Male", True) == []


def test_empty_occupation():
    test_data = [
        {
            "name": "Hero",
            "appearance": {
                "gender": "Male",
                "height": ["-", "180 cm"],
            },
            "work": {
                "occupation": "",
            },
        }
    ]

    assert get_filter_heroes(test_data, "Male", False) == [(180.0, "Hero")]


def test_gender_dash():
    test_data = [
        {
            "name": "Unknown",
            "appearance": {
                "gender": "-",
                "height": ["-", "190 cm"],
            },
            "work": {
                "occupation": "Teacher",
            },
        }
    ]

    assert get_filter_heroes(test_data, "-", True) == [(190.0, "Unknown")]

# Тесты get_tallest_hero

@patch("tallest_superhero.get_heroes")
def test_tallest_male(mock_get):
    mock_get.return_value = heroes
    assert get_tallest_hero("Male", True) == "Hero4"


@patch("tallest_superhero.get_heroes")
def test_tallest_female(mock_get):
    mock_get.return_value = heroes
    assert get_tallest_hero("Female", True) == "Hero3"


@patch("tallest_superhero.get_heroes")
def test_no_hero(mock_get):
    mock_get.return_value = heroes
    assert get_tallest_hero("Female", False) is None


@patch("tallest_superhero.get_heroes")
def test_same_max_height(mock_get):
    mock_get.return_value = [
        {
            "name": "Batman",
            "appearance": {"gender": "Male", "height": ["-", "200 cm"]},
            "work": {"occupation": "Detective"},
        },
        {
            "name": "Superman",
            "appearance": {"gender": "Male", "height": ["-", "200 cm"]},
            "work": {"occupation": "Reporter"},
        },
    ]

    assert get_tallest_hero("Male", True) == "Batman"
