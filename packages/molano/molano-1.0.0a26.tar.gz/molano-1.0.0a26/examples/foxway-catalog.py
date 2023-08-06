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
from typing import Any

from headless.ext.foxway import FoxwayClient

from molano.canon import ExternalCatalog
from molano.canon import ExternalCatalogItem
from molano.canon import ProductCatalog
from molano.lib import foxway
from molano.__main__ import application


logger: logging.Logger = logging.getLogger('cbra')


def postprocess_laptop(item: ExternalCatalogItem):
    item.product_name = '{item.product_name} {item.features[computer.keyboard.layout]}'.format(item=item)
    if item.features.get('appearance.color'):
        item.product_name = '{item.product_name} {item.features[appearance.color]}'.format(item=item)
    if item.features['quality.grade.apparent'] not in {None, 'Any', 'N/A'}:
        item.product_name = '{item.product_name} {item.features[quality.grade.apparent]}'.format(item=item)
    return item


def postprocess_samsung(item: ExternalCatalogItem):
    if item.features.get('product.brand') != 'Samsung':
        return
    if not item.features.get('computer.storage.primary'):
        return
    item.product_name = '{item.product_name} {item.features[quality.grade.apparent]}'.format(item=item)
    item.product_name = '{item.features[product.brand]} {item.features[product.model]}'.format(item=item)
    item.product_name = '{item.product_name} {item.features[computer.storage.primary]} {item.features[appearance.color]}'.format(item=item)
    if item.features.get('computer.networking.cellular') in {'4G', '5G'}:
        item.product_name = '{item.product_name} {item.features[computer.networking.cellular]}'.format(item=item)
    if item.features.get('cellular.sim.slots') == '2':
        item.product_name = f'{item.product_name} Dual Sim'
    item.product_name = '{item.product_name} {item.features[quality.grade.apparent]}'.format(item=item)


