from opnsense_api.base_client import BaseClient
from opnsense_api.pydantic.Category import Category
from opnsense_api.pydantic.Result import Result
from opnsense_api.pydantic.SearchResult import CategorySearchResult


class FirewallCategoryClient(BaseClient):

    def firewall_category_add_item(self, category: Category) -> Result:
        data = self._post('firewall/category/add_item', category)
        return Result(**data)

    def firewall_category_search_item(self) -> CategorySearchResult:
        data = self._get('firewall/category/search_item')
        return CategorySearchResult.from_ui_dict(data, Category)

    def firewall_category_get(self, uuid=None) -> Category:
        data = self._get('firewall/category/get_item' + self._get_arg_formatter(uuid))
        # print(data)
        return Category.from_ui_dict(data)
