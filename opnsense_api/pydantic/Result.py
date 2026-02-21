from typing import Optional
from opnsense_api.pydantic.pydantic_base import UIAwareMixin


class Result(UIAwareMixin):
    result: str
    uuid: Optional[str] = None
