# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import argparse
import asyncio
import logging

import base36
import cbra.core as cbra
from cbra.ext.picqer import PicqerClient
from cbra.ext.picqer import DefaultPicqerClient
from cbra.types import IPolymorphicRepository
from headless.ext.picqer import v1

from molano.canon import ProductCatalog
from molano.canon import ProductDefinition
from molano.canon import ProductVariant
from molano.__main__ import application


logger: logging.Logger = logging.getLogger('cbra')
parser = argparse.ArgumentParser("Assigns identifiers to the product catalog")
parser.add_argument('catalog')
parser.add_argument('--force', action='store_true', dest='force_create')
parser.add_argument('--link', action='store_true')


PICQER_PART_ID_FIELD: int = 3963

PICQER_FIELD_MAPPING: dict[str, int] = {
    'appearance.color'          : 2690,
    'computer.storage.primary'  : 2609,
    'quality.grade.apparent'    : 2605,
    'product.model'             : 2608,
    'product.variant'           : 3990,
    'product.release.generation': 3993,
    'cellular.sim.slots'        : 3992
}

PICQER_DEFAULTS: dict[int, str] = {
    2604: 'ABC'
}

PICQER_SUPPLIER_SKU_FIELDS: dict[str, int] = {
    'foxway.shop': 3991
}

IDENTIFIERS: list[str] = [
    'v1.molano.nl/sku',
    'v2.molano.nl/sku',
    'v3.molano.nl/sku'
]


def create_sku(number: int) -> str:
    return str.upper(base36.dumps(number)) # type: ignore


async def create_product(picqer: PicqerClient, catalog: ProductCatalog, product: ProductDefinition, variant: ProductVariant):
    return await picqer.create(v1.Product, {
        'name': variant.product_name,
        'productcode': variant.identifiers['v3.molano.nl/sku'],
        'price': '0.0',
        'productfields': [
            {
                'idproductfield': PICQER_PART_ID_FIELD,
                'value': variant.part_id
            },
            *[
                {
                    'idproductfield': idfield,
                    'value': (product.get_feature(feature) or variant.get_feature(feature))
                }
                for feature, idfield in PICQER_FIELD_MAPPING.items()
                if feature in catalog.features and all([
                    product.has_feature(feature),
                    variant.has_feature(feature),
                ])
            ],
            *[
                {'idproductfield': idfield, 'value': value}
                for idfield, value in PICQER_DEFAULTS.items()
            ],
            *[
                {'idproductfield': idfield, 'value': variant.get_supplier_sku(supplier)}
                for supplier, idfield in PICQER_SUPPLIER_SKU_FIELDS.items()
                if variant.get_supplier_sku(supplier)
            ]
        ]
    })


class Abort(Exception):
    pass


async def manual_link(picqer: PicqerClient, catalog: ProductCatalog, products: v1.ProductCatalog, product: ProductDefinition, variant: ProductVariant, skip_manual: bool, force_create: bool):
    if skip_manual:
        return
    if force_create:
        action = 'c'
    else:
        action = str.lower(input(f"Unable to link product: {variant.product_name}. (C)reate, (M)anual, (S)kip or (A)bort: ") or '')
    if action == 's':
        return
    elif action == 'm':
        dto = products.get_by_sku(input("Enter the SKU: "))
        if dto is None:
            print("SKU does not exist")
        return
    elif action == 'c':
        logger.info("Creating product %s", variant.product_name)
        dto = await create_product(picqer, catalog, product, variant)
        variant.add_resource('Part', dto.resource_name)
    elif action == 'a':
        raise Abort
    else:
        return


async def link_picqer(client: PicqerClient, catalog: ProductCatalog, args: argparse.Namespace):
    products = v1.ProductCatalog(client)
    await products.retrieve()
    skip_manual = False
    for product, variant in catalog.get_variants():
        if variant.has_feature('product.release.market')\
        and variant.get_feature('product.release.market') in {'Japan', 'China'}:
            continue
        if variant.has_resource('Part', 'molano.picqer.com'):
            continue
        matches: list[v1.Product | None] = []
        for kind in IDENTIFIERS:
            identifier = variant.get_identifier(kind)
            if not identifier:
                continue
            matches.append(products.get_by_sku(identifier))
        matches = list(filter(bool, matches))
        if not any(matches):
            logger.debug(
                "No matches on %s (id: %s, name: %s)",
                ', '.join(variant.identifiers.values()),
                variant.part_id, variant.product_name
            )
            try:
                await manual_link(client, catalog, products, product, variant, skip_manual=skip_manual, force_create=args.force_create)
            except Abort:
                skip_manual = True
                continue
            continue
        if len({x.idproduct for x in matches if x}) > 1:
            logger.warning("Multiple products found for %s", variant.product_name)
            for match in matches:
                assert match is not None
                logger.warning("Found %s (sku: %s)", match.name, match.productcode)
            continue
        assert isinstance(matches[0], v1.Product)
        logger.info("Matched variant to product (id: %s, picqer: %s)", variant.part_id, matches[0].idproduct)
        variant.add_resource('Part', matches[0].resource_name)
    catalog.dump(commit=True)

async def main(
    repo: IPolymorphicRepository = cbra.instance('PolymorphicRepository'),
    picqer: PicqerClient = DefaultPicqerClient,
):
    args = parser.parse_args()
    catalog = ProductCatalog.open(args.catalog)
    logger.info("Importing catalog")
    unassigned: list[ProductDefinition | ProductVariant] = []
    identifiers: list[int] = []
    n = 0
    for product in catalog.products.values():
        if product.id is None:
            n += 1
            unassigned.append(product)
        for variant in product.variants.values():
            if variant.part_id is None:
                n += 1
            if variant.id is None:
                n += 1
            if not variant.identifiers.get('v3.molano.nl/sku'):
                n += 1
            if variant.id is None or variant.part_id is None or not variant.identifiers.get('v3.molano.nl/sku'):
                unassigned.append(variant)

    logger.info("Assigning %s identifiers", n)
    identifiers = await repo.allocate_many('Orderable', n)
    for obj in unassigned:
        if obj.id is None:
            obj.id = identifiers.pop()
        if isinstance(obj, ProductVariant):
            if obj.part_id is None:
                obj.part_id = identifiers.pop()
            if not obj.identifiers.get('v3.molano.nl/sku'):
                obj.identifiers['v3.molano.nl/sku'] = create_sku(identifiers.pop())
        
    catalog.dump(commit=True)
    if args.link:
        async with picqer:
            await link_picqer(picqer, catalog, args)


if __name__ == '__main__':
    asyncio.run(application.run(main))