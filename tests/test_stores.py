import pytest
import requests
from lib.base_case import BaseCase


class TestStores(BaseCase):
    parametersList1 = ["07652", "71601", "47025"]
    parametersList2 = [("07450", '25922'), ("07450", '28047')]
    json_keys = ['companyId', 'companyName', 'address', 'city', 'state', 'zip', 'distance', 'adPatchId', 'latitude', 'longitude']

    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_get_six_stores(self, Zip_Code):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) <= 6, 'Returned stores are more than 6'

    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_response_structure(self, Zip_Code):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        for key_name in self.json_keys:
            assert key_name in response_as_dict[0], f'There is no "{key_name}" json key  in response'

    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_first_nearest_store(self, Zip_Code):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        min_distance = response_as_dict[0]['distance']
        for store in response_as_dict:
            assert min_distance <= store['distance'], 'The first store is not the nearest one'

    @pytest.mark.parametrize('Zip_Code, Store_Id', parametersList2)
    def test_same_adpatch_as_given_store(self, Zip_Code, Store_Id):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code, 'storeId': Store_Id}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        expected_adPatchId = response_as_dict[0]['adPatchId']
        for i in range(1, len(response_as_dict)):
            assert response_as_dict[i]['adPatchId'] == expected_adPatchId, f"Wrong adPatchId for {response_as_dict[i]['companyId']}"
        # for store in response_as_dict:
        #     assert store['adPatchId'] == expected_adPatchId, f"Wrong adPatchId for {store['companyId']}"

    def test_negative_validation_error(self):
        invalidZip = '0745'
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': invalidZip}, headers={"Authorization": self.token})
        assert response.status_code == 422, 'Wrong status code'

        # response_as_dict = response.json()
        # assert response_as_dict['validationErrors'][0]['errorMessage'] == 'Zipcode should be 5 digits', 'Wrong error message'
