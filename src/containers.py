import logging
from src.adapters.cache.cache_inMemory import InMemoryCache
from src.adapters.database.async_mongo import DatabaseClient
from src.domain.repository.client import ClientRepository
from src.domain.services.client_service import ClientService

class Containers:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        self.cache = InMemoryCache()

        mongo_db_url = "mongodb://localhost:27017/"


        try:
            self.database_client = DatabaseClient("Client_accounts" , self.logger, mongo_db_url)
            self.client_repository = ClientRepository(self.database_client, self.logger)
            self.client_service = ClientService(self.cache, self.logger, self.client_repository)
        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB client: {e}")
            raise e
        
        
