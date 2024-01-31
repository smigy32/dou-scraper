# DOU Scraper

DOU Scraper is a project that allows you to retrieve data from the [DOU](https://dou.ua/) website (a Ukrainian resource for software development professionals). This scraper enables you to gather information about job vacancies posted on DOU.

## Features

- Retrieval of data about job vacancies: title, link, company name.
- Downloading the obtained data as a .csv file.

## Requirements

To use DOU Scraper, you need to have the following components installed:

- Python 3.10
- Libraries specified in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Smigy32/dou-scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd dou-scraper
   ```

3. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use DOU Scraper, run `run.py`:

```bash
python run.py
```

After that, simply go to the link <http://127.0.0.1:5000/>

By default, the program uses **Selenium** as the scraping technology. If you want to use **Scrapy**, go to <http://127.0.0.1:5000/?debug=1> and select **Scrapy** from the dropdown.
