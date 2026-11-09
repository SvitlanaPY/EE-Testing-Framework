import allure
import pytest
# import requests
from lib.ee_requests import EERequests
from lib.base_case import BaseCase
from testing_data.data_products_materials import parametersList


@allure.feature("GET /products/materials")
class TestProductsMaterials(BaseCase):
    json_keys = ['attributes', 'colors', 'description', 'imageUrl', 'installedMinSqFt', 'isInstalled', 'jointPoints',
                 'materialID', 'prodOnlyMinSqFt', 'rank']

    @allure.title("Check response structure for products/materials/ (ZIP: {ZIP_Code}, Store: {store_id}, Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, store_id, retailer', parametersList)
    def test_productsMaterials_response_structure(self, ZIP_Code, store_id, retailer):
        # response = requests.get(f"{self.base_url}products/materials", params={'zipCode': ZIP_Code, 'storeId': store_id}, headers={"Authorization": self.tokens_list.get(retailer)})
        response = EERequests.get(f"/products/materials", params={'zipCode': ZIP_Code, 'storeId': store_id}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        assert len(response_json) > 0, "None material is returned"

        for key_name in self.json_keys:
            assert key_name in response_json[0], f'There is no "{key_name}" json key in response'

    @allure.title("Check colors availability in products/materials/ (ZIP: {ZIP_Code}, Store: {store_id}, Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, store_id, retailer', parametersList)
    def test_productsMaterials_get_colors(self, ZIP_Code, store_id, retailer):
        response = EERequests.get(f"/products/materials", params={'zipCode': ZIP_Code, 'storeId': store_id}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        for i in range(len(response_json)):
            assert len(response_json[i]['colors']) > 0, f"None color is returned"

    @allure.title("Check materials sorting by rank in products/materials/ (ZIP: {ZIP_Code}, Store: {store_id}, Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, store_id, retailer', parametersList)
    def test_productsMaterials_sort_materials_by_rank(self, ZIP_Code, store_id, retailer):
        response = EERequests.get(f"/products/materials", params={'zipCode': ZIP_Code, 'storeId': store_id}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        for i in range(len(response_json)):
            if response_json[i]['rank'] is None:
                response_json[i]['rank'] = 999999999999

        for i in range(len(response_json) - 1):
            assert response_json[i + 1]['rank'] >= response_json[i]['rank'], "Materials are not sorted"
