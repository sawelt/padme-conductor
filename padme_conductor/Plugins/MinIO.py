from minio import Minio

from padme_conductor.Plugins.DatabasePlugin import DatabasePlugin

class MinioClient(DatabasePlugin):
    def __init__(
        self,
        endpoint,
        access_key=None,
        secret_key=None,
        session_token=None,
        secure=True,
        region=None,
        http_client=None,
        credentials=None,
    ) -> None:
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            session_token=session_token,
            secure=secure,
            region=region,
            http_client=http_client,
            credentials=credentials,
        )

    def connect(self):
        pass

    def _query(self, query):
        return query(self.client)
