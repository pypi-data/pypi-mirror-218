# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
import re
from typing import Any
from typing import Callable
from typing import AsyncIterable

from headless.types import IClient
from headless.ext.foxway.v1 import PricelistProduct

from molano.canon import ExternalCatalog
from molano.canon import ExternalCatalogItem
from molano.canon import ProductCatalog
from molano.lib.sku import v5


FEATURE_MAPPING: dict[str, str] = {
    'Appearance'            : 'quality.grade.apparent',
    'Battery status'        : 'electronic.battery.health',
    'Brand'                 : 'marketing.brand',
    'Boxed'                 : 'quality.packaging.state',
    'Functionality'         : 'quality.functional.state',
    'Color'                 : 'appearance.color',
    'Cloud Lock'            : 'network.locked',
    'CPU desktops'          : 'computer.cpu',
    'CPU Laptops'           : 'computer.cpu.integrated',
    'GPU desktops'          : 'computer.gpu',
    'GPU laptops'           : 'computer.gpu.integrated',
    'COA'                   : 'computer.os.coa',
    'Drive'                 : 'computer.storage',
    'Keyboard'              : 'computer.keyboard.layout',
    'RAM'                   : 'computer.ram',
    'LCD Graphics array'    : 'computer.display.resolution',
    'Additional Info'       : 'product.remarks.additional',
    'Form factor'           : 'xx'
}

FEATURE_VALUES: dict[str, dict[str, str]] = {
    'molano.nl/grade': {
        'Grade A+'  : 'A+',
        'Grade A'   : 'A',
        'Grade B+'  : 'B+',
        'Grade B'   : 'B',
        'Grade C+'  : 'C+',
        'Grade C'   : 'C',
    }
}

IGNORED_DIMENSIONS: set[str] = {
    'Cloud Lock',
}

IGNORED_KEYBOARD: set[str] = {
    'SCA', 'CHE', 'DEU', 'SWE/FIN', 'DNK', 'SVK', 'CZE',
    'Missing Keyboard', 'ARABIC', 'KOR', 'RUS', 'NOR'
}

IGNORED_PACKAGING: set[str] = {
    'Original Box',
    'UK Original Box',
    'US Original Box',
    'Damaged Box',
    'Incomplete Box'
}

IGNORED_DRIVE: set[str] = {
    'faulty drive',
    'missing drive'
}

IGNORED_BATTERY: set[str] = {
    'physical battery issue (damaged/swollen)',
    'Untested',
    'Worn Battery',
    'Missing Battery',
}

ITEM_GROUP_BRAND_PATTERNS: dict[str, re.Pattern[str]] = {
    '1' : re.compile('^.*(Apple|Samsung).*$'),
    '12': re.compile(r'^.*(Acer|Asus|Apple|Dell|HP|Lenovo|Microsoft|Samsung|Toshiba).*$'),
}

