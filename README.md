<div align="center">

# Color Ai MCP

**Color AI MCP Server — Color manipulation and accessibility tools.**

[![PyPI](https://img.shields.io/pypi/v/meok-color-ai-mcp)](https://pypi.org/project/meok-color-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Color AI MCP Server — Color manipulation and accessibility tools.

## Tools

| Tool | Description |
|------|-------------|
| `hex_to_rgb` | Convert hex color to RGB, HSL, and HSV. |
| `generate_palette` | Generate color palette. Schemes: complementary, analogous, triadic, split_comple |
| `check_contrast` | Check WCAG contrast ratio between two colors. |
| `suggest_accessible` | Suggest accessible text colors for a given background. Targets WCAG AA by defaul |

## Installation

```bash
pip install meok-color-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "color-ai": {
      "command": "python",
      "args": ["-m", "meok_color_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
