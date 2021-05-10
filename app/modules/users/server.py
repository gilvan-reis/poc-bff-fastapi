import grpc

from app.grpc.src.items_pb2 import ItemsGetRequest
from app.grpc.src.items_pb2_grpc import ItemsStub
from app.grpc.src.users_pb2 import UsersGetItemResponse, UsersGetRequest, UsersGetResponse, \
    UsersListRequest, UsersListResponse
from app.grpc.src.users_pb2_grpc import UsersServicer, UsersStub


class UsersServer(UsersServicer):
    def Get(self, request, context):
        if request.username == 'alice':
            return UsersGetResponse(
                username='alice',
                email='alice@example.com',
                hashed_password='XXX',
            )

        return UsersGetResponse(username=request.username)

    def GetItem(self, request, context):
        host = 'localhost:50051'

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
