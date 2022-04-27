import os
import discord
import dotenv
from discord.ext import tasks
from sitecheckers.adafruit_com import AdaFruitChecker
from sitecheckers.base_checker import ProductPageStatus
from sitecheckers.pishop_us import PiShopChecker

dotenv.load_dotenv(".env")
discord_client = discord.Client()

adafruit_checker = AdaFruitChecker()
pishop_checker = PiShopChecker()

products = [
    ProductPageStatus("https://www.adafruit.com/product/4295", "RPi 4B - 1GB", adafruit_checker),
    ProductPageStatus("https://www.adafruit.com/product/4292", "RPi 4B - 2GB", adafruit_checker),
    ProductPageStatus("https://www.adafruit.com/product/4296", "RPi 4B - 4GB", adafruit_checker),
    ProductPageStatus("https://www.adafruit.com/product/4564", "RPi 4B - 8GB", adafruit_checker),
    ProductPageStatus("https://www.pishop.us/product/raspberry-pi-4-model-b-8gb/", "RPi 4B - 8GB", pishop_checker),
    ProductPageStatus("https://www.pishop.us/product/raspberry-pi-4-model-b-4gb/", "RPi 4B - 4GB", pishop_checker),
    ProductPageStatus("https://www.pishop.us/product/raspberry-pi-4-model-b-2gb/", "RPi 4B - 2GB", pishop_checker),
    ProductPageStatus("https://www.pishop.us/product/raspberry-pi-4-model-b-1gb/", "RPi 4B - 1GB", pishop_checker),
]


async def alert_product(product: ProductPageStatus):
    """
    When a product becomes available, alert it to the appropriate Discord channels
    :param product:
    :return:
    """
    channel_ids = [int(channel_id) for channel_id in os.getenv('CHANNEL_IDS').split(',')]
    for channel_id in channel_ids:
        channel = await discord_client.fetch_channel(channel_id)
        await channel.send(product.get_alert_message())
    product.alerted()


async def check_sites():
    """
    Check all products for availability and alert if available
    :return:
    """
    for product in products:
        if product.is_available() and product.alert_allowed():
            await alert_product(product)


def run_discord_bot():

    @tasks.loop(seconds=10)  # this doesn't necessarily control the time between checks, see base_checker.py for that
    async def site_check_loop():
        await check_sites()

    site_check_loop.start()
    discord_client.run(os.getenv('BOT_TOKEN'))


run_discord_bot()

