# LLM Pricing SDK
LLM Pricing SDK is a Python package designed to scrape and organize pricing information for large language models (LLMs) from the following webpage: https://www.botgenuity.com/tools/llm-pricing.

## Installation
~~You can install the package using pip:~~ (not yet available)

~~pip install llm_pricing_sdk~~

To install the package, you can clone the repository and install it using the following commands:
```bash
git clone git@github.com:WilliamJlvt/llm_pricing_sdk.git
cd llm_pricing_sdk
pip install .
```


## Usage
Once you have installed the SDK, you can use it to quickly retrieve the current pricing information from the website.
```python
from llm_pricing_sdk.llm_pricing import LlmPricingScraper

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