ITEM_GROUP_NAME_EXTRACTORS: dict[str, dict[str, list[tuple[re.Pattern[str], str | None, dict[str, Any]]]]] = {
    '1': {
        '*': [
            (re.compile(r'.*\s([0-9]+)(GB|TB).*'), None, {
                'computer.storage.primary': '{0}{1}'
            }),
            (re.compile(r'Apple\s(.*)\s([0-9]+(GB|TB))'), None, {
                'product.brand': 'Apple',
                'product.line': 'iPhone',
                'product.kind': 'Smartphone',
                'product.model': 1,
                'computer.storage.primary': 2
            }),
            (re.compile(r'^Samsung.*$'), None, {'product.kind': 'Smartphone', 'product.brand': 'Samsung'}),
            (re.compile(r'^Samsung\sGalaxy.*$'), None, {'product.line': 'Galaxy'}),
            (re.compile(r'^Samsung\sWave\s([3Y])\s(S[0-9]+)(?:\sDS)?$'), None, {'product.line': 'Wave', 'product.model': 'Wave {0}', 'product.variant': 2}),
            (re.compile(r'^Samsung\sOmnia\s(W).*(i[0-9]+)(?:\sDS)?$'), None, {'product.line': 'Omnia', 'product.model': 'Omnia {0}', 'product.variant': 2}),
            (re.compile(r'^Samsung\sMonte.*(S[0-9]+)(?:\sDS)?$'), None, {'product.line': 'Monte', 'product.model': 'Monte {0}', 'product.variant': 1}),
            (re.compile(r'^Samsung\sGalaxy\s((A|S|Z)[0-9a-z]+(?:\sPlus)?).*$'), None, {
                'product.model': 'Galaxy {0}'
            }),
            (re.compile(r'^Samsung\sGalaxy\sFold\s([0-9]+GB).*(F[0-9A-Z]+)$'), None, {'product.model': 'Galaxy Fold', 'product.variant': 2}),
            (re.compile(r'^Samsung\sGalaxy\sFold\s([0-9]+)\s.*'), None, {'product.model': 'Galaxy Fold {0}'}),
            (re.compile(r'^Samsung\sGalaxy\s(J7\sPrime|M[0-9]+|Note\s[0-9]{1,2}|S\sIII\sMini|Trend\s[0-9]+|Trend|Xcover\sPro|Xcover\s3\sValue\sEdition|Xcover\s[0-9s]|Young\s[0-9]|Z\sFlip\s[0-9]|Z\sFlip|Z\sFold\s[0-9]+|Z\sFold).*\s([iFGMNS][0-9A-Z]+)(?:\sDS)?$'), None, {
                'product.model': 'Galaxy {0}',
                'product.variant': 2
            }),
            (re.compile(r'^Samsung\sGalaxy\s(J[34567]).*\s(J[0-9A-Z]+)(?:\sDS)?$'), None, {'product.model': 'Galaxy {0}', 'product.variant': 2}),
            (re.compile(r'^Samsung.*\sJ510FN(?:\sDS)?$'), None, {'computer.storage.primary': '16GB'}),
            (re.compile(r'^Samsung.*\sJ530F(?:\sDS)?$'), None, {'computer.storage.primary': '10GB'}),
            (re.compile(r'^Samsung.*\sJ500FN(?:\sDS)?$'), None, {'computer.storage.primary': '8GB'}),
            (re.compile(r'^Samsung.*\sG610F(?:\sDS)?$'), None, {'computer.storage.primary': '64GB'}),
            (re.compile(r'^Samsung.*\sN910F(?:\sDS)?$'), None, {'computer.storage.primary': '32GB'}),
            (re.compile(r'^Samsung.*\si8190(?:\sDS)?$'), None, {'computer.storage.primary': '8GB'}),
            (re.compile(r'^Samsung.*\si9195(?:\sDS)?$'), None, {'computer.storage.primary': '8GB'}),
            (re.compile(r'^Samsung.*\sG903F(?:\sDS)?$'), None, {'computer.storage.primary': '16GB'}),
            (re.compile(r'^Samsung.*\sG313HN(?:\sDS)?$'), None, {'computer.storage.primary': '4GB'}),
            (re.compile(r'^Samsung.*\sS7560(?:\sDS)?$'), None, {'computer.storage.primary': '4GB'}),
            (re.compile(r'^Samsung.*\sG389F(?:\sDS)?$'), None, {'computer.storage.primary': '8GB'}),
            (re.compile(r'^Samsung.*\si8350(?:\sDS)?$'), None, {'computer.storage.primary': '8GB'}),
            (re.compile(r'^Samsung.*\sG390F(?:\sDS)?$'), None, {'computer.storage.primary': '16GB'}),
            (re.compile(r'^Samsung.*\sG130H(?:\sDS)?$'), None, {'computer.storage.primary': '4GB'}),
            (re.compile(r'^Samsung.*\sG130HN(?:\sDS)?$'), None, {'computer.storage.primary': '4GB'}),
            (re.compile(r'^Samsung.*\sS5620(?:\sDS)?$'), None, {'computer.storage.primary': '200MB'}),
            (re.compile(r'^Samsung.*\sS5380(?:\sDS)?$'), None, {'computer.storage.primary': '150MB'}),
            (re.compile(r'^Samsung\sGalaxy\sCore\sPrime.*G361F$'), None, {
                'product.model': 'Galaxy Core Prime',
                'product.variant': 'G361F',
                'computer.storage.primary': '8GB'
            }),
            (re.compile(r'^Samsung\sGalaxy\s(Ace\s[0-9]+).*\sLTE\s(S[0-9]+)(?:\sDS)?$'), None, {
                'product.model': 'Galaxy {0}',
                'product.variant': 2,
                'computer.storage.primary': '8GB'
            }),
            (re.compile(r'Samsung\sGalaxy\sA[6789]\s\(20[0-9]+\).*\s(A[0-9A-Z]+)(?:\sDS)?$'), None, {'product.variant': 1}),
            (re.compile(r'Samsung\sGalaxy\s((A|S|Z)([0-9]+(?:[a-z])?))\s(?:5G\s)?([0-9]+(GB|TB))\s([^\s]+).*'), None, {
                'product.model': 'Galaxy {1}{2}',
                'product.variant': 6
            }),
            (re.compile(r'^Samsung\sGalaxy\s([SA][0-9]+\sPlus|S[0-9]+\sFE|S[0-9]+\sUltra|S[0-9]+\sMini|S[0-9]+\sNeo|S[0-9]+).*\s([iA-Z][0-9BFG]+)(?:\sDS)?$'), None, {
                'product.model': 'Galaxy {0}',
                'product.variant': 2
            }),
            (re.compile(r'Samsung\sGalaxy\sA3\s(A[0-9A-Z]+)?$'), None, {
                'product.kind': 'Smartphone',
                'product.brand': 'Samsung',
                'product.line': 'Galaxy',
                'product.model': 'Galaxy A3',
                'product.variant': 1,
                #'product.release.year': 1,
            }),
            (re.compile(r'^.*\s5G\s.*$'), None, {'computer.networking.cellular': '5G'}),
            (re.compile(r'^.*\sLTE\s.*$'), None, {'computer.networking.cellular': '4G'}),
            (re.compile(r'^Samsung\sGalaxy.*\sDS$'), None, {'cellular.sim.slots': '2'}),
            (re.compile(r'Samsung Galaxy Z Flip 3 5G Bespoke Edition 256GB F711B'), None, {
                'product.model': 'Galaxy Z Flip 3 (Bespoke Edition)',
                'product.release.generation': '3',
                'product.variant': 'F711B'
            }),
        ],
        'Apple': [
            (re.compile(r'^iPhone XR(.*)$'), r'iPhone Xr\1', {}),
            (re.compile(r'^iPhone SE$'), 'iPhone SE', {
                'product.model': 'iPhone SE',
                'product.release.generation': '1'
            }),
            (re.compile(r'^iPhone\sSE\s\(2020\)$'), 'iPhone SE', {
                'product.model': 'iPhone SE',
                'product.release.generation': '2'
            }),
            (re.compile(r'^iPhone\sSE\s\(2022\)$'), 'iPhone SE', {
                'product.model': 'iPhone SE',
                'product.release.generation': '3'
            }),
            (re.compile(r'^(iPhone\s[0-9]+\s)Mini(.*)$'), r'\1mini\2', {}),
            (re.compile(r'^iPhone 5C(.*)$'), r'iPhone 5c\1', {}),
            (re.compile(r'^iPhone 5S(.*)$'), r'iPhone 5s\1', {}),
            (re.compile(r'^iPhone 6S(.*)$'), r'iPhone 6s\1', {}),
        ],
        'Samsung': []
    },
    '12': {
        '*': [
            (re.compile(r'^([A-Za-z]+)\s(.+?)\s([0-9.]+)"$'), None, {
                'product.brand': 1,
                'product.model': 2,
                'computer.display.diameter': 3
            })
        ],
        'Asus': [
            (re.compile(r'^([^\s]+).*'), None, {'product.line': 1}),
            (re.compile(r'^Zenbook(.*$)'), r'ZenBook\1', {'product.line': 'ZenBook'}),
        ],
        'Dell': [
            (re.compile(r'^(Latitude\s[0-9]+)\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^([^\s]+(?:\sx360)?).*'), None, {'product.line': 1}),
        ],
        'HP': [
            (re.compile(r'^Elitebook(.*)$'), r'EliteBook\1', {}),
            (re.compile(r'^(EliteBook\s[0-9]+\sG[0-9])\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^(EliteBook\sx360\s[0-9]+\sG[0-9])\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^(Spectre.*)\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^((EliteBook|ZBook)(.*))\sG([0-9]+)$'), r'\1', {'product.release.generation': 4}),
            (re.compile(r'^([^\s]+).*'), None, {'product.line': 1}),
        ],
        'Lenovo': [
            (re.compile(r'^(V14)\sG([0-9]+)\s(.*)$'), r'\1-\3', {'product.release.generation': 2}),
            (re.compile(r'^Thinkpad(.*)$'), r'ThinkPad\1', {}),
            (re.compile(r'^Ideapad(.*)$'), r'IdeaPad\1', {}),
            (re.compile(r'^(ThinkPad\sT[0-9]+|IdeaPad\s[^\s]+)\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^(Yoga.*)\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^(ThinkPad\s[A-Z][0-9]+)\s[Gg]en\s([0-9]+)(?:\s\(Intel\))?$'), r'\1', {'product.release.generation': 2}),
            (re.compile(r'^(ThinkPad.*)\s\(([0-9]+)(st|nd|rd|th)\s[Gg]en\)'), r'\1', {'product.release.generation': 2}),
            (re.compile(r'^([^\s]+).*'), None, {'product.line': 1}),
        ],
        'Microsoft': [
            (re.compile(r'^(Surface\sLaptop\s[0-9]+)\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^(Surface\sLaptop).*'), None, {'product.line': 1}),
        ],
        'Samsung': [
            (re.compile(r'^(Galaxy\sBook.*)\sTouch'), r'\1', {'computer.display.touch': 'Yes'}),
            (re.compile(r'^(Galaxy\sBook)(.*$)'), r'\1\2', {'product.line': 1}),
        ],
        'Toshiba': [
            (re.compile(r'^(Satellite\sPro).*'), None, {'product.line': 1}),
        ]
    }
}

