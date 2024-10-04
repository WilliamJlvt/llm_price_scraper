import unittest
import requests_mock
from llm_pricing_sdk.scrapers import LlmPricingScraper, DataSources


class TestLlmPricingScraper(unittest.TestCase):

    def test_scrape_returns_at_least_one_result(self):
        pricing_data = LlmPricingScraper.scrape(DataSources.HUGGINGFACE)
        self.assertTrue(len(pricing_data) > 0)
        pricing_data = LlmPricingScraper.scrape(DataSources.DOCSBOT)
        self.assertTrue(len(pricing_data) > 0)
        pricing_data = LlmPricingScraper.scrape(DataSources.HUHUHANG)
        self.assertTrue(len(pricing_data) > 0)
        pricing_data = LlmPricingScraper.scrape(DataSources.BOTGENUITY)
        self.assertTrue(len(pricing_data) > 0)

    @requests_mock.Mocker()
    def test_scrape_empty_table(self, mock_request):
        # Mock an empty table scenario
        mock_request.get('https://www.botgenuity.com/tools/llm-pricing', text="""
        <html><body><table></table></body></html>
        """)
        results = LlmPricingScraper.scrape(DataSources.BOTGENUITY)
        # No data in table, expect empty list
        self.assertEqual(len(results),0)

    @requests_mock.Mocker()
    def test_scrape_raises_error_on_failure(self, mock_request):
        # Mock a bad status response
        mock_request.get('https://www.botgenuity.com/tools/llm-pricing', status_code=404)

        # Expect the scrape method to raise an exception
        with self.assertRaises(Exception) as context:
            LlmPricingScraper.scrape(DataSources.BOTGENUITY)

        self.assertTrue('Failed to retrieve the webpage' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
