import abc


class CacheInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def set_item(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_item(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_item(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_items(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def empty(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_item(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def exists(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def ping(self, *args, **kwargs):
        raise NotImplementedError
