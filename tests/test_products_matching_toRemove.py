import pytest
import requests
from lib.base_case import BaseCase


class TestEPM(BaseCase):
    """sent_productID, sent_typeId, target_zipCode, target_storeId, target_materialId, target_materialName, target_colorId, target_productQteGrpId"""
    parametersList = [
        (39091, 1111, "07652", 25922, 2510, "Quartz", 0, 740),
        (40926, 1102, "07652", 25922, 2510, "Quartz", 0, 740),
        (40921, 1102, "07652", 25922, 2510, "Quartz", 0, 740),
        (30692, 1111, "07652", 25922, 2500, "Natural Stone", 0, 780),
        (39114, 1111, "07652", 25922, 2500, "Natural Stone", 0, 780),
        (39112, 1111, "07652", 25922, 2500, "Natural Stone", 0, 780),
        (40926, 1106, "07652", 25922, 2500, "Natural Stone", 0, 780),
        (40924, 1106, "07652", 25922, 2500, "Natural Stone", 0, 780)
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

    @pytest.mark.parametrize(
        "sent_product_id, sent_type_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id",
        parametersList)
    def test_EPM_products_to_replace(self, sent_product_id, sent_type_id, zip_code, store_id,
                                     material_id, material_name, color_id, qte_grp_id):
        # Формуємо payload
        current_payload = self.get_payload(
            sent_product_id, sent_type_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id
        )

        response = requests.post(f"{self.base_url}products/matching", json=current_payload, headers={"Authorization": self.token})
        assert response.status_code == 200, f"Wrong status code - 200 is expected, but got {response.status_code}: {response.reason}"

        response_json = response.json()

        assert len(response_json["productsToRemove"]) != 0, f"Mapping error! Expected productID: {sent_product_id} to be removed, but no product returned to remove."
        assert "productId" in response_json["productsToRemove"][0], "Response JSON does not contain 'productId' field"
        # Отримуємо newProductID, який повернув сервер
        received_product_id = response_json["productsToRemove"][0]["productId"]

        assert received_product_id == sent_product_id, f"Mapping error! Sent productID {sent_product_id} is not removed."
