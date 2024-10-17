import falcon

from elasticsearch import Elasticsearch
from rest.user_controller import UserGet, UserPost
from service.user_service import UserService
from waitress import serve

es_client = Elasticsearch(['http://localhost:9200/'])
user_service = UserService(es_client)

app = falcon.App()
app.add_route('/user-post', UserPost(user_service))
app.add_route('/user-get/{email}', UserGet(user_service))
app.add_route('/user-get', UserGet(user_service))

serve(app, host='127.0.0.1', port=8000)