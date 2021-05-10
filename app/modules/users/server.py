import grpc
from homi import Service

from app.grpc.src.items_pb2 import ItemsGetRequest
from app.grpc.src.items_pb2_grpc import ItemsStub
from app.grpc.src.users_pb2 import DESCRIPTOR as UsersDescriptor, UsersGetItemResponse, \
    UsersGetRequest, UsersGetResponse, UsersListRequest, UsersListResponse
from app.grpc.src.users_pb2_grpc import UsersServicer, UsersStub


class UsersServer(UsersServicer):
    def Get(self, request, context):
        if request.username == 'alice':
            return UsersGetResponse(
                username='alice1',
                email='alice@example.com',
                hashed_password='XXX',
            )

        return UsersGetResponse(username=request.username)

    def GetItem(self, request, context):
        port = request.port
        host = f'localhost:{port if port else "50051"}'

        with grpc.insecure_channel(host) as channel:
            stub = UsersStub(channel)

            request = UsersListRequest()
            response = stub.List(request)
            usernames = response.usernames

            request = UsersGetRequest(username=usernames[-1])
            response = stub.Get(request)
            result = UsersGetItemResponse(username=response.username, email=response.email)

            stub = ItemsStub(channel)

            item_id = 'gun'
            request = ItemsGetRequest(id=item_id)
            response = stub.Get(request)
            result.item_name = response.name

        return result

    def List(self, request, context):
        usernames = ['johndoe', 'alice']

        return UsersListResponse(usernames=usernames)


users_service = Service(UsersDescriptor.services_by_name['Users'])


@users_service.method()
def Get(username, **kwargs):
    if username == 'alice':
        return {
            'username': 'alice2',
            'email': 'alice@example.com',
            'hashed_password': 'XXX',
        }

    return {'username': username}


@users_service.method()
def GetItem(port, **kwargs):
    host = f'localhost:{port if port else "50051"}'

    with grpc.insecure_channel(host) as channel:
        stub = UsersStub(channel)

        request = UsersListRequest()
        response = stub.List(request)
        usernames = response.usernames

        request = UsersGetRequest(username=usernames[-1])
        response = stub.Get(request)
        result = {
            'username': response.username,
            'email': response.email,
        }

        stub = ItemsStub(channel)

        item_id = 'gun'
        request = ItemsGetRequest(id=item_id)
        response = stub.Get(request)
        result['item_name'] = response.name

    return result


@users_service.method()
def List(**kwargs):
    usernames = ['johndoe', 'alice']

    return {'usernames': usernames}
