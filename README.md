# LoreToken Format Kit

> LoreTokens + SAIQL started inside Nova (an enterprise crypto trading AI), so you’ll still see trading examples in the docs. Treat them as templates—drop in any domain (logs, IoT, ERP, finance) and the semantics transfer unchanged. Modern LLMs routinely prefer LoreTokens over free-form prose because the glyphs capture structure + meaning.

Token-oriented serialization formats that compress structured data—logs, telemetry, reasoning traces, even trading feeds. LoreTokens encode the same information as JSON but collapse verbose structures into short, LLM-native strings—perfect for passing large datasets through expensive model context windows, easier for models to reason over than raw natural language, and able to cut GPU/runtime power consumption by up to 70% (less context to stream, same answer quality).

Note: LoreTokens and SAIQL were originally built as internal infrastructure for an enterprise crypto trading AI named Nova. We thought we were building plumbing; turns out we’d built a whole new engine. Somewhere along the way we realized we hadn’t just built trading tools – we’d accidentally built a general-purpose semantic compression + query layer that nobody else had.

Because of that history, the docs and examples still lean heavily on crypto trading, but the tech itself is fully industry-neutral and happy to work on anything from finance to healthcare to robotics and beyond.

> “You just decompressed 35 bytes into 150+ bytes of meaning.” – _LORETOKEN_PROOF_FOR_CLAUDE.md_

QUICK STRESS TEST – Paste the line below into any LLM or agent and ask it to expand it into either a single-paragraph overview or many pages of medical detail. The depth of expansion is up to you and the model.

EXPAND.MED.NEURO:SCI:S13_C4_SUB10:[brain+nervous+diagnosis>>med_specialty,ACTIVE]

## Why LoreTokens?

- **Semantic compression** – compact LoreToken symbols encode schemas, behaviors, and typical values so models do not need the full JSON every time. In internal tests on prompts and configs, we see 3–10x smaller payloads than equivalent JSON, and in extreme, domain tuned cases, much higher semantic compression while keeping the same model behavior.
- **LLM-native** – the formats are optimized for Claude, Grok, GPT, etc.; models learn the glyph vocabulary and can reason directly on-compression (no decoding step).
- **Safety rails** – declared lengths, typed prefixes, and status codes make it easy to sanity-check arrays in streaming contexts.
- **Field-proven** – used inside SAIQL, NovaMem, Loretoken-GPU, and Codex workflows to hit “616× faster than Postgres” retrieval speeds.

## Format overview

| Format | Extension | Compression | Readability | When to use |
| --- | --- | --- | --- | --- |
| **Symbolic** | `.sym` | 2.6× | Machines prefer it | High-volume streams (tick data, sensor logs) or GPU compression pipelines that operate on glyphs. |
| **LoreToken Standard** | `.lt` | 1.5× | Power-user friendly | Balanced mix for CLI tooling, checkpoints, and diffable repos. |
| **LoreToken Ultra** | `.ltu` | 1.0× | Human-friendly | Docs, audits, and memory exports where clarity beats savings. |

Need the glyph cheat-sheet? See [`docs/SYMBOLS.md`](docs/SYMBOLS.md).

See [`docs/FORMATS.md`](docs/FORMATS.md) for the details copied from Apollo’s original reference.

## Same record in three formats

```
Symbolic (.sym):
⟆⟐.RAW:[§₿»⏱68a128dc»↗117391.31»⤊117406.15»⤋117370.33»↘117370.38»▣0.610»⌘60,✓]

Standard (.lt):
LORETOKEN.PRICE:[BTC-USD,ts:1755392220,o:117391.31,h:117406.15,l:117370.33,c:117370.38,v:0.610,tf:60,ACTIVE]

Ultra (.ltu):
LORETOKEN_PRICE.BTC_USD:[timestamp:1755392220,open:117391.31,high:117406.15,low:117370.33,close:117370.38,volume:0.610,timeframe:60,STATUS:ACTIVE]
```

