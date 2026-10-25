import allure
import pytest
from lib.base_case import BaseCase
from testing_data.data_zipCode import parametersList
from testing_data.data_zipCode import parametersListNegative
from lib.ee_requests import EERequests
# import requests

"""Latitude is specified in degrees within the range [-90, 90].
Longitude is specified in degrees within the range [-180, 180).
422: "Validation Error"
"""


@allure.feature("GET /zip-code")
class TestZipCode(BaseCase):
    # def setup_method(self):
    #     self.headers_ = {
    #         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjI5MTEsImlhdCI6MTY5ODg1NTM5NywibmJmIjoxNjk4ODU1Mzk3LCJleHAiOjE3MzAzOTEzOTd9.A8ns_cKXjPHcMupLeJddePhdkYhwStzmuwYSgwdG5FY"
    #     }
    @allure.title("Check zipcode search by latitude and longitude (Lat: {lat}, Long: {long}, Retailer: {retailer})")
    @pytest.mark.parametrize("lat, long, expected_zipCode, expected_statusCode, retailer", parametersList)
    def test_zipCode_get_zipcode_by_latitude_longitude(self, lat, long, expected_zipCode, expected_statusCode, retailer):
        # response = requests.get(f"{self.base_url}zip-code", params={'latitude': lat, 'longitude': long}, headers={"Authorization": self.tokens_list.get(retailer)})
        response = EERequests.get(f"/zip-code", params={'latitude': lat, 'longitude': long}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == expected_statusCode, 'Wrong status code'

        actual_zipCode = response.text
        assert actual_zipCode == expected_zipCode, 'Actual zipCode_parameter is incorrect'

    @allure.title("Check zipCode validation by invalid coordinates (Lat: {lat}, Long: {long}, Retailer: {retailer})")
    @pytest.mark.parametrize("lat, long, retailer", parametersListNegative)
    def test_negative_zipCode_validation_failures(self, lat, long, retailer):
        response = EERequests.get(f"/zip-code", params={'latitude': lat, 'longitude': long}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 422, 'Wrong status code - 422:ValidationError is expected'
