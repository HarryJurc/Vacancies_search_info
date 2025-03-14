import pytest

from src.job_api import HeadHunterAPI


@pytest.fixture
def api():
    return HeadHunterAPI()


def test_get_vacancies(api):
    vacancies = api.get_vacancies("Python", count=5)
    assert isinstance(vacancies, list)
    assert len(vacancies) <= 5
    for vacancy in vacancies:
        assert "name" in vacancy
        assert "alternate_url" in vacancy
