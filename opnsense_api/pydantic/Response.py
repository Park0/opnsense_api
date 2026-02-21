from opnsense_api.pydantic.pydantic_base import UIAwareMixin


class Response(UIAwareMixin):
    response: str
