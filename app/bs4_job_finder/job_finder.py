import csv
from typing import List
import httpx
from bs4 import BeautifulSoup
import time

BASE_URL = "https://jobs.dou.ua"


headers = {
    "Origin": BASE_URL,
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
}


def get_csrf_token(client: httpx.Client) -> str | None:
    """Gather CSRF token from cookies

    Args:
        client (httpx.Client): httpx client to make a request

    Returns:
        str: CSRF token
    """
    r = client.get(BASE_URL)
    return client.cookies.get("csrftoken")


def write_vacancies_to_csv(filename: str, data: List[dict]):
    """Write jobs data into .csv

    Args:
        filename (str): Result file name
        data (List[dict]): Jobs to write
    """
    fieldnames = ["title", "company", "link"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def fetch_all_jobs(category: str, additional_info: str | None = None) -> List[dict]:
    """Gather jobs from dou.ua and write them into .csv file

    Args:
        category (str): Technology name
        additional_info (str | None, optional): Additional info about a job. Defaults to None.

    Returns:
        List[dict]: List of jobs with title, link and company name
    """
    xhr_url = f"{BASE_URL}/vacancies/xhr-load/?category={category}"
    if additional_info:
        xhr_url += f"&search={additional_info}"
    jobs = []
    count = 0

    with httpx.Client(headers=headers) as client:
        csrf = get_csrf_token(client)
        client.headers["X-CSRFToken"] = csrf

        while True:
            data = {
                "count": count,
            }
            response = client.post(xhr_url, data=data)
            soup = BeautifulSoup(response.json().get("html"), "html.parser")
            vacancies = soup.find_all("li", class_="l-vacancy")

            if not vacancies:
                break

            for v in vacancies:
                title = v.find("a", class_="vt").text
                link = v.find("a", class_="vt")["href"]
                company = v.find("a", class_="company").text
                jobs.append({"title": title, "company": company, "link": link})

            count += 40
            time.sleep(0.5)  # a little pause to prevent spam

    write_vacancies_to_csv("vacancies.csv", jobs)
    return jobs


fetch_all_jobs("Python")