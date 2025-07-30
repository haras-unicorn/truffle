from typing import Final

from truffle_cli.config.input import (
  BEAUTIFUL_SOUP_HTML_PROCESSOR_FILE_CONFIG_TYPE,
  OPENAI_LLM_SERVICE_FILE_CONFIG_TYPE,
  SYNC_WORKER_CONFIG_FILE_TYPE,
  ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE,
)

# NOTE: This data contains example configurations only and must be
# customized for your use case. Please respect the TOS and robots.txt
# of all target sites before scraping.

STATIC_CONFIG: Final[dict] = {
  "scraping_service": {
    "type": ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE,
    "base_url": "https://api.zyte.com/v1/extract",
    "requires_browser": False,
  },
  "llm_service": {
    "type": OPENAI_LLM_SERVICE_FILE_CONFIG_TYPE,
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "extraction_prompt": "Please extract salary range in 'salary' field"
    + " (if one value provided set min/max to same value)"
    + ", job post date in ISO format in 'date' field"
    + ", job location in 'location' field"
    + ", full/part time in one field named 'hours'"
    + ", remote/hybrid/in-office in one field named 'remote'",
    "summary_prompt": "Please summarize the job post based off of the CV.",
    "scoring_prompt": "Please provide a score based off of the CV.",
  },
  "worker": {
    "type": SYNC_WORKER_CONFIG_FILE_TYPE,
  },
  "sites": {
    # spell-checker: disable-next-line
    "posao": {
      "base_url": "https://www.posao.hr",
      "pagination": {
        "template": "https://www.posao.hr/poslovi/djelatnost/informatika-i-telekomunikacije/stranica/{}",
        "start": 0,
        "stop": 50,
        "step": 1,
      },
      "scraping_service": {
        "type": ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE,
        "base_url": "https://api.zyte.com/v1/extract",
        "requires_browser": True,
        "list_payload": {
          "actions": [
            {
              "action": "waitForSelector",
              "selector": {
                "type": "css",
                "value": 'a[href^="https://www.posao.hr/oglasi/"]',
              },
            }
          ]
        },
        "details_payload": {
          "actions": [
            {
              "action": "waitForSelector",
              "selector": {
                "type": "css",
                "value": 'div[class="ad_mask"]',
              },
            }
          ]
        },
      },
      "html_processor": {
        "type": BEAUTIFUL_SOUP_HTML_PROCESSOR_FILE_CONFIG_TYPE,
        "link_selector": 'a[href^="https://www.posao.hr/oglasi/"]',
        "title_selector": "h1",
        "details_selector": 'div[class="ad_mask"]',
      },
    },
  },
}
