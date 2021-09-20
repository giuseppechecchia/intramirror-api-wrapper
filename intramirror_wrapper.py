#!/usr/bin/python
###############################################################################
# Copyleft (K) 2020-2022
# Developer: Giuseppe Checchia @eldoleo (<https://github.com/giuseppechecchia>)
###############################################################################

import requests
import json

class IntramirrorApi():

    def __init__(self, store_id, products=None):

        self.url = "http://api.intramirror.com"
        self.stage_url = "http://sha.staging.api.intramirror.com"

        self.store_id = store_id
        self.v = "1.0"

        self.empty_headers = {}
        self.headers = {
            'Content-Type': 'application/json'
        }

        if products:
            self.payload = self.loadProducts(products)
        else:
            self.payload = None

        super(IntramirrorApi, self).__init__()

    def loadProducts(self, products):

        mandatory_fields = [
            'sku',
            'season_code',
            'retail_price',
            'product_description',
            'cover_img',
            'color_code',
            'category_l1',
            'category_l2',
            'category_l3',
            'brand_id',
            'brand',
            'boutique_id'
        ]

        if isinstance(products, list):
            if len(products) == 0:
                raise Exception("the list cannot be empty")
            for x in products:
                c = 0
                for k in x.keys():
                    if k in mandatory_fields:
                        c += 1
                if int(c) != len(mandatory_fields):
                    raise Exception(
                        "you must have all mandatory fields in json")
        else:
            raise Exception("products must be a list of dict")

        return products

    def createProducts(self, products=None):

        if products:
            payload = self.payload = self.loadProducts(products)
        else:
            payload = json.dumps(self.payload)

        if len(payload) == 0:
            raise Exception("you must load your products before")

        url = \
            f"{self.url}/createProduct?StoreID={self.store_id}&Version={self.v}"

        response = \
            requests.request("POST", url, headers=self.headers, data=payload)

        if response.status_code != 200:
            raise Exception("something goes wrong during the http call")

        if response.json():
            if response.json()['ResponseStatus'] == '1000':
                return True
            else:
                return False
        else:
            return False

    def updateStocks(self, stocks):

        base_fields = ['boutique_id', 'size', 'stock', 'barcode']
        payloads = list()
        append_payloads = payloads.append

        url = \
            f"{self.url}/updateSKUStock?StoreID={self.store_id}&Version={self.v}"

        if isinstance(stocks, list):
            if len(stocks) == 0:
                raise Exception("the list cannot be empty")
            for x in stocks:
                c = 0
                if 'sku' in x.keys():
                    for k in x['sku']:
                        for field in k.keys():
                            if field in base_fields:
                                c += 1
                    if int(c) != len(base_fields):
                        raise Exception(
                            "you must have all mandatory fields in json")
                    else:
                        append_payloads(x)
                else:
                    raise Exception("sku field is mandatory")
        else:
            raise Exception("stocks must be a list of dict")

        for el in payloads:
            response = \
                requests.request("POST", url, headers=self.headers, data=el)

            if response.status_code != 200:
                raise Exception("something goes wrong during the http call")

            if response.json():
                if response.json()['ResponseStatus'] == '1000':
                    pass
                else:
                    raise Exception(f"error {response.json()['ResponseStatus']}")
            else:
                raise Exception("Something goes wrong")

        return True

    def getOrders(
        self,
        start_created,
        end_created,
        offset=0,
        limit=50
    ):

        url = \
            f"{self.url}/getOrderByDate?StoreID={self.store_id}&Version=1.0&start_created={start_created}&end_created={end_created}&offset=0&limit=50"

        response = \
            requests.request("POST", url, headers=self.headers)

        if response:
            return True
        else:
            raise Exception("Something goes wrong")
