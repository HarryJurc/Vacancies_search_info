from typing import Optional

def format_salary(salary: Optional[dict]) -> str:
    """Форматирует данные о зарплате."""
    if not salary:
        return "Зарплата не указана"
    from_salary, to_salary, currency = salary.get("from"), salary.get("to"), salary.get("currency", "RUR")
    gross = "до вычета налогов" if salary.get("gross", False) else "на руки"
    if from_salary and to_salary:
        return f"{from_salary} - {to_salary} {currency} ({gross})"
    if from_salary:
        return f"от {from_salary} {currency} ({gross})"
    if to_salary:
        return f"до {to_salary} {currency} ({gross})"
    return f"Не указана точная сумма, {currency} ({gross})"