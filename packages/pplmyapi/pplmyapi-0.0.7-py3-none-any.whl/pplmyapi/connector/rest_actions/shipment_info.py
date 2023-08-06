import logging
from time import sleep
from pplmyapi.models.package import Package
from pplmyapi.conf import (LabelReturnChanel, LabelSettingModel, ImportStatus, LABEL_SERVICES )
import requests
import json
import base64

class RESTActionShipmentInfo:
    
    url = 'https://api.dhl.com/ecs/ppl/myapi2/shipment'

    def __init__(self, 
        token: str = None,
        shipment_numbers: list[str] = [],
        invoice_numbers: list[str] = [],
        customer_reference_numbers: list[str] = [],
        variable_symbol_numbers: list[str] = [],
        session = None,
    ):
        self.append_url_param(
            'limit',
            '100'
        )
        self.append_url_param(
            'offset',
            '0'
        )

        # append url parameters
        self.shipment_numbers = shipment_numbers
        if len(self.shipment_numbers) > 0:
            self.append_url_param('ShipmentNumbers', ','.join(self.shipment_numbers))
        self.invoice_numbers = invoice_numbers
        if len(self.invoice_numbers) > 0:
            self.append_url_param('InvoiceNumbers', ','.join(self.invoice_numbers))
        self.customer_reference_numbers = customer_reference_numbers
        if len(self.customer_reference_numbers) > 0:
            self.append_url_param('CustomerReferences', ','.join(self.customer_reference_numbers))
        self.variable_symbol_numbers = variable_symbol_numbers
        if len(self.variable_symbol_numbers) > 0:
            self.append_url_param('VariableSymbols', ','.join(self.variable_symbol_numbers))
        
        if token is None:
            raise Exception('Token is required')

        if session is None and token is not None:
            self.session = requests.Session()
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
        else:
            self.session = session

    def append_url_param(self, key, value):
        if len(value) > 0:
            if '?' not in self.url:
                self.url += '?'
            else:
                self.url += '&'
            self.url += f'{key}={value}'

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
                raise Exception(f'Error while getting shipments: {response.text}')
            
            if 'errors' in error:
                raise Exception(f'Error while getting shipments: {error["errors"]}')
            else:
                raise Exception(f'Error while getting shipments: {error}')

        # response was success
        return response.json()