import pytest
import requests
from lib.base_case import BaseCase


class TestEPM(BaseCase):
    """sent_productID, sent_typeId, expected_newProductID, target_zipCode, target_storeId, target_materialId, target_materialName, target_colorId, target_productQteGrpId"""
    parametersList = [
        (30644, 1102, 30672, "07652", 25922, 2510, "Quartz", 0, 740),
        (30645, 1102, 30673, "07652", 25922, 2510, "Quartz", 0, 740),
        (30646, 1102, 30676, "07652", 25922, 2510, "Quartz", 0, 740),
        (30647, 1102, 30674, "07652", 25922, 2510, "Quartz", 0, 740),
        (30648, 1102, 30675, "07652", 25922, 2510, "Quartz", 0, 740),
        (30649, 1102, 30677, "07652", 25922, 2510, "Quartz", 0, 740),
        (30655, 1104, 30680, "07652", 25922, 2510, "Quartz", 0, 740),
        (30656, 1104, 30681, "07652", 25922, 2510, "Quartz", 0, 740),
        (30657, 1104, 30682, "07652", 25922, 2510, "Quartz", 0, 740),
        (30658, 1104, 30683, "07652", 25922, 2510, "Quartz", 0, 740),
        (30659, 1104, 30684, "07652", 25922, 2510, "Quartz", 0, 740),
        (-999, None, -999, "07652", 25922, 2510, "Quartz", 0, 740),
        (30652, 1105, 30687, "07652", 25922, 2510, "Quartz", 0, 740),
        (-997, None, -997, "07652", 25922, 2510, "Quartz", 0, 740),
        (30653, 1107, 30685, "07652", 25922, 2510, "Quartz", 0, 740),
        (30654, 1107, 30686, "07652", 25922, 2510, "Quartz", 0, 740),
        (30660, 1107, 30688, "07652", 25922, 2510, "Quartz", 0, 740),
        (30665, 1108, 30693, "07652", 25922, 2510, "Quartz", 0, 740),
        (30666, 1108, 30694, "07652", 25922, 2510, "Quartz", 0, 740),
        (51579, 1111, 51579, "07652", 25922, 2510, "Quartz", 0, 740),
        (51580, 1111, 51580, "07652", 25922, 2510, "Quartz", 0, 740),
        (39138, 1111, 39137, "07652", 25922, 2510, "Quartz", 0, 740),
        (39136, 1111, 39135, "07652", 25922, 2510, "Quartz", 0, 740),
        (30667, 1111, 30695, "07652", 25922, 2510, "Quartz", 0, 740),
        (30651, 1111, 30679, "07652", 25922, 2510, "Quartz", 0, 740),
        (51144, 1106, 51140, "07652", 25922, 2510, "Quartz", 0, 740),
        (51145, 1106, 51141, "07652", 25922, 2510, "Quartz", 0, 740),
        (51146, 1106, 51142, "07652", 25922, 2510, "Quartz", 0, 740),
        (51147, 1106, 51143, "07652", 25922, 2510, "Quartz", 0, 740),
        (51158, 1106, 51148, "07652", 25922, 2510, "Quartz", 0, 740),
        (51164, 1106, 51154, "07652", 25922, 2510, "Quartz", 0, 740),
        (51160, 1106, 51150, "07652", 25922, 2510, "Quartz", 0, 740),
        (51163, 1106, 51153, "07652", 25922, 2510, "Quartz", 0, 740)
    ]

    def get_payload(self,
                    product_id,
                    type_id,
                    zip_code,
                    store_id,
                    material_id,
                    material_name,
                    color_id,
                    qte_grp_id
                    ):
        """Хелпер-метод для динамічного формування payload"""
        return {
            "products": [{"productID": product_id, "typeID": type_id}],
            "targetParams": {
                "zipCode": zip_code,
                "storeId": store_id,
                "material": {
                    "materialId": material_id,
                    "materialName": material_name
                },
                "color": {
                    "colorId": color_id,
                    "colorName": "string",
                    "thicknessOptions": "string"
                },
                "productQteGrpId": qte_grp_id
            },
            "retailerId": 0
        }


    @pytest.mark.parametrize("sent_product_id, sent_type_id, expected_product_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id", parametersList)
    def test_EPM_products_to_replace(self, sent_product_id, sent_type_id, expected_product_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id):
        # Формуємо payload
        current_payload = self.get_payload(
            sent_product_id, sent_type_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id
        )

        response = requests.post(f"{self.base_url}products/matching", json=current_payload, headers={"Authorization": self.token})
        assert response.status_code == 200, f"Wrong status code - 200 is expected, but got {response.status_code}: {response.reason}"

        response_json = response.json()

        assert len(response_json["productsToReplace"]) != 0, f"Mapping error! Expected a product to replace for productID: {sent_product_id}, but no matching product returned to replace."
        assert "newProductID" in response_json["productsToReplace"][0], "Response JSON does not contain 'newProductID' field"
        # Отримуємо newProductID, який повернув сервер
        received_product_id = response_json["productsToReplace"][0]["newProductID"]

        assert received_product_id == expected_product_id, f"Mapping error! Sent productID: {sent_product_id}. Expected to get: {expected_product_id}, but actually received: {received_product_id}"

