import asyncio

from flask import Flask, request, render_template, send_file

from app.selenium_job_finder.job_finder import find_jobs
from app.scrapy_job_finder.run_scraper import Scraper
from app.bs4_job_finder.job_finder_async import fetch_all_jobs


RESULT_FILE_NAME = "vacancies.csv"

app = Flask(__name__, template_folder="app/templates")
app.static_folder = "app/static"


@app.route("/", methods=["GET", "POST"])
def get_jobs():
    """
    Take job information from the form, get vacancies based on the data
    and returns .csv file that contains main info about the jobs
    """
    if request.method == "POST":
        category = request.form.get("category")
        additional_info = request.form.get("additional_info")

        if not request.form or not category:
            return render_template(
                "error.html", message="Категорія обов'язкова для заповнення!",
                back_url="/"), 400

        scrapping_technology = request.form.get("engine")
        if scrapping_technology in ("Selenium", None):
            find_jobs(category=category, additional_info=additional_info)
        elif scrapping_technology == "Scrapy":
            scraper = Scraper()
            scraper.run_spiders(category=category,
                                additional_info=additional_info)
        else:
            asyncio.run(fetch_all_jobs(category, additional_info))
        return send_file(RESULT_FILE_NAME)

    debug = request.args.get("debug")
    return render_template("form.html", debug=debug)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
