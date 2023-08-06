# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from canonical import ResourceName


class ProductVariantResource(pydantic.BaseModel):
    kind: str
    service_name: str
    relname: str

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//{self.service_name}/{self.relname}')

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.kind, self.service_name, self.relname)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other: 'ProductVariantResource'):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.key == other.key