import csv
import time
import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


logger = logging.getLogger(__name__)


URL = "https://jobs.dou.ua/"


def get_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    driver = Chrome(options=options)
    return driver


def find_jobs(category: str, additional_info: str | None = None):
    driver = get_driver()
    driver.get(URL)
    all_category_links = driver.find_element(
        By.CLASS_NAME, "b-recent-searches")
    try:
        all_category_links.find_element(
            By.LINK_TEXT, category).click()
        if additional_info:
            driver.find_element(
                By.XPATH, "//input[@name='search']").send_keys(additional_info)
            driver.find_element(By.CLASS_NAME, "btn-search").click()

        show_more = driver.find_element(
            By.XPATH, "//div[@class='more-btn']/a")
        while show_more.is_displayed():
            time.sleep(1)
            show_more.click()
            time.sleep(1)

    except NoSuchElementException:
        pass

    vacancy_elements = driver.find_elements(By.CLASS_NAME, "l-vacancy")
    results = []

    # Проходимося по кожному елементу вакансії та отримуємо назву та компанію
    for vacancy_element in vacancy_elements:
        title_element = vacancy_element.find_element(By.CLASS_NAME, "vt")
        title = title_element.text
        link = title_element.get_attribute("href")
        company = vacancy_element.find_element(By.CLASS_NAME, "company").text
        results.append({
            "title": title,
            "company": company,
            "link": link,
        })

    fieldnames = ["title", "company", "link"]
    filename = "vacancies.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Записуємо заголовки стовпців
        writer.writerows(results)  # Записуємо рядки даних

    driver.quit()

    return filename
