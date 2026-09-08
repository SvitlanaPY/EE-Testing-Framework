import pytest
import requests
from lib.base_case import BaseCase
from .data_lookup_retailer import parametersList

class TestLookupRetailer(BaseCase):

    @pytest.mark.parametrize('client_Host, expected_api_HostName, expected_retailer_Code', parametersList)
    def test_lookup_retailer(self, client_Host, expected_api_HostName, expected_retailer_Code):
        response = requests.get(f"{self.base_url}lookup/retailer", params={'clientHost': client_Host})

        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert response_as_dict['apiHostname'] == expected_api_HostName, f"Expected apiHostname: {expected_api_HostName}, but got: {response_as_dict['apiHostname']}"
        assert response_as_dict['retailerCode'] == expected_retailer_Code, f"Expected retailerCode: {expected_retailer_Code}, but got: {response_as_dict['retailerCode']}"


    def test_lookup_retailer_invalid_clientHost(self):
        invalid_clientHost = "invalid.clienthost.com"
        response = requests.get(f"{self.base_url}lookup/retailer", params={'clientHost': invalid_clientHost})

        assert response.status_code == 200, f"Expected status code 200 for invalid clientHost, but got {response.status_code}"

        response_as_dict = response.json()
        assert response_as_dict['apiHostname'] == None, f"Expected apiHostname: None, but got: {response_as_dict['apiHostname']}"
        assert response_as_dict['retailerCode'] == None, f"Expected retailerCode: None, but got: {response_as_dict['retailerCode']}"
