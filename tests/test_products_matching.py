import pytest
import requests
from lib.base_case import BaseCase


class TestEPM(BaseCase):

    payload_data = {
      "products": [
        {
          "productID": 30644,
          "typeID": 1102
        },
        {
          "productID": 30645,
          "typeID": 1102
        },
        {
          "productID": 30646,
          "typeID": 1102
        },
        {
          "productID": 30647,
          "typeID": 1102
        },
        {
          "productID": 30649,
          "typeID": 1102
        },
        {
          "productID": 30648,
          "typeID": 1102
        }
      ],
      "targetParams": {
        "zipCode": "07652",
        "storeId": 25922,
        "material": {
          "materialId": 2510,
          "materialName": "Quartz"
        },
        "color": {
          "colorId": 0,
          "colorName": "string",
          "thicknessOptions": "string"
        },
        "productQteGrpId": 740
      },
      "retailerId": 0
    }

    def test_EPM(self):
        response = requests.post(f"{self.base_url}products/matching", json=self.payload_data, headers={"Authorization": self.token})

        assert response.status_code == 200, f"Wrong status code - 200 is expected, but got {response.status_code}"

