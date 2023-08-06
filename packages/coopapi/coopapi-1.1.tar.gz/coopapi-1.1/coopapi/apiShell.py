import uvicorn
from fastapi import Body, Request, status
from coopapi import http_request_handlers as hrh
from typing import Any, Dict, List, Callable, Tuple, Optional
from fastapi import APIRouter
from pydantic.dataclasses import dataclass as pydataclass, Field
from dataclasses import dataclass, field
import json
from urllib.parse import parse_qs
import logging
from coopapi.enums import RequestType

logger = logging.getLogger('APIHandler')

def route(callback: hrh.requestCallback,
          schema: type = None):
    if schema is None:
        def internal(request: Request)-> schema:
            ret = hrh.request_handler(request=request,
                                      item=None,
                                      callback=callback
                                      )

            return ret
    else:
        def internal(request: Request, item: schema = Body(...)) -> schema:
            ret = hrh.request_handler(request=request,
                                           item=item,
                                           callback=callback
                                           )

            return ret
    return internal




# def post_route(create_callback: hrh.postRequestCallback,
#                schema: type):
#     def create(request: Request, item: schema = Body(...)) -> schema:
#         ret = hrh.post_request_handler(request=request,
#                                        item=item,
#                                        on_post_callback=create_callback
#                                        )
#
#         return ret
#     return create
#
# def put_route(update_callback: hrh.putRequestCallback,
#               schema: type):
#     def update(request: Request, id: str, update_values: Dict = Body(...)) -> schema:
#         return hrh.put_request_handler(request=request,
#                                        id=id,
#                                        obj_type=schema,
#                                        update_values=update_values,
#                                        on_put_callback=update_callback)
#     return update
#
# def delete_route(delete_callback: hrh.deleteRequestCallback,
#                  schema: type,
#                  redirect_url: str = None):
#     def delete(request: Request, id: str):
#         return hrh.delete_request_handler(id=id,
#                                           request=request,
#                                           obj_type=schema,
#                                           on_delete_callback=delete_callback,
#                                           redirect_url=redirect_url)
#     return delete
#
# def getone_route(find_callback: hrh.getOneRequestCallback,
#                  schema: type):
#     def find(request: Request, id: str) -> schema:
#         return hrh.getone_request_handler(id=id,
#                                           request=request,
#                                           obj_type=schema,
#                                           on_getone_callback=find_callback)
#     return find
#
# def getmany_route(list_callback: hrh.getManyRequestCallback,
#                   schema: type):
#     def list(request: Request, query: str = None, limit: int = 100) -> List[schema]:
#         if query is not None:
#             query = json.loads(query)
#         ret = hrh.getmany_request_handler(request,
#                                           on_getmany_callback=list_callback,
#                                           query=query,
#                                           limit=limit)
#         return ret
#     return list


# dirtyCleaner = Callable[[Dict], Dict]
#
# def dirty_post_route(create_callback: hrh.postRequestCallback,
#                      schema: type,
#                      cleaner: dirtyCleaner):
#     def dirty_post_route(request: Request, dirty_str: str = Body(...)) -> schema:
#         dirty_data = parse_qs(dirty_str)
#         clean_data = cleaner(dirty_data)
#         logger.info(f"Received Data: {dirty_str}\n"
#                     f"Cleaned Data: {clean_data}")
#
#         obj = schema(**clean_data)
#         ret = hrh.post_request_handler(request=request,
#                                        item=obj,
#                                        on_post_callback=create_callback
#                                        )
#
#         return ret
#     return dirty_post_route

# class Config:
#     arbitrary_types_allowed = True

@dataclass
class RequestCallbackPackage:
    method: RequestType
    callback: Callable
    response_schema: type
    input_body_schema: Optional[type]