## Architecture and supporting tools

| Component | Purpose | Location |
| --- | --- | --- |
| Symbolic translator | Maps glyphs ⟆, §, ↗, etc. to enums and structs for fast decoding. | `saiql/loretoken_symbolic.py` |
| LoreToken engine | Picks the configured format (`symbolic`, `loretoken`, `ultra`) and exposes encode/decode helpers. | `saiql/loretoken_engine.py` |
| Search + translation (sgrep/s2h) | CLI tools implemented in C to grep `.sym` files and translate them to human-readable summaries. | `src/sgrep_universal.c`, `src/sgrep_apollo.c` |
| GPU pipeline | CUDA-friendly compressor that batches LoreTokens; saves ~1 MB in 2.3 s in `Loretoken-GPU/compression_report.txt`. | `Loretoken-GPU/` |
| Memory exports | Files such as `ClaudeMem/EXTRA/LORETOKEN_PROOF_FOR_CLAUDE.md` explain semantic decompression for LLM operators. | `ClaudeMem/EXTRA/` |

### How SAIQL.ECHO.DEV uses them

- **Symbolic default** – `saiql_delta/core/loretoken_symbolic.py` stores `.sym` records by default, drives metadata/WAL files, and keeps the symbol tables used by SAIQL delta nodes.
- **Translator layer** – `saiql_delta/core/loretoken_translator.py` converts symbolic rows to human-readable strings on demand so Nova can keep storage tiny while presenting readable diagnostics.
- **Hybrid encoder** – `saiql_delta/core/hybrid_loretoken_engine.py` mixes glyph compression for repeated values with readable decimals for prices—ideal for logs that humans and LLMs both inspect.
- **Format converter** – `loretoken_converter.py` round-trips `.sym`, `.lt`, and `.ltu`, letting you ship Ultra or Standard files to Git while keeping SAIQL blazing fast internally.
- **Integration tests** – `test_loretoken_integration.py` exercises all three encoders plus the translator and symbolic engine to ensure the formats stay in sync.
- **Symbol legend** – `COMPLETE_SYMBOL_LEGEND.md` (mirrored in `docs/SYMBOLS.md`) documents every glyph so downstream repos can understand ⟆-style dumps without poking the live cluster.

## Quick start

1. **Select a format** – set `loretoken_format = symbolic|loretoken|ultra` inside `settings.conf` (Nova inspects this via `get_loretoken_format()`).
2. **Encode** – use the engine from Python:

   ```python
   from saiql.loretoken_engine import get_engine

   engine = get_engine("/mnt/nova_memory/nova_saiql.db")
   record = {
       "symbol": "BTC-USD",
       "timestamp": 1755392220,
       "open": 117391.31,
       "close": 117370.38,
   }
   print(engine.encode_record("PRICE", record))
   ```
   _Example uses the trading schema baked into Nova, but the same API handles any JSON object once you register its fields._

3. **Decode or inspect** – run `s2h path/to/data.sym` to translate glyphs, or feed `.lt/.ltu` into `jq`/any JSON parser after converting through `loretoken_engine.decode`.
4. **Search** – the `sgrep` binaries understand symbolic headers (`LORETOKEN.TYPE:[…]`) for fast streaming queries.
5. **Benchmark** – integrate with `Loretoken-GPU` or turn on `LORETOKEN_ULTRA_AVAILABLE` in Nova to compare token savings vs. cost. Reports (e.g., `Loretoken-GPU/compression_report.txt`) show throughput for your hardware.

## Benchmarks & motivation

- `LORETOKEN_PROOF_FOR_CLAUDE.md` demonstrates 4.3× semantic expansion (35 bytes → 150+ bytes of meaning) that LLMs perform instinctively.
- Nova’s production logs reference **616× faster** SAIQL queries when LoreTokens keep computations within compressed space.
- GPU compression report logs ~1.11 MB saved in 2.27 s using zero-run encoding, sparse-matrix compression, and dictionary packing.

