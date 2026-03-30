from services.forecast_service import ForecastService
from services.scraper_service import ScraperService
from services.storage_service import StorageService

from repositories import S3Repository
import config as c


class ServiceFactory:
    @staticmethod
    def get_scraper_service() -> ScraperService:
        return ScraperService()

    @staticmethod
    def get_storage_service() -> StorageService:
        return StorageService(S3Repository(c.data_bucket))

    @staticmethod
    def get_forecast_service() -> ForecastService:
        return ForecastService()
