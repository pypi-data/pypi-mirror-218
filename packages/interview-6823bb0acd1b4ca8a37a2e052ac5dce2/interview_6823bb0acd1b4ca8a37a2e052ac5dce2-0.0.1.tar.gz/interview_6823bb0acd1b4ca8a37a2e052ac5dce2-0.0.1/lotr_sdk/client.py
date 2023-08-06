from dataclasses import dataclass
from typing import TypeVar, Iterable, Iterator, Optional

from requests import Session

from .utils import join_urls


@dataclass
class PaginatorParams:
    sort: Optional[str]
    page_size: int


class BaseClient:
    def __init__(
        self,
        api_key,
        *,
        root="https://the-one-api.dev/v2",
    ):
        self.root = root
        self.session = Session()

        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
            }
        )

    def _get(self, path, params=None):
        url = join_urls(self.root, path)
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _collection(self, resource_type, path, params: PaginatorParams):
        return ResourceCollection[resource_type](
            resource_type,
            Paginator(
                client=self,
                path=path,
                params=params,
            ),
        )


class Paginator:
    def __init__(
        self,
        *,
        client: BaseClient,
        path: str,
        params: PaginatorParams,
    ):
        self.client = client
        self.path = path
        self.params = params
        self.page_num = 1
        self.current_response = self._get()

        def pages():
            yield self.current_response
            while True:
                if self.page_num >= self.current_response["pages"]:
                    break
                self.page_num += 1
                self.current_response = self._get()
                yield self.current_response

        self.pages = pages()

    def __iter__(self):
        for page in self.pages:
            yield from page["docs"]

    def _get(self):
        params = {
            "limit": self.params.page_size,
            "page": self.page_num,
        }
        if self.params.sort is not None:
            params["sort"] = self.params.sort
        return self.client._get(self.path, params=params)


T = TypeVar("T")


class ResourceCollection(Iterable[T]):
    def __init__(self, resource_type, paginator):
        self.paginator = paginator
        self._resource_type = resource_type

    def __iter__(self) -> Iterator[T]:
        for raw_data in self.paginator:
            yield self._resource_type(
                self.paginator.client,
                join_urls(self.paginator.path, raw_data["_id"]),
                raw_data,
            )

    def __len__(self):
        return self.paginator.current_response["total"]


class BaseResource:
    def __init__(self, client: BaseClient, path, raw_data=None):
        self._client = client
        self._path = path
        if raw_data is None:
            [raw_data] = self._client._get(self._path)["docs"]
        self.raw_data = raw_data

    @property
    def id(self) -> str:
        return self.raw_data["_id"]

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def _collection(self, resource_type, subpath, params: PaginatorParams):
        return self._client._collection(
            resource_type,
            join_urls(self._path, subpath),
            params,
        )
