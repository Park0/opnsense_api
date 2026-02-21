from pydantic import Field
from opnsense_api.pydantic.pydantic_base import UIAwareMixin


class ApiUser(UIAwareMixin):
    username: str = Field(...)
    key: str = Field(...)
    id: str = Field(...)