@dataclass
class ApiShell:
    base_route: str
    on_post_callback: RequestCallbackPackage = field(default=None)
    on_put_callback: RequestCallbackPackage = field(default=None)
    on_delete_callback: RequestCallbackPackage = field(default=None)
    on_getone_callback: RequestCallbackPackage = field(default=None)
    on_getmany_callback: RequestCallbackPackage = field(default=None)
    # dirty_create: dirtyCleaner = field(default=None)
    router: APIRouter = field(default_factory=APIRouter)


    def __post_init__(self):
        self.register_routes()
        print(f"{self.base_route} routes registered")

    # def __post_init_post_parse__(self):
    #     self.register_routes()
    #     print(f"{self.base_route} routes registered")


    def _register_route_internal(self,
                                 callback_package: RequestCallbackPackage):
        self.router.add_api_route(
            f"{self.base_route}/api/",
            route(callback=callback_package.callback, schema=callback_package.input_body_schema),
            methods=[callback_package.method.value],
            response_description=f"{callback_package.method.value} a new {callback_package.response_schema.__name__}",
            response_model=callback_package.response_schema,
            status_code=ApiShell._success_status_code(callback_package.method))

    @staticmethod
    def _success_status_code(method: RequestType):
        switch = {
            RequestType.POST: status.HTTP_201_CREATED,
            RequestType.PUT: status.HTTP_202_ACCEPTED,
            RequestType.GET: status.HTTP_200_OK,
            RequestType.DELETE: status.HTTP_202_ACCEPTED,
        }
        return switch.get(method)

    def register_routes(self):
        if self.on_post_callback is not None:
            self._register_route_internal(self.on_post_callback)

        if self.on_put_callback is not None:
            self._register_route_internal(self.on_put_callback)

        if self.on_delete_callback is not None:
            self._register_route_internal(self.on_delete_callback)

        if self.on_getone_callback is not None:
            self._register_route_internal(self.on_getone_callback)

        if self.on_getmany_callback is not None:
            self._register_route_internal(self.on_getmany_callback)

        # '''
        # Basic CRUD api_routers routes
        # '''
        # # create route
        # if self.on_post_callback is not None:
        #     self.router.add_api_route(
        #         f"{self.base_route}/api/",
        #         route(callback=self.on_post_callback.callback, schema=self.on_post_callback.input_schema),
        #         methods=['POST'],
        #         response_description=f"POST a new {self.on_post_callback.input_schema.__name__}",
        #         response_model=self.on_post_callback.response_schema,
        #         status_code=status.HTTP_201_CREATED)
        #
        # # update route
        # if self.on_put_callback is not None:
        #     self.router.add_api_route(
        #         f"{self.base_route}/api/{{id}}",
        #         route(callback=self.on_put_callback.callback, schema=self.on_put_callback.input_schema),
        #         methods=['PUT'],
        #         response_description=f"PUT a {self.target_schema.__name__}",
        #         response_model=self.target_schema,
        #         status_code=status.HTTP_202_ACCEPTED
        #     )
        #
        # # delete route
        # if self.on_delete_callback is not None:
        #     self.router.add_api_route(
        #         f"{self.base_route}/api/{{id}}",
        #         delete_route(delete_callback=self.on_delete_callback, schema=self.target_schema),
        #         methods=['DELETE'],
        #         response_description=f"DELETE a {self.target_schema.__name__}",
        #         response_model=bool,
        #         status_code=status.HTTP_200_OK
        #     )
        #
        # # find route
        # if self.on_getone_callback is not None:
        #     self.router.add_api_route(
        #         f"{self.base_route}/api/{{id}}",
        #         getone_route(find_callback=self.on_getone_callback, schema=self.target_schema),
        #         methods=['GET'],
        #         response_description=f"GET a single {self.target_schema.__name__} by id",
        #         response_model=self.target_schema,
        #         status_code=status.HTTP_200_OK)
        #
        # # list route
        # if self.on_getmany_callback is not None:
        #     self.router.add_api_route(
        #         f"{self.base_route}/api/",
        #         getmany_route(list_callback=self.on_getmany_callback, schema=self.target_schema),
        #         methods=['GET'],
        #         response_description=f"GET all {self.target_schema.__name__}s",
        #         response_model=List[self.target_schema],
        #         status_code=status.HTTP_200_OK
        #     )
        #
        #
        # '''
        # routes specific to being accessed via HTML elements. Since all hrefs assume a requirement for 'GET' requests,
        # they must be structured differently. Rather than using the /api_routers/ routes, instead, include the operation
        # (eg, 'delete') in the url, and send it as a 'GET' route. These should include redirect_urls back to the base
        # route.
        # '''
        #
        # if self.on_delete_callback is not None:
        #     self.router.add_api_route(
        #         f"{self.base_route}/delete/{{id}}",
        #         delete_route(delete_callback=self.on_delete_callback, schema=self.target_schema, redirect_url=f"{self.base_route}"),
        #         methods=['GET'],
        #         response_description=f"Delete a {self.target_schema.__name__}",
        #         response_model=bool,
        #         status_code=status.HTTP_200_OK
        #     )

        # '''
        # Dirty route (used for taking in data in a format we know wont work directly, but can be manipulated to use
        # the endpoints
        # '''
        # if self.dirty_create is not None:
        #     if self.on_post_callback is None:
        #         raise NotImplementedError(f"Cannot supply a dirty create without an on_create_callback")
        #
        #     self.router.add_api_route(
        #         f"{self.base_route}/dirty/",
        #         dirty_post_route(create_callback=self.on_post_callback, schema=self.target_schema, cleaner=self.dirty_create),
        #         methods=['POST'],
        #         response_description=f"Create a {self.target_schema.__name__}",
        #         response_model=self.target_schema,
        #         status_code=status.HTTP_200_OK
        #     )




if __name__ == "__main__":
    from dataclasses import dataclass
    from fastapi import FastAPI
    import uvicorn

    @dataclass
    class DummyIn:
        a: str
        b: int
        d: Dict


    @dataclass
    class DummyOut:
        c: Tuple[str, int]
        e: Dict

    def callback(req: Request, i: DummyIn) -> DummyOut:
        return DummyOut(c=(i.a, i.b), e=i.d)

    cpac = RequestCallbackPackage(
        method=RequestType.POST,
        callback=callback,
        input_body_schema=DummyIn,
        response_schema=DummyOut
    )

    shell = ApiShell(base_route='/dummy',
                     on_post_callback=cpac)

    app = FastAPI()
    app.include_router(shell.router)

    uvicorn.run(app)