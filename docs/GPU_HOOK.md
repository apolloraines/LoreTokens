# LoreToken GPU Hook Workflow

This mirrors the CUDA hook shipped in `/home/nova/Loretoken-GPU`. It explains how to convert payloads into LoreTokens before they hit the GPU and how to preload the hook so compression/decompression happens transparently.

## 1. Build the hook libraries

```bash
cd /home/nova/Loretoken-GPU
make all             # builds libloretoken_cuda_hook.so, production, and transparent variants
```

Key outputs:

- `build/libloretoken_cuda_hook.so` – baseline hook
- `build/libproduction_cuda_hook.so` – integrated decode path
- `build/libtransparent_cuda_hook.so` – logs memcpy calls without modifying data

See `Loretoken-GPU/Makefile` for other targets (`install`, `uninstall`, etc.).

## 2. Convert inputs to LoreTokens

Always serialize your tensors/records to a LoreToken string before the GPU copy. You can either:

### a. Use the Symbolic encoder (extend `FIELDS` for your domain)

```python
from saiql_delta.core.loretoken_symbolic import SymbolicLoreToken

record = {
    "symbol": "BTC-USD",
    "timestamp": 1755392220,
    "open": "117391.31",
    "close": "117370.38",
    "volume": "0.60979011",
    "granularity": "60",
}
payload = SymbolicLoreToken.encode("RECORD", "RAW_PRICES", record, "ACTIVE")

# Write payload to a pinned buffer before cudaMemcpy
with open("/tmp/loretoken_batch.sym", "wb") as fh:
    fh.write(payload.encode())
```

### b. Use the converter CLI

```python
from loretoken_converter import LoreTokenConverter, DBMode

# Works for any JSON-like payload; drop in your own keys/values
line = "sensor_id>>A17 timestamp>>1755392220 temp_c>>41.2 humidity>>0.31 status>>ACTIVE"
symbolic_line = LoreTokenConverter.convert_line(line, target_format=DBMode.LTS)
```

The hook looks for LoreToken headers (e.g., `LORETOKEN.`, `⟆⟐`) to decide whether a buffer is compressible.

## 3. Preload the hook when launching GPU workloads

Wrap your CUDA/PyTorch program with `LD_PRELOAD` so every `cudaMalloc` / `cudaMemcpy` call routes through the LoreToken hook:

```bash
cd /home/nova/Loretoken-GPU
LD_PRELOAD=./build/libloretoken_cuda_hook.so python your_script.py
```

- Use `libtransparent_cuda_hook.so` during integration debugging.
- Use `libproduction_cuda_hook.so` once you want automatic decompression on GPU reads.

The hook writes telemetry to `Loretoken-GPU/logs/*.log` showing `MEMCPY_COMPRESSED`, compressed sizes, and GPU decode throughput.

## 4. Typical pipeline

1. Gather text/JSON.
2. Encode to `.sym` or `.lt` via `SymbolicLoreToken.encode` or `LoreTokenConverter`.
3. Feed the encoded bytes into your tensor buffer.
4. Launch the model with `LD_PRELOAD=libloretoken_cuda_hook.so`.
5. Inspect `logs/cuda_hook.log` (or `transparent_hook.log`) for compression ratios (~6.8× in Apollo’s report).

## References

- `Loretoken-GPU/FINAL_SUMMARY.md` – system overview and quick commands.
- `Loretoken-GPU/src/transparent_cuda_hook.cpp` – entry points for the transparent hook.
- `Loretoken-GPU/src/production_cuda_hook.cpp` – production hook with integrated decode.
- `Loretoken-GPU/src/test_production_hook.py` – end-to-end PyTorch demo using the hook.
