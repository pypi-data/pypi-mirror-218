# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import copy
import logging
import re
from typing import Any
from typing import AsyncIterable
from typing import Callable
from typing import Sequence

from headless.types import IClient

from molano.canon import ExternalCatalog
from molano.canon import ExternalCatalogItem
from molano.canon import ProductCatalog
from molano.lib.sku import v1
from molano.lib.sku import v5

from molano.lib.sku.const import APPLE_IDENTIFIERS
from molano.lib.sku.const import APPLE_MODELS
from molano.lib.sku.extract import parse_iphonewiki


logger: logging.Logger = logging.getLogger('cbra')


FEATURE_CLEANERS: dict[str, list[tuple[re.Pattern[str], str, dict[str, str]]]] = {
    'product.model': [
        (re.compile(r'^iPhone SE \(1st generation\)$'), 'iPhone SE', {}),
        (re.compile(r'^iPhone SE \(2nd generation\)$'), 'iPhone SE', {}),
        (re.compile(r'^iPhone SE \(3rd generation\)$'), 'iPhone SE', {}),
        (re.compile(r'^(iPhone\s)XR(.*$)'), r'\1Xr\2', {}),
        (re.compile(r'^(iPhone\s)XS(.*$)'), r'\1Xs\2', {}),
        (re.compile(r'^(iPad Pro|iPad mini|iPad Air).*$'), r'\1', {}),
        (re.compile(r'^iPad\s[\(0-9].*$'), r'iPad', {}),
    ],
    'computer.storage.primary': [
        (re.compile(r'^([0-9]+(GB|TB))\[[0-9]\]$'), r'\1', {})
    ]
}


REQUIRED_FEATURES: set[str] = {
    'product.brand',
    'product.kind',
    'product.line',
    'product.model',
}


DEFAULT_FEATURES: dict[str, str] = {
    'product.brand'             : 'Apple',
    'product.release.market'    : 'Worldwide',
    'quality.functional.state'  : 'Working',
    'quality.packaging.state'   : 'Repackaged',
}

LINE_FEATURES: dict[str, dict[str, str]] = {
    'iphone': {
        'product.line': 'iPhone',
    },
    'ipad': {
        'product.line': 'iPad',
    },
}

ROW_FEATURES: dict[str, Callable[[Sequence[str]], dict[str, str]]] = {
    'iphone': lambda row: {
        'appearance.color': row[-3],
        'computer.storage.primary': str.replace(row[-2], ' ', ''),
        'product.kind': 'Smartphone',
        'product.model': row[0],
        'product.identifier': row[5]
    },
    'ipad': lambda row: {
        'appearance.color': row[-3],
        'computer.storage.primary': str.replace(row[-2], ' ', ''),
        'product.kind': 'Tablet',
        'product.model': row[0],
        'product.identifier': row[5]
    },
}

FOOTNOTE_FEATURES: dict[int, str] = {
    1: 'apple:model:exclusive:cn',
    2: 'apple:model:limited:iphone6',
    3: 'apple:model:exclusive:jp',
    4: 'apple:model:exclusive:jp',
    5: 'apple:model:exclusive:cn',
    6: 'apple:model:demo',
    7: 'apple:model:exclusive:cn',
}

TAG_FEATURES: dict[str, dict[str, str]] = {
    'apple:model:exclusive:cn': {
        'product.release.market': 'China'
    },
    'apple:model:exclusive:jp': {
        'product.release.market': 'Japan'
    },
}

PRODUCT_LINE_DEFAULTS: dict[str, dict[str, str]] = {
    'iPhone': {
        'product.release.market': 'Worldwide'
    },
    'iPad': {
        'product.release.market': 'Worldwide'
    },
}

