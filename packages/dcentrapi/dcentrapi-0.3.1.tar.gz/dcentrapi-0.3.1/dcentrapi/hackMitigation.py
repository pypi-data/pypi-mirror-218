import traceback

from dcentrapi.Base import Base, DapiError
from dcentrapi.requests_dappi import requests_get


class HackMitigation(Base):

    def are_addresses_blacklisted(self, addresses: [str]):
        url = self.url + "generic_freeze_signal/are_addresses_blacklisted"
        data = {
            "addresses": addresses,
        }
        response = None
        try:
            response = requests_get(url, params=data, headers=self.headers)
            return response.json()
        except Exception as e:
            return DapiError(response=response.__dict__, exception=f"e: {e}, traceback: {traceback.format_exc()}")
