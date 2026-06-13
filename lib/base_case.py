from json.decoder import JSONDecodeError

import requests
from requests import Response
# Response - це class в модулі requests

class BaseCase:
    base_url = "https://ee-api-ssi.staging.inscyth.com/"
    tokens_list = {}

    def setup_class(self):
        # retailer = {'clientHost': 'fd.staging.inscyth.com'}
        #
        # response = requests.get("https://ee-api-ssi.staging.inscyth.com/lookup/retailer", params = retailer)
        # assert response.status_code == 200, 'Wrong status code'
        #
        # assert "token" in response.json(), "There is no Bearer token in the response_"
        # self.token = response.json().get("token")

        retailers = ['fd.staging.inscyth.com', 'homeoutlet.staging.inscyth.com', 'lowes.staging.inscyth.com']

        for item in retailers:
            response = requests.get(f"{self.base_url}lookup/retailer", params={'clientHost': item})

            assert response.status_code == 200, 'Wrong status code'

            assert "token" in response.json(), "There is no Bearer token in the response_"
            token = response.json().get("token")

            assert "retailerCode" in response.json(), "There is no retailerCode in the response_"
            raw_retailerCode = response.json().get("retailerCode")
            clean_retailerCode = raw_retailerCode.lower()

            self.tokens_list.update({clean_retailerCode: token})

