import csv
from typing import List, Optional
import asyncio
import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://jobs.dou.ua"

headers = {
    "Origin": BASE_URL,
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
}


async def get_csrf_token(client: httpx.AsyncClient) -> Optional[str]:
    """Gather CSRF token from cookies

    Args:
        client (httpx.Client): httpx client to make a request

    Returns:
        str: CSRF token
    """
    r = await client.get(BASE_URL)
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


async def fetch_all_jobs(category: str, additional_info: Optional[str] = None) -> List[dict]:
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

    async with httpx.AsyncClient(headers=headers) as client:
        csrf = await get_csrf_token(client)
        client.headers["X-CSRFToken"] = csrf

        while True:
            data = {"count": count}
            response = await client.post(xhr_url, data=data)
            html = response.json().get("html")

            soup = BeautifulSoup(html, "html.parser")
            vacancies = soup.find_all("li", class_="l-vacancy")

            if not vacancies:
                break

            for v in vacancies:
                title = v.find("a", class_="vt").text
                link = v.find("a", class_="vt")["href"]
                company = v.find("a", class_="company").text
                jobs.append({"title": title, "company": company, "link": link})

            count += 40
            await asyncio.sleep(0.5)  # пауза між запитами, не блокує цикл

    write_vacancies_to_csv("vacancies.csv", jobs)
    return jobs
