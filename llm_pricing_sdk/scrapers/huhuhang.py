import requests
from datetime import datetime
from llm_pricing_sdk.models import LLMModelPricing

class HuhuhangScraper:
    @staticmethod
    def scrape():
        url = "https://llm-price.huhuhang.workers.dev/"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

        data = response.json()

        results = []

        for item in data:
            try:
                fields = item["fields"]
                model_name = fields.get("model_name", "")
                provider = fields.get("provider", "")
                input_tokens_price = fields.get("input_tokens", 0.0)
                output_tokens_price = fields.get("output_tokens", 0.0)
                source_url = fields.get("url", "")
                updated_str = fields.get("update_time", "")

                updated_date = datetime.strptime(updated_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

                pricing_data = LLMModelPricing(
                    model=model_name,
                    provider=provider,
                    input_tokens_price=input_tokens_price,
                    output_tokens_price=output_tokens_price,
                    context="",
                    source=source_url,
                    updated=updated_date
                )

                results.append(pricing_data)

            except Exception as e:
                print(f"Error processing item {item['id']}: {e}")

        return results
