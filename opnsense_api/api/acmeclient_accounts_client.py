from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Account import Account
from opnsense_api.pydantic.SearchRequest import SearchRequest
from opnsense_api.pydantic.SearchResult import AccountSearchResult


class AcmeclientAccountsClient(BaseClient):

    def acmeclient_accounts_search(self, search: SearchRequest = None) -> AccountSearchResult:
        s = search
        if s is not None:
            s = s.__dict__
        data = self._post('acmeclient/accounts/search', s)
        # print(data)
        return AccountSearchResult.from_basic_dict(data, Account)
