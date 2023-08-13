from config import db_name, username, password, host, port
from functions import get_hh_data

# Создание экземпляра класса DBManager
db_manager = DBManager(db_name, username, password, host, port)

# Подключение к базе данных
db_manager.connect()

# Создание таблиц в базе данных
db_manager.create_tables()

# Получение данных о работодателях и вакансиях с сайта hh.ru
employers_data, vacancies_data = get_hh_data()

# Заполнение таблиц данными о работодателях и вакансиях
db_manager.fill_tables(employers_data, vacancies_data)

# Выполнение запросов
# Получает список всех компаний и количество вакансий у каждой компании.
companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
print(companies_and_vacancies)

# Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
all_vacancies = db_manager.get_all_vacancies()
print(all_vacancies)

# Получает среднюю зарплату по вакансиям.
avg_salary = db_manager.get_avg_salary()
print(avg_salary)

# Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
print(higher_salary_vacancies)

# Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
keyword = "python"
vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
print(vacancies_with_keyword)

# Закрытие соединения с базой данных
db_manager.close_connection()
