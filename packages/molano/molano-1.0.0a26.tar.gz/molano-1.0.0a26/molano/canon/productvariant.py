# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal
import hashlib

import pydantic
from canonical import ResourceName

from .appliedproductfeature import AppliedProductFeature
from .externalcatalogitem import ExternalCatalogItem
from .productsupplier import ProductSupplier
from .productvariantresource import ProductVariantResource


class ProductVariant(pydantic.BaseModel):
    id: int | None = None
    part_id: int | None = None
    grouping_key: str
    product_name: str | None = None
    features: list[AppliedProductFeature] = []
    suppliers: list[ProductSupplier] = []
    identifiers: dict[str, str] = {}
    resources: list[ProductVariantResource] = []

    @property
    def key(self) -> str:
        h = hashlib.md5()
        h.update(str.encode(self.grouping_key, 'utf-8'))
        for feature in sorted(self.features, key=lambda x: x.attname):
            h.update(str.encode(feature.attname, 'utf-8'))
            h.update(str.encode(str.lower(feature.value), 'utf-8'))
        return h.hexdigest()

    def add_resource(self, kind: str, resource_name: ResourceName) -> None:
        resource = ProductVariantResource(
            kind=kind,
            service_name=resource_name.service,
            relname=resource_name.relname
        )
        if resource not in self.resources:
            self.resources.append(resource)

    def add_supplier(self, item: ExternalCatalogItem, supplier: str, sku: str):
        suppliers: dict[str, ProductSupplier] = {x.domain: x for x in self.suppliers}
        ps = ProductSupplier.parse_obj({
            'domain': supplier,
            'sku': sku,
            'resource': item.resource_name
        })
        if ps in self.suppliers:
            return
        if ps.domain in suppliers and suppliers[ps.domain].sku != sku:
            raise ValueError(suppliers[ps.domain].sku, sku)
        self.suppliers.append(ps)

    def add_required_feature(self, attname: str, value: str):
        feature = AppliedProductFeature.required(attname=attname, value=value)
        if feature not in self.features:
            self.features.append(feature)

    def add_selectable_feature(self, attname: str, value: str):
        feature = AppliedProductFeature.selectable(attname=attname, value=value)
        if feature not in self.features:
            self.features.append(feature)

    def has_feature(self, name: str) -> bool:
        return any([feature.attname == name for feature in self.features])

    def get_feature(self, name: str) -> str:
        value = None
        for feature in self.features:
            if feature.attname != name:
                continue
            value = feature.value
            break
        if value is None:
            raise LookupError(name)
        return value

    def get_identifier(self, kind: str) -> str | None:
        return self.identifiers.get(kind)

    def get_supplier_sku(self, supplier: str) -> str | None:
        return self.suppliers.get(supplier)

    def get_resource(self, kind: str, service_name: str) -> ResourceName:
        for ref in self.resources:
            if ref.kind != kind or ref.service_name != service_name:
                continue
            resource = ref.resource_name
            break
        else:
            resource = None
        if resource is None:
            raise LookupError
        return resource

    def has_resource(self, kind: str, service_name: str) -> bool:
        return any([
            kind == x.kind and service_name == x.service_name
            for x in self.resources
        ])

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other: 'ProductVariant'):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.key == other.key

    class Config:
        json_encoders = {
            decimal.Decimal: str
        }