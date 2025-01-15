from enum import Enum
from .base_scraper import JobScraper
from .scroll_scraper import ScrollScraper
from .pagination_scraper import PaginationScraper

class ScraperType(Enum):
    SCROLL = "scroll"
    PAGINATION = "pagination"

class ScraperFactory:
    @staticmethod
    def create_scraper(scraper_type: ScraperType, url: str, driver_path: str, **kwargs) -> JobScraper:
        if scraper_type == ScraperType.SCROLL:
            return ScrollScraper(url, driver_path)
        elif scraper_type == ScraperType.PAGINATION:
            return PaginationScraper(url, driver_path,
                                   kwargs.get('next_button_x'),
                                   kwargs.get('next_button_y'))
        raise ValueError(f"Type de scraper non supporté: {scraper_type}")