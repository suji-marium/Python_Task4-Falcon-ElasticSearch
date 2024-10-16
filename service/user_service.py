class UserService:
    def __init__(self, es_client):
        self.es_client = es_client
        self.index = 'users'
        self.create_index()

    def create_index(self):
        # Check if the index exists
        if not self.es_client.indices.exists(index=self.index):

            self.es_client.indices.create(index=self.index, body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "name": {"type": "text"},
                        "email": {"type": "keyword"},
                        "age": {"type": "integer"}
                    }
                }
            })
            print(f"Index '{self.index}' created.")