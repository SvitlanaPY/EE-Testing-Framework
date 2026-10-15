from typing import List, Optional

import pytest
import requests
from pydantic import BaseModel, ValidationError
from lib.base_case import BaseCase
from .data_products_optional_items import parametersList


class OptionalItemsPromoSchema(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    maxQty: Optional[int]
    colorProductIds: Optional[str]


class OptionalItemsProductSchema(BaseModel):
    productId: int
    name: str
    consumerDesc: Optional[str]
    abbrevDesc: Optional[str]
    price: float
    priceWithoutDiscount: Optional[float]
    expirationPromotionDate: Optional[str]
    imageUrl: Optional[str]
    unitOfMeasure: Optional[str]
    qteTypeId: int
    qteTypeCode: str
    qteCodeId: Optional[int]
    qteCode: Optional[str]
    qteSubCodeId: Optional[int]
    qteSubCode: Optional[str]
    promos: Optional[List[OptionalItemsPromoSchema]]
    masterSku: str


class TestProductsOptionalItems(BaseCase):
    # GROUPS = ['cutouts', 'tear-outs', 'dishwashers', 'chip-minimizer', 'others']

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_productsOptionalItems_response_structure(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = requests.get(f"{self.base_url}products/optional-items",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()
        # for group in self.GROUPS:
        for group in response_json:
            # assert group in response_json, f'There is no "{group}" json key in response'
            group_value = response_json[group]
            if isinstance(group_value, list):
                if len(group_value) == 0:
                    continue
                else:
                    first_item = group_value[0]
            else:
                if group_value is None:
                    continue
                else:
                    first_item = group_value

            try:
                OptionalItemsProductSchema(**first_item)
                # OptionalItemsProductSchema.model_validate(first_item)
            except ValidationError as error:
                assert False, f'Response schema mismatches for /products/optional-items endpoint in group "{group}":\n{error}'

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_productsOptionalItems_response_content(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = requests.get(
            f"{self.base_url}products/optional-items",
            params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
            headers={"Authorization": self.tokens_list.get(retailer)}
        )
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()

        for group in response_json:
            group_value = response_json[group]
            if isinstance(group_value, list):
                if len(group_value) == 0:
                    continue
                first_item = group_value[0]
            else:
                if group_value is None:
                    continue
                first_item = group_value

            assert 'productId' in first_item, f'productId is missing for group "{group}"'
            assert 'name' in first_item, f'name is missing for group "{group}"'
            assert 'price' in first_item, f'price is missing for group "{group}"'
            assert 'masterSku' in first_item, f'masterSku is missing for group "{group}"'

            assert first_item['productId'] is not None, f'productId cannot be null (group "{group}")'
            assert first_item['name'] is not None, f'name cannot be null (group "{group}")'
            assert first_item['price'] is not None, f'price cannot be null (group "{group}")'
            assert first_item['masterSku'] is not None, f'masterSku cannot be null (group "{group}")'
