import allure
import pytest
# import requests
from lib.ee_requests import EERequests
from lib.base_case import BaseCase


@allure.feature("GET /stores")
class TestStores(BaseCase):
    parametersList1 = ["07652", "71601", "47025"]
    parametersList2 = [("07450", '25922'), ("07450", '28047')]
    json_keys = ['companyId', 'companyName', 'address', 'city', 'state', 'zip', 'distance', 'adPatchId', 'latitude', 'longitude']

    @allure.title("Check maximum 6 stores returned for ZIP: {Zip_Code}")
    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_stores_get_six_stores(self, Zip_Code):
        # response = requests.get(f"{self.base_url}stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.tokens_list.get('flooranddecor')})
        response = EERequests.get(f"/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.tokens_list.get('flooranddecor')})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        assert len(response_json) <= 6, 'Returned stores are more than 6'

    @allure.title("Check if the first store is the nearest one (ZIP: {Zip_Code})")
    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_stores_first_nearest_store(self, Zip_Code):
        response = EERequests.get(f"/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.tokens_list.get('flooranddecor')})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        min_distance = response_json[0]['distance']
        for store in response_json:
            assert min_distance <= store['distance'], 'The first store is not the nearest one'

    @allure.title("Check same adPatchId as given store adPatch: {expected_adPatchId} (ZIP: {Zip_Code}, Store ID: {Store_Id})")
    @pytest.mark.parametrize('Zip_Code, Store_Id', parametersList2)
    def test_stores_same_adPatch_as_given_store(self, Zip_Code, Store_Id):
        response = EERequests.get(f"/stores", params={'ZipCode': Zip_Code, 'storeId': Store_Id}, headers={"Authorization": self.tokens_list.get('flooranddecor')})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        expected_adPatchId = response_json[0]['adPatchId']
        allure.dynamic.title(f"Check same adPatchId as given store adPatch: {expected_adPatchId} (ZIP: {Zip_Code}, Store ID: {Store_Id})")
        for i in range(1, len(response_json)):
            assert response_json[i]['adPatchId'] == expected_adPatchId, f"Wrong adPatchId for {response_json[i]['companyId']}"
        # for store in response_as_dict:
        #     assert store['adPatchId'] == expected_adPatchId, f"Wrong adPatchId for {store['companyId']}"

    @allure.title("Check negative stores validation error for invalid ZIP")
    def test_negative_stores_validation_error(self):
        invalidZip = '0745'
        response = EERequests.get(f"/stores", params={'ZipCode': invalidZip}, headers={"Authorization": self.tokens_list.get('flooranddecor')})
        assert response.status_code == 422, 'Wrong status code - 422:UNPROCESSABLE CONTENT is expected'
        # response_json = BaseCase.get_json_body(response)
        # assert response_json['validationErrors'][0]['errorMessage'] == 'Zipcode should be 5 digits', 'Wrong error message'

    @allure.title("Check response structure for /stores (ZIP: {Zip_Code})")
    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_stores_response_structure(self, Zip_Code):
        response = EERequests.get(f"/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.tokens_list.get('flooranddecor')})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)
        assert len(response_json) > 0, "None store is returned"

        response_json = BaseCase.get_json_body(response)
        for key_name in self.json_keys:
            assert key_name in response_json[0], f'There is no "{key_name}" json key  in response'
