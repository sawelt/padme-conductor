from fhirpy import SyncFHIRClient

from padme_conductor.Plugins.DatabasePlugin import DatabasePlugin


class FHIRClient(DatabasePlugin):
    def __init__(
        self,
        endpointURL,
        authorization=None,
        extra_headers=None,
        # request_config=None,
    ) -> None:
        self.endpointURL = endpointURL
        self.authorization = authorization
        self.extra_headers = extra_headers
        # self.request_config = request_config
        # self.client = self.connect()
        self.client = SyncFHIRClient(
            self.endpointURL,
            self.authorization,
            self.extra_headers,
            # self.request_config,
        )

    def connect(self):
        pass

    def _query(self, query):
        return query(self.client)
