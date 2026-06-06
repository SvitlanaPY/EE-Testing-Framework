from json.decoder import JSONDecodeError

import requests
from requests import Response
# Response - це class в модулі requests

class BaseCase:
    def setup_class(self):
        retailer = {'clientHost': 'fd.staging.inscyth.com'}

        response_ = requests.get("https://ee-api-ssi.staging.inscyth.com/lookup/retailer", params=retailer)
        assert response_.status_code == 200, 'Wrong status code'

        assert "token" in response_.json(), "There is no Bearer token in the response_"
        self.token = response_.json().get("token")

        