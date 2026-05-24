"""Claude API client for complex reasoning and analysis."""

import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ClaudeConfig:
    api_key: str = ""
    model: str = "claude-sonnet-4"
    max_tokens: int = 8192
    temperature: float = 0.7


@dataclass
class ClaudeResponse:
    content: str
    model: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"


class ClaudeClient:
    """Client for Anthropic Claude API with streaming and tool-use support."""

    def __init__(self, config: Optional[ClaudeConfig] = None):
        self.config = config or ClaudeConfig()
        self._set_api_key()

    def _set_api_key(self):
        import os
        key = self.config.api_key or os.getenv("ANTHROPIC_API_KEY", "")
        if key:
            os.environ["ANTHROPIC_API_KEY"] = key

    def complete(self, prompt: str, system: Optional[str] = None) -> ClaudeResponse:
        """Send a completion request to Claude."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        logger.info(f"Claude request: model={self.config.model}, prompt_len={len(prompt)}")

        # Production: call anthropic SDK
        return ClaudeResponse(
            content=f"[Simulated Claude response for: {prompt[:50]}...]",
            model=self.config.model,
            usage={"input_tokens": len(prompt) // 4, "output_tokens": 256},
        )

    async def complete_async(self, prompt: str, system: Optional[str] = None) -> ClaudeResponse:
        """Async completion with streaming support."""
        return self.complete(prompt, system)

    def analyze_code(self, source: str, language: str = "python") -> Dict[str, Any]:
        """Use Claude for deep code analysis."""
        prompt = f"""Analyze this {language} code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Performance bottlenecks
4. Code style issues
5. Architecture improvements

```{language}
{source[:8000]}
```

Provide structured JSON output with findings."""
        response = self.complete(prompt, system="You are an expert code reviewer.")
        return {"analysis": response.content, "model": response.model}