PRODUCT_SKU_ATTRS: dict[tuple[str, str] | str, set[str]] = {
    ('Apple', 'iPhone'): NotImplemented,
    ('Samsung', 'Galaxy'): NotImplemented,
    ('Samsung', 'Monte'): NotImplemented,
    ('Samsung', 'Omnia'): NotImplemented,
    ('Samsung', 'Wave'): NotImplemented,
    '12': {'computer.display.diameter'}
}

MODEL_FEATURE_MAPPING: dict[tuple[str, str, str], str | None] = {
    ('Apple iPhone 5 16GB', 'appearance.color', 'Black'): 'Black & Slate',
    ('Apple iPhone 5 32GB', 'appearance.color', 'Black'): 'Black & Slate',
    ('Apple iPhone 5 64GB', 'appearance.color', 'Black'): 'Black & Slate',
    ('Apple iPhone 5 16GB', 'appearance.color', 'White'): 'White & Silver',
    ('Apple iPhone 5 32GB', 'appearance.color', 'White'): 'White & Silver',
    ('Apple iPhone 5 64GB', 'appearance.color', 'White'): 'White & Silver',
    ('Apple iPhone 5S 8GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 5S 16GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 5S 32GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 16GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 32GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 Plus 16GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 Plus 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6 Plus 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S 16GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S 32GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S Plus 16GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S Plus 32GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S Plus 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 6S Plus 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 7 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 7 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 7 Plus 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 7 Plus 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 8 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 8 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 8 Plus 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 8 Plus 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 8 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 8 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 8 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 8 Plus 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 8 Plus 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 8 Plus 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone X 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone X 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone XR 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone XR 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone XR 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone XR 64GB', 'appearance.color', 'Orange'): 'Coral',
    ('Apple iPhone XR 128GB', 'appearance.color', 'Orange'): 'Coral',
    ('Apple iPhone XR 256GB', 'appearance.color', 'Orange'): 'Coral',
    ('Apple iPhone Xs 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone Xs 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone Xs 512GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone Xs Max 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone Xs Max 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone Xs Max 512GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 11 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 11 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 11 Pro 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 Pro 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 Pro 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 Pro Max 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 Pro Max 256GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 Pro Max 512GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone 11 Pro 64GB', 'appearance.color', 'Green'): 'Midnight Green',
    ('Apple iPhone 11 Pro 256GB', 'appearance.color', 'Green'): 'Midnight Green',
    ('Apple iPhone 11 Pro 512GB', 'appearance.color', 'Green'): 'Midnight Green',
    ('Apple iPhone 11 Pro Max 64GB', 'appearance.color', 'Green'): 'Midnight Green',
    ('Apple iPhone 11 Pro Max 256GB', 'appearance.color', 'Green'): 'Midnight Green',
    ('Apple iPhone 11 Pro Max 512GB', 'appearance.color', 'Green'): 'Midnight Green',
    ('Apple iPhone SE 16GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone SE 32GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone SE 64GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone SE 128GB', 'appearance.color', 'Grey'): 'Space Gray',
    ('Apple iPhone SE 64GB', 'appearance.color', 'Black'): None,
    ('Apple iPhone SE (2020) 64GB', 'appearance.color', 'Silver'): None,
    ('Apple iPhone SE (2020) 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone SE (2020) 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone SE (2020) 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone SE (2020) 64GB', 'appearance.color', 'Grey'): None,
    ('Apple iPhone SE (2020) 128GB', 'appearance.color', 'Grey'): None,
    ('Apple iPhone SE (2020) 256GB', 'appearance.color', 'Grey'): None,
    ('Apple iPhone SE (2022) 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone SE (2022) 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone SE (2022) 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone SE (2022) 64GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone SE (2022) 128GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone SE (2022) 256GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone SE (2022) 64GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone SE (2022) 128GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone SE (2022) 256GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 12 Mini 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 12 Mini 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 12 Mini 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 12 64GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 12 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 12 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 12 Pro 128GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 12 Pro 256GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 12 Pro 512GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 12 Pro Max 128GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 12 Pro Max 256GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 12 Pro Max 512GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 12 Pro 128GB', 'appearance.color', 'Blue'): 'Pacific Blue',
    ('Apple iPhone 12 Pro 256GB', 'appearance.color', 'Blue'): 'Pacific Blue',
    ('Apple iPhone 12 Pro 512GB', 'appearance.color', 'Blue'): 'Pacific Blue',
    ('Apple iPhone 12 Pro Max 128GB', 'appearance.color', 'Blue'): 'Pacific Blue',
    ('Apple iPhone 12 Pro Max 256GB', 'appearance.color', 'Blue'): 'Pacific Blue',
    ('Apple iPhone 12 Pro Max 512GB', 'appearance.color', 'Blue'): 'Pacific Blue',
    ('Apple iPhone 13 Mini 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 13 Mini 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 13 Mini 512GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 13 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 13 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 13 512GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 13 Mini 128GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 13 Mini 256GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 13 Mini 512GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 13 128GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 13 256GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 13 512GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 13 Mini 128GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 13 Mini 256GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 13 Mini 512GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 13 128GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 13 256GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 13 512GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 13 Pro 128GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro 256GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro 512GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro 1TB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro Max 128GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro Max 256GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro Max 512GB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro Max 1TB', 'appearance.color', 'Grey'): 'Graphite',
    ('Apple iPhone 13 Pro 128GB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro 256GB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro 512GB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro 1TB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro Max 128GB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro Max 256GB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro Max 512GB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro Max 1TB', 'appearance.color', 'Green'): 'Alpine Green',
    ('Apple iPhone 13 Pro 128GB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro 256GB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro 512GB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro 1TB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro Max 128GB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro Max 256GB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro Max 512GB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 13 Pro Max 1TB', 'appearance.color', 'Blue'): 'Sierra Blue',
    ('Apple iPhone 14 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 14 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 14 512GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 14 Plus 128GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 14 Plus 256GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 14 Plus 512GB', 'appearance.color', 'Red'): 'PRODUCT(RED)',
    ('Apple iPhone 14 128GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 14 256GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 14 512GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 14 Plus 128GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 14 Plus 256GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 14 Plus 512GB', 'appearance.color', 'White'): 'Starlight',
    ('Apple iPhone 14 128GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 14 256GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 14 512GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 14 Plus 128GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 14 Plus 256GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 14 Plus 512GB', 'appearance.color', 'Black'): 'Midnight',
    ('Apple iPhone 14 Pro 128GB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro 256GB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro 512GB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro 1TB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro Max 128GB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro Max 256GB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro Max 512GB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro Max 1TB', 'appearance.color', 'Purple'): 'Deep Purple',
    ('Apple iPhone 14 Pro 128GB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro 256GB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro 512GB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro 1TB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro Max 128GB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro Max 256GB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro Max 512GB', 'appearance.color', 'Black'): 'Space Black',
    ('Apple iPhone 14 Pro Max 1TB', 'appearance.color', 'Black'): 'Space Black',
}


