# ==============================================================================
#
# Client (HTTP-client)
#
# This file was generated by a code generator.
# Don't make changes to it manually.
#
# ==============================================================================

# jinja2: lstrip_blocks: "True"
# mypy: ignore-errors

from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime

from httpx import Timeout


try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import logging
from typing import IO
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import httpx
from pydantic import BaseModel
from pydantic import Field


# backward compatibility for httpx<0.18.2
try:
    DEFAULT_AUTH = httpx.USE_CLIENT_DEFAULT
except AttributeError:
    DEFAULT_AUTH = None


@dataclass
class RequestBox:
    client_name: str
    method: str
    url: str
    params: Dict[str, Any]
    headers: Dict[str, Any]
    content: Any


@dataclass
class ResponseBox:
    status_code: int


class BaseLogsIntegration(abc.ABC):
    @abc.abstractmethod
    def log_extra(self, **kwargs: Any) -> Dict[str, Any]:
        ...

    @abc.abstractmethod
    def log_error(self, req: RequestBox, resp: ResponseBox) -> None:
        ...

    @abc.abstractmethod
    def get_log_level(self, req: RequestBox, resp: ResponseBox) -> int:
        ...


class DefaultLogsIntegration(BaseLogsIntegration):
    def log_extra(self, **kwargs: Any) -> Dict[str, Any]:
        return {'props': {'data': kwargs}}

    def log_error(self, req: RequestBox, resp: ResponseBox) -> None:
        msg = f"request error"
        msg += f" | client={req.client_name}"
        msg += f" | method={req.method}"
        msg += f" | url={req.url}"
        msg += f" | params={req.params}"
        msg += f" | content={req.content}"
        msg += f" | headers={req.headers}"

        level = self.get_log_level(req, resp)

        logging.log(
            level,
            msg,
            extra=self.log_extra(
                client=req.client_name,
                method=req.method,
                content=req.content,
                url=req.url,
                params=req.params,
            ),
        )

    def get_log_level(self, req: RequestBox, resp: ResponseBox) -> int:
        if resp.status_code >= 500:
            return logging.ERROR
        elif resp.status_code >= 400:
            return logging.WARNING
        elif resp.status_code >= 300:
            return logging.INFO
        elif resp.status_code >= 200:
            return logging.INFO
        else:
            return logging.INFO


FileContent = Union[IO[str], IO[bytes], str, bytes]
FileTypes = Union[
    # file (or text)
    FileContent,
    # (filename, file (or text))
    Tuple[Optional[str], FileContent],
    # (filename, file (or text), content_type)
    Tuple[Optional[str], FileContent, Optional[str]],
]


class EmptyBody(BaseModel):
    status_code: int
    text: str


