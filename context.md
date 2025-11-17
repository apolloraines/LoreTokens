# Rollover Context with SAIQL Backing

Token windows are finite, but Nova uses LoreTokens plus SAIQL to give the illusion of “unlimited” context. The process resembles a circular buffer backed by a database:

1. **Active context window** – Keep only the most relevant N messages/records in the live prompt (e.g., 16K tokens).
2. **Rollover** – As soon as the window overflows, serialize the overflow slice into LoreTokens and insert it into a SAIQL table (e.g., `conversation_history`).
3. **Index linkage** – Each LoreToken block stores a monotonic range ID + metadata (topic, user, tags) so you can fetch it later via SAIQL.
4. **On-demand recall** – When the user references earlier content (“Remind me what we decided last week”), query SAIQL by metadata or range, fetch the relevant LoreTokens, and hydrate them back into the prompt.
5. **Window re-entry** – Only the necessary rows are reinserted into the active context, preserving tokens for the new query.

## Implementation Sketch

```python
from saiql.loretoken_engine import get_engine
from saiql.loretoken_symbolic import SymbolicLoreToken

engine = get_engine("/mnt/nova_memory/nova_saiql.db")

ACTIVE_WINDOW = []
WINDOW_LIMIT = 16000  # tokens

# When you add a message:
def add_message(role, content):
    ACTIVE_WINDOW.append({"role": role, "content": content})
    if token_count(ACTIVE_WINDOW) > WINDOW_LIMIT:
        rollover_chunk = ACTIVE_WINDOW[:-1]
        ACTIVE_WINDOW[:] = ACTIVE_WINDOW[-1:]
        store_rollover(rollover_chunk)


def store_rollover(messages):
    payload = SymbolicLoreToken.encode("CONTEXT", "ROLL", {
        "messages": json.dumps(messages),
        "range_id": next_range_id(),
    }, status="ACTIVE")
    engine.insert("context_rollover", {
        "range_id": current_range,
        "payload": payload,
    })


def recall(range_id):
    row = engine.select_one("context_rollover", range_id=range_id)
    context = json.loads(row.payload_decoded)
    ACTIVE_WINDOW[:0] = context  # prepend if needed
```

## Why It Works

- **LoreToken serialization** keeps rollover slices compact; storing millions of tokens becomes cheap.
- **SAIQL indexing** makes retrieval deterministic—no vector search required unless you want semantic similarity.
- **Deterministic re-entry** means prompts remain stable. You only expand the window when a query explicitly references older info.

## Practical Tips

- Track `range_id` per user/session so you can walk history chronologically or jump to tagged segments (e.g., “Milestone Decisions”).
- Combine with Claude/Grok system prompts such as “Context may be partially loaded; ask `/recall` if something is missing.”
- Use metadata columns (topic, priority) to prefetch likely-needed slices when a new task starts.

With this rollover pattern, context size is bounded by storage, not by the model’s native window. Use a smaller, cheaper LLM with LoreToken-backed SAIQL and regain unlimited memory without paying for 1M-token contexts.
