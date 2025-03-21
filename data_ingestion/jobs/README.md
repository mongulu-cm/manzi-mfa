# Job Scraping Tool

This project is a CLI tool for scraping job positions from various websites. It supports both scrolling and pagination scraping methods.

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Get Positions

To get the coordinates of an element by clicking on it:
```bash
python main.py positions --url <URL>
```

### Store new company

To store a new company in the database
```bash
export DATABASE_URL=xxxxxxxx # On Windows use $env:DATABASE_URL = "xxxxxxxx"
python main.py store --url '<URL>' --nom '<NAME>' --contact '<CONTACT NAME>' --type '<TYPE SCRAPPER>' --metadata '{\"x_pos\": x_pos, \"y_pos\": y_pos, \"cookie_x\": cookie_x, \"cookie_y\": cookie_y}'
```

### Scrape Jobs

To scrape jobs using a CSV file:
```bash
python main.py scrape --csv <CSV_FILE>
```
with a sample CSV file that follows the structure:
```plaintext
company;url;type_scrapper;pos x;pos y;cookie x;cookie y
Ivalua;https://www.ivalua.com/company/careers/;scroll;;;495;648
```

Or specify the URL and scraper type directly:
```bash
export OPENAI_API_KEY=xxxxxxxx # On Windows use $env:OPENAI_API_KEY = "xxxxxxxx"
python main.py scrape --url <URL> --type scroll --comp <COMPANY> --cookiex <COOKIE_X> --cookiey <COOKIE_Y>
python main.py scrape --url <URL> --type pagination --comp <COMPANY> --x <X_POS_NEXT_BUTTON> --y <Y_POS_NEXT_BUTTON> --cookiex <COOKIE_X> --cookiey <COOKIE_Y>
```
