from src.vacancy import Vacancy

def test_vacancy_creation():
    vacancy = Vacancy(
        "Python Developer",
        "http://example.com",
        {"from": 50000, "to": 70000, "currency": "RUR", "gross": True},
        "Разработка и поддержка Python-приложений"
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary == "50000 - 70000 RUR (до вычета налогов)"
    assert vacancy.description == "Разработка и поддержка Python-приложений"

def test_vacancy_salary_parsing():
    vacancy_no_salary = Vacancy("Без зарплаты", "http://example.com", None, "Описание")
    assert vacancy_no_salary.salary == "Зарплата не указана"

    vacancy_from_salary = Vacancy(
        "От зарплаты", "http://example.com",
        {"from": 60000, "currency": "RUR", "gross": False},
        "Описание"
    )
    assert vacancy_from_salary.salary == "от 60000 RUR (на руки)"