cleaners: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r'^Brand New$'), 'New'),
    (re.compile(r'^Holds Charge$'), 'Functional'),
    (re.compile(r'^High Cycle Count$'), 'Worn'),
    (re.compile(r'^Missing$'), 'N/A'),
    (re.compile(r'^(UK|US)\sOriginal(\sBox)?$'), r'Original (\1)'),
    (re.compile(r'^Original(\sBox)?$'), r'Original'),
    (re.compile(r'^Charger included$'), 'Repackaged (with charger)'),
    (re.compile(r'^Unboxed$'), 'Repackaged'),
    (re.compile(r'^(A10 Pro-8730B|A10-8770E|A12-9800E|A6-8550B|A8 Pro-8600B|A9-9430|A10-8770E Pro R7)$'), r'AMD \1'),
    (re.compile(r'^(Athlon|FirePro||Sempron|Radeon|Ryzen)\s(.*)$'), r'AMD \1 \2'),
    (re.compile(r'^(Celeron|Core|UHD Graphics|HD Graphics|Iris Plus||Iris|Pentium|Xeon)\s(.*)$'), r'Intel \1 \2'),
    (re.compile(r'^(Snapdragon)\s(.*)$'), r'Qualcomm \1 \2'),
    (re.compile(r'^Geforce\s(.*)$'), r'GeForce \1'),
    (re.compile(r'^(NVS 310|GeForce|Quadro|RTX)\s(.*)$'), r'NVIDIA \1 \2'),
    (re.compile(r'^(Grade\s)(.*)$'), r'\2'),
    (re.compile(r'^(Win|WIN)\s(.*)$', re.IGNORECASE), r'Microsoft Windows \2'),
    (re.compile(r'^(Microsoft Windows\s[0-9.]+)\sPro'), r'\1 Professional'),
    (re.compile(r'^(Microsoft Windows\s[0-9.]+)\sEdu'), r'\1 Education'),
    (re.compile(r'^(Microsoft Windows\s[0-9.]+)\sUlt'), r'\1 Ultimate'),
    (re.compile(r'^(.*)\sinstalled', re.IGNORECASE), r'\1'),
    (re.compile(r'^(.*)\(([0-9]+)\sx\s([0-9]+)\)$'), r'\1 (\2x\3)'),
    (re.compile(r'^(.*)\s\(([0-9]+x[0-9]+)\)$'), r'\2 (\1)'),
    (re.compile(r'^dual FirePro\s(.*)$'), r'2x AMD FirePro \1'),
    (re.compile(r'^(.*)\s\((.*)\s\)$'), r'\1 (\2)')
]


