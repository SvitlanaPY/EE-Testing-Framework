import pytest
import requests
from lib.base_case import BaseCase


class TestCity(BaseCase):
    parametersList = [
        ("07450", "Ridgewood", "NJ"),
        ("77450", "Katy", "TX"),
        ("47025", "Lawrenceburg", "IN"),
        ("96001", "Redding", "CA"),
        ("30030", "Decatur", "GA"),
        ("50050", "Churdan", "IA"),
        ("9255700", "Moreno Valley", "CA")
    ]

    parametersListNegative = [
        ("35001"),
        ("00000"),
        ("47o25"),
        (""),
        ("4702")
        # ("77450")  # щоб негативний тест не пройшов, а впав з помилкою
    ]


    @pytest.mark.parametrize('ZIP_Code, expected_city, expected_state', parametersList)
    def test_search_city_state_by_zipCode(self, ZIP_Code, expected_city, expected_state):
        response = requests.get(f"{self.base_url}zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get('fd')})
        assert response.status_code == 200, 'Wrong status code'

        assert 'city' in response.json(), "There is no city_parameter returned"
        actual_city = response.json()['city']
        # self.actual_city = self.get_json_value(response, "city")
        assert actual_city.upper() == expected_city.upper(), 'Actual city_parameter is INcorrect'

        assert 'state' in response.json(), "There is no state_parameter returned"
        actual_state = response.json()['state']
        # actual_state = self.get_json_value(response, "state")
        assert actual_state.upper() == expected_state.upper(), 'Actual state_parameter is INcorrect'

    @pytest.mark.parametrize('ZIP_Code', parametersListNegative)
    def test_negative_city_state_notFound(self, ZIP_Code):
        response = requests.get(f"{self.base_url}zip-code/city", params={'zipCode': ZIP_Code}, headers={"Authorization": self.tokens_list.get('fd')})
        assert response.status_code == 404, 'Wrong status code - 404:NotFound is expected'
