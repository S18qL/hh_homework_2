import requests
import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host, port):
        """
       Инициализирует экземпляр класса DBManager.

       Аргументы:
       - dbname (str): имя базы данных
       - user (str): имя пользователя базы данных
       - password (str): пароль пользователя базы данных
       - host (str): хост базы данных
       - port (int): порт базы данных
       """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        """
        Устанавливает соединение с базой данных.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            print("Successfully connected to the database")
        except psycopg2.Error as e:
            print("Error while connecting to the database:", e)

    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.cur.close()
        self.conn.close()
        print("Connection to the database is closed")

    def create_tables(self):
        """
        Создает таблицы employers и vacancies в базе данных, если они не существуют.
        """
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    description TEXT
                )
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(id),
                    name TEXT,
                    salary INTEGER,
                    link TEXT
                )
            """)
            self.conn.commit()
            print("Tables created successfully")
        except psycopg2.Error as e:
            print("Error creating tables:", e)

    def fill_tables(self, employers_data, vacancies_data):
        """
        Заполняет таблицы employers и vacancies данными из переданных списков работодателей и вакансий.

        Аргументы:
        - employers_data (list): список работодателей с их именами и описаниями
        - vacancies_data (dict): словарь вакансий, где ключами являются имена работодателей, а значениями - списки вакансий
        """

        try:
            for employer_data in employers_data:
                self.cur.execute("""
                    INSERT INTO employers (name, description)
                    VALUES (%s, %s)
                    RETURNING id
                """, (employer_data["name"], employer_data["description"]))
                employer_id = self.cur.fetchone()[0]

                for vacancy_data in vacancies_data[employer_data["name"]]:
                    self.cur.execute("""
                        INSERT INTO vacancies (employer_id, name, salary, link)
                        VALUES (%s, %s, %s, %s)
                    """, (employer_id, vacancy_data["name"], vacancy_data["salary"], vacancy_data["link"]))

            self.conn.commit()
            print("Data inserted into tables successfully")
        except psycopg2.Error as e:
            print("Error inserting data into tables:", e)

    def get_companies_and_vacancies_count(self):
        """
        Возвращает список с именами работодателей и количеством вакансий, отсортированный по именам работодателей.

        Возвращает:
        - rows (list): список кортежей с именами работодателей и количеством вакансий
        """
        try:
            self.cur.execute("""
                SELECT employers.name, COUNT(vacancies.id) AS vacancy_count
                FROM employers
                LEFT JOIN vacancies ON employers.id = vacancies.employer_id
                GROUP BY employers.name
            """)
            rows = self.cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error executing get_companies_and_vacancies_count query:", e)
            return []

    def get_all_vacancies(self):
        """
         Возвращает список с информацией о всех вакансиях, включая название компании, название вакансии, зарплату и ссылку.

         Возвращает:
         - rows (list): список кортежей с информацией о вакансиях
         """
        try:
            self.cur.execute("""
                SELECT employers.name AS company_name, vacancies.name AS vacancy_name, vacancies.salary, vacancies.link
                FROM vacancies
                JOIN employers ON employers.id = vacancies.employer_id
            """)
            rows = self.cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error executing get_all_vacancies query:", e)
            return []

    def get_avg_salary(self):
        """
          Возвращает среднюю зарплату всех вакансий в базе данных.

          Возвращает:
          - avg_salary (float): средняя зарплата всех вакансий
          """
        try:
            self.cur.execute("""
                SELECT AVG(salary) AS avg_salary
                FROM vacancies
            """)
            row = self.cur.fetchone()
            return row[0]
        except psycopg2.Error as e:
            print("Error executing get_avg_salary query:", e)
            return None

    def get_vacancies_with_higher_salary(self):
        """
        Возвращает список вакансий с зарплатой выше средней.

        Возвращает:
        - rows (list): список кортежей с информацией о вакансиях с зарплатой выше средней
        """
        try:
            avg_salary = self.get_avg_salary()
            self.cur.execute("""
                SELECT employers.name AS company_name, vacancies.name AS vacancy_name, vacancies.salary, vacancies.link
                FROM vacancies
                JOIN employers ON employers.id = vacancies.employer_id
                WHERE vacancies.salary > %s
            """, (avg_salary,))
            rows = self.cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error executing get_vacancies_with_higher_salary query:", e)
            return []

    def get_vacancies_with_keyword(self, keyword):
        """
        Возвращает список вакансий, содержащих заданное ключевое слово в названии.
    
        Аргументы:
        - keyword (str): ключевое слово для поиска
    
        Возвращает:
        - rows (list): список кортежей с информацией о вакансиях, соответствующих заданному ключевому слову
        """
        try:
            self.cur.execute("""
                SELECT employers.name AS company_name, vacancies.name AS vacancy_name, vacancies.salary, vacancies.link
                FROM vacancies
                JOIN employers ON employers.id = vacancies.employer_id
                WHERE vacancies.name ILIKE %s
            """, ('%' + keyword + '%',))
            rows = self.cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error executing get_vacancies_with_keyword query:", e)
            return []