def clean_feature(value: str) -> str:
    for pattern, replacement in cleaners:
        m = pattern.match(value)
        if not m:
            continue
        value = pattern.sub(replacement, value)
    return value


def _run_extractors(name: str, pattern: re.Pattern[str], replace: str | None, attrs: dict[str, Any]) -> dict[str, str]:
    features: dict[str, Any] = {}
    m = pattern.match(name)
    if not m:
        return {}
    if replace:
        features['product.model'] = pattern.sub(replace, name)
    for k, v in attrs.items():
        if isinstance(v, str):
            features[k] = v.format(*m.groups())
            continue
        assert isinstance(v, int)
        try:
            features[k] = m.group(v)
        except IndexError:
            raise ValueError(f"Pattern does not contain group {v} (item: {name})")
    return features


def extract_features(item_group_id: str, brand: str, dto: PricelistProduct) -> dict[str, Any]:
    name = dto.product_name
    features: dict[str, str] = {}
    for pattern, replace, attrs in (ITEM_GROUP_NAME_EXTRACTORS[item_group_id].get('*') or []):
        features.update(_run_extractors(name, pattern, replace, attrs))
    if brand not in ITEM_GROUP_NAME_EXTRACTORS[item_group_id]:
        raise NotImplementedError(dto.product_name, features['product.model'], features)
    for pattern, replace, attrs in ITEM_GROUP_NAME_EXTRACTORS[item_group_id][brand]:
        features.update(_run_extractors(features['product.model'], pattern, replace, attrs))
    return features

