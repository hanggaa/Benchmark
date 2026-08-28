from __future__ import annotations

import abc
import json
import logging
import re
from typing import Any, Dict, Optional, Tuple

from benchmarks.models import TokenUsage

logger = logging.getLogger(__name__)


class BaseRunner(abc.ABC):
    """Abstract base class for all CLI benchmark adapters with Smart Tier Pricing Inference."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pricing_table = config.get("pricing_per_1m_tokens", {})

    @abc.abstractmethod
    def run_prompt(
        self,
        prompt: str,
        model: str,
        effort: Optional[str] = None,
        timeout_seconds: int = 300,
        cwd: Optional[str] = None,
    ) -> Tuple[str, TokenUsage, float, Optional[str]]:
        """
        Runs a prompt through the target CLI tool.
        Returns:
            (response_text, token_usage, duration_seconds, error_message)
        """
        pass

    def estimate_prompt_tokens(self, prompt: str) -> int:
        """
        Estimates the baseline input tokens consumed when sending a prompt to an agent CLI harness.
        Agent CLIs load system instructions and repository tools (~15,000-20,000 baseline tokens)
        in addition to the user prompt text.
        """
        char_tokens = max(len(prompt) // 4, 500)
        return char_tokens + 15000

    def get_pricing(self, model: str) -> Dict[str, float]:
        """
        Smart pricing lookup with Automatic Tier Inference.
        If a new model (like Gemini 4.0 Pro or o4-mini) is released, it automatically
        infers the pricing tier without requiring manual config.json edits.
        """
        model_clean = model.lower().replace(" ", "-").replace(".", "-").replace(":", "-")

        # 1. Exact or partial match in custom config table
        for key, price in self.pricing_table.items():
            if key in model_clean or model_clean in key:
                return price

        # 2. Smart Tier Inference (Zero-Config for New Models)
        m = model.lower()

        # Free tier models
        if "free" in m or "ollama" in m:
            return {"input": 0.0, "output": 0.0, "thinking": 0.0, "cache_read": 0.0}

        # Google Gemini Family
        if "gemini" in m:
            if "flash" in m or "lite" in m:
                # Gemini Flash tier ($0.75 / $3.75 per 1M)
                return {"input": 0.75, "output": 3.75, "thinking": 3.75, "cache_read": 0.1875}
            elif "pro" in m or "ultra" in m:
                # Gemini Pro tier ($2.50 / $15.00 per 1M)
                return {"input": 2.50, "output": 15.00, "thinking": 15.00, "cache_read": 0.625}

        # OpenAI / Codex Family
        if any(prefix in m for prefix in ("gpt-", "o1", "o3", "o4", "chatgpt")):
            if "sol" in m:
                return {"input": 5.00, "output": 30.00, "thinking": 30.00, "cache_read": 0.500}
            elif "terra" in m:
                return {"input": 2.00, "output": 12.00, "thinking": 12.00, "cache_read": 0.200}
            elif "luna" in m:
                return {"input": 0.200, "output": 1.20, "thinking": 1.20, "cache_read": 0.0200}
            elif "mini" in m or "nano" in m:
                return {"input": 1.10, "output": 4.40, "thinking": 4.40, "cache_read": 0.55}
            return {"input": 2.00, "output": 12.00, "thinking": 12.00, "cache_read": 0.20}

        # Anthropic Claude Family
        if "claude" in m:
            if "haiku" in m:
                return {"input": 0.80, "output": 4.00, "thinking": 4.00, "cache_read": 0.08}
            elif "opus" in m:
                return {"input": 15.00, "output": 75.00, "thinking": 75.00, "cache_read": 1.50}
            return {"input": 3.00, "output": 15.00, "thinking": 15.00, "cache_read": 0.30}

        # Open Weights / DeepSeek / Qwen Family
        if "deepseek" in m or "qwen" in m:
            return {"input": 0.27, "output": 1.10, "thinking": 1.10, "cache_read": 0.07}

        # 3. Fallback default pricing
        return self.pricing_table.get(
            "default",
            {"input": 1.0, "output": 3.0, "thinking": 3.0, "cache_read": 0.25},
        )
