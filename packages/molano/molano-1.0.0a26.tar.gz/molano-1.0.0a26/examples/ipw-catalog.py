# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import argparse
import asyncio
import logging

from headless.core.httpx import Client

from molano.canon import ExternalCatalog
from molano.canon import ProductCatalog
from molano.lib import ipw
from molano.__main__ import application


logger: logging.Logger = logging.getLogger('cbra')
parser = argparse.ArgumentParser("Imports products from the specified source.")
parser.add_argument('-p', action='append', dest='presets')
parser.add_argument('--commit', action='store_true', dest='commit')


async def main():
    args = parser.parse_args()
    products = ProductCatalog.open('var/products.yml')
    logger.info("Importing The iPhone Wiki products")
    async with Client(base_url="") as client:
        fn = 'var/catalogs/ipw.yml'
        catalog = ExternalCatalog.open(fn, supplier=None)
        await ipw.catalog(
            client,
            catalog,
            products=products,
            logger=logger,
            supplier=catalog.supplier,
        )
        if args.commit:
            catalog.dump(commit=True)

    if args.commit:
        products.dump(commit=True)
        raise SystemExit
    
    print(products.dump(commit=False, include={'features'}))
    #sheet.extend(rows)

if __name__ == '__main__':
    asyncio.run(application.run(main))