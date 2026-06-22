import pytest
import requests
from lib.base_case import BaseCase


class TestCity(BaseCase):
    parametersList = [("07652", 25922, "fd"), ("30152", 28059, "cliqstudios"), ("47025", 21885, "lowes")]
    json_keys = ['attributes', 'colors', 'description', 'imageUrl', 'installedMinSqFt', 'isInstalled', 'jointPoints', 'materialID', 'prodOnlyMinSqFt', 'rank']


    @pytest.mark.parametrize('ZIP_Code, store_id, retailer', parametersList)
    def test_response_structure(self, ZIP_Code, store_id, retailer):

        response = requests.get(f"{self.base_url}products/materials", params={'zipCode': ZIP_Code, 'storeId': store_id}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) > 0, f"None material is returned"

        for key_name in self.json_keys:
            assert key_name in response_as_dict[0], f'There is no "{key_name}" json key  in response'


    @pytest.mark.parametrize('ZIP_Code, store_id, retailer', parametersList)
    def test_(self, ZIP_Code, store_id, retailer):

        response = requests.get(f"{self.base_url}products/materials", params={'zipCode': ZIP_Code, 'storeId': store_id}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
