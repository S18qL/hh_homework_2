# Получение данных о работодателях и вакансиях с сайта hh.ru

def get_hh_data():
    # URL для получения данных о работодателях
    url = "https://api.hh.ru/employers"
    # Заголовки для запроса
    headers = {"User-Agent": "Your User Agent"}

    # Интересующие компании с их идентификаторами
    interesting_companies = [
        "1740",
        "924205",
        "3443196",
        "1455",
        "247118",
        "5122356",
        "2624103",
        "5417029",
        "5179890",
        "974435"
    ]

    # Список данных о работодателях
    employers_data = []

    # Словарь данных о вакансиях по компаниям
    vacancies_data = {}

    for company in interesting_companies:
        # Получаем данные о работодателе
        employers_response = requests.get(f"{url}/{company}", headers=headers)
        employer_data = employers_response.json()
        # Добавляем данные о работодателе в список
        employers_data.append({
            "name": employer_data.get("name"),
            "description": employer_data.get("description")
        })

        # Получаем данные о вакансиях компании
        vacancies_response = requests.get(f"https://api.hh.ru/vacancies", headers=headers, params={"employer_id": int(company)})
        vacancies_data[employer_data.get("name")] = []
        vacancies = vacancies_response.json().get("items")
        for vacancy in vacancies:
            # Получаем информацию о зарплате
            salary = vacancy.get("salary")
            if salary is not None:
                salary = vacancy.get("salary").get("from") or vacancy.get("salary").get("to") or vacancy.get("salary")
            # Добавляем данные о вакансии в словарь
            vacancies_data[employer_data.get("name")].append({
                "name": vacancy.get("name"),
                "salary": salary,
                "link": vacancy.get("alternate_url")
            })

    return employers_data, vacancies_data

