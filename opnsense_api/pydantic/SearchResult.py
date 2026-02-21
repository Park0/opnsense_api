from typing import Generic, TypeVar, List, Dict, Any, Type

from opnsense_api.pydantic.Account import Account
from opnsense_api.pydantic.Action import Action
from opnsense_api.pydantic.Alias import Alias
from opnsense_api.pydantic.ApiUser import ApiUser
from opnsense_api.pydantic.BaseObject import BaseObject
from opnsense_api.pydantic.Ca import Ca
from opnsense_api.pydantic.Category import Category
from opnsense_api.pydantic.Cert import Cert
from opnsense_api.pydantic.CertBase import CertBase
from opnsense_api.pydantic.Certificate import Certificate
from opnsense_api.pydantic.Group import Group
from opnsense_api.pydantic.Lua import Lua
from opnsense_api.pydantic.Rule import Rule
from opnsense_api.pydantic.SNATRule import Rule as SNATRule
from opnsense_api.pydantic.OneToOneRule import Rule as OneToOneRule
from opnsense_api.pydantic.DNATRule import Rule as DNATRule
from opnsense_api.pydantic.User import User
from opnsense_api.pydantic.Vlan import Vlan
from opnsense_api.pydantic.KeaDhcpv4 import Subnet4, Reservation, Peer
from opnsense_api.pydantic.Unbound import Acl as UnboundAcl, Blocklist, Dot, Alias as UnboundAlias, Host as UnboundHost
from opnsense_api.pydantic.Validation import Validation
from opnsense_api.pydantic.pydantic_base import UIAwareMixin

T = TypeVar('T')
class SearchResult(UIAwareMixin, Generic[T]):
    rows: List[T]
    rowCount: int
    total: int
    current: int

    @classmethod
    def from_ui_dict(cls, data: Dict[str, Any], row_type: Type[T]) -> 'SearchResult[T]':
        """Parse SearchResult from dict, converting each row dict to typed object"""
        parsed_rows = [row_type.from_ui_dict(row_dict) for row_dict in data['rows']]
        return cls(
            rows=parsed_rows,
            rowCount=data['rowCount'],
            total=data['total'],
            current=data['current']
        )

    @classmethod
    def from_basic_dict(cls, data: Dict[str, Any], row_type: Type[T]) -> 'SearchResult[T]':
        """Parse SearchResult from dict, converting each row dict to typed object"""
        parsed_rows = [row_type.from_basic_dict(row_dict) for row_dict in data['rows']]
        return cls(
            rows=parsed_rows,
            rowCount=data['rowCount'],
            total=data['total'],
            current=data['current']
        )

    def get_by(self, key, value) -> T:
        for row in self.rows:
            if getattr(row,key) == value:
                return row
        return None

    def get_by_name(self, name) -> T:
        return self.get_by('name', name)

BaseObjectSearchResult = SearchResult[BaseObject]
CertSearchResult = SearchResult[Cert]
RuleSearchResult = SearchResult[Rule]
AliasSearchResult = SearchResult[Alias]
CategorySearchResult = SearchResult[Category]
ActionSearchResult = SearchResult[Action]
CertificateSearchResult = SearchResult[Certificate]
CaSearchResult = SearchResult[Ca]
CertBaseSearchResult = SearchResult[CertBase]
AccountSearchResult = SearchResult[Account]
ValidationSearchResult = SearchResult[Validation]
LuaSearchResult = SearchResult[Lua]
UserSearchResult = SearchResult[User]
GroupSearchResult = SearchResult[Group]
ApiUserSearchResult = SearchResult[ApiUser]
SNATRuleSearchResult = SearchResult[SNATRule]
OneToOneRuleSearchResult = SearchResult[OneToOneRule]
VlanSearchResult = SearchResult[Vlan]
Subnet4SearchResult = SearchResult[Subnet4]
ReservationSearchResult = SearchResult[Reservation]
PeerSearchResult = SearchResult[Peer]
UnboundAclSearchResult = SearchResult[UnboundAcl]
UnboundBlocklistSearchResult = SearchResult[Blocklist]
UnboundDotSearchResult = SearchResult[Dot]
UnboundAliasSearchResult = SearchResult[UnboundAlias]
UnboundHostSearchResult = SearchResult[UnboundHost]
DNATRuleSearchResult = SearchResult[DNATRule]
