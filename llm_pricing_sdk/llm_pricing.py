from datetime import datetime
from enum import Enum
from bs4 import BeautifulSoup

import re
import requests

from llm_pricing_sdk.utils import fetch_ts_file


class DataSources(Enum):
    BOTGENUITY = "botgenuity"
    HUGGINGFACE = "huggingface"


class LLMModelPricing:
    """ Pricing information model for LLM models. """

    def __init__(self, model, provider, input_tokens_price,
                 output_tokens_price, context, source, updated):
        self.model = model
        self.provider = provider
        self.input_tokens_price = input_tokens_price  # price per 1M tokens in dollars USD
        self.output_tokens_price = output_tokens_price  # price per 1M tokens in dollars USD
        self.context = context  # context for the model
        self.source = source  # source of the pricing information
        self.updated = updated

    def __str__(self):
        return f"Model: {self.model}, " \
               f"Provider: {self.provider}, " \
               f"Input Price: {self.input_tokens_price}, " \
               f"Output Price: {self.output_tokens_price}, " \
               f"Context: {self.context}, " \
               f"Source: {self.source}, " \
               f"Updated: {self.updated}"


class LlmPricingScraper:
    @staticmethod
    def botgenuity_scrape():
        url = "https://www.botgenuity.com/tools/llm-pricing"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve the webpage. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table element on the webpage
        table = soup.find("table")
        if not table:
            raise Exception("No table found on the page.")

        # Extract rows of data
        rows = []
        for tr in table.find_all("tr")[1:]:  # Skip the header row
            cells = tr.find_all("td")
            if len(cells) >= 5:
                provider = cells[0].text.strip()
                model = cells[1].text.strip()
                context = cells[2].text.strip()
                input_tokens_price = cells[3].text.strip()
                input_tokens_price = input_tokens_price[1:]
                output_tokens_price = cells[4].text.strip()
                output_tokens_price = output_tokens_price[1:]
                updated = datetime.strptime(cells[6].text.strip(),
                                            "%B %d, %Y").strftime("%B %d, %Y")

                # Create an object for each row
                pricing_info = LLMModelPricing(
                    provider=provider,
                    model=model,
                    context=context,
                    input_tokens_price=input_tokens_price,
                    output_tokens_price=output_tokens_price,
                    source=url,
                    updated=updated
                )

                rows.append(pricing_info)

        return rows

    @staticmethod
    def huggingface_scrape():
        url = "https://huggingface.co/spaces/philschmid/llm-pricing/resolve/main/src/lib/data.ts"

        provider_regex = re.compile(r"provider: '(.*?)',")  # Nom du provider
        uri_regex = re.compile(r"uri: '(.*?)',")  # URI (source)
        models_regex = re.compile(
            r"\{ name: '(.*?)', inputPrice: ([\d.]+), outputPrice: ([\d.]+) \}")  # Modèles/prix

        providers = []

        content = fetch_ts_file(url)

        # Découper le contenu TS par block de provider
        provider_blocks = content.split('},\n  {')

        for block in provider_blocks:
            # Extraire le provider
            provider_match = provider_regex.search(block)
            uri_match = uri_regex.search(block)

            if provider_match and uri_match:
                provider_name = provider_match.group(1)
                provider_uri = uri_match.group(1)

                # Extraire les modèles (nom, prix d'entrée, prix de sortie)
                models = models_regex.findall(block)

                for model in models:
                    model_name, input_price, output_price = model
                    # Créer une instance de LLMModelPricing pour chaque modèle
                    pricing_data = LLMModelPricing(
                        model=model_name,
                        provider=provider_name,
                        input_tokens_price=float(input_price),
                        output_tokens_price=float(output_price),
                        context="",
                        source=provider_uri,
                        updated=str(datetime.now().date())  # Date actuelle
                    )
                    providers.append(pricing_data)

        return providers


    @staticmethod
    def scrape(source: DataSources = DataSources.HUGGINGFACE):
        """
        Scrape the LLM pricing information from the specified source.

        :arg source: The source to scrape the pricing information from. Default is "botgenuity".

        :returns
            A list of LLMModelPricing objects, where each object contains pricing info like:
            LLMModelPricing(model, provider, input_tokens_price, output_tokens_price, context, source, updated)
        """
        if source == DataSources.BOTGENUITY:
            return LlmPricingScraper.botgenuity_scrape()
        elif source == DataSources.HUGGINGFACE:
            return LlmPricingScraper.huggingface_scrape()
        else:
            raise Exception(f"Source '{source}' is not supported.")