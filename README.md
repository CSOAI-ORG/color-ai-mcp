# color-ai-mcp

MCP server for color manipulation and accessibility tools.

## Tools

- **hex_to_rgb** — Convert hex to RGB, HSL, HSV with luminance
- **generate_palette** — Generate color palettes (complementary, analogous, triadic, etc.)
- **check_contrast** — Check WCAG contrast ratio between colors
- **suggest_accessible** — Suggest accessible text colors for backgrounds

## Usage

```bash
pip install mcp
python server.py
```

## Rate Limits

50 calls/day per tool (free tier).
