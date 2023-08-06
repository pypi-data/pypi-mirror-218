# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import decimal
import hashlib

import pydantic
from canonical import Price
from canonical import ResourceName


class ExternalCatalogItem(pydantic.BaseModel):
    available: int = 0
    grouping_key: str
    product_name: str
    resource_name: ResourceName | None
    sku: str | None
    features: dict[str, str]
    prices: list[Price] = []
    url: str | None = None
    identifiers: dict[str, str] = {}

    def get_variant_key(self, grouping_key: str, using: set[str], defaults: dict[str, str] | None = None) -> str:
        features = {**(defaults or {}), **self.features}
        h = hashlib.md5()
        h.update(str.encode(grouping_key, 'utf-8'))
        for feature in sorted(using):
            h.update(str.encode(feature, 'utf-8'))
            h.update(str.encode(str.lower(features[feature]), 'utf-8'))
        return h.hexdigest()

    def clone(self):
        return self.parse_obj(copy.deepcopy(self.dict()))

    def __hash__(self):
        return hash(self.sku)

    def __eq__(self, other: 'ExternalCatalogItem'):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sku == other.sku

    class Config:
        json_encoders = {
            decimal.Decimal: str
        }