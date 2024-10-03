import requests
from bs4 import BeautifulSoup
from datetime import datetime

from llm_pricing_sdk.models import LLMModelPricing


class BotgenuityScraper:
    @staticmethod
    def scrape():
        url = "https://www.botgenuity.com/tools/llm-pricing"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        if not table:
            raise Exception("No table found on the page.")

        rows = []
        for tr in table.find_all("tr")[1:]:  # Skip the header row
            cells = tr.find_all("td")
            if len(cells) >= 5:
                provider = cells[0].text.strip()
                model = cells[1].text.strip()
                context = cells[2].text.strip()
                input_tokens_price = cells[3].text.strip().replace("$", "")
                output_tokens_price = cells[4].text.strip().replace("$", "")
                updated = datetime.strptime(cells[6].text.strip(), "%B %d, %Y").strftime("%B %d, %Y")

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
