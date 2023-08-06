import logging
from time import sleep
from pplmyapi.models.package import Package
from pplmyapi.conf import (
    LabelReturnChanel,
    LabelSettingModel,
    ImportStatus,
    LABEL_SERVICES,
)
import requests
import json
import base64
import copy


class RESTActionShipmentBatch:
    url = "https://api.dhl.com/ecs/ppl/myapi2/shipment/batch"

    def keep_or_remove_services(self, package: Package):
        svc = package.package_services

        if svc is None or len(svc) == 0:
            return

        new_svc = []
        for s in svc:
            # validate service code againts LABEL_SERVICES list of enum item
            if s.get_type() in LABEL_SERVICES:
                # remove service from package
                new_svc.append(s)
        package.package_services = new_svc
        return package

    def validate_package(self, package: Package):
        return self.keep_or_remove_services(package)

    def __init__(
        self,
        token: str = None,
        packages: list[Package] = [],
        return_chanel_type: LabelReturnChanel = LabelReturnChanel.HTTP,
        return_chanel_address: str = None,
        return_chanel_format: LabelSettingModel = LabelSettingModel.PDF,
        return_chanel_dpi: int = 300,
        session=None,
    ):
        self.packages = packages
        self.return_chanel_type = return_chanel_type
        self.return_chanel_address = return_chanel_address
        self.return_chanel_format = return_chanel_format
        self.return_chanel_dpi = return_chanel_dpi

        for package in self.packages:
            package = self.validate_package(package)

        if token is None:
            raise Exception("Token is required")

        if session is None and token is not None:
            self.session = requests.Session()
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        else:
            self.session = session

        self.label_settings = {
            "format": return_chanel_format.value,
            "dpi": return_chanel_dpi,
            "completeLabelSettings": {
                "isCompleteLabelRequested": True,
                "pageSize": "A4",
                "position": 1,
            },
        }
        # return chanel
        if return_chanel_type != LabelReturnChanel.HTTP:
            if not return_chanel_address:
                raise Exception("return_chanel_address is required")
            self.label_settings["returnChanel"] = {
                "type": return_chanel_type.value,
                "address": return_chanel_address,
            }

    def get_labels_from_url(self, label_urls):
        # get labels for packages - call api
        labels = []
        for label_url in label_urls:
            # response = self.session.get(label_url)
            # if response.status_code != 200:
            #     raise Exception(f'Error while getting labels: {response.text}')
            # labels.append(base64.b64encode(response.content).decode('utf-8'))
            label = self.get_label_from_url(label_url)
            labels.append(label)
        return labels

    def get_label_from_url(self, url):
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception(f"Error while getting labels: {response.text}")
        return base64.b64encode(response.content).decode("utf-8")

    def control_parcel_status(self, response):
        # check if all parcels have Complete status
        # if not, return None
        # if yes, return list of label URLs
        waiting = False
        if "items" in response:
            for item in response["items"]:
                status = self.parse_control_parcel_status(item)
                # check if all items have Complete status
                if status == ImportStatus.ERROR:
                    continue
                if status == ImportStatus.ACCEPTED:
                    waiting = True
                if status == ImportStatus.INPROCESS:
                    waiting = True
                if status == ImportStatus.COMPLETE:
                    continue
        return waiting

    def parse_control_parcel_status(self, parcel):
        if parcel["importState"] == "Error":
            return ImportStatus.ERROR
        if parcel["importState"] == "Accepted":
            return ImportStatus.ACCEPTED
        if parcel["importState"] == "InProcess":
            return ImportStatus.INPROCESS
        if parcel["importState"] == "Complete":
            return ImportStatus.COMPLETE

    def parse_data(self, response):
        """
        Method used to fetch base64 encoded labels from response
        and return list of packages with their shipmentNumber and labels
        """
        label_urls = None
        if "labelUrls" in response:
            label_urls = response["labelUrls"]
        if "completeLabel" in response:
            if "labelUrls" in response["completeLabel"]:
                label_urls = response["completeLabel"]["labelUrls"]
        if label_urls is None:
            raise Exception("No label URLs found in response")
        labels = self.get_labels_from_url(label_urls)
        print("LABEL URLS", label_urls)
        # iterate over response, get shipmentNumber and label
        for item in response["items"]:
            for package in self.packages:
                if package.reference_id == item["referenceId"]:
                    # found package object for this item in response
                    package.shipment_number = item["shipmentNumber"]
                    package.import_state = self.parse_control_parcel_status(item)
                    # get label for this package
                    package.label_base64 = self.get_label_from_url(item["labelUrl"])
                    # check if it has related parcels
                    if (
                        "relatedItems" in item
                        and package.package_set != None
                        and len(item["relatedItems"])
                        == package.package_set.total_packages - 1
                    ):  # -1 because of base package
                        # deep copy base package
                        base_package = copy.deepcopy(package)
                        base_package.payment_info = None
                        base_package.package_set = None
                        base_package.insurance = None
                        # sort related items by shipmentNumber (because they are not sorted in response.........)
                        related_items_correct_order = sorted(
                            item["relatedItems"], key=lambda d: int(d["shipmentNumber"])
                        )
                        for related_item in related_items_correct_order:
                            related_package = copy.deepcopy(base_package)
                            related_package.shipment_number = related_item[
                                "shipmentNumber"
                            ]
                            related_package.import_state = (
                                self.parse_control_parcel_status(related_item)
                            )
                            related_package.label_base64 = self.get_label_from_url(
                                related_item["labelUrl"]
                            )
                            package.package_set.related_packages.append(related_package)

        return {"labels": labels, "packages": self.packages}

    def get_shipments_from_response(self, response_url):
        """
        Get shipments from async response URL
        wait until all shipments are Complete or Error
        and then return main label url, shipment label urls and shipmentNumber for each referenceId
        """
        waiting = True
        response = None
        while waiting:
            response = self.session.get(response_url)
            if response.status_code != 200:
                raise Exception(f"Error while getting shipments: {response.text}")
            response = response.json()
            logging.debug(f"Shipment status: {response}")
            # iterate over response and check if all shipments have Complete status
            # if not, return None
            # if yes, return list of label URLs

            # check if all parcels have Complete status
            # if not, continue waiting but sleep 2 seconds so that we don't spam the API
            waiting = self.control_parcel_status(response)
            if waiting:
                sleep(2)
                continue

        # looks like all items have Complete or Error status
        # get labels and shipmentNumbers
        return self.parse_data(response)

    def post_packages(self):
        """wrapper around requests.post method to PPL api"""
        return self.session.post(
            self.url,
            json={
                "labelSettings": self.label_settings,
                "shipments": [
                    package.to_json()
                    for package in self.packages
                    if package.import_state
                    != ImportStatus.ERROR  # we don't want to import packages with errors again (we would get the same error again)
                ],
            },
        )

    def parse_errors(self, error):
        """parse dictionary of errors and assign them to packages"""
        # ppl api returns errors in this format:
        # "errors": {
        #     "Shipments[1]": [
        #         "Unknown parcel shop code"
        #     ]
        # }
        # we need to parse this and assign errors to packages

        if "errors" in error:
            for key, value in error["errors"].items():
                # key is in format Shipments[1]
                # we need to get the index
                if "Shipments[" not in key:
                    continue
                index = int(key.split("[")[1].split("]")[0])
                self.packages[
                    index
                ].import_state = (
                    ImportStatus.ERROR
                )  # this will help us to filter out packages with errors when recovering from error
                self.packages[index].error = value[0]  # we only take first error

    def send_or_recover(self):
        print(
            "packages",
            [
                package.to_json()
                for package in self.packages
                if package.import_state != ImportStatus.ERROR
            ],
        )

        # call requests.post
        response = self.post_packages()
        if response.status_code != 201:
            print("ERROR", response.status_code, response.text)
            # try to get error message in response
            try:
                error = response.json()
                self.parse_errors(error)
                return None
            except:
                raise Exception(f"Error while posting shipments: {response.text}")
        print("RESPONSE", response)
        return response

    def __call__(self):
        # POST data to the self.url
        # obtain response, get label url from response (Location header)
        # if return_chanel_type == LabelReturnChanel.HTTP:
        #   fetch label url and return base64
        # else:
        #   return response (status)

        # this is a workaround for PPL API bug where it cannot handle batch of packages with some errors in it
        # we need to send packages and if there is an error, we need to recover from it and send packages again
        # (but without packages with errors)
        response = None
        counter = 0
        for i in range(0, 3):
            try:
                response = self.send_or_recover()
                if response is not None:
                    break
            except Exception as e:
                print("EXCEPTION", e)

        # response was success
        # get Location from headers and fetch it
        if not "Location" in response.headers or response.headers["Location"] == "":
            raise Exception(
                f"Error while getting labels: Location header not found in response"
            )

        # get parcels from response
        print(len(self.packages), "packages")
        shipments_with_labels = self.get_shipments_from_response(
            response.headers["Location"]
        )
        print(len(shipments_with_labels["packages"]), "packages2")
        return shipments_with_labels
