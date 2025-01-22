import abc

class DatabaseClientInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_one(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_many(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def ping(self, *args, **kwargs):
        raise NotImplementedError
    
    class DatabaseClientException(Exception):
        pass