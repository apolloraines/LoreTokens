# LoreToken Format Reference

Summaries adapted from the Nova production docs in `SAIQL.ECHO.DEV/docs/LORETOKEN_FORMATS.md`. Inside SAIQL, `.sym` is the default on-disk representation while `.lt`/`.ltu` power exports, APIs, and human-facing tooling. The examples below use price data because that’s how Nova is wired, but the same syntax can describe any JSON structure (support tickets, telemetry, documents, etc.).

## 1. Symbolic (`.sym`)

- **Compression**: ~2.6× vs. formatted JSON
- **Best for**: GPU/FPGA pipelines, NovaMem, realtime feeds
- **Structure**:

  ```
  ⟆⟐.RAW:[§₿»⏱68a128dc»↗117391.31»⤊117406.15»⤋117370.33»↘117370.38»▣0.610»⌘60,✓]
  ```

- Glyph legend:

  | Glyph | Meaning |
  | --- | --- |
  | `⟆` | LoreToken prefix |
  | `⟐` | Record |
  | `⊤` | Table |
  | `◊` | Metadata |
  | `⟡` | Transaction |
  | `§` | Symbol |
  | `⏱` | Timestamp |
  | `↗/⤊/⤋/↘` | OHLC |
  | `▣` | Volume |
  | `⌘` | Timeframe |
  | `✓/✗/◉` | Status |
  | `»` | Field separator |

## 2. LoreToken Standard (`.lt`)

- **Compression**: ~1.5×
- **Best for**: CLI tooling, repos, diffable configs
- **Pattern**: `LORETOKEN.TYPE:[field:value,...,STATUS]`
- **Example**:

  ```
  LORETOKEN.PRICE:[BTC-USD,ts:1755392220,o:117391.31,h:117406.15,l:117370.33,c:117370.38,v:0.610,tf:60,ACTIVE]
  ```

  where abbreviations map to timestamp (`ts`), open (`o`), high (`h`), low (`l`), close (`c`), volume (`v`), timeframe (`tf`).

## 3. LoreToken Ultra (`.ltu`)

- **Compression**: ~1.0× (similar to compact JSON but friendlier)
- **Best for**: audits, documentation, when humans read the source
- **Pattern**: `LORETOKEN_TYPE.IDENTIFIER:[full_key:value,...,STATUS:value]`
- **Example**:

  ```
  LORETOKEN_PRICE.BTC_USD:[timestamp:1755392220,open:117391.31,high:117406.15,low:117370.33,close:117370.38,volume:0.610,timeframe:60,STATUS:ACTIVE]
  ```

## Comparison

| Format | Example length | Notes |
| --- | --- | --- |
| Symbolic | 67 chars | Maximum compression, glyph vocabulary |
| Standard | 115 chars | Abbreviated keys, comma-separated |
| Ultra | 172 chars | Full keys, easiest to scan |

## Configuration flags

Nova reads the desired format from `settings.conf`:

```ini
[database]
loretoken_format = symbolic  # or loretoken / ultra
```

`loretoken_engine.get_loretoken_format()` inspects this flag and configures downstream services automatically.
- **SAIQL usage**: Stored by `SymbolicLoreTokenEngine` with translator hooks so humans can expand on demand.
- **SAIQL usage**: Used by `loretoken_converter.py` and API gateways when symbolic data needs to ship as plain text.
- **SAIQL usage**: Referenced in Claude/Nova memory dumps and any place where field names must stay explicit.
