# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import decimal
import itertools
import json
import logging
import os
from typing import Any
from typing import Callable
from typing import Iterable

import pydantic
import yaml

from .externalcatalogitem import ExternalCatalogItem
from .productdefinition import ProductDefinition
from .productvariant import ProductVariant
from .productsupplier import ProductSupplier


REQUIRED_FEATURES: set[str] = {
    'product.brand',
    'product.line',
    'product.model',
}

logger: logging.Logger = logging.getLogger('cbra')


class ProductCatalog(pydantic.BaseModel):
    filename: str | None
    features: dict[str, set[str]] = {}
    products: dict[str, ProductDefinition] = {}
    _variants: dict[str, ProductVariant] = {}
    _identifiers: dict[tuple[str, str], ProductVariant] = {}

    @pydantic.root_validator(pre=False)
    def postprocess_values(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        variants = itertools.chain(*[p.variants.values() for p in values['products'].values()])
        identifiers: dict[tuple[str, str], ProductVariant] = {}
        values.update({
            '_variants': {x.key: x for x in variants},
            '_identifiers': identifiers
        })
        for variant in variants:
            assert isinstance(variant, ProductVariant)
            for kind, name in variant.identifiers.items():
                k = (kind, name)
                assert k not in identifiers
                identifiers[k] = variant
        return values

    @classmethod
    def open(cls, fn: str):
        if os.path.exists(fn):
            logger.info("Loading product catalog from %s", fn)
            return cls.parse_obj({**yaml.safe_load(open(fn).read()), 'filename': fn})
        else:
            return cls(filename=fn)

    def get_features(self) -> list[tuple[str, str]]:
        return list(itertools.chain(*[itertools.product([k], v) for k, v in self.features.items()]))

    def link(self, item: ExternalCatalogItem, supplier: str | None, selectable: set[str], strict: bool = True, defaults: dict[str, str] | None = None) -> None:
        # Check if all features are known.
        logger.info("Linking item (sku: %s, name: %s)", item.sku, item.product_name)
        for attname, value in item.features.items():
            if attname in self.features and value in self.features[attname]:
                continue
            if strict:
                raise ValueError(f"Unknown feature value (product: {item.product_name}, feature: {attname}, value: {value})")
        if item.grouping_key not in self.products:
            if strict:
                raise ValueError(f"Can not link variant to parent (key: {item.grouping_key}, name: {item.product_name})")
            logger.warning("Grouping key not in product catalog (supplier: %s, sku: %s, item: %s)", supplier, item.sku, item.product_name)
            return
        product = self.products[item.grouping_key]
        k = item.get_variant_key(product.grouping_key, product.selectables, defaults=defaults)
        if k not in product.variants:
            if strict:
                raise ValueError('No such variant', item.product_name, item.features)
            logger.warning(
                "Unable to link product: %s (group: %s, features: %s)",
                item.product_name, item.grouping_key,
                ', '.join([f'{k}={v}' for k, v in sorted(item.features.items(), key=lambda x: x[0])])
            )
            return
        variant = product.variants[k]
        if supplier is not None:
            assert item.sku is not None
            ps = ProductSupplier.parse_obj({
                'domain': supplier,
                'resource': item.resource_name,
                'sku': item.sku
            })
            if ps not in variant.suppliers:
                variant.suppliers.append(ps)
                logger.info("Linking items (supplier: %s, sku: %s, product: %s)", supplier, item.sku, variant.product_name)

    def variant(
        self,
        item: ExternalCatalogItem,
        name_template: str | Callable[[ExternalCatalogItem], str] = '{features[product.brand]} {features[product.model]}',
        required: set[str] | None = None,
        optional: set[str] | None = None,
        selectable: set[str] | None = None,
        ignore: set[str] | None = None,
        supplier: str | None = None,
        defaults: dict[str, str] | None = None,
        logger: logging.Logger = logging.getLogger('cbra'),
        allow_create: list[Callable[[dict[str, str]], bool]] | None | bool = None,
    ):
        allow_create = allow_create or []
        defaults = defaults or {}
        optional = optional or set()
        required = required or set()
        ignore = ignore or set()
        selectable = selectable or set()
        if isinstance(allow_create, bool):
            allow_create = [lambda features: True]
        if not any([f(item.features) for f in allow_create]):
            self.link(item, supplier, selectable, defaults=defaults)
            return
        for attname, value in item.features.items():
            if attname in ignore or value == NotImplemented:
                continue
            if attname not in self.features:
                self.features[attname] = set()
            self.features[attname].add(value)

        product = self.get_product(item.grouping_key)
        if product.product_name is None:
            if isinstance(name_template, str):
                product.product_name = name_template.format(features=item.features)
            else:
                product.product_name = name_template(item)
            logger.info("Added product %s (key: %s, item: %s)", product.product_name, product.grouping_key, item.product_name)

        features: set[str] = set([x for x in item.features.keys() if x not in ignore])
        for attname in {*REQUIRED_FEATURES, *required}:
            product.add_required_feature(attname, item.features.get(attname) or defaults[attname])
            if attname in features:
                features.remove(attname)
        for attname in selectable:
            if attname not in item.features:
                continue
            product.add_selectable_feature(attname, item.features.get(attname) or defaults[attname])
            features.remove(attname)
        for attname in optional:
            if attname not in item.features:
                continue
            product.add_optional_feature(attname, item.features[attname])
            features.remove(attname)
        if features:
            raise ValueError(f"Unconsumed features: {','.join([f'{x} ({item.features[x]})' for x in features])}")
        product.features = list(sorted(product.features, key=lambda x: (x.applicable, x.attname)))

        # Add variant.
        variant, created = product.add_variant(item, selectable, optional, supplier=supplier, defaults=defaults)
        if created:
            assert variant.key not in self._variants
            self._variants[variant.key] = variant
            logger.info("Added variant %s (key: %s, variant: %s)", variant.product_name, product.grouping_key, variant.key)
        else:
            if variant.product_name != item.product_name:
                logger.info("Changing product name (old: %s, new: %s, id: %s)", variant.product_name, item.product_name, variant.id)
                variant.product_name = item.product_name
            if  set(variant.identifiers.items()) != set(item.identifiers.items()):
                for k in item.identifiers:
                    value = item.identifiers[k]
                    if k not in variant.identifiers:
                        logger.info("Adding identifier (kind: %s, product: %s, name: %s)", k, variant.product_name, value)
                        variant.identifiers[k] = value
                        continue
                    if variant.identifiers[k] != value:
                        logger.info("Changing identifier (kind: %s, product: %s, old: %s, new: %s)", k, variant.product_name, variant.identifiers[k], value)
                        variant.identifiers[k] = value
                        continue

        variant.identifiers = item.identifiers
        if supplier is not None:
            assert item.sku is not None
            if variant.add_supplier(item, supplier, item.sku):
                logger.info("Linking items (supplier: %s, sku: %s, product: %s)", supplier, item.sku, variant.product_name)

    def get_product(self, grouping_key: str) -> ProductDefinition:
        if grouping_key not in self.products:
            self.products[grouping_key] = ProductDefinition(grouping_key=grouping_key)
        return self.products[grouping_key]

    def dump(
        self,
        commit: bool = False,
        logger: logging.Logger = logging.getLogger('cbra'),
        **kwargs: Any
    ) -> str:
        exclude = kwargs.setdefault('exclude', set())
        exclude.add('_identifiers')
        exclude.add('_variants')
        data = yaml.safe_dump(json.loads(self.json(**kwargs)), default_flow_style=False)
        if commit:
            logger.info("Writing products to %s", self.filename)
            assert self.filename is not None
            with open(self.filename, 'w') as f:
                f.write('---\n')
                f.write(data)
        return data

    def get_variants(self) -> Iterable[tuple[ProductDefinition, ProductVariant]]:
        for product in self.products.values():
            for variant in product.variants.values():
                yield product, variant

    class Config:
        json_encoders: dict[type, Callable[..., Any]] = {
            collections.defaultdict: dict,
            decimal.Decimal: str,
            set: lambda x: list(sorted(x))
        }