PRODUCT_LINE_FEATURES: dict[str, dict[str, set[str]]] = collections.defaultdict(lambda: collections.defaultdict(set), {
    'iPhone': collections.defaultdict(set, {
        'required': {
            'product.release.generation',
            'product.release.year'
        },
        'selectable': {
            'appearance.color',
            'computer.storage.primary',
            'product.release.market',
            'quality.functional.state',
            'quality.grade.apparent',
            'quality.packaging.state',
        }
    }),
    'iPad': collections.defaultdict(set, {
        'required': {
            'computer.display.diameter',
            'product.release.generation',
            'product.release.year'
        },
        'selectable': {
            'appearance.color',
            'computer.storage.primary',
            'product.release.market',
            'quality.functional.state',
            'quality.grade.apparent',
            'quality.packaging.state',
        },
        'optional': {
            'computer.networking.cellular',
        }
    })
})

MODEL_FEATURES: dict[str, dict[str, str]] = {
    'iPhone SE (1st generation)': {
        'product.release.year': '2016',
        'product.release.generation': '1',
    },
    'iPhone SE (2nd generation)': {
        'product.release.year': '2020',
        'product.release.generation': '2',
    },
    'iPhone SE (3rd generation)': {
        'product.release.year': '2022',
        'product.release.generation': '3',
    },
}


def get_apple_features(model: str, identifier: str) -> dict[str, str]:
    params = {**APPLE_MODELS[model], **APPLE_IDENTIFIERS.get(identifier, {})}
    name_mapping = {
        'year'          : 'product.release.year',
        'screen_size'   : 'computer.display.diameter',
        'generation'    : 'product.release.generation',
        'cellular'      : 'computer.networking.cellular',
    }
    features: dict[str, str] = {}
    for k, v in name_mapping.items():
        if k in {'screen_size', 'cellular'} and not str.startswith(identifier, 'iPad'):
            continue
        if k == 'generation' and str.startswith(identifier, 'iPhone') and not model.startswith('iPhone SE'):
            continue
        value = params[k]
        if not isinstance(value, str) and k not in {'year', 'generation', 'cellular'}:
            raise NotImplementedError(model, identifier, k, v, repr(value))
        if value is not None:
            features[v] = str(value)
    return features


def clean_features(features: dict[str, str]) -> dict[str, str]:
    for attname, value in list(features.items()):
        if attname not in FEATURE_CLEANERS:
            continue
        for pattern, replace, attrs in FEATURE_CLEANERS[attname]:
            m = pattern.match(value)
            if m is None:
                continue
            features.update(attrs)
            value = pattern.sub(replace, value)
        features[attname] = value
    return features


def generate_product_name(features: dict[str, str]) -> str:
    name = None
    color = features['appearance.color']
    grade = features['quality.grade.apparent']
    market = features.get('product.release.market')
    if market == 'Worldwide':
        market = None
    generation = features.get('product.release.generation')
    cellular = features.get('computer.networking.cellular')
    has_generation = generation not in {'N/A', None}
    model = features['product.model']
    if model == 'iPad Pro':
        model = '{model} {f[computer.display.diameter]}"'.format(model=model, f=features)
    if has_generation and market:
        name = '{model} ({f[product.release.year]}, {f[product.release.market]}) {f[computer.storage.primary]}'.format(model=model, f=features)
    elif has_generation:
        name = '{model} ({f[product.release.year]}) {f[computer.storage.primary]}'.format(model=model, f=features)
    elif market:
        name = '{model} ({f[product.release.market]}) {f[computer.storage.primary]}'.format(model=model, f=features)
    else:
        name = '{model} {f[computer.storage.primary]}'.format(model=model, f=features)
    assert name is not None
    if cellular:
        if cellular:
            name = f'{name} WiFi+{cellular}'
        else:
            name = f'{name} WiFi'
    if color not in {'Mixed'}:
        name = f'{name} {color}'
    if grade not in {'Any'}:
        name = f'{name} {grade}'
    return name


def generate_group_name(item: ExternalCatalogItem) -> str:
    if item.features['product.model'] == 'iPhone SE':
        return '{features[product.brand]} {features[product.model]} ({features[product.release.year]})'.format(features=item.features)
    elif item.features['product.line'] == 'iPad':
        return '{features[product.brand]} {features[product.model]} ({features[product.release.year]})'.format(features=item.features)
    else:
        return '{features[product.brand]} {features[product.model]}'.format(features=item.features)
    raise NotImplementedError


