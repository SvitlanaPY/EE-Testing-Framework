import pytest
import requests
import json

class TestStores:
    parametersList1 = ["07652", "77450", "47025"]
    parametersList2 = [("07450", '25922'), ("07450", '28047')]
    json_keys = ['companyId', 'companyName', 'address', 'city', 'state', 'zip', 'distance', 'adPatchId', 'latitude', 'longitude']

    def setup_class(self):
        retailer = {'clientHost': 'fd.staging.inscyth.com'}

        response_ = requests.get("https://ee-api-ssi.staging.inscyth.com/lookup/retailer", params=retailer)
        assert response_.status_code == 200, 'Wrong status code'

        assert "token" in response_.json(), "There is no Bearer token in the response_"
        self.token = response_.json().get("token")


    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_get_six_stores(self, Zip_Code):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) <= 6, 'Returned stores are more than 6'


    @pytest.mark.parametrize('Zip_Code', parametersList1)
    def test_stores_json_structure(self, Zip_Code):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        for key_name in self.json_keys:
            assert key_name in response_as_dict[0], f'There is no "{key_name}" json field  in response'


    @pytest.mark.parametrize('Zip_Code, Store_Id', parametersList2)
    def test_get_stores_by_storeId(self, Zip_Code, Store_Id):
        response = requests.get("https://ee-api-ssi.staging.inscyth.com/stores", params={'ZipCode': Zip_Code, 'storeId': Store_Id}, headers={"Authorization": self.token})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        expected_adPatchId = response_as_dict[0]['adPatchId']
        for i in range(1, len(response_as_dict)):
            assert response_as_dict[i]['adPatchId'] == expected_adPatchId, f"Wrong adPatchId for {response_as_dict[i]['companyId']}"

        # for store in response_as_dict:
        #     assert store['adPatchId'] == expected_adPatchId, f"Wrong adPatchId for {store['companyId']}"

