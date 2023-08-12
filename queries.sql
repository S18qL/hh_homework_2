SELECT employers.name, COUNT(vacancies.id) AS vacancy_count
FROM employers
         LEFT JOIN vacancies ON employers.id = vacancies.employer_id
GROUP BY employers.name


SELECT employers.name AS company_name, vacancies.name AS vacancy_name, vacancies.salary, vacancies.link
FROM vacancies
         JOIN employers ON employers.id = vacancies.employer_id


SELECT AVG(salary) AS avg_salary
FROM vacancies


SELECT employers.name AS company_name, vacancies.name AS vacancy_name, vacancies.salary, vacancies.link
FROM vacancies
         JOIN employers ON employers.id = vacancies.employer_id
WHERE vacancies.salary > avg_salary