import pytest
import requests
from lib.base_case import BaseCase
from .data_retailer_cfis import parametersList


class TestCity(BaseCase):
    json_keys = ['address', 'city', 'companyId', 'companyName', 'deliveryStore', 'distance', 'state', 'zip']

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, radius, retailer', parametersList)
    def test_cfis_response_structure(self, ZIP_Code, store_id, prodQteGrp_ID, radius, retailer):
        response = requests.get(f"{self.base_url}retailer/cfis",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) > 0, "None cfi is returned"

        for key_name in self.json_keys:
            assert key_name in response_as_dict[0], f'There is no "{key_name}" json key in response'

    @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, radius, retailer', parametersList)
    def test_first_cfi_is_nearest(self, ZIP_Code, store_id, prodQteGrp_ID, radius, retailer):
        response = requests.get(f"{self.base_url}retailer/cfis",
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
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
                                params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
                                headers={"Authorization": self.tokens_list.get(retailer)})
        assert response.status_code == 200, 'Wrong status code'

        response_as_dict = response.json()
        assert len(response_as_dict) > 0, "None cfi is returned"

        for cfi in response_as_dict:
            assert cfi['distance'] <= radius, 'CFI distance is greater than extra service radius.'

    # @pytest.mark.parametrize('ZIP_Code, store_id, prodQteGrp_ID, retailer', parametersList)
    # def test_distance_is_changed_by_address(self, ZIP_Code, store_id, prodQteGrp_ID, retailer):
    #     response = requests.get(f"{self.base_url}retailer/cfis", params={'zipCode': ZIP_Code, 'storeId': store_id, 'prodQteGrpId': prodQteGrp_ID},
    #                             headers={"Authorization": self.tokens_list.get(retailer)})
    #     assert response.status_code == 200, 'Wrong status code'
    #
    #     response_as_dict = response.json()
    #
