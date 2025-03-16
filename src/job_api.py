import os
from abc import ABC, abstractmethod
from typing import List, Optional

import requests
from dotenv import load_dotenv


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, query: str, count: int) -> List[dict]:
        """Получает список вакансий."""
        pass

    @abstractmethod
    def _connect_to_api(self, params: dict) -> dict:
        """Подключается к API и возвращает ответ."""
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.url = os.getenv("BASE_URL")
        if not self.url:
            raise ValueError("Переменная окружения 'BASE_URL' не установлена.")

    def _connect_to_api(self, params: dict) -> Optional[dict]:
        """Подключается к API и возвращает ответ."""
        try:
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP ошибка: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
        return None

    def get_vacancies(self, query: str, count: int = 10) -> List[dict]:
        """Ищет вакансии по ключевому слову."""
        params = {"text": query, "per_page": count}
        data = self._connect_to_api(params)
        if isinstance(data, dict):
            return data.get("items", [])
        return []
