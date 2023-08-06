# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib
from typing import Any

from .const import APPLE_IDENTIFIERS
from .const import APPLE_MODELS
from .v4 import APPLE_COLORS
from .v4 import GRADES


MARKETS: dict[str, str] = {
    'China': 'CN',
    'Japan': 'JP',
}


def generate_grouping_key(params: dict[str, Any], using: set[str] | None = None, exclude: set[str] | None = None) -> str:
    exclude = exclude or set()
    using = (using or set()) - exclude
    attrs: dict[str, bytes] = {k: str.encode(str.lower(v), 'utf-8') for k, v in params.items() if v}

    assert b'generation' not in attrs['product.model'], attrs

    # TODO: Very ugly hack.
    if b'iphone se' in attrs['product.model']:
        assert 'product.release.generation' in attrs
        attrs['product.model'] = b'iphone se'
    h = hashlib.md5()
    h.update(attrs['product.brand'])
    h.update(attrs['product.model'])
    if attrs.get('product.release.generation') not in {'N/A', None}:
        h.update(attrs['product.release.generation'])
    if using != NotImplemented:
        for attname in sorted(using):
            h.update(attrs[attname])
    return str.upper(h.hexdigest())


def generate_sku(features: dict[str, str], trading: bool = False, bulk: bool = False, colors: dict[str, str] | None = None) -> str:
    if bulk or trading:
        raise NotImplementedError
    sku = None
    colors = colors or APPLE_COLORS
    params = {
        **features,
        **APPLE_MODELS[ str.lower(features['product.model']) ],
        **APPLE_IDENTIFIERS.get(features['product.identifier'], {}),
        'color.code': colors[ features['appearance.color'] ]
    }
    screen_size = params.get('screen_size')
    match features['product.line']:
        case 'iPhone':
            sku = '{p[base]}{p[color.code]}{p[computer.storage.primary]}'.format(p=params)
        case _:
            if params['base'] != 'IPAP':
                sku = '{p[base]}{p[generation]}{p[color.code]}{p[computer.storage.primary]}'.format(p=params)
            else:
                assert screen_size is not None
                screen_inch = str.split(str(screen_size), '.')[0]
                sku = '{p[base]}{p[generation]}{p[screen_inch]}{p[color.code]}{p[computer.storage.primary]}'.format(p={**params, 'screen_inch': screen_inch})
    assert sku is not None

    # TODO: this is a hack for ipads that come in 3G and 4G variants.
    network_mapping: dict[str, str] = {
        '5G': 'F',
        '4G': 'L',
        '3G': 'G'
    }
    if features.get('product.identifier') in {'ipad3,2', 'iPad3,3'}:
        sku += 'W' if not params['cellular'] else network_mapping[ str(params['cellular']) ]
        #sku += 'W' if not params['cellular'] else 'C'
    elif str.startswith(str(params['base']), 'IPA'):
        sku += 'W' if not params['cellular'] else 'C'
    if params.get('product.release.market') not in {'Worldwide', None}:
        sku += MARKETS[ str(params['product.release.market']) ]
    if params.get('quality.grade.apparent'):
        sku += str(GRADES[ str(params['quality.grade.apparent']) ])
    return sku