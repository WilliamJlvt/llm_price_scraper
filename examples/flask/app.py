from flask import Flask, jsonify, request
from llm_pricing_sdk.enums import DataSources
from llm_pricing_sdk.scrapers import LlmPricingScraper

app = Flask(__name__)


@app.route('/api/pricing/', methods=['GET'])
def get_pricing():
    source = request.args.get('source', default='huggingface', type=str)

    try:
        if source.lower() == DataSources.DOCSBOT.value:
            results = LlmPricingScraper.scrape(DataSources.DOCSBOT)
        elif source.lower() == DataSources.BOTGENUITY.value:
            results = LlmPricingScraper.scrape(DataSources.BOTGENUITY)
        elif source.lower() == DataSources.HUGGINGFACE.value:
            results = LlmPricingScraper.scrape(DataSources.HUGGINGFACE)
        elif source.lower() == DataSources.HUHUHANG.value:
            results = LlmPricingScraper.scrape(DataSources.HUHUHANG)
        else:
            return jsonify(
                {"error": f"Source '{source}' is not supported."}), 400

        pricing_data = [
            {
                "model": result.model,
                "provider": result.provider,
                "input_tokens_price": result.input_tokens_price,
                "output_tokens_price": result.output_tokens_price,
                "context": result.context,
                "source": result.source,
                "updated": result.updated
            }
            for result in results
        ]

        return jsonify({"pricing_data": pricing_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
