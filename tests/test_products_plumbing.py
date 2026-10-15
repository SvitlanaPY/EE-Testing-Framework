from typing import List, Optional

import pytest
import requests
from pydantic import BaseModel, ValidationError
from lib.base_case import BaseCase
from .data_products_plumbing import parametersList


class PlumbingPromoSchema(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    maxQty: Optional[int]
    colorProductIds: Optional[str]


class PlumbingProductSchema(BaseModel):
    """
    Schema according to the Swagger Example Value for GET /products/plumbing.
    Fields without a default value are REQUIRED (Optional[...] only allows null).
    """
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
    promos: List[PlumbingPromoSchema]
    masterSku: str


class TestProductsPlumbing(BaseCase):

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_productsPlumbing_response_structure(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = requests.get(f"{self.base_url}products/plumbing",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()
        assert len(response_json) > 0, "None product is returned"

        try:
            # Validates only first product in the list
            PlumbingProductSchema(**response_json[0])
        except ValidationError as error:
            assert False, f"Response schema mismatches for /products/plumbing endpoint:\n{error}"

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_productsPlumbing_response_content(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
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
