# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from canonical import DomainName
from canonical import ResourceName


class ProductSupplier(pydantic.BaseModel):
    domain: DomainName
    resource: ResourceName | None = None
    sku: str

    @property
    def key(self) -> tuple[str, str]:
        return (str(self.domain), self.sku)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other: 'ProductSupplier'):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.key == other.key