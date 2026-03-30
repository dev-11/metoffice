from services.scraper_service import ScraperService


class ServiceFactory:
    @staticmethod
    def get_scraper_service() -> ScraperService:
        return ScraperService()
