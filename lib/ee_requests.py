import requests


class EERequests:
    @staticmethod
    def get(url: str, params=None, headers=None, cookies=None):
        return EERequests._send(url, params, headers, cookies, None, "GET")

    @staticmethod
    def post(url: str, data=None, headers=None, cookies=None, json=None):
        return EERequests._send(url, data, headers, cookies, json, "POST")

    @staticmethod
    def put(url: str, data=None, headers=None, cookies=None, json=None):
        return EERequests._send(url, data, headers, cookies, json, "PUT")

    @staticmethod
    def delete(url: str, data=None, headers=None, cookies=None, json=None):
        return EERequests._send(url, data, headers, cookies, json, "DELETE")

    @staticmethod
    def _send(url: str, data: dict | None, headers: dict | None, cookies: dict | None, json: dict | None, method: str):

        base_url = "https://ee-api-ssi.staging.inscyth.com"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        if json is None:
            json = {}

        if method == "GET":
            response = requests.get(f"{base_url}{url}", params=data, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(f"{base_url}{url}", data=data, json=json, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(f"{base_url}{url}", data=data, json=json, headers=headers, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(f"{base_url}{url}", data=data, json=json, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Invalid HTTP method: '{method}' was provided. Supported methods are: GET, POST, PUT, DELETE.")

        return response
