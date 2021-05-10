from grpc import StatusCode
from homi import Service

from app.grpc.src.items_pb2 import DESCRIPTOR as ItemsDescriptor, ItemsGetResponse
from app.grpc.src.items_pb2_grpc import ItemsServicer


class ItemsServer(ItemsServicer):
    fake_items_db = {'plumbus': {'name': 'Plumbus'}, 'gun': {'name': 'Portal Gun'}}

    def Get(self, request, context):
        response = ItemsGetResponse()

        if request.id not in self.fake_items_db:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Item not found.')

            return response

        return ItemsGetResponse(
            id=request.id,
            name=self.fake_items_db[request.id]['name'],
        )


items_service = Service(ItemsDescriptor.services_by_name['Items'])


@items_service.method()
def Get(id, **kwargs):
    fake_items_db = {'plumbus': {'name': 'Plumbus'}, 'gun': {'name': 'Portal Gun'}}

    if id not in fake_items_db:
        context = kwargs['context']
        context.set_code(StatusCode.NOT_FOUND)
        context.set_details('Item not found.')

        return {}

    return {
        'id': id,
        'name': fake_items_db[id]['name'],
    }
