from llm_pricing_sdk.enums import DataSources
from llm_pricing_sdk.scrapers.botgenuity import BotgenuityScraper
from llm_pricing_sdk.scrapers.huggingface import HuggingfaceScraper
from llm_pricing_sdk.scrapers.huhuhang import HuhuhangScraper

class LlmPricingScraper:
    @staticmethod
    def scrape(source: DataSources = DataSources.HUGGINGFACE):
        """
        Scrape the LLM pricing information from the specified source.

        :returns: A list of LLMModelPricing objects.
        """
        if source == DataSources.BOTGENUITY:
            return BotgenuityScraper.scrape()
        elif source == DataSources.HUGGINGFACE:
            return HuggingfaceScraper.scrape()
        elif source == DataSources.HUHUHANG:
            return HuhuhangScraper.scrape()
        else:
            raise Exception(f"Source '{source}' is not supported.")
