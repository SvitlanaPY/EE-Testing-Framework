import pytest
import requests
from lib.base_case import BaseCase


class TestEPM(BaseCase):
    """sent_productID, sent_typeId, target_zipCode, target_storeId, target_materialId, target_materialName, target_colorId, target_productQteGrpId, retailer"""
    parametersList = [(39091, 1111, "07652", 25922, 2510, "Quartz", 0, 740, 'fd'),
                      (40926, 1102, "07652", 25922, 2510, "Quartz", 0, 740, 'fd'),
                      (40921, 1102, "07652", 25922, 2510, "Quartz", 0, 740, 'fd'),
                      (30692, 1111, "07652", 25922, 2500, "Natural Stone", 0, 780, 'fd'),
                      (39114, 1111, "07652", 25922, 2500, "Natural Stone", 0, 780, 'fd'),
                      (39112, 1111, "07652", 25922, 2500, "Natural Stone", 0, 780, 'fd'),
                      (40919, 1106, "07652", 25922, 2500, "Natural Stone", 0, 780, 'fd'),
                      (40924, 1106, "07652", 25922, 2500, "Natural Stone", 0, 780, 'fd'),
                      (35938, 1102, "45245", 26198, 2513, "Solid Surface", 0, 780, 'homeoutlet'),
                      (35958, 1107, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (36132, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (36134, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (35963, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40911, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (35958, 1107, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (35959, 1107, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40906, 1107, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (35957, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (36134, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (35963, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40284, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40285, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40286, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40287, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (40288, 1111, "45245", 26198, 2513, "Solid Surface", 0, 750, 'homeoutlet'),
                      (37479, 1102, "45245", 26198, 2500, "Natural Stone", 0, 780, 'homeoutlet'),
                      (40939, 1111, "45245", 26198, 2500, "Natural Stone", 0, 780, 'homeoutlet'),
                      (37495, 1107, "45245", 26198, 2500, "Natural Stone", 0, 780, 'homeoutlet')
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
        "sent_product_id, sent_type_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id, retailer",
        parametersList)
    def test_EPM_products_to_replace(self, sent_product_id, sent_type_id, zip_code, store_id,
                                     material_id, material_name, color_id, qte_grp_id, retailer):
        # Формуємо payload
        current_payload = self.get_payload(
            sent_product_id, sent_type_id, zip_code, store_id, material_id, material_name, color_id, qte_grp_id
        )

        response = requests.post(f"{self.base_url}products/matching", json=current_payload,
                                 headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, f"Wrong status code - 200 is expected, but got {response.status_code}: {response.reason}"

        response_json = response.json()

        assert len(response_json[
                       "productsToRemove"]) != 0, f"Mapping error! Expected productID: {sent_product_id} to be removed, but no product returned to remove."
        assert "productId" in response_json["productsToRemove"][0], "Response JSON does not contain 'productId' field"
        # Отримуємо newProductID, який повернув сервер
        received_product_id = response_json["productsToRemove"][0]["productId"]

        assert received_product_id == sent_product_id, f"Mapping error! Sent productID {sent_product_id} is not removed."
