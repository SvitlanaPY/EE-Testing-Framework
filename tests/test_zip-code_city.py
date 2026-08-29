import pytest
import requests
from lib.base_case import BaseCase
from .data_zipCode_City import parametersList
from .data_zipCode_City import parametersListNegative

class TestCity(BaseCase):

    @pytest.mark.parametrize('ZIP_Code, expected_city, expected_state, retailer', parametersList)
    def test_search_city_state_by_zipCode(self, ZIP_Code, expected_city, expected_state, retailer):
        response = requests.get(f"{self.base_url}zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        assert 'city' in response.json(), "There is no city_parameter returned"
        actual_city = response.json()['city']
        # self.actual_city = self.get_json_value(response, "city")
        assert actual_city.upper() == expected_city.upper(), 'Actual city_parameter is INcorrect'

        assert 'state' in response.json(), "There is no state_parameter returned"
        actual_state = response.json()['state']
        # actual_state = self.get_json_value(response, "state")
        assert actual_state.upper() == expected_state.upper(), 'Actual state_parameter is INcorrect'

    @pytest.mark.parametrize('ZIP_Code, retailer', parametersListNegative)
    def test_negative_city_state_notFound(self, ZIP_Code, retailer):
        response = requests.get(f"{self.base_url}zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 404, 'Wrong status code - 404:NotFound is expected'
