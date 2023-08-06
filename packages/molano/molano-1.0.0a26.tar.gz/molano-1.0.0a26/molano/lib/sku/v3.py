# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .const import APPLE_MODELS
from .v2 import APPLE_COLORS


GRADES: dict[str, str] = {
    'A+'    : '0',
    'A'     : '1',
    'B+'    : '2',
    'B'     : '3',
    'C+'    : '4',
    'C'     : '5',
    'D'     : '6',
    'Any'   : 'A',
    'New'   : 'N',
}


def generate_sku(params: dict[str, Any]) -> str:
    params.update(APPLE_MODELS[params['model']]) # type: ignore
    params.setdefault('series', params['model'])
    if params.get('screen_size'):
        params.setdefault('screen_inch', str.split(params['screen_size'], '.')[0])
    kind = params.get('kind')
    color_code = APPLE_COLORS[params['color']] if params.get('color') else None
    is_bulk = params.get('bulk')
    is_trading = params.get('trading')
    model_suffix: str = ''
    if is_bulk:
        model_suffix = 'B'
    if is_trading:
        model_suffix = 'T'
    match kind:
        case "iPad":
            if params['base'] not in {'IPA', 'IPAA', 'IPAM'}:
                sku = '{base}{generation}{screen_inch}{color_code}{storage}'.format(color_code=color_code, **params)
            else:
                sku = '{base}{generation}{color_code}{storage}'.format(color_code=color_code, **params)
            sku += 'C' if params.get('cellular') else 'W'
        case "iPhone":
            params.update(APPLE_MODELS[params['model']]) # type: ignore
            params.setdefault('generation', '')
            if color_code:
                sku = '{base}{color_code}{storage}'.format(color_code=color_code, **params)
            else:
                sku = '{base}{model_suffix}{storage}'.format(color_code=color_code, model_suffix=model_suffix, **params)
        case _:
            raise NotImplementedError
    if params.get('restricted'):
        sku += params['restricted']
    if params.get('grade'):
        grade: str = params['grade']
        if not grade.isdigit():
            grade = GRADES[grade]
        sku += grade
    return sku