async def catalog(
    client: IClient[Any, Any],
    catalog: ExternalCatalog,
    products: ProductCatalog | None = None,
    defaults: dict[str, str] | None = None,
    required: set[str] | None = None,
    optional: set[str] | None = None,
    selectable: set[str] | None = None,
    supplier: str | None = None,
    allow_create: list[Callable[[dict[str, str]], bool]] | None = None,
    **params: Any
) -> ExternalCatalog:
    logger = logging.getLogger('cbra')
    async for dto in items(client, optional=optional, **params):
        if any([
            dto.product_name.startswith('iPhone 3G'),
            dto.product_name.startswith('iPhone 4GB'),
            dto.product_name.startswith('iPhone 8GB'),
            dto.product_name.startswith('iPhone 16GB'),
        ]):
            continue
        assert dto.features.get('computer.networking.cellular') != 'N/A', dto
        added = catalog.add(dto, ignore={'product.identifier'})
        dto = copy.deepcopy(dto)
        dto.features.setdefault('product.release.generation', NotImplemented)
        if added:
            logger.info("Add %s %s", dto.sku, dto.product_name)
        if products is not None:
            products.variant(
                item=dto,
                name_template=generate_group_name,
                required={*PRODUCT_LINE_FEATURES[ dto.features['product.line'] ]['required'], *REQUIRED_FEATURES},
                optional={*(optional or set()), *PRODUCT_LINE_FEATURES[ dto.features['product.line'] ]['optional']},
                selectable=PRODUCT_LINE_FEATURES[ dto.features['product.line'] ]['selectable'],
                supplier=supplier,
                defaults=PRODUCT_LINE_DEFAULTS[ dto.features['product.line'] ],
                ignore={'product.identifier'},
                allow_create=[lambda features: True]
            )
    return catalog


