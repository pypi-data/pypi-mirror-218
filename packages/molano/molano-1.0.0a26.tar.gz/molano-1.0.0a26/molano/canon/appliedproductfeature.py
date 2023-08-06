# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic


class AppliedProductFeature(pydantic.BaseModel):
    applicable: str
    attname: str
    value: str

    @classmethod
    def optional(cls, **kwargs: Any):
        return cls.parse_obj({
            **kwargs,
            'applicable': 'OPT'
        })

    @classmethod
    def required(cls, **kwargs: Any):
        return cls.parse_obj({
            **kwargs,
            'applicable': 'REQ'
        })

    @classmethod
    def selectable(cls, **kwargs: Any):
        return cls.parse_obj({
            **kwargs,
            'applicable': 'SEL'
        })

    def __hash__(self):
        return hash((self.applicable, self.attname, self.value))

    def __eq__(self, other: 'AppliedProductFeature'):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.applicable, self.attname, self.value) == (other.applicable, other.attname, other.value)