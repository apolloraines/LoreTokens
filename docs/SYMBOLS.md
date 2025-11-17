# Symbolic LoreToken Legend

Condensed from `SAIQL.ECHO.DEV/COMPLETE_SYMBOL_LEGEND.md` so you can decode `.sym` payloads without the rest of SAIQL. Nova’s default glyphs focus on market telemetry, but the same mechanism works for any domain—extend the maps if your fields differ.

## Core markers

| Glyph | Meaning |
| --- | --- |
| `⟆` | LoreToken prefix |
| `⊤` | Table |
| `⟐` | Record |
| `⊕/⊖/⊙` | Insert, update, select |
| `⟡` | Transaction |
| `⟢` | Checkpoint |

## Status markers

| Glyph | Meaning |
| --- | --- |
| `✓` | Active |
| `✗` | Inactive |
| `◉` | Proven/committed |
| `◯` | Pending |
| `⊗` | Failed/delete |
| `⚠` | Warning |

## Trading fields

| Glyph | Field |
| --- | --- |
| `§` | Symbol |
| `⏱` | Timestamp |
| `↗/⤊/⤋/↘` | Open, high, low, close |
| `▣` | Volume |
| `⌘` | Timeframe/granularity |

## Crypto tickers

| Glyph | Pair |
| --- | --- |
| `₿` | BTC-USD |
| `Ξ` | ETH-USD |
| `◎` | SOL-USD |
| `✕` | XRP-USD |
| `Ð` | DOGE-USD |
| `₳` | ADA-USD |
| `△` | AVAX-USD |
| `●` | DOT-USD |
| `▽` | MATIC-USD |
| `⬡` | LINK-USD |

## Misc

| Glyph | Meaning |
| --- | --- |
| `⊱` | Created |
| `⋁` | Version |
| `⊜` | Compression level |
| `⊞` | Tables list |
| `♯` | Data hash |
| `№` | Record count |
| `⊡` | Schema description |

For the full authoritative mapping, sync against `SAIQL.ECHO.DEV/COMPLETE_SYMBOL_LEGEND.md`. The translator module (`saiql_delta/core/loretoken_translator.py`) uses the same set when converting `.sym` lines to human-readable text.
