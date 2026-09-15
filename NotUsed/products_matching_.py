import pytest
import requests
from lib.base_case import BaseCase


class TestEPM(BaseCase):
    parametersList = [(30652, 1105, 30687), (-997, None, -997)]

    def get_payload(self, product_id, type_id):
        """Хелпер-метод для динамічного формування payload"""
        return {
            "products": [{"productID": product_id, "typeID": type_id}],
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

    @pytest.mark.parametrize("sent_product_id, sent_type_id, expected_product_id", parametersList)
    def test_EPM_products_to_replace(self, sent_product_id, sent_type_id, expected_product_id):
        # Формуємо payload
        current_payload = self.get_payload(sent_product_id, sent_type_id)

        response = requests.post(f"{self.base_url}products/matching", json=current_payload, headers={"Authorization": self.token})
        assert response.status_code == 200, f"Wrong status code - 200 is expected, but got {response.status_code}"

        response_json = response.json()
        assert "newProductID" in response_json["productsToReplace"][0], "Response JSON does not contain 'newProductID' field"
        # Отримуємо newProductID, який фактично повернув сервер
        received_product_id = response_json["productsToReplace"][0]["newProductID"]

        assert received_product_id == expected_product_id, f"Mapping error! Sent productID: {sent_product_id}. Expected to get: {expected_product_id}, but actually received: {received_product_id}"
