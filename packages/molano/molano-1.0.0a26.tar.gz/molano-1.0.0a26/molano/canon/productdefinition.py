# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal

import pydantic

from .appliedproductfeature import AppliedProductFeature
from .externalcatalogitem import ExternalCatalogItem
from .productvariant import ProductVariant


class ProductDefinition(pydantic.BaseModel):
    id: int | None = None
    grouping_key: str
    product_name: str | None = None
    features: list[AppliedProductFeature] = []
    variants: dict[str, ProductVariant] = {}

    @property
    def selectables(self) -> set[str]:
        return {x.attname for x in self.features if x.applicable == 'SEL'}

    def add_variant(
        self,
        dto: ExternalCatalogItem,
        selectable: set[str],
        optional: set[str],
        supplier: str | None = None,
        defaults: dict[str, str] | None = None
    ) -> tuple[ProductVariant,  bool]:
        defaults = defaults or {}
        variant = ProductVariant(grouping_key=self.grouping_key, product_name=dto.product_name)
        for attname in selectable:
            variant.add_required_feature(attname, dto.features.get(attname) or defaults[attname])
        for attname in optional:
            if attname not in dto.features:
                continue
            variant.add_required_feature(attname, dto.features[attname])
        if variant.key not in self.variants:
            created = True
            self.variants[variant.key] = variant
        else:
            created = False
            variant = self.variants[variant.key]
        if supplier:
            assert dto.sku is not None
            variant.add_supplier(dto, supplier, dto.sku)
        return variant, created

    def add_required_feature(self, attname: str, value: str):
        if value == NotImplemented: return
        feature = AppliedProductFeature.required(attname=attname, value=value)
        if feature not in self.features:
            self.features.append(feature)

    def add_optional_feature(self, attname: str, value: str):
        if value == NotImplemented: return
        feature = AppliedProductFeature.optional(attname=attname, value=value)
        if feature not in self.features:
            self.features.append(feature)

    def add_selectable_feature(self, attname: str, value: str):
        if value == NotImplemented: return
        feature = AppliedProductFeature.selectable(attname=attname, value=value)
        if feature not in self.features:
            self.features.append(feature)

    def has_feature(self, name: str) -> bool:
        return any([feature.attname == name for feature in self.features])

    def get_feature(self, name: str) -> str | None:
        value = None
        for feature in self.features:
            if feature.attname != name or feature.applicable != 'REQ':
                continue
            value = feature.value
            break
        return value

    def get_selectable(self, name: str) -> set[str]:
        values: set[str] = set()
        for feature in self.features:
            if feature.attname != name or feature.applicable != 'SEL':
                continue
            values.add(feature.value)
            break
        return values

    def __hash__(self):
        return hash(self.grouping_key)

    def __eq__(self, other: 'ProductDefinition'):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.grouping_key == other.grouping_key

    class Config:
        json_encoders = {
            decimal.Decimal: str
        }