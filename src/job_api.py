from abc import ABC, abstractmethod
from typing import List, Optional

import requests


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, query: str, count: int) -> List[dict]:
        """Получает список вакансий."""
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API hh.ru."""

    _BASE_URL = "https://api.hh.ru/vacancies"

    def __connect_to_api(self, params: dict) -> Optional[dict]:
        """Подключается к API и возвращает ответ."""
        try:
            response = requests.get(self._BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
            return None

    def get_vacancies(self, query: str, count: int = 10) -> List[dict]:
        """Ищет вакансии по ключевому слову."""
        params = {"text": query, "per_page": count}
        data = self.__connect_to_api(params)
        return data.get("items", []) if data else []
