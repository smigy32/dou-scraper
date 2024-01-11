from flask import Flask, request, render_template, send_file

from app.selenium_job_finder.job_finder import find_jobs

app = Flask(__name__, template_folder="app/templates")
app.static_folder = "app/static"


@app.route("/", methods=["GET", "POST"])
def get_jobs():
    if request.method == "POST":
        category = request.form.get("category")
        additional_info = request.form.get("additional_info")

        if not request.form or not category:
            return render_template(
                "error.html", message="Категорія обов'язкова для заповнення!",
                back_url="/"), 400

        filename = find_jobs(
            category=category, additional_info=additional_info)
        return send_file(filename)
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
