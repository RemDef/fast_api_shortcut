from urllib.parse import urlencode

from fastapi import Request


def page_url(request: Request, *, limit: int, offset: int) -> str:
    query_params = dict(request.query_params)
    query_params["limit"] = str(limit)
    query_params["offset"] = str(offset)
    return str(request.url.replace(query=urlencode(query_params)))
