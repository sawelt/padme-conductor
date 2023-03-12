from abc import ABC, abstractmethod


class DatabasePlugin(ABC):
    @abstractmethod
    def connect(self, username, password):
        pass

    @abstractmethod
    def _query(self, query):
        pass

    # def create_queries(self, queries):
    #     for query in queries:
    #         query.plugin = self

    #     return queries
