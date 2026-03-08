"""Shared Nova Nexa configuration utilities.

Centralises reading of ~/.nova-nexa/configuration.json so that the runner
and every agent template share one implementation instead of copy-pasting
helper functions.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from framework.graph.edge import DEFAULT_MAX_TOKENS

# ---------------------------------------------------------------------------
# Low-level config file access
# ---------------------------------------------------------------------------

# Support both new and legacy config paths for backward compatibility
NEXA_CONFIG_FILE = Path.home() / ".nova-nexa" / "configuration.json"
LEGACY_CONFIG_FILE = Path.home() / ".hive" / "configuration.json"
# Expose as HIVE_CONFIG_FILE for backward compatibility with existing code
HIVE_CONFIG_FILE = NEXA_CONFIG_FILE
logger = logging.getLogger(__name__)


def _resolve_config_file() -> Path:
    """Return the active config file path, preferring new location."""
    if NEXA_CONFIG_FILE.exists():
        return NEXA_CONFIG_FILE
    if LEGACY_CONFIG_FILE.exists():
        return LEGACY_CONFIG_FILE
    return NEXA_CONFIG_FILE


def get_nexa_config() -> dict[str, Any]:
    """Load Nova Nexa configuration from ~/.nova-nexa/configuration.json."""
    config_file = _resolve_config_file()
    if not config_file.exists():
        return {}
    try:
        with open(config_file, encoding="utf-8-sig") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(
            "Failed to load Hive config %s: %s",
            config_file,
            e,
        )
        return {}


# Backward-compatible alias
get_hive_config = get_nexa_config


# ---------------------------------------------------------------------------
# Derived helpers
# ---------------------------------------------------------------------------

# Default models: Nova Pro for orchestrator, Nova Micro for workers
NOVA_PRO_MODEL = "bedrock/amazon.nova-pro-v1:0"
NOVA_MICRO_MODEL = "bedrock/amazon.nova-micro-v1:0"
NOVA_LITE_MODEL = "bedrock/amazon.nova-lite-v1:0"


def get_preferred_model() -> str:
    """Return the user's preferred LLM model string.

    Defaults to Amazon Nova Pro for orchestration tasks.
    """
    llm = get_nexa_config().get("llm", {})
    if llm.get("provider") and llm.get("model"):
        return f"{llm['provider']}/{llm['model']}"
    return NOVA_PRO_MODEL


def get_worker_model() -> str:
    """Return the model for worker nodes.

    Defaults to Amazon Nova Micro for cost-efficient execution.
    """
    llm = get_nexa_config().get("llm", {})
    worker_model = llm.get("worker_model")
    if worker_model:
        return worker_model
    return NOVA_MICRO_MODEL


def get_max_tokens() -> int:
    """Return the configured max_tokens, falling back to DEFAULT_MAX_TOKENS."""
    return get_nexa_config().get("llm", {}).get("max_tokens", DEFAULT_MAX_TOKENS)


def get_api_key() -> str | None:
    """Return the API key, supporting env var and AWS Bedrock credentials.

    Priority:
    1. AWS Bedrock (uses boto3 credential chain — no explicit key needed)
    2. Claude Code subscription (``use_claude_code_subscription: true``)
    3. Codex subscription (``use_codex_subscription: true``)
    4. Environment variable named in ``api_key_env_var``.
    """
    llm = get_nexa_config().get("llm", {})

    # AWS Bedrock: uses boto3 credential chain, no explicit API key needed
    provider = llm.get("provider", "")
    if provider == "bedrock" or provider.startswith("amazon"):
        # Bedrock uses AWS credentials (env vars, ~/.aws/credentials, IAM role)
        return os.environ.get("AWS_ACCESS_KEY_ID")

    # Claude Code subscription: read OAuth token directly
    if llm.get("use_claude_code_subscription"):
        try:
            from framework.runner.runner import get_claude_code_token

            token = get_claude_code_token()
            if token:
                return token
        except ImportError:
            pass

    # Codex subscription: read OAuth token from Keychain / auth.json
    if llm.get("use_codex_subscription"):
        try:
            from framework.runner.runner import get_codex_token

            token = get_codex_token()
            if token:
                return token
        except ImportError:
            pass

    # Standard env-var path
    api_key_env_var = llm.get("api_key_env_var")
    if api_key_env_var:
        return os.environ.get(api_key_env_var)
    return None


def get_gcu_enabled() -> bool:
    """Return whether GCU (browser automation) is enabled in user config."""
    return get_nexa_config().get("gcu_enabled", True)


def get_api_base() -> str | None:
    """Return the api_base URL for OpenAI-compatible endpoints, if configured."""
    llm = get_nexa_config().get("llm", {})
    if llm.get("use_codex_subscription"):
        return "https://chatgpt.com/backend-api/codex"
    return llm.get("api_base")


def get_llm_extra_kwargs() -> dict[str, Any]:
    """Return extra kwargs for LiteLLMProvider (e.g. OAuth headers, AWS region)."""
    llm = get_nexa_config().get("llm", {})

    # AWS Bedrock: pass region configuration
    provider = llm.get("provider", "")
    if provider == "bedrock" or provider.startswith("amazon"):
        region = llm.get("aws_region", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
        return {"aws_region_name": region}

    if llm.get("use_claude_code_subscription"):
        api_key = get_api_key()
        if api_key:
            return {
                "extra_headers": {"authorization": f"Bearer {api_key}"},
            }
    if llm.get("use_codex_subscription"):
        api_key = get_api_key()
        if api_key:
            headers: dict[str, str] = {
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "CodexBar",
            }
            try:
                from framework.runner.runner import get_codex_account_id

                account_id = get_codex_account_id()
                if account_id:
                    headers["ChatGPT-Account-Id"] = account_id
            except ImportError:
                pass
            return {
                "extra_headers": headers,
                "store": False,
                "allowed_openai_params": ["store"],
            }
    return {}


# ---------------------------------------------------------------------------
# RuntimeConfig – shared across agent templates
# ---------------------------------------------------------------------------


@dataclass
class RuntimeConfig:
    """Agent runtime configuration loaded from ~/.nova-nexa/configuration.json."""

    model: str = field(default_factory=get_preferred_model)
    worker_model: str = field(default_factory=get_worker_model)
    temperature: float = 0.7
    max_tokens: int = field(default_factory=get_max_tokens)
    api_key: str | None = field(default_factory=get_api_key)
    api_base: str | None = field(default_factory=get_api_base)
    extra_kwargs: dict[str, Any] = field(default_factory=get_llm_extra_kwargs)
