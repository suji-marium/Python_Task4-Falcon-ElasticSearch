import falcon
import re
from elasticsearch import Elasticsearch
from user_write import write_user_to_file
from models.user_model import User

class UserGet:
    def __init__(self, user_service):
        self.user_service = user_service

    def on_get(self, req, resp, email=None):
        if email:
            user = self.user_service.es_client.search(index=self.user_service.index, body={
                "query": {
                    "match": {
                        "email": email
                    }
                }
            })

            if user['hits']['total']['value'] > 0:
                resp.status = falcon.HTTP_200
                resp.media = user['hits']['hits'][0]['_source']
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'message': 'User not found'}
        else:
            users = self.user_service.es_client.search(index=self.user_service.index, body={
                "query": {
                    "match_all": {}
                }
            })
            resp.status = falcon.HTTP_200
            resp.media = [hit['_source'] for hit in users['hits']['hits']]


class UserPost:
    def __init__(self, user_service):
        self.user_service = user_service

    def on_post(self, req, resp):
        data = req.media

        # Validate required fields
        if not all([data.get('name'), data.get('email'), data.get('age')]):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'User name, age and email are required fields'}
            return

        # Validate name
        if not isinstance(data.get('name'), str):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid name'}
            return

        # Validate age
        if not isinstance(data.get('age'), int) or data.get('age') < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid age'}
            return

        # Check if email already exists
        email_count = self.user_service.es_client.count(index=self.user_service.index, body={
            "query": {
                "match": {
                    "email": data.get('email')
                }
            }
        })['count']

        if email_count > 0:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Email already exists'}
            return

        # Validate email format
        email = data.get('email')
        if not isinstance(email, str) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Invalid email address'}
            return

        # Filter allowed fields and prepare user data
        allowed_fields = ['name', 'email', 'age']
        filtered_data = {key: data[key] for key in allowed_fields if key in data}
        print(filtered_data)

        user = User.__new__(User)
        user.__dict__.update(filtered_data)


        self.user_service.es_client.index(index=self.user_service.index, body=user.__dict__)
        write_user_to_file(user.__dict__)
        resp.status = falcon.HTTP_201
        resp.media = {'message': 'User created successfully'}
