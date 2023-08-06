# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
from typing import Any

from .const import APPLE_MODELS as _APPLE_MODELS
from .v3 import APPLE_COLORS
from .v3 import GRADES


APPLE_MODELS: dict[str, Any] = {str.lower(k): v for k, v in _APPLE_MODELS.items()}

PRODUCT_RED_MODELS: set[str] = {
    'IPH7',
    'IPH7P',
    'IPH8',
    'IPH8P',
    'IPHXR',
    'IPH11',
    'IPHSE2',
    'IPH12M',
    'IPH12',
    'IPH13M',
    'IPH13',
    'IPHSE3',
    'IPH14',
    'IPH14P'
}

def get_color(color: str) -> str:
    return APPLE_COLORS[color]


def get_attrs(name: str) -> dict[str, Any]:
    return APPLE_MODELS[str.lower(name)]


def generate_sku(params: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    params = copy.deepcopy(params)
    if params.get('product.line') != 'iPhone':
        raise NotImplementedError
    params.update(get_attrs(params['product.model']))
    return generate_iphone_sku(params)


def generate_iphone_sku(params: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    color = params['appearance.color']
    sku = params['base']
    if params['base'] in PRODUCT_RED_MODELS and color == 'Red':
        color = 'PRODUCT(RED)'
    sku += APPLE_COLORS[color]
    sku += params['computer.storage.primary']
    sku += GRADES[ params['quality.grade.apparent'] ]
    return sku, {
        'appearance.color': color,
        'product.release.year': params['year']
    }