def get_feature_value(key: str, value: str) -> str:
    try:
        value = FEATURE_VALUES[key][value]
    except KeyError:
        pass
    return clean_feature(value)


def get_features(dto: PricelistProduct) -> dict[str, Any]:
    return {
        FEATURE_MAPPING[dimension.key]: get_feature_value(FEATURE_MAPPING[dimension.key], dimension.value)
        for dimension in dto.dimension if dimension.key not in IGNORED_DIMENSIONS
    }


def is_importable(
    dto: PricelistProduct,
) -> bool:
    must_skip = False
    if 'Bespoke Edition' in dto.product_name:
        # Ignore personalized products.
        return False
    for dimension in dto.dimension:
        if dimension.key == 'Boxed' and dimension.value in IGNORED_PACKAGING:
            must_skip = True
        if dimension.key == 'Drive' and dimension.value in IGNORED_DRIVE:
            must_skip = True
        if dimension.key == 'PC Fault Descriptions':
            must_skip = True
        if dimension.key == 'PC Additional Fault':
            must_skip = True
        if dimension.key == 'Battery status' and dimension.value in IGNORED_BATTERY:
            must_skip = True
        if dimension.key == 'Functionality' and dimension.value != 'Working':
            must_skip = True
        if dimension.key == 'Keyboard' and dimension.value in IGNORED_KEYBOARD:
            must_skip = True
        if dimension.value == 'Not tested':
            must_skip = True
        if dimension.key == 'Cloud Lock' and dimension.value != 'CloudOFF':
            must_skip = True
        if dimension.key == 'Additional Info' and str.strip(dimension.value):
            # Exclude products with non-original batteries or that have been modified, customized, or
            # have issues otherwise.
            must_skip = True
        if dimension.key == 'Appearance' and dimension.value in {'Swap'}:
            must_skip = True

    if dto.product_name.startswith('Apple') and 'USA' in dto.product_name:
        must_skip = True

    return not must_skip


