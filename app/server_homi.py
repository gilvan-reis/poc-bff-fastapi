from homi import App, Server

from app.modules.items.server import items_service
from app.modules.users.server import users_service


app = App(
    services=[
        items_service,
        users_service,
    ],
)


def serve():
    server = Server(app)
    server.run()


def init():
    if __name__ == '__main__':
        serve()


init()