CATEGORIES: dict[str, dict[str, Any]] = {
    'mobile.samsung': {
        'when': lambda x: all([ # type: ignore
            x.features['product.brand'] == 'Samsung', # type: ignore
            x.features['product.line'] == 'Galaxy', # type: ignore
            not x.product_name.startswith('Samsung Galaxy A3'), # type: ignore
            not x.product_name.startswith('Samsung Galaxy A5'), # type: ignore
            #not x.product_name.startswith('Samsung Galaxy A6'), # type: ignore
            #not x.product_name.startswith('Samsung Galaxy A7'), # type: ignore
        ]),
        'postprocess': postprocess_samsung,
        'defaults': {
            'cellular.sim.slots': '1',
            'computer.networking.cellular': 'Unknown',
            'product.release.generation': 'N/A',
            'product.release.market': 'Worldwide',
        },
        'color_mapping': {
            'Galaxy S23': {
                'Beige': 'Cream',
                'Green': None,
                'Black': 'Phantom Black',
                'Purple': 'Lavender',
            },
            'Galaxy S23 Plus': {
                'Beige': 'Cream',
                'Black': 'Phantom Black',
                'Green': None,
                'Purple': 'Lavender',
            },
            'Galaxy S23 Ultra': {
                'Beige': 'Cream',
                'Black': 'Phantom Black',
                'Green': None,
                'Grey': 'Graphite',
                'Purple': 'Lavender',
            },
            'Galaxy S22': {
                'Black': 'Phantom Black',
                'White': 'Phantom White',
                'Pink': 'Pink Gold',
                'Grey': 'Graphite',
                'Green': 'Green',
                'Purple': 'Bora Purple',
            },
            'Galaxy S22 Plus': {
                'Black': 'Phantom Black',
                'White': 'Phantom White',
                'Pink': 'Pink Gold',
                'Green': 'Green',
                'Grey': 'Graphite',
                'Yellow': 'Cream',
            },
            'Galaxy S22 Ultra': {
                'Black': 'Phantom Black',
                'White': 'Phantom White',
                'Green': 'Green',
                'Red': None,
                'Blue': 'Sky Blue',
                'Grey': 'Graphite',
                'Purple': NotImplemented
            },
            'Galaxy S9': {
                'Black': 'Midnight Black',
                'Blue': 'Coral Blue',
                'Purple': 'Lilac Purple',
                'Grey': 'Titanium Gray'
            },
            'Galaxy S9 Plus': {
                'Black': 'Midnight Black',
                'Blue': 'Coral Blue',
                'Purple': 'Lilac Purple',
                'Grey': 'Titanium Gray'
            },
            'Galaxy S8': {
                'Blue': 'Coral Blue',
                'Pink': 'Rose Pink',
                'Silver': 'Arctic Silver',
                'Black': 'Midnight Black',
                'Grey': 'Orchid Grey',
            },
            'Galaxy S8 Plus': {
                'Blue': 'Coral Blue',
                'Pink': 'Rose Pink',
                'Silver': 'Arctic Silver',
                'Black': 'Midnight Black',
                'Grey': 'Orchid Grey',
            },
            'Galaxy S7': {
                'White': 'White Pearl',
                'Black': 'Black Onyx',
                'Gold': 'Gold Platinum'
            },
            'Galaxy Z Fold 4': {
                'Black': 'Phantom Black',
                'Beige': None,
                'Grey': 'Graygreen',
            },
            'Galaxy Z Fold 3': {
                'Black': 'Phantom Black',
                'Green': 'Phantom Green',
                'Silver': 'Phantom Silver',
            },
            'Galaxy Z Fold 2': {
                'Bronze': 'Mystic Bronze',
                'Black': 'Mystic Black',
                'Grey': NotImplemented
            },
            'Galaxy Z Flip 4': {
                'Blue': 'Blue',
                'Purple': 'Bora Purple',
                'Rose Gold': 'Pink Gold',
                'Grey': 'Graphite',
                'Gold': NotImplemented,
                'White': NotImplemented
            },
            'Galaxy Z Flip 3': {
                'Pink'  : NotImplemented,
                'Beige': 'Cream',
                'Black': 'Phantom Black',
                'Purple': 'Lavender',
                'Green': 'Green',
                'Grey': 'Grey',
            },
        },
        'categories': [('1', '1')],
        'required': {
            'product.brand',
            'product.kind',
            'product.line',
            'product.model',
            'product.release.generation'
        },
        'selectable': {
            'appearance.color',
            'cellular.sim.slots',
            'computer.networking.cellular',
            'computer.storage.primary',
            'quality.functional.state',
            'quality.grade.apparent',
            'quality.packaging.state',
            'product.variant',
        }
    },
    'mobile': {
        'when': lambda x: x.features['product.brand'] == 'Apple', # type: ignore
        'defaults': {
            'product.release.generation': 'N/A',
            'product.release.market': 'Worldwide',
        },
        'categories': [('1', '1')],
        'required': {
            'product.brand',
            'product.kind',
            'product.line',
            'product.model',
            'product.release.generation'
        },
        'selectable': {
            'appearance.color',
            'computer.storage.primary',
            'quality.functional.state',
            'quality.grade.apparent',
            'quality.packaging.state',
            'product.release.market',
        }
    },
    'laptops': {
        'categories': [('11', '12')],
        'name_template': '{features[product.brand]} {features[product.model]} {features[computer.display.diameter]}"',
        'postprocess': postprocess_laptop,
        'color_mapping': {
            'IdeaPad 3 15IIL05': {'Black': 'Black', 'Grey': 'Arctic Gray'},
            'IdeaPad S145-15IWL': {'Black': 'Black', 'Grey': 'Platinum Grey'},
            'IdeaPad C340-14IML': {'Black': 'Black'},
            'IdeaPad Y700-15ISK': {'Black': 'Black'},
            'Legion 5 15IMH05H': {'Black': 'Black'},
            'ThinkPad X270': {'Black': 'Black'},
            'ThinkPad E590': {'Black': 'Black'},
            'ThinkPad L13': {'Black': 'Black'},
            'ThinkPad P51s': {'Black': 'Black'},
            'ThinkPad P52': {'Black': 'Black'},
            'ThinkPad T14': {'Black': 'Black'},
            'ThinkPad T470': {'Black': 'Black'},
            'ThinkPad T470': {'Black': 'Black'},
            'ThinkPad T490': {'Black': 'Black'},
            'ThinkPad T490s': {'Black': 'Black'},
            'ThinkPad T495': {'Black': 'Black'},
            'ThinkPad T580': {'Black': 'Black'},
            'ThinkPad X1 Carbon': {'Black': 'Black'},
            'Yoga 910-13IKB': {'Black': 'Black'},
            'Yoga Slim 7 14ARE05': {
                'Black': 'Black',
                'Grey': 'Slate Grey',
            },
        },
        'defaults': {
            'computer.os.coa': 'N/A',
            'product.release.generation': 'N/A',
            #'product.release.market': 'Worldwide',
        },
        'required': {
            'computer.display.diameter',
            'product.release.generation',
        },
        'optional': {
            'computer.display.touch',
        },
        'selectable': {
            'appearance.color',
            'computer.cpu.integrated',
            'computer.display.resolution',
            'computer.gpu.integrated',
            'computer.keyboard.layout',
            'computer.os.coa',
            'computer.ram',
            'computer.storage',
            'electronic.battery.health',
            'quality.functional.state',
            'quality.grade.apparent',
            'quality.packaging.state'
        },
    }
}

parser = argparse.ArgumentParser("Imports products from the specified source.")
parser.add_argument('-p', action='append', dest='presets')
parser.add_argument('-c', dest='catalog')
parser.add_argument('--commit', action='store_true', dest='commit')
parser.add_argument('--create', action='store_true', dest='allow_create')
parser.add_argument('--features', action='store_true', dest='show_features')


async def main():
    args = parser.parse_args()
    products = ProductCatalog.open(args.catalog)
    logger.info("Importing Foxway products")
    async with FoxwayClient() as client:
        for preset, params in CATEGORIES.items():
            if args.presets and preset not in args.presets:
                logger.info("Skipping preset %s", preset)
                continue
            logger.info("Fetching products for preset %s", preset)
            fn = 'var/catalogs/foxway_{preset}.yml'.format(preset=str.replace(preset, '.', '_'))
            catalog = ExternalCatalog.open(fn, supplier='foxway.shop')
            await foxway.catalog(
                client,
                logger,
                catalog=catalog,
                products=products,
                supplier=catalog.supplier,
                allow_create=args.allow_create,
                **params
            )
            if args.commit:
                catalog.dump(commit=True)
            if args.show_features:
                print(catalog.dump(commit=False, include={'features'}))

    if args.commit:
        if input("Type 'yes' to commit: ") == 'yes':
            products.dump(commit=True)
        raise SystemExit


if __name__ == '__main__':
    asyncio.run(application.run(main))