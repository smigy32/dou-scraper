import subprocess

from flask import Flask, request, render_template, send_file

from app.selenium_job_finder.job_finder import find_jobs

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
            filename = find_jobs(
                category=category, additional_info=additional_info)
            return send_file(filename)
        else:
            command = f"scrapy crawl dou -a category={category} -a additional_info={additional_info}"
            subprocess.run(command, shell=True, cwd="app/scrapy_job_finder")

    debug = request.args.get("debug")
    return render_template("form.html", debug=debug)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
