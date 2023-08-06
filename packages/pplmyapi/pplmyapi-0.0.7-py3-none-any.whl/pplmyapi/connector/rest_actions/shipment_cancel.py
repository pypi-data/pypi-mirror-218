import logging
from time import sleep
from pplmyapi.models.package import Package
from pplmyapi.conf import (LabelReturnChanel, LabelSettingModel, ImportStatus, LABEL_SERVICES )
import requests
import json
import base64

class RESTActionShipmentCancel:
    
    url = 'https://api.dhl.com/ecs/ppl/myapi2/shipment'

    def __init__(self, 
        shipment_number: str,
        token: str = None,
        session = None,
    ):
        if shipment_number is None:
            raise Exception('Shipment number is required')
        self.shipment_number = shipment_number
        self.url += f'/{self.shipment_number}/Cancel'

        if token is None:
            raise Exception('Token is required')

        if session is None and token is not None:
            self.session = requests.Session()
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
        else:
            self.session = session

    def __call__(self):
        # GET data from the self.url
        
        print('url', self.url)

        response = self.session.get(
            self.url,
        )
        if response.status_code != 200:
            # try to get error message in response
            error = None
            try:
                error = response.json()
            except:
                raise Exception(f'Error while canceling shipment: {response.text}')
            
            if 'errors' in error:
                raise Exception(f'Error while canceling shipment: {error["errors"]}')
            else:
                raise Exception(f'Error while canceling shipment: {error}')

        # response was success
        return response.json()