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
import json
import logging
import os
from typing import Any
from typing import Callable

import pydantic
import yaml

from .externalcatalogitem import ExternalCatalogItem


class ExternalCatalog(pydantic.BaseModel):
    filename: str | None
    supplier: str | None
    features: dict[str, set[str]] = {}
    items: list[ExternalCatalogItem] = []

    @classmethod
    def open(cls, fn: str, **kwargs: Any):
        if os.path.exists(fn):
            return cls.parse_obj({**yaml.safe_load(open(fn).read()), 'filename': fn})
        else:
            return cls(filename=fn, **kwargs)

    def dump(
        self,
        commit: bool = False,
        logger: logging.Logger = logging.getLogger('cbra'),
        **kwargs: Any
    ) -> str:
        n = len({x.sku for x in self.items})
        assert n == len(self.items), f'{n} != {len(self.items)}'
        exclude: set[str] = kwargs.setdefault('exclude', set())
        exclude.add('filename')
        data = yaml.safe_dump(json.loads(self.json(**kwargs)), default_flow_style=False)
        if commit:
            assert self.filename is not None
            logger.info("Writing catalog to %s", self.filename)
            with open(self.filename, 'w') as f:
                f.write('---\n')
                f.write(data)
        return data

    def add(
        self,
        item: ExternalCatalogItem,
        ignore: set[str] | None = None,
    ) -> bool:
        ignore = ignore or set()
        for attname, value in item.features.items():
            if attname in ignore or value == NotImplemented:
                continue
            if attname not in self.features:
                self.features[attname] = set()
            self.features[attname].add(value)
        added = False
        if item not in self.items:
            added = True
            self.items.append(item)
        item = self.items[self.items.index(item)]
        return added

    class Config:
        json_encoders: dict[type, Callable[..., Any]] = {
            collections.defaultdict: dict,
            decimal.Decimal: str,
            set: lambda x: list(sorted(x))
        }