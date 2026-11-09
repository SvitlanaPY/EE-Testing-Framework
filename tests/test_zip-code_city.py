import allure
import pytest
# import requests
from lib.ee_requests import EERequests
from lib.base_case import BaseCase
from testing_data.data_zipCode_City import parametersList
from testing_data.data_zipCode_City import parametersListNegative


@allure.feature("GET /zip-code/city")
class TestZipCodeCity(BaseCase):

    @allure.title("Check city and state search by ZIP code: {ZIP_Code} (Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, expected_city, expected_state, retailer', parametersList)
    def test_zipCodeCity_search_city_state_by_zipCode(self, ZIP_Code, expected_city, expected_state, retailer):
        # response = requests.get(f"{self.base_url}zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get(retailer)})
        response = EERequests.get(f"/zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = BaseCase.get_json_body(response)

        assert 'city' in response_json, "There is no city_parameter returned"
        actual_city = response_json['city']
        assert actual_city.upper() == expected_city.upper(), 'Actual city_parameter is INcorrect'

        assert 'state' in response_json, "There is no state_parameter returned"
        actual_state = response_json['state']
        assert actual_state.upper() == expected_state.upper(), 'Actual state_parameter is INcorrect'

    @allure.title("Check negative ZIP code search - not found for ZIP: {ZIP_Code} (Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, retailer', parametersListNegative)
    def test_negative_zipCodeCity_city_state_notFound(self, ZIP_Code, retailer):
        response = EERequests.get(f"/zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 404, 'Wrong status code - 404:NotFound is expected'
