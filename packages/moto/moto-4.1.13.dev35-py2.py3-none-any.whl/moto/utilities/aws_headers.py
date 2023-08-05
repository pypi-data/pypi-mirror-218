from functools import wraps
from typing import Any, Callable, Dict, TypeVar, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Protocol
else:
    Protocol = object

import binascii
import re
from moto.moto_api._internal import mock_random as random


TypeDec = TypeVar("TypeDec", bound=Callable[..., Any])


class GenericFunction(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...


def gen_amz_crc32(response: Any, headerdict: Optional[Dict[str, Any]] = None) -> int:
    if not isinstance(response, bytes):
        response = response.encode("utf-8")

    crc = binascii.crc32(response)

    if headerdict is not None and isinstance(headerdict, dict):
        headerdict.update({"x-amz-crc32": str(crc)})

    return crc


def gen_amzn_requestid_long(headerdict: Optional[Dict[str, Any]] = None) -> str:
    req_id = random.get_random_string(length=52)

    if headerdict is not None and isinstance(headerdict, dict):
        headerdict.update({"x-amzn-requestid": req_id})

    return req_id


def amz_crc32(f: TypeDec) -> GenericFunction:
    @wraps(f)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:  # type: ignore[misc]
        response = f(*args, **kwargs)

        headers = {}
        status = 200

        if isinstance(response, str):
            body = response
        else:
            if len(response) == 2:
                body, new_headers = response
                status = new_headers.get("status", 200)
            else:
                status, new_headers, body = response
            headers.update(new_headers)
            # Cast status to string
            if "status" in headers:
                headers["status"] = str(headers["status"])

        gen_amz_crc32(body, headers)

        return status, headers, body

    return _wrapper


def amzn_request_id(f: TypeDec) -> GenericFunction:
    @wraps(f)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:  # type: ignore[misc]
        response = f(*args, **kwargs)

        headers = {}
        status = 200

        if isinstance(response, str):
            body = response
        else:
            if len(response) == 2:
                body, new_headers = response
                status = new_headers.get("status", 200)
            else:
                status, new_headers, body = response
            headers.update(new_headers)

        request_id = gen_amzn_requestid_long(headers)

        # Update request ID in XML
        try:
            body = re.sub(r"(?<=<RequestId>).*(?=<\/RequestId>)", request_id, body)
        except Exception:  # Will just ignore if it cant work
            pass

        return status, headers, body

    return _wrapper
