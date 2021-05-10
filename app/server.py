from concurrent import futures

import grpc

from app.grpc.src.items_pb2_grpc import add_ItemsServicer_to_server
from app.grpc.src.users_pb2_grpc import add_UsersServicer_to_server
from app.modules.items.server import ItemsServer
from app.modules.users.server import UsersServer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    add_ItemsServicer_to_server(ItemsServer(), server)
    add_UsersServicer_to_server(UsersServer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def init():
    if __name__ == '__main__':
        serve()


init()
