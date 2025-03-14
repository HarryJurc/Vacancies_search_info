import json
import os
from abc import ABC, abstractmethod
from typing import List

from src.vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с файлами."""
    @abstractmethod
    def save(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет вакансии в файл."""
        pass

    @abstractmethod
    def load(self) -> List[Vacancy]:
        """Загружает вакансии из файла."""
        pass

    @abstractmethod
    def delete(self, vacancy_title: str) -> None:
        """Удаляет вакансию из файла."""
        pass


class JSONVacancyStorage(VacancyStorage):
    """Класс для работы с JSON-файлами."""
    def __init__(self, file_path: str = "data/vacancies.json"):
        """Инициализирует экземпляр с указанным файлом."""
        self._file_path = file_path
        directory = os.path.dirname(self._file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def save(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет список вакансий в JSON-файл."""
        existing_vacancies = self.load()
        new_vacancies = {v.title: v for v in existing_vacancies}
        for vacancy in vacancies:
            new_vacancies[vacancy.title] = vacancy
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {slot: getattr(vacancy, slot) for slot in Vacancy.__slots__}
                    for vacancy in new_vacancies.values()
                ],
                f,
                ensure_ascii=False,
                indent=4
            )

    def load(self) -> List[Vacancy]:
        """Загружает список вакансий из JSON-файла."""
        if not os.path.exists(self._file_path) or os.path.getsize(self._file_path) == 0:
            return []
        with open(self._file_path, "r", encoding="utf-8") as f:
            try:
                # Преобразуем ключи из приватных обратно в публичные
                return [
                    Vacancy(
                        title=data["_title"],
                        url=data["_url"],
                        salary=data["_salary"],
                        description=data["_description"]
                    ) for data in json.load(f)
                ]
            except json.JSONDecodeError:
                print("Ошибка чтения JSON файла. Он может быть поврежден или пуст.")
                return []

    def delete(self, vacancy_title: str) -> None:
        """Удаляет вакансию по названию."""
        vacancies = self.load()

        vacancies = [vacancy for vacancy in vacancies if vacancy.title != vacancy_title]


        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {slot: getattr(vacancy, slot) for slot in Vacancy.__slots__}
                    for vacancy in vacancies
                ],
                f,
                ensure_ascii=False,
                indent=4
            )

