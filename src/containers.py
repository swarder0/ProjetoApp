import logging
from adapters.cache.cache_inMemory import InMemoryCache
from adapters.database.async_mongo import DatabaseClient
from domain.repository.client import ClientRepository
from domain.services.client_service import ClientService

class Containers:
    def __init__(self):
        self.logger = logging.getLogger("Containers")
        logging.basicConfig(level=logging.INFO)

        self.cache = InMemoryCache()

        db_uri = "mongodb://localhost:27017/Cliente_Estudos"

        try:
            self.database_client = DatabaseClient(self.logger, db_uri, "Client_accounts")
            self.client_repository = ClientRepository(self.database_client, self.logger)
            self.client_service = ClientService(self.cache, self.client_repository, self.logger)
        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB client: {e}")
            raise e
