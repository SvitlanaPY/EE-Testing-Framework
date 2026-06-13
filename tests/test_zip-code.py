import pytest
import requests
from lib.base_case import BaseCase

# Latitude is specified in degrees within the range [-90, 90].
# Longitude is specified in degrees within the range [-180, 180).

class TestZipCode(BaseCase):
    parametersList = [
        ("39.1627", "-84.8914", "47025", 200),
        ("29.7437", "-95.7318", "77450", 200),
        ("40.6247", "-122.4659", "96001", 200),
        ("33.7709", "-84.2924", "30030", 200),
        ("42.1342", "-94.5133", "50050", 200),
        ("32.8266", "-106.1180", "88330", 200),
        ("49.81573772684511", "23.98527865454019", "", 204),
        ("0", "0", "", 204)
    ]
    parametersListNegative = [
        ("-91", "-84.8552564674385"),
        ("91", "-84.8552564674385"),
        ("39.182648106851005", "-181"),
        ("39.182648106851005", "181")
    ]

    # def setup_method(self):
    #     self.headers_ = {
    #         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjI5MTEsImlhdCI6MTY5ODg1NTM5NywibmJmIjoxNjk4ODU1Mzk3LCJleHAiOjE3MzAzOTEzOTd9.A8ns_cKXjPHcMupLeJddePhdkYhwStzmuwYSgwdG5FY"
    #     }
    @pytest.mark.parametrize('lat, long, expected_zipCode, expected_statusCode', parametersList)
    def test_get_zipCode_by_latitude_longitude(self, lat, long, expected_zipCode, expected_statusCode):
        response = requests.get(f"{self.base_url}zip-code", params={'latitude': lat, 'longitude': long}, headers={"Authorization": self.tokens_list.get('fd')})
        assert response.status_code == expected_statusCode, 'Wrong status code'

        actual_zipCode = response.text
        assert actual_zipCode == expected_zipCode, 'Actual zipCode_parameter is INcorrect'

    @pytest.mark.parametrize('lat, long', parametersListNegative)
    def test_negative_zipCode_validation_failures(self, lat, long):
        response = requests.get(f"{self.base_url}zip-code", params={'latitude': lat, 'longitude': long}, headers={"Authorization": self.tokens_list.get('fd')})
        assert response.status_code == 422, 'Wrong status code - 422:ValidationError is expected'
