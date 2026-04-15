# Color AI MCP Server

> By [MEOK AI Labs](https://meok.ai) — Color conversion, palette generation, and WCAG contrast checking

## Installation

```bash
pip install color-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `hex_to_rgb`
Convert hex color to RGB, HSL, HSV, and CSS formats with luminance calculation.

**Parameters:**
- `hex_color` (str): Hex color (e.g., '#ff6600')

### `generate_palette`
Generate color palette from a base color using various schemes.

**Parameters:**
- `base_hex` (str): Base hex color
- `scheme` (str): Scheme — 'complementary', 'analogous', 'triadic', 'split_complementary', 'monochromatic', 'tetradic'
- `count` (int): Number of colors (default 5)

### `check_contrast`
Check WCAG contrast ratio between two colors with AA/AAA compliance.

**Parameters:**
- `foreground` (str): Foreground hex color
- `background` (str): Background hex color

### `suggest_accessible`
Suggest accessible text colors for a given background targeting WCAG AA/AAA.

**Parameters:**
- `background` (str): Background hex color
- `min_ratio` (float): Minimum contrast ratio (default 4.5)

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
