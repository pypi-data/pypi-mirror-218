# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from canonical import ResourceName


class PartResourceName(ResourceName):

    @classmethod
    def frompk(cls, pk: int, domain: str = 'erp.molanoapis.com'):
        return cls(f'//{domain}/parts/{pk}')

    @property
    def part_id(self) -> int:
        return int(self.id)