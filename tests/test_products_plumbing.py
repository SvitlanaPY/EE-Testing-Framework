import pytest
import requests
from jsonschema import ValidationError, validate
from lib.base_case import BaseCase
from .data_products_plumbing import parametersList


class TestProductsPlumbing(BaseCase):
    """
    Перевірка JSON-структури відповіді за Swagger Example Value:
    [
        {
        "productId": 0,
        "name": "string",
        "consumerDesc": "string",
        "abbrevDesc": "string",
        "price": 0,
        "priceWithoutDiscount": 0,
        "expirationPromotionDate": "2026-09-13T17:52:16.383Z",
        "imageUrl": "string",
        "unitOfMeasure": "string",
        "qteTypeId": 0,
        "qteTypeCode": "string",
        "qteCodeId": 0,
        "qteCode": "string",
        "qteSubCodeId": 0,
        "qteSubCode": "string",
        "promos": [
          {"id": 0, "quantity": 0, "maxQty": 0, "colorProductIds": "string"}
        ],
        "masterSku": "string"
        }
    ]
    """

    PRODUCT_SCHEMA = {
        "type": "object",
        "required": [
            "productId",
            "name",
            "consumerDesc",
            "abbrevDesc",
            "price",
            "priceWithoutDiscount",
            "expirationPromotionDate",
            "imageUrl",
            "unitOfMeasure",
            "qteTypeId",
            "qteTypeCode",
            "qteCodeId",
            "qteCode",
            "qteSubCodeId",
            "qteSubCode",
            "promos",
            "masterSku",
        ],
        "properties": {
            "abbrevDesc": {"type": ["string", "null"]},
            "consumerDesc": {"type": ["string", "null"]},
            "expirationPromotionDate": {"type": ["string", "null"]},
            "imageUrl": {"type": "string"},
            "masterSku": {"type": "string"},
            "name": {"type": "string"},
            "price": {"type": "number"},
            "priceWithoutDiscount": {"type": "number"},
            "productId": {"type": "integer"},
            "promos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "quantity", "maxQty", "colorProductIds"],
                    "properties": {
                        "colorProductIds": {"type": ["string", "null"]},
                        "id": {"type": "integer"},
                        "maxQty": {"type": "integer"},
                        "quantity": {"type": "integer"},
                    },
                },
            },
            "qteCodeId": {"type": ["integer", "null"]},
            "qteCode": {"type": ["string", "null"]},
            "qteSubCodeId": {"type": ["integer", "null"]},
            "qteSubCode": {"type": ["string", "null"]},
            "qteTypeCode": {"type": "string"},
            "qteTypeId": {"type": "integer"},
            "unitOfMeasure": {"type": ["string", "null"]},
        },
    }

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_products_plumbing_response_structure(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = requests.get(f"{self.base_url}products/plumbing",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()
        assert len(response_json) > 0, "None product is returned"

        json_element = response_json[0]
        try:
            validate(instance=json_element, schema=self.PRODUCT_SCHEMA)
        except ValidationError as error:
            assert False, f"Response schema mismatch for /products/plumbing endpoint in json-property: {error.json_path}, {error.message}"

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_products_plumbing_response_content(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = requests.get(f"{self.base_url}products/plumbing",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()
        assert len(response_json) > 0, "None product is returned"
        assert response_json[0]['productId'] is not None, "productId cannot be null"
        assert response_json[0]['name'] is not None, "name cannot be null"
        assert response_json[0]['price'] is not None, "price cannot be null"
        assert response_json[0]['masterSku'] is not None, "masterSku cannot be null"
