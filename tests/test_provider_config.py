from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import experiment_utils  # noqa: E402


class ProviderConfigTests(unittest.TestCase):
    def test_deepseek_default_config_uses_current_chat_endpoint(self) -> None:
        with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-key"}, clear=True):
            config, error = experiment_utils.resolve_provider_config(provider="deepseek")

        self.assertIsNone(error)
        self.assertIsNotNone(config)
        assert config is not None
        self.assertEqual(config.provider, "deepseek")
        self.assertEqual(config.model, "deepseek-v4-flash")
        self.assertEqual(config.endpoint, "https://api.deepseek.com/chat/completions")
        self.assertEqual(config.protocol, "openai_chat_compatible")

    def test_kimi_default_config_accepts_moonshot_env_alias(self) -> None:
        with patch.dict("os.environ", {"MOONSHOT_API_KEY": "test-key"}, clear=True):
            config, error = experiment_utils.resolve_provider_config(provider="kimi")

        self.assertIsNone(error)
        self.assertIsNotNone(config)
        assert config is not None
        self.assertEqual(config.provider, "kimi")
        self.assertEqual(config.model, "kimi-k2.7-code")
        self.assertEqual(config.endpoint, "https://api.moonshot.cn/v1/chat/completions")
        self.assertEqual(config.protocol, "openai_chat_compatible")

    def test_kimi_chat_payload_omits_incompatible_sampling_parameters(self) -> None:
        captured_payloads: list[dict[str, object]] = []

        def fake_post_json(url, headers, payload, *, max_retries=5):
            del url, headers, max_retries
            captured_payloads.append(dict(payload))
            return {"choices": [{"message": {"content": "{\"ok\": true}"}}]}

        config = experiment_utils.ProviderConfig(
            provider="kimi",
            api_key="test-key",
            model="kimi-k2.7-code",
            endpoint="https://api.moonshot.cn/v1/chat/completions",
            protocol="openai_chat_compatible",
        )
        with patch.object(experiment_utils, "_post_json", side_effect=fake_post_json):
            response_text, _ = experiment_utils.call_model("Return JSON.", config)

        self.assertEqual(response_text, "{\"ok\": true}")
        self.assertEqual(len(captured_payloads), 1)
        self.assertNotIn("temperature", captured_payloads[0])
        self.assertNotIn("top_p", captured_payloads[0])

    def test_deepseek_chat_payload_requests_json_object(self) -> None:
        captured_payloads: list[dict[str, object]] = []

        def fake_post_json(url, headers, payload, *, max_retries=5):
            del url, headers, max_retries
            captured_payloads.append(dict(payload))
            return {"choices": [{"message": {"content": "{\"ok\": true}"}}]}

        config = experiment_utils.ProviderConfig(
            provider="deepseek",
            api_key="test-key",
            model="deepseek-v4-flash",
            endpoint="https://api.deepseek.com/chat/completions",
            protocol="openai_chat_compatible",
        )
        with patch.object(experiment_utils, "_post_json", side_effect=fake_post_json):
            response_text, _ = experiment_utils.call_model("Return JSON.", config)

        self.assertEqual(response_text, "{\"ok\": true}")
        self.assertEqual(len(captured_payloads), 1)
        self.assertEqual(captured_payloads[0]["temperature"], 0)
        self.assertEqual(captured_payloads[0]["response_format"], {"type": "json_object"})


if __name__ == "__main__":
    unittest.main()