def parse_brand(item_group_id: str, dto: PricelistProduct) -> str | None:
    try:
        m = ITEM_GROUP_BRAND_PATTERNS[item_group_id].match(dto.product_name)
        if not m:
            return None
        return m.group(1)
    except KeyError:
        raise ValueError(f"Unknown group (id: {item_group_id}, product: {dto.product_name})")



async def catalog(
    client: IClient[Any, Any],
    logger: logging.Logger,
    catalog: ExternalCatalog,
    postprocess: Callable[[ExternalCatalogItem], ExternalCatalogItem] = lambda x: x,
    when: Callable[[ExternalCatalogItem], bool] = lambda _: True,
    pricelist: str = 'working',
    categories: list[tuple[str, str]] = [('11', '12')],
    products: ProductCatalog | None = None,
    defaults: dict[str, str] | None = None,
    required: set[str] | None = None,
    optional: set[str] | None = None,
    selectable: set[str] | None = None,
    supplier: str | None = None,
    name_template: str = '{features[product.brand]} {features[product.model]}',
    color_mapping: dict[str, str] | None = None,
    allow_create: list[Callable[[dict[str, str]], bool]] | None | bool = None,
    **params: Any
) -> ExternalCatalog:
    for dimension_group, item_group in categories:
        params = {'vatMargin': 'false', 'dimensionGroupId': dimension_group}
        logger.info("Fetching products for supplier %s", supplier)
        async for dto in items(client, item_group_id=item_group, logger=logger, postprocess=postprocess, when=when, color_mapping=color_mapping, **params):
            added = False
            if catalog.add(dto):
                added = True
            if products is not None:
                products.variant(
                    item=dto,
                    name_template=name_template,
                    required=required,
                    optional=optional,
                    selectable=selectable,
                    supplier=supplier,
                    defaults=defaults,
                    allow_create=allow_create
                )
            if added:
                logger.info("Added %s %s (%s)", dto.sku, dto.product_name, dto.grouping_key)
    return catalog


