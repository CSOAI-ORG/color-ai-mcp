"""Color AI MCP Server — Color manipulation and accessibility tools."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import colorsys
import math
import time
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("color-ai", instructions="MEOK AI Labs MCP Server")
_calls: dict[str, list[float]] = {}
DAILY_LIMIT = 50

def _rate_check(tool: str) -> bool:
    now = time.time()
    _calls.setdefault(tool, [])
    _calls[tool] = [t for t in _calls[tool] if t > now - 86400]
    if len(_calls[tool]) >= DAILY_LIMIT:
        return False
    _calls[tool].append(now)
    return True

def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def _relative_luminance(r: int, g: int, b: int) -> float:
    def linearize(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

@mcp.tool()
def hex_to_rgb(hex_color: str, api_key: str = "") -> dict[str, Any]:
    """Convert hex color to RGB, HSL, and HSV."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("hex_to_rgb"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        r, g, b = _hex_to_rgb(hex_color)
    except (ValueError, IndexError):
        return {"error": "Invalid hex color. Use #RRGGBB or #RGB"}
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hv, sv, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    lum = _relative_luminance(r, g, b)
    return {
        "hex": _rgb_to_hex(r, g, b), "rgb": {"r": r, "g": g, "b": b},
        "hsl": {"h": round(h * 360), "s": round(s * 100), "l": round(l * 100)},
        "hsv": {"h": round(hv * 360), "s": round(sv * 100), "v": round(v * 100)},
        "luminance": round(lum, 4),
        "css_rgb": f"rgb({r}, {g}, {b})",
        "css_hsl": f"hsl({round(h*360)}, {round(s*100)}%, {round(l*100)}%)",
        "is_dark": lum < 0.179
    }

@mcp.tool()
def generate_palette(base_hex: str, scheme: str = "complementary", count: int = 5, api_key: str = "") -> dict[str, Any]:
    """Generate color palette. Schemes: complementary, analogous, triadic, split_complementary, monochromatic, tetradic."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("generate_palette"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        r, g, b = _hex_to_rgb(base_hex)
    except (ValueError, IndexError):
        return {"error": "Invalid hex color"}
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    colors = []
    if scheme == "complementary":
        offsets = [0, 0.5]
    elif scheme == "analogous":
        offsets = [-2/12, -1/12, 0, 1/12, 2/12]
    elif scheme == "triadic":
        offsets = [0, 1/3, 2/3]
    elif scheme == "split_complementary":
        offsets = [0, 5/12, 7/12]
    elif scheme == "monochromatic":
        offsets = [0] * count
    elif scheme == "tetradic":
        offsets = [0, 0.25, 0.5, 0.75]
    else:
        return {"error": "Unknown scheme"}
    for i, off in enumerate(offsets[:count]):
        nh = (h + off) % 1.0
        if scheme == "monochromatic":
            nl = max(0.1, min(0.9, l + (i - len(offsets) // 2) * 0.12))
            cr, cg, cb = colorsys.hls_to_rgb(h, nl, s)
        else:
            cr, cg, cb = colorsys.hls_to_rgb(nh, l, s)
        colors.append(_rgb_to_hex(round(cr * 255), round(cg * 255), round(cb * 255)))
    return {"base": _rgb_to_hex(r, g, b), "scheme": scheme, "palette": colors}

@mcp.tool()
def check_contrast(foreground: str, background: str, api_key: str = "") -> dict[str, Any]:
    """Check WCAG contrast ratio between two colors."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("check_contrast"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        fr, fg, fb = _hex_to_rgb(foreground)
        br, bg_, bb = _hex_to_rgb(background)
    except (ValueError, IndexError):
        return {"error": "Invalid hex color"}
    l1 = _relative_luminance(fr, fg, fb)
    l2 = _relative_luminance(br, bg_, bb)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    ratio = (lighter + 0.05) / (darker + 0.05)
    return {
        "foreground": _rgb_to_hex(fr, fg, fb), "background": _rgb_to_hex(br, bg_, bb),
        "contrast_ratio": round(ratio, 2),
        "wcag_aa_normal": ratio >= 4.5, "wcag_aa_large": ratio >= 3.0,
        "wcag_aaa_normal": ratio >= 7.0, "wcag_aaa_large": ratio >= 4.5,
        "rating": "Excellent" if ratio >= 7 else "Good" if ratio >= 4.5 else "Fair" if ratio >= 3 else "Poor"
    }

@mcp.tool()
def suggest_accessible(background: str, min_ratio: float = 4.5, api_key: str = "") -> dict[str, Any]:
    """Suggest accessible text colors for a given background. Targets WCAG AA by default."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("suggest_accessible"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        br, bg_, bb = _hex_to_rgb(background)
    except (ValueError, IndexError):
        return {"error": "Invalid hex color"}
    bg_lum = _relative_luminance(br, bg_, bb)
    suggestions = []
    # Try black and white first
    for text in ["#000000", "#ffffff"]:
        tr, tg, tb = _hex_to_rgb(text)
        tl = _relative_luminance(tr, tg, tb)
        ratio = (max(bg_lum, tl) + 0.05) / (min(bg_lum, tl) + 0.05)
        if ratio >= min_ratio:
            suggestions.append({"color": text, "ratio": round(ratio, 2)})
    # Try shades
    for v in range(0, 256, 17):
        hex_c = _rgb_to_hex(v, v, v)
        tl = _relative_luminance(v, v, v)
        ratio = (max(bg_lum, tl) + 0.05) / (min(bg_lum, tl) + 0.05)
        if ratio >= min_ratio:
            suggestions.append({"color": hex_c, "ratio": round(ratio, 2)})
    seen = set()
    unique = []
    for s in sorted(suggestions, key=lambda x: -x["ratio"]):
        if s["color"] not in seen:
            seen.add(s["color"])
            unique.append(s)
    return {"background": _rgb_to_hex(br, bg_, bb), "min_ratio": min_ratio, "suggestions": unique[:10]}

if __name__ == "__main__":
    mcp.run()
