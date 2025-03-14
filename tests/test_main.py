from unittest.mock import patch

from main import user_interface
from src.vacancy import Vacancy


def test_find_vacancies():
    mock_vacancies = [
        {
            "name": "Python Developer",
            "alternate_url": "http://example.com/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR", "gross": False},
            "snippet": {"responsibility": "Python development"},
        },
        {
            "name": "QA Engineer",
            "alternate_url": "http://example.com/2",
            "salary": None,
            "snippet": {"responsibility": "Testing software"},
        },
    ]

    with patch("builtins.input", side_effect=["1", "Python", "4"]), patch(
        "src.job_api.HeadHunterAPI.get_vacancies", return_value=mock_vacancies
    ), patch("src.storage.JSONVacancyStorage.save") as mock_save, patch("builtins.print"):

        user_interface()

        expected_vacancies = [
            Vacancy(
                title="Python Developer",
                url="http://example.com/1",
                salary={"from": 100000, "to": 150000, "currency": "RUR", "gross": False},
                description="Python development",
            ),
            Vacancy(title="QA Engineer", url="http://example.com/2", salary=None, description="Testing software"),
        ]
        mock_save.assert_called_once_with(expected_vacancies)


def test_show_saved_vacancies():
    vacancy1 = Vacancy("Python Developer", "http://example.com", "100000", "Python development")
    vacancy2 = Vacancy("QA Engineer", "http://example.com/2", "Зарплата не указана", "Testing software")

    with patch("builtins.input", side_effect=["2", "4"]), patch(
        "src.storage.JSONVacancyStorage.load", return_value=[vacancy1, vacancy2]
    ), patch("builtins.print") as mock_print:

        user_interface()

        mock_print.assert_any_call(vacancy1)
        mock_print.assert_any_call(vacancy2)


def test_delete_vacancy():
    vacancy1 = Vacancy("Python Developer", "http://example.com", "100000", "Python development")
    vacancy2 = Vacancy("QA Engineer", "http://example.com/2", "Зарплата не указана", "Testing software")

    with patch("builtins.input", side_effect=["3", "Python Developer", "4"]), patch(
        "src.storage.JSONVacancyStorage.load", return_value=[vacancy1, vacancy2]
    ), patch("src.storage.JSONVacancyStorage.delete") as mock_delete, patch("builtins.print") as mock_print:

        user_interface()

        mock_delete.assert_called_with("Python Developer")
        mock_print.assert_any_call("Вакансия удалена.")


def test_exit_program():
    with patch("builtins.input", side_effect=["4"]), patch("builtins.print") as mock_print:

        user_interface()

        mock_print.assert_any_call("1. Найти вакансии\n2. Показать сохранённые\n3. Удалить вакансию\n4. Выйти")
