import pytest
from pytest import FixtureRequest

from truffle_cli_tests.test_system import TestSystem


# spell-checker: disable-next-line
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# spell-checker: disable-next-line
def pytest_runtest_makereport(item):
  outcome = yield
  rep = outcome.get_result()
  setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def test_system(request: FixtureRequest):
  system = TestSystem(args=[], env={}, files={})
  system.set_env("zyte_api_key", "sk-xxxxxxxxxxxxx")
  system.set_env("openai_api_key", "sk-xxxxxxxxxxxxx")
  system.set_config_file(
    {
      "llm_service": {
        "cv": "My CV.",
        "extraction_prompt": "Please extract data from content.",
        "scoring_prompt": "Please score the content.",
        "summary_prompt": "Please summarize the content.",
      }
    }
  )

  yield system

  if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
    print(f"System:\n\n{system}")
