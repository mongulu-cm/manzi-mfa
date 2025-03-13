from abc import ABC, abstractmethod
from typing import List
from models.job import Job

class JobScraper(ABC):
    @abstractmethod
    def scrape(self) -> List[Job]:
        """Méthode abstraite pour scraper les offres d'emploi"""
        pass