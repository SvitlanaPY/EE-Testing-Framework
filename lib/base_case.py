from json.decoder import JSONDecodeError

import requests
from requests import Response


# Response - це class в модулі requests


class BaseCase:
    # base_url = "https://ee-api-ssi.qa.inscyth.com/"
    base_url = "https://ee-api-ssi.staging.inscyth.com/"
    tokens_list = {}

    def setup_class(self):
        retailers = [
            'bjs.staging.myprojectestimates.com',
            'cabinetstogo.staging.myprojectestimates.com',
            'cliqstudios.staging.myprojectestimates.com',
            'flooranddecor.staging.myprojectestimates.com',
            'flooringliquidators.staging.myprojectestimates.com',
            'homeoutlet.staging.myprojectestimates.com',
            'lowes.staging.myprojectestimates.com',
            'lowesime.staging.myprojectestimates.com',
            'thertastore.staging.myprojectestimates.com',
            'wholesalecabinets.staging.myprojectestimates.com',
            'fd.staging.inscyth.com'
        ]
        # 'bjs.staging.inscyth.com',
        # 'cabinetstogo.staging.inscyth.com',
        # 'cliqstudios.staging.inscyth.com',
        # 'flooringliquidators.staging.inscyth.com',
        # 'homeoutlet.staging.inscyth.com',
        # 'lowes.staging.inscyth.com',
        # 'lowesime.staging.inscyth.com',
        # 'thertastore.staging.inscyth.com',
        # 'wholesalecabinets.staging.inscyth.com'

        # retailers = [
        #     'bjs.qa.myprojectestimates.com',
        #     'cabinetstogo.qa.myprojectestimates.com',
        #     'cliqstudios.qa.myprojectestimates.com',
        #     'flooranddecor.qa.myprojectestimates.com',
        #     'flooringliquidators.qa.myprojectestimates.com',
        #     'homeoutlet.qa.myprojectestimates.com',
        #     'lowes.qa.myprojectestimates.com',
        #     'lowesime.qa.myprojectestimates.com',
        #     'lowesime.qa.myprojectestimates.com',
        #     'thertastore.qa.myprojectestimates.com',
        #     'wholesalecabinets.qa.myprojectestimates.com',
        #     'fd.qa.inscyth.com'
        # ]

        for item in retailers:
            response = requests.get(f"{self.base_url}lookup/retailer", params={'clientHost': item})

            assert response.status_code == 200, 'Wrong status code'

            assert "token" in response.json(), "There is no Bearer token in the response."
            token = response.json().get("token")

            assert "retailerCode" in response.json(), "There is no retailerCode in the response."
            raw_retailerCode = response.json().get("retailerCode")
            clean_retailerCode = raw_retailerCode.lower()

            self.tokens_list.update({clean_retailerCode: token})
