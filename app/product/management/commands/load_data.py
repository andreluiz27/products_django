import asyncio
import aiohttp
import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from upload.models import Product

# get root path
from django.conf import settings


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        # file path as argument
        parser.add_argument("file_path", type=str)

    async def get_address_by_cep(self, cep):
        """
        Get a Brazilian address based on CEP using an external API assynchronously
        Will return the address str logradouro + complemento + bairro + localidade + uf
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://viacep.com.br/ws/{cep}/json/") as response:
                    response = await response.json()
                    address = f"{response['logradouro']} {response['complemento']} {response['bairro']} {response['localidade']} {response['uf']}"
                    return address
        except Exception as e:
            print(f"Error: {e}")
            return "Address not found"
    def handle(self, *args, **options):
        root_path = settings.BASE_DIR
        data = pd.read_csv(f"{root_path}/{options['file_path']}")
        for index, row in data.iterrows():
            product = Product(
                id=row["ID"],
                name=row["NAME"],
                category=row["CATEGORY"],
                manufacturer=row["MANUFACTURER"],
                price_brl=row["PRICE_BRL"],
                product_storage_address=asyncio.run(self.get_address_by_cep(row["CEP"])),
            )
            product.save()
