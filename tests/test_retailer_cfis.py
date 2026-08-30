import pytest
import requests
from lib.base_case import BaseCase
from .data_retailer_cfis import parametersList
from .data_retailer_cfis import parametersList_ValidAddress
from .data_retailer_cfis import parametersList_inValidAddress


class TestCity(BaseCase):
    json_keys = ['companyId', 'companyName', 'address', 'city', 'state', 'zip', 'distance', 'deliveryStore']

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, radius, retailer', parametersList)
    def test_retailer_cfis_response_structure(self, ZIP_Code, store_id, prodQteGrp_ID, radius, retailer):
        response = requests.get(f"{self.base_url}retailer/cfis",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) > 0, "None cfi is returned"

        for key_name in self.json_keys:
            assert key_name in response_as_dict[0], f'There is no "{key_name}" json key in response'

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, radius, retailer', parametersList)
    def test_first_cfi_is_nearest(self, ZIP_Code, store_id, prodQteGrp_ID, radius, retailer):
        response = requests.get(f"{self.base_url}retailer/cfis",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) > 0, "None cfi is returned"

        min_distance = response_as_dict[0]['distance']
        for cfi in response_as_dict:
            assert min_distance <= cfi['distance'], 'The first cfi is not the nearest one'
        # for i in range(len(response_as_dict) - 1):
        #     assert response_as_dict[i + 1]['distance'] >= min_distance, "The first cfi is not the nearest one"

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, radius, retailer', parametersList)
    def test_distance_by_extra_service_radius_miles(self, ZIP_Code, store_id, prodQteGrp_ID, radius, retailer):
        response = requests.get(f"{self.base_url}retailer/cfis",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpID': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) > 0, "None cfi is returned"

        for cfi in response_as_dict:
            assert cfi['distance'] <= radius, 'CFI distance is greater than extra service radius.'

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, address, city, state, retailer', parametersList_ValidAddress)
    def test_distance_is_changed_by_address(self, ZIP_Code, store_id, prodQteGrp_ID, address, city, state, retailer):
        response_no_address = requests.get(f"{self.base_url}retailer/cfis",
                                           params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
                                           headers={"Authorization": self.tokens_list.get(retailer)})
        assert response_no_address.status_code == 200, 'Wrong status code'

        response_with_address = requests.get(f"{self.base_url}retailer/cfis",
                                             params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID, 'address': address, 'city': city, 'state': state},
                                             headers={"Authorization": self.tokens_list.get(retailer)})
        assert response_with_address.status_code == 200, 'Wrong status code'

        cfis_without_address = response_no_address.json()
        cfis_with_address = response_with_address.json()

        for cfi_no_address in cfis_without_address:
            if cfi_no_address.get('deliveryStore') is None:
                deliveryStore_storeID_noAddress = ""
            else:
                deliveryStore_storeID_noAddress = cfi_no_address.get('deliveryStore')['storeId']
            for cfi_w_address in cfis_with_address:
                if cfi_w_address['companyId'] == cfi_no_address['companyId']:
                    if cfi_w_address.get('deliveryStore') is None:
                        deliveryStore_storeID_wAddress = ""
                    else:
                        deliveryStore_storeID_wAddress = cfi_w_address.get('deliveryStore')['storeId']
                    if deliveryStore_storeID_noAddress == deliveryStore_storeID_wAddress:
                        assert cfi_no_address['distance'] != cfi_w_address['distance'], "Defining the project's installation address does not affect the distance to the CFI."
                    break

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, address, city, state, retailer', parametersList_inValidAddress)
    def test_distance_not_changed_by_wrong_address(self, ZIP_Code, store_id, prodQteGrp_ID, address, city, state, retailer):
        response_no_address = requests.get(f"{self.base_url}retailer/cfis",
                                           params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
                                           headers={"Authorization": self.tokens_list.get(retailer)})
        assert response_no_address.status_code == 200, 'Wrong status code'

        cfis_without_address = response_no_address.json()

        response_with_address = requests.get(f"{self.base_url}retailer/cfis",
                                             params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID, 'address': address, 'city': city, 'state': state},
                                             headers={"Authorization": self.tokens_list.get(retailer)})
        assert response_with_address.status_code == 200, 'Wrong status code'
        cfis_with_address = response_with_address.json()

        for cfi_no_address in cfis_without_address:
            if cfi_no_address.get('deliveryStore') is None:
                deliveryStore_storeID_noAddress = ""
            else:
                deliveryStore_storeID_noAddress = cfi_no_address.get('deliveryStore')['storeId']
            for cfi_w_address in cfis_with_address:
                if cfi_w_address['companyId'] == cfi_no_address['companyId']:
                    if cfi_w_address.get('deliveryStore') is None:
                        deliveryStore_storeID_wAddress = ""
                    else:
                        deliveryStore_storeID_wAddress = cfi_w_address.get('deliveryStore')['storeId']
                    assert deliveryStore_storeID_noAddress == deliveryStore_storeID_wAddress or cfi_no_address['distance'] == cfi_w_address['distance'], "Defining the invalid project's installation address does affect the distance to the CFI."
                    break

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    def test_bad_zip(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
        response = requests.get(f"{self.base_url}retailer/cfis", params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 400, 'Wrong status code - 400:BAD ZI is expected'
