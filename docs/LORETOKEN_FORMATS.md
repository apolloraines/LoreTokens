# LORETOKEN FORMAT REFERENCE
**CRITICAL**: This file defines the three LoreToken formats used in the Nova system.
AI systems should read this to understand the formats.

## 1. SYMBOLIC FORMAT (.sym files)
**Compression**: 2.6x (MAXIMUM)
**AI Efficiency**: BEST - Most data per token
**Human Readability**: Requires s2h translation tool

### Symbol Mappings
```
# Types
⟆ = LORETOKEN prefix
⟐ = RECORD
⊤ = TABLE
◊ = META
⟡ = TRANSACTION

# Fields
§ = symbol
⏱ = timestamp
↗ = open
⤊ = high
⤋ = low
↘ = close
▣ = volume
⌘ = timeframe

# Crypto Symbols
₿ = BTC-USD
Ξ = ETH-USD
◎ = SOL-USD
✕ = XRP-USD
Ð = DOGE-USD

# Status
✓ = ACTIVE
✗ = INACTIVE
◉ = COMMITTED

# Separator
» = field separator (like comma)
```

### Example Record
```
⟆⟐.RAW:[§₿»⏱68a128dc»↗117391.31»⤊117406.15»⤋117370.33»↘117370.38»▣0.610»⌘60,✓]
```

### Decoded
```
LORETOKEN.RECORD.RAW:[
  symbol: BTC-USD,
  timestamp: 1755392220 (hex: 68a128dc),
  open: 117391.31,
  high: 117406.15,
  low: 117370.33,
  close: 117370.38,
  volume: 0.610,
  timeframe: 60,
  status: ACTIVE
]
```

## 2. LORETOKEN STANDARD FORMAT (.lt files)
**Compression**: 1.5x (HIGH)
**AI Efficiency**: GOOD - Balanced compression
**Human Readability**: MODERATE - Structured but compressed

### Format Pattern
```
LORETOKEN.TYPE:[field:value,field:value,STATUS]
```

### Example Record
```
LORETOKEN.PRICE:[BTC-USD,ts:1755392220,o:117391.31,h:117406.15,l:117370.33,c:117370.38,v:0.610,tf:60,ACTIVE]
```

### Field Abbreviations
- ts = timestamp
- o = open
- h = high
- l = low
- c = close
- v = volume
- tf = timeframe

## 3. LORETOKEN ULTRA FORMAT (.ltu files)
**Compression**: 1.0x (STANDARD)
**AI Efficiency**: STANDARD - More tokens but clearer
**Human Readability**: EXCELLENT - Like ApolloMem.txt

### Format Pattern
```
LORETOKEN_TYPE.IDENTIFIER:[full_field_name:value,full_field_name:value,STATUS:value]
```

### Example Record
```
LORETOKEN_PRICE.BTC_USD:[timestamp:1755392220,open:117391.31,high:117406.15,low:117370.33,close:117370.38,volume:0.610,timeframe:60,STATUS:ACTIVE]
```

### Characteristics
- Full field names (no abbreviations)
- Underscores in type names
- Clear key:value pairs
- Human-friendly formatting

## COMPARISON

### Same data in all three formats:

**SYMBOLIC (67 chars)**:
```
⟆⟐.RAW:[§₿»⏱68a128dc»↗117391.31»⤊117406.15»⤋117370.33»↘117370.38»▣0.610»⌘60,✓]
```

**LORETOKEN (115 chars)**:
```
LORETOKEN.PRICE:[BTC-USD,ts:1755392220,o:117391.31,h:117406.15,l:117370.33,c:117370.38,v:0.610,tf:60,ACTIVE]
```

**ULTRA (172 chars)**:
```
LORETOKEN_PRICE.BTC_USD:[timestamp:1755392220,open:117391.31,high:117406.15,low:117370.33,close:117370.38,volume:0.610,timeframe:60,STATUS:ACTIVE]
```

## CONFIGURATION
Set in `/home/nova/settings.conf`:
```ini
[database]
loretoken_format = symbolic  # or 'loretoken' or 'ultra'
```

## USAGE IN CODE
```python
from loretoken_engine import get_engine, get_loretoken_format

# Automatically uses the configured format
engine = get_engine("/path/to/db")
format_type = get_loretoken_format()  # Returns: 'symbolic', 'loretoken', or 'ultra'
```

## TOOLS
- **sgrep**: Search symbolic files with human queries
- **s2h**: Translate symbolic to human-readable
- **loretoken_engine.py**: Format selector based on settings.conf

---
**Created by Apollo Raines** - SAIQL and LoreToken inventor
**AI Note**: Once you read this mapping, you can process any format equally well