class LogsuserintothesystemResponse200(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    text: Optional[str] = None


class CreateslistofuserswithgiveninputarrayRequestBody(BaseModel):
    """
    None
    """

    # required ---

    # optional ---


class ReturnspetinventoriesbystatusResponse200(BaseModel):
    """
    None
    """

    # required ---

    # optional ---


class UploadsanimageRequestBody(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    content: Optional[bytes] = None


class FindsPetsbytagsResponse200(BaseModel):
    """
    None
    """

    # required ---

    # optional ---


class FindsPetsbystatusResponse200(BaseModel):
    """
    None
    """

    # required ---

    # optional ---


class AddanewpetortagtothestoreRequestBody(BaseModel):
    """
    None
    """

    __root__: Union[
        'Pet',
        'Tag',
    ]


class AddanewpetortagtothestoreResponse200(BaseModel):
    """
    None
    """

    __root__: Union[
        'Pet',
        'Tag',
    ]


class ApiResponse(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None


class Tag(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    id: Optional[int] = None
    name: Optional[str] = None


class Category(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    """
    None
    """

    # required ---
    name: str
    photoUrls: List[str]

    # optional ---
    id: Optional[int] = None
    category: Optional[Category] = None
    tags: Optional[List[Tag]] = None
    status: Optional[Literal['available', 'pending', 'sold']] = Field(description="pet status in the store")


class User(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    id: Optional[int] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    userStatus: Optional[int] = Field(description="User Status")


class Address(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None


class Customer(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    id: Optional[int] = None
    username: Optional[str] = None
    address: Optional[List[Address]] = None


class Order(BaseModel):
    """
    None
    """

    # required ---

    # optional ---
    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    shipDate: Optional[datetime] = None
    status: Optional[Literal['placed', 'approved', 'delivered']] = Field(description="Order Status")
    complete: Optional[bool] = None


class BasicAuth(BaseModel):
    username: str
    password: str


class Client:
    def __init__(
        self,
        base_url: str,
        timeout: int = 5,
        client_name: str = "",
        client: Optional[httpx.Client] = None,
        headers: Optional[Dict[str, str]] = None,
        logs_integration: Optional[BaseLogsIntegration] = DefaultLogsIntegration(),
    ):
        self.client = client or httpx.Client(timeout=Timeout(timeout))
        self.base_url = base_url
        self.headers = headers or {}
        self.logs_integration = logs_integration
        self.client_name = client_name

    def findPetsByStatus(
        self,
        status: Optional[Literal['available', 'pending', 'sold']] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[List[Pet], EmptyBody]:
        url = self._get_url(f'/pet/findByStatus')

        params = {}
        if status is not None:
            params['status'] = status

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return [Pet.parse_obj(item) for item in response.json()]

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def findPetsByTags(
        self,
        tags: Optional[List[str]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[List[Pet], EmptyBody]:
        url = self._get_url(f'/pet/findByTags')

        params = {}
        if tags is not None:
            params['tags'] = tags

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return [Pet.parse_obj(item) for item in response.json()]

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def getPetById(
        self,
        petId: int,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, Pet]:
        url = self._get_url(f'/pet/{petId}')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return Pet.parse_obj(response.json())

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 404:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def getInventory(
        self,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[ReturnspetinventoriesbystatusResponse200]:
        url = self._get_url(f'/store/inventory')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return ReturnspetinventoriesbystatusResponse200.parse_obj(response.json())

    def getOrderById(
        self,
        orderId: int,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, Order]:
        url = self._get_url(f'/store/order/{orderId}')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return Order.parse_obj(response.json())

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 404:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def loginUser(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, LogsuserintothesystemResponse200]:
        url = self._get_url(f'/user/login')

        params = {}
        if username is not None:
            params['username'] = username
        if password is not None:
            params['password'] = password

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return LogsuserintothesystemResponse200(text=response.text)

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def logoutUser(
        self,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> None:
        url = self._get_url(f'/user/logout')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

    def getUserByName(
        self,
        username: str,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, User]:
        url = self._get_url(f'/user/{username}')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("get", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="get",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return User.parse_obj(response.json())

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 404:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def addPet(
        self,
        body: Optional[Union[Pet, Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, Pet]:
        url = self._get_url(f'/pet')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, Pet):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "post", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return Pet.parse_obj(response.json())

        if response.status_code == 405:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def addPet(
        self,
        body: Optional[Union[AddanewpetortagtothestoreRequestBody, Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, AddanewpetortagtothestoreResponse200]:
        url = self._get_url(f'/pet_or_tag')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, AddanewpetortagtothestoreRequestBody):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "post", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return self._parse_any_of(response.json(), [Pet, Tag])

        if response.status_code == 405:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def updatePetWithForm(
        self,
        petId: int,
        name: Optional[str] = None,
        status: Optional[str] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[EmptyBody]:
        url = self._get_url(f'/pet/{petId}')

        params = {}
        if name is not None:
            params['name'] = name
        if status is not None:
            params['status'] = status

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("post", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 405:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def uploadFile(
        self,
        petId: int,
        body: Optional[Union[bytes, Dict[str, Any]]] = None,
        additional_metadata: Optional[str] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[ApiResponse]:
        url = self._get_url(f'/pet/{petId}/uploadImage')

        params = {}
        if additional_metadata is not None:
            params['additionalMetadata'] = additional_metadata

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, bytes):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "post", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return ApiResponse.parse_obj(response.json())

    def placeOrder(
        self,
        body: Optional[Union[Order, Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, Order]:
        url = self._get_url(f'/store/order')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, Order):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "post", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return Order.parse_obj(response.json())

        if response.status_code == 405:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def createUser(
        self,
        body: Optional[Union[User, Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> None:
        url = self._get_url(f'/user')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, User):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "post", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

    def createUsersWithListInput(
        self,
        body: Optional[Union[List[User], Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[User]:
        url = self._get_url(f'/user/createWithList')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, List[User]):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "post", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="post",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return User.parse_obj(response.json())

    def updatePet(
        self,
        body: Optional[Union[Pet, Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Union[EmptyBody, Pet]:
        url = self._get_url(f'/pet')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, Pet):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "put", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="put",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 200:
            return Pet.parse_obj(response.json())

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 404:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 405:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def updateUser(
        self,
        username: str,
        body: Optional[Union[User, Dict[str, Any]]] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> None:
        url = self._get_url(f'/user/{username}')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        if isinstance(body, dict):
            json = body
        elif isinstance(body, User):
            json = body.dict()
        else:
            json = None

        try:
            response = self.client.request(
                "put", url, json=json, headers=headers_, params=params, content=content, auth=auth_
            )
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="put",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

    def deletePet(
        self,
        petId: int,
        api_key: Optional[str] = None,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[EmptyBody]:
        url = self._get_url(f'/pet/{petId}')

        params = {}

        headers_ = self.headers.copy()
        if api_key is not None:
            headers_['api_key'] = api_key

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("delete", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="delete",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def deleteOrder(
        self,
        orderId: int,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[EmptyBody]:
        url = self._get_url(f'/store/order/{orderId}')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("delete", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="delete",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 404:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def deleteUser(
        self,
        username: str,
        auth: Optional[BasicAuth] = None,
        content: Optional[Union[str, bytes]] = None,
    ) -> Optional[EmptyBody]:
        url = self._get_url(f'/user/{username}')

        params = {}

        headers_ = self.headers.copy()

        if auth is None:
            auth_ = DEFAULT_AUTH
        elif isinstance(auth, httpx.Auth):
            auth_ = auth
        else:
            auth_ = (auth.username, auth.password)

        try:
            response = self.client.request("delete", url, headers=headers_, params=params, content=content, auth=auth_)
        except Exception as exc:
            raise exc

        req = RequestBox(
            client_name=self.client_name,
            method="delete",
            url=url,
            params=params,
            headers=headers_,
            content=content,
        )

        resp = ResponseBox(
            status_code=response.status_code,
        )

        if response.status_code == 400:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

        if response.status_code == 404:
            if response.content is None:
                content = None
            else:
                content = response.content[:500]

            if self.logs_integration:
                self.logs_integration.log_error(req, resp)

            return EmptyBody(status_code=response.status_code, text=response.text)

    def close(self) -> None:
        self.client.close()

    def _get_url(self, path: str) -> str:
        return f'{self.base_url}{path}'

    def log_extra(self, **kwargs: Any) -> Dict[str, Any]:
        return {'extra': {'props': {'data': kwargs}}}

    def log_error(self, client_name: str, method, url: str, params, content, headers) -> None:
        msg = f"request error"
        msg += f" | client={client_name}"
        msg += f" | method={method}"
        msg += f" | url={url}"
        msg += f" | params={params}"
        msg += f" | content={content}"
        msg += f" | headers={headers}"

        logging.error(
            msg,
            **self.log_extra(
                client=client_name,
                method=method,
                content=content,
                url=url,
                params=params,
            ),
        )

    def _parse_any_of(self, item: Dict[str, Any], schema_classes: List[Any]) -> Any:
        for schema_class in schema_classes:
            try:
                return schema_class.parse_obj(item)
            except:
                continue

        raise Exception("Can't parse \"{item}\"")


LogsuserintothesystemResponse200.update_forward_refs()
CreateslistofuserswithgiveninputarrayRequestBody.update_forward_refs()
ReturnspetinventoriesbystatusResponse200.update_forward_refs()
UploadsanimageRequestBody.update_forward_refs()
FindsPetsbytagsResponse200.update_forward_refs()
FindsPetsbystatusResponse200.update_forward_refs()
AddanewpetortagtothestoreRequestBody.update_forward_refs()
AddanewpetortagtothestoreResponse200.update_forward_refs()
ApiResponse.update_forward_refs()
Tag.update_forward_refs()
Category.update_forward_refs()
Pet.update_forward_refs()
User.update_forward_refs()
Address.update_forward_refs()
Customer.update_forward_refs()
Order.update_forward_refs()
