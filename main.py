from src.job_api import HeadHunterAPI
from src.storage import JSONVacancyStorage
from src.vacancy import Vacancy


def user_interface() -> None:
    """Функция для взаимодействия с пользователем."""
    api = HeadHunterAPI()
    storage = JSONVacancyStorage()

    while True:
        print("1. Найти вакансии\n2. Показать сохранённые\n3. Удалить вакансию\n4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            vacancies = api.get_vacancies(query)
            vacancy_objects = [
                Vacancy(v["name"], v["alternate_url"], v.get("salary"), v["snippet"].get("responsibility", ""))
                for v in vacancies
            ]
            storage.save(vacancy_objects)
            print("Вакансии сохранены.")
        elif choice == "2":
            vacancies = storage.load()
            for v in vacancies:
                print(v)
        elif choice == "3":
            title = input("Введите название вакансии для удаления: ")
            storage.delete(title)
            print("Вакансия удалена.")
        elif choice == "4":
            break
        else:
            print("Некорректный ввод.")


if __name__ == "__main__":
    user_interface()
