# LLM Price Scraper
LLM Price Scraper is a Python package designed to scrape and organize pricing information for large language models (LLMs)
from the following sources:
- https://docsbot.ai/tools/gpt-openai-api-pricing-calculator (best source for now)
- https://huggingface.co/spaces/philschmid/llm-pricing
- https://www.botgenuity.com/tools/llm-pricing
- https://llm-price.com

## Installation
You can install the package using pip:
```bash
pip install llm-price-scraper==1.0.0
```

## Usage
Once you have installed the scrapper, you can use it to quickly retrieve the current pricing information from the website.
```python
from llm_price_scraper.scrapers import LlmPricingScraper

# Get the pricing information
pricing_data = LlmPricingScraper.scrape()

# Loop through each pricing entry and print data
for entry in pricing_data:
    print(f"Model: {entry.model}")
    print(f"Provider: {entry.provider}")
    print(f"1M input tokens: {entry.input_tokens_price}$")
    print(f"1M output tokens: {entry.output_tokens_price}$")
    print(f"Context: {entry.context}")
    print(f"Source: {entry.source}")
    print(f"Updated: {entry.updated}")
    print("-" * 40)
    
# get all gpt-4o models
gpt_4o_models = [entry for entry in pricing_data if "gpt-4o" in entry.model.lower()]
print("GPT-4o models:")
for entry in gpt_4o_models:
    print(f"Model: {entry.model}")
    print(f"Provider: {entry.provider}")
    print(f"1M input tokens: {entry.input_tokens_price}$")
    print(f"1M output tokens: {entry.output_tokens_price}$")
    print(f"Context: {entry.context}")
    print(f"Source: {entry.source}")
    print(f"Updated: {entry.updated}")
    print("-" * 40)
```
You can also chose the source of the data you want to scrape by passing the source as an argument to the `scrape` method. The available sources are defined in the `DataSources` enum.
```python
from llm_price_scraper.scrapers import LlmPricingScraper, DataSources

pricing_data = LlmPricingScraper.scrape(DataSources.HUGGINGFACE)
```

### Example Output
After running the above code, you should see an output like this:

```
Model: gpt-4-32k
Provider: OpenAI
1M input tokens: 60
1M output tokens: 120
Context: 32K
Source: https://www.botgenuity.com/tools/llm-pricing
Updated: March 16, 2024
----------------------------------------
...
```

### Error Handling
In case of a failure to connect to the webpage, an exception will be thrown with an appropriate message. For example:

```
Exception: Failed to retrieve the webpage. Status code: 404
```

## Contributing
Contributions, bug reports, and feature requests are welcome! Feel free to submit a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