async def items(
    client: IClient[Any, Any],
    item_group_id: str | None,
    logger: logging.Logger = logging.getLogger('cbra'),
    category: str = 'working',
    postprocess: Callable[[ExternalCatalogItem], ExternalCatalogItem] = lambda x: x,
    when: Callable[[ExternalCatalogItem], bool] = lambda _: True,
    color_mapping: dict[str, str] | None = None,
    **params: Any
) -> AsyncIterable[ExternalCatalogItem]:
    if item_group_id is not None:
        params['itemGroupId'] = item_group_id
    seen: set[str] = set()
    async for dto in client.listall(PricelistProduct, category, params=params):
        item_group_id = str(dto.item_group_id)
        assert dto.sku not in seen
        seen.add(dto.sku)
        if not is_importable(dto):
            continue
        #for dimension in dto.dimension:
        #    print(f'- {dimension.key}: {dimension.value}')
        product_brand = parse_brand(item_group_id, dto)
        if not product_brand:
            continue
        features = {
            **get_features(dto),
            **extract_features(item_group_id, product_brand, dto)
        }

        # Check if there are overrides since Foxway using different colors
        # for Apple products.
        must_skip = False
        for feature, value in list(features.items()):
            k = (dto.product_name, feature, value)
            if k not in MODEL_FEATURE_MAPPING:
                continue
            if MODEL_FEATURE_MAPPING[k] is None:
                must_skip = True
                break
            features[feature] = MODEL_FEATURE_MAPPING[k]
        if must_skip:
            continue

        try:
            using = (
                PRODUCT_SKU_ATTRS.get((features['product.brand'], features['product.line']))
                or PRODUCT_SKU_ATTRS[item_group_id]
            )
        except KeyError:
            raise
        item = ExternalCatalogItem.parse_obj({
            'product_name': dto.product_name,
            'grouping_key': v5.generate_grouping_key(features, using=using),
            'sku': dto.sku,
            'resource_name': f'//foxway.shop/sku/{dto.sku}',
            'prices': [{'currency': dto.currency, 'amount': str(dto.price)}],
            'features': features,
            'available': dto.quantity
        })
        if not when(item):
            continue
        model = features['product.model']
        color = features['appearance.color']
        if color_mapping is not None and model not in color_mapping:
            logger.warning(
                "Skipping model, colors missing (model: %s, generation: %s, variant: %s)",
                model, features.get('product.release.generation'), item.product_name
            )
            continue
        if color_mapping is not None:
            logger.debug("Matching color (sku: %s, model: %s, color: %s)", dto.sku, model, color)
            mapped_color = color_mapping[model][color] or color
            if mapped_color == NotImplemented:
                logger.warning("Skipping not implemented color (sku: %s, model: %s, color %s)", dto.sku, model, color)
                continue
            item.features['appearance.color'] = mapped_color
        if item.features.get('product.variant') == 'FN':
            raise Exception(item)
        if item.features.get('product.release.generation') == 'G313HN':
            raise Exception(item)
        postprocess(item)
        if item.features.get('computer.os.coa') == 'N/A':
            continue
        yield item