from typing import List, Optional

import allure
import pytest
# import requests
from lib.ee_requests import EERequests
from pydantic import BaseModel, ValidationError
from lib.base_case import BaseCase
from testing_data.data_products_mileage import parametersList


class MileagePromoSchema(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    maxQty: Optional[int]
    colorProductIds: Optional[str]


class MileageProductSchema(BaseModel):
    """
    Schema according to the Swagger Example Value for GET /products/mileage.
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
    promos: List[MileagePromoSchema]
    masterSku: str


@allure.feature("GET /products/mileage")
class TestProductsMileage(BaseCase):

    @allure.title("Check response schema for products/mileage (ZIP: {ZIP_Code}, Store: {store_id}, QteGrp: {prodQteGrp_ID}, Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_productsMileage_response_structure(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        # response = requests.get(f"{self.base_url}products/mileage", params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID}, headers={"Authorization": self.tokens_list.get(retailer)})
        response = EERequests.get(f"/products/mileage", params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()
        assert len(response_json) > 0, "None product is returned"

        try:
            # Validates EVERY product in the list, not only the first one
            # TypeAdapter(List[MileageProduct]).validate_python(response_json)
            # Validates only first product in the list
            MileageProductSchema(**response_json[0])
        except ValidationError as error:
            assert False, f"Response schema mismatches for /products/mileage endpoint:\n{error}"

    @allure.title("Check required fields content for products/mileage (ZIP: {ZIP_Code}, Store: {store_id}, QteGrp: {prodQteGrp_ID}, Retailer: {retailer})")
    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_productsMileage_response_content(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = EERequests.get(f"/products/mileage", params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID}, headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_json = response.json()
        assert len(response_json) > 0, "None product is returned"
        assert response_json[0]['productId'] is not None, "productId cannot be null"
        assert response_json[0]['name'] is not None, "name cannot be null"
        assert response_json[0]['price'] is not None, "price cannot be null"
        assert response_json[0]['masterSku'] is not None, "masterSku cannot be null"
