from homi import App, Server
from homi.extend.service import health_service

from app.modules.items.server import items_service
from app.modules.users.server import users_service


app = App(
    services=[
        items_service,
        users_service,
        health_service,
    ],
)


def serve():
    server = Server(app)
    server.run()


def init():
    if __name__ == '__main__':
        serve()


init()