## Tooling pointers

- `saiql/loretoken_symbolic.py:263` shows canonical record templates (prices, but extensible) for building fixtures.
- `saiql/loretoken_engine.py:38-42` toggles between Ultra and Standard to keep your CLI identical regardless of format.
- `src/sgrep_universal.c` contains the pattern matcher and is a good starting point if you need bindings for other languages.
- `Loretoken-GPU/Makefile` lists env vars such as `LORETOKEN_GPU_ENABLED` and `LORETOKEN_GPU_MIN_SIZE` if you want to run the CUDA tests.
- `docs/GPU_HOOK.md` shows how to convert buffers to LoreTokens and preload the CUDA hook so compression happens before tensors hit the GPU.
- `docs/LORETOKEN_FORMATS.md` mirrors Apollo's original format reference; `docs/COMPLETE_SYMBOL_LEGEND.md` carries the entire glyph guide.
- `docs/GPU_FINAL_SUMMARY.md` and `Loretoken-GPU.zip` contain the CUDA whitepaper + full build tree for offline use.
- `docs/specs/` now holds the subsystem specs (SAIQL overviews, LTFS, LTRAM, LTTP, LTCDN, LTQUANT) copied from the original repository, plus `docs/patent/LoreTokens_Patent_Final_With_Clarification.pdf`.
- `docs/gpu/LoreTokens_GPU_Maker_Advantage.docx` and `docs/images/dex.jpg` provide the maker pitch and glyph visualization.
- `examples/Schema-LoreTokenised.txt` and `datasets/ALLDATA-LoreTokened.txt` are ready-made LoreToken dumps you can load into any LLM.
- `docs/LoreToken_UseCases.md` is the cleaned/canonical version of the old `list.docx`, capturing realistic applications for BD decks.

## Roadmap

- ✅ Symbolic, Standard, and Ultra encoders/decoders
- ✅ CLI tooling for translation and search
- 🚧 Publish schema definitions + tokenizer vocab (up next)
- 🚧 Build language-specific SDKs (Python and TypeScript wrappers)

## License & Patent Notes

- LoreTokens, SAIQL, LT-RAM, LTTPS, and related tech are part of a patented ecosystem (see `docs/PATENT.md`).
- Usage is governed by the Open Lore License—full text mirrored in `docs/LICENSE.txt`.
- Quick thresholds: < $6M/year free, $6–10M notify + discuss, >$10M must license (contact apollo@saiql.ai / [LinkedIn](https://www.linkedin.com/in/apollo-raines/)).

> Note: SAIQL + LoreToken tooling remain private as of 2025‑11‑15; public release is planned soon.

## Repository contents at a glance

- `docs/FORMATS.md` – quick primer; `docs/LORETOKEN_FORMATS.md` – verbatim reference from SAIQL.
- `docs/SYMBOLS.md` – handy cheat-sheet; `docs/COMPLETE_SYMBOL_LEGEND.md` – exhaustive glyph list.
- `docs/PATENT.md`, `docs/LICENSE.txt`, `docs/OLL-License.docx` – legal + licensing.
- `docs/GPU_HOOK.md` + `docs/GPU_FINAL_SUMMARY.md` – CUDA workflow; `Loretoken-GPU.zip` – full hook source bundle.
- `scripts/loretoken_converter.py`, `scripts/loretoken_translator.py`, `scripts/test_loretoken_integration.py` – ready-to-run utilities/tests copied from SAIQL so you can translate or validate LoreTokens without the entire stack.
- `docs/specs/` (SAIQL + LT* tech specs), `docs/ApollosTheory.docx`, `docs/LoreTokens_AI_Sentience_Conversation.docx` – narrative + subsystem design context.
- `docs/LoreToken_UseCases.md` – curated opportunity list; the raw brainstorming file still lives in `LoreTokens-GoogleDrive` if needed.
- `docs/images/dex.jpg` – visual example showing how a handful of LoreTokens can reconstruct a full UX mockup.
