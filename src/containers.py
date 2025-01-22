import logging
from adapters.database.async_mongo import DatabaseClient

class Containers:
    def __init__(self):
        db_uri = "mongodb://localhost:27017/Cliente_Estudos"

        # Configuração do logger
        self.logger = logging.getLogger("Containers")
        logging.basicConfig(level=logging.INFO)

        try:
            self.database_client = DatabaseClient(self.logger, db_uri)
        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB client: {e}")
            raise e