import os

import pytest

from src.storage import JSONVacancyStorage
from src.vacancy import Vacancy


@pytest.fixture
def storage():
    file_path = "test_vacancies.json"
    yield JSONVacancyStorage(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)


def test_save_and_load(storage):
    vacancy = Vacancy("Python Developer", "http://example.com", "100000", "Описание")
    storage.save([vacancy])
    loaded_vacancies = storage.load()
    assert len(loaded_vacancies) == 1
    assert loaded_vacancies[0].title == "Python Developer"


def test_delete(storage):
    vacancy1 = Vacancy("Vacancy 1", "http://example.com", "50000", "Описание 1")
    vacancy2 = Vacancy("Vacancy 2", "http://example.com", "60000", "Описание 2")
    storage.save([vacancy1, vacancy2])

    storage.delete("Vacancy 1")
    loaded_vacancies = storage.load()
    assert len(loaded_vacancies) == 1
    assert loaded_vacancies[0].title == "Vacancy 2"
