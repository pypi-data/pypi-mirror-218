# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .appleudid import AppleUDID
from .decimalmeid import DecimalMEID
from .deviceserialnumber import DeviceSerialNumber
from .documentreference import DocumentReference
from .externalcatalog import ExternalCatalog
from .externalcatalogitem import ExternalCatalogItem
from .fulfillmentrejectedreason import FulfillmentRejectedReason
from .imei import IMEI
from .meid import MEID
from .ordernumber import OrderNumber
from .productcatalog import ProductCatalog
from .productdefinition import ProductDefinition
from .productvariant import ProductVariant
from .privateenterprisenumber import PrivateEnterpriseNumber
from .purchaseordernumber import PurchaseOrderNumber
from .receiptnumber import ReceiptNumber
from .trackedmobiledevicereference import TrackedMobileDeviceReference


__all__: list[str] = [
    'AppleUDID',
    'DecimalMEID',
    'DeviceSerialNumber',
    'DocumentReference',
    'ExternalCatalog',
    'ExternalCatalogItem',
    'FulfillmentRejectedReason',
    'IMEI',
    'MEID',
    'PrivateEnterpriseNumber',
    'OrderNumber',
    'ProductCatalog',
    'ProductDefinition',
    'ProductVariant',
    'PurchaseOrderNumber',
    'ReceiptNumber',
    'TrackedMobileDeviceReference',
]