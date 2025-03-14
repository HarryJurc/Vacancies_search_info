from typing import Optional


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("_title", "_url", "_salary", "_description")

    def __init__(self, title: str, url: str, salary: Optional[str], description: str) -> None:
        """Инициализирует объект вакансии с приватными атрибутами."""
        self._title = title
        self._url = url
        self._salary = self._validate_salary(salary)
        self._description = description

    @property
    def title(self) -> str:
        """Возвращает название вакансии."""
        return self._title

    @property
    def url(self) -> str:
        """Возвращает URL вакансии."""
        return self._url

    @property
    def salary(self) -> str:
        """Возвращает информацию о зарплате."""
        return self._salary

    @property
    def description(self) -> str:
        """Возвращает описание вакансии."""
        return self._description

    def __repr__(self) -> str:
        """Возвращает строковое представление вакансии."""
        return f"{self.title} ({self.salary}): {self.url}"

    def __lt__(self, other) -> bool:
        """Сравнивает вакансии по зарплате."""
        return (self.salary or 0) < (other.salary or 0)

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (
                self.title == other.title and
                self.url == other.url and
                self.salary == other.salary and
                self.description == other.description
        )

    @staticmethod
    def _validate_salary(salary: Optional[dict]) -> str:
        """Валидация и форматирование данных о зарплате."""
        if not salary:
            return "Зарплата не указана"
        if isinstance(salary, dict):
            from_salary = salary.get("from")
            to_salary = salary.get("to")
            currency = salary.get("currency", "RUR")
            gross = "до вычета налогов" if salary.get("gross", False) else "на руки"

            if from_salary and to_salary:
                return f"{from_salary} - {to_salary} {currency} ({gross})"
            elif from_salary:
                return f"от {from_salary} {currency} ({gross})"
            elif to_salary:
                return f"до {to_salary} {currency} ({gross})"
            else:
                return f"Не указана точная сумма, {currency} ({gross})"
        return str(salary)