async def items(
    client: IClient[Any, Any],
    category: str = 'working',
    optional: set[str] | None = None,
    **params: Any
) -> AsyncIterable[ExternalCatalogItem]:
    optional = optional or set()
    grades: list[str] = ['Any', 'New', 'A+', 'A', 'B+', 'B', 'C+', 'C']
    product_lines: list[tuple[str, set[str]]] = [
        ('iphone', set()),
        ('ipad', {'computer.networking.cellular'})
    ]
    for product_line, optional in product_lines:
        v1_seen: dict[str, ExternalCatalogItem] = {}
        seen: set[str] = set()
        async for row in parse_iphonewiki(client, product_line):
            for grade in grades:
                features = clean_features({
                    **get_apple_features(row[0], row[5]),
                    **DEFAULT_FEATURES,
                    **LINE_FEATURES[product_line],
                    **ROW_FEATURES[product_line](row),
                    **MODEL_FEATURES.get(row[0], {}),
                    'quality.grade.apparent': grade
                })
                using: set[str] = set()
                if features['product.line'] == 'iPad':
                    using.add('computer.display.diameter')
                item = ExternalCatalogItem.parse_obj({
                    'product_name': generate_product_name(features),
                    'grouping_key': v5.generate_grouping_key({**features}, using=using, exclude=optional),
                    'sku': v5.generate_sku({**features, 'product.model': row[0]}),
                    'features': {k: v for k, v in features.items() if v != NotImplemented},
                })
                assert item.sku is not None
                item.identifiers.update({
                    'v1.molano.nl/sku': v5.generate_sku({
                        **features,
                        'product.model': row[0]
                    }, colors=v1.APPLE_COLORS),
                    'v2.molano.nl/sku': item.sku,
                    'v3.molano.nl/sku': item.sku
                })

                # iPhone 8 128GB is not listed by The iPhone Wiki
                if item.features['product.model'] in {'iPhone 8', 'iPhone 8 Plus'} and item.features['computer.storage.primary'] == '256GB':
                    iphone8 = item.clone()
                    iphone8.features.update({
                        'computer.storage.primary': '128GB'
                    })
                    iphone8.product_name = generate_product_name(iphone8.features)
                    iphone8.sku = v5.generate_sku({**iphone8.features, 'product.model': row[0]})
                    iphone8.identifiers.update({
                        'v1.molano.nl/sku': v5.generate_sku({**iphone8.features, 'product.model': row[0]}, colors=v1.APPLE_COLORS),
                        'v2.molano.nl/sku': iphone8.sku,
                        'v3.molano.nl/sku': iphone8.sku
                    })
                    yield iphone8
                    mixed_sku = v5.generate_sku({**iphone8.features,
                        'appearance.color': 'Mixed',
                        'product.model': row[0],
                        'quality.grade.apparent': 'Any'
                    })
                    if mixed_sku not in seen:
                        mixed = iphone8.clone()
                        mixed.features.update({
                            'appearance.color': 'Mixed',
                            'quality.grade.apparent': 'Any'
                        })
                        mixed.product_name = generate_product_name(mixed.features)
                        mixed.sku = v5.generate_sku({**mixed.features, 'product.model': row[0]})
                        mixed.identifiers = {
                            'v3.molano.nl/sku': mixed.sku
                        }
                        yield mixed
                        for number in row[1]:
                            if not number.get('tag'):
                                continue
                            restricted = mixed.clone()
                            restricted.features.update(TAG_FEATURES[ number['tag'] ])
                            restricted.sku = v5.generate_sku({**restricted.features, 'product.model': row[0]})
                            restricted.product_name = generate_product_name(restricted.features)
                            restricted.identifiers = {
                                'v3.molano.nl/sku': restricted.sku
                            }
                            yield restricted

                # Create also items that have mixed color and no grading,
                # these are used for bulk procurement and trading.
                mixed_sku = v5.generate_sku({**features,
                    'appearance.color': 'Mixed',
                    'product.model': row[0],
                    'quality.grade.apparent': 'Any'
                })
                if mixed_sku not in seen:
                    mixed = item.clone()
                    mixed.features.update({
                        'appearance.color': 'Mixed',
                        'quality.grade.apparent': 'Any'
                    })
                    mixed.product_name = generate_product_name(mixed.features)
                    mixed.sku = v5.generate_sku({**mixed.features, 'product.model': row[0]})
                    mixed.identifiers = {
                        'v3.molano.nl/sku': mixed.sku
                    }
                    yield mixed
                    for number in row[1]:
                        if not number.get('tag'):
                            continue
                        restricted = mixed.clone()
                        restricted.features.update(TAG_FEATURES[ number['tag'] ])
                        restricted.sku = v5.generate_sku({**restricted.features, 'product.model': row[0]})
                        restricted.product_name = generate_product_name(restricted.features)
                        restricted.identifiers = {
                            'v3.molano.nl/sku': restricted.sku
                        }
                        yield restricted

                if item.sku not in seen:
                    assert item.sku is not None
                    seen.add(item.sku)
                    if item.identifiers['v1.molano.nl/sku'] in v1_seen:
                        old = v1_seen[item.identifiers['v1.molano.nl/sku']]
                        logger.warning("Sku already seen (old: %s, new: %s)", old.product_name, item.product_name)
                        item.identifiers.pop('v1.molano.nl/sku')
                    else:
                        v1_seen[item.identifiers['v1.molano.nl/sku']] = item
                    yield item
                for number in row[1]:
                    if not number.get('tag'):
                        continue
                    restricted = item.clone()
                    restricted.features.update(TAG_FEATURES[ number['tag'] ])
                    restricted.sku = v5.generate_sku({**features, 'product.model': row[0]})
                    restricted.product_name = generate_product_name(restricted.features)
                    restricted.identifiers.update({
                        'v3.molano.nl/sku': restricted.sku
                    })
                    if restricted.sku not in seen:
                        assert restricted.sku is not None
                        seen.add(restricted.sku)
                        yield restricted