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

### Scrape Jobs

To get the coordinates of an element by clicking on it:
```bash
python main.py scrape --csv <CSV_FILE>
```
with sample csv file that follows structure:
```bash
https://www.example.com/jobs,SCROLL
https://www.example.com/jobs,PAGINATION,810,2089
```

Or specify the URL and scraper type directly:
```bash
export OPENAI_API_KEY=xxxxxxxx # On Windows use $env:OPENAI_API_KEY = "xxxxxxxx"
python main.py scrape --url <URL> --type scroll
python main.py scrape --url <URL> --type pagination --x <X_POS_NEXT_BUTTON> --y <Y_POS_NEXT_BUTTON>
```
