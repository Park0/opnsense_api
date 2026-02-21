from typing import Optional
from pydantic import Field
from opnsense_api.pydantic.pydantic_base import UIAwareMixin


class CertBase(UIAwareMixin):
    refid: Optional[str] = None
    descr: str = Field(...)
