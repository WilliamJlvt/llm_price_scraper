import requests
from bs4 import BeautifulSoup
from datetime import datetime


class LLMModelPricing:
    """ Pricing information model for LLM models. """

    def __init__(self, model, provider, input_tokens_price,
                 output_tokens_price, context, source, updated):
        self.model = model
        self.provider = provider
        self.input_tokens_price = input_tokens_price
        self.output_tokens_price = output_tokens_price
        self.context = context
        self.source = source
        self.updated = updated

    def __str__(self):
        return f"Model: {self.model}, Provider: {self.provider}, Input Price: {self.input_tokens_price}, " \
               f"Output Price: {self.output_tokens_price}, Context: {self.context}, " \
               f"Source: {self.source}, Updated: {self.updated}"

class LlmPricingScraper:
    @staticmethod
    def scrape():
        """
        Scrape the LLM pricing information from the specified webpage.

        Returns:
            A list of LLMModelPricing objects, where each object contains pricing info like:
            LLMModelPricing(model, provider, input_tokens_price, output_tokens_price, context, source, updated)
        """
        url = "https://www.botgenuity.com/tools/llm-pricing"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

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
                updated = datetime.strptime(cells[6].text.strip(), "%B %d, %Y").strftime("%B %d, %Y")

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