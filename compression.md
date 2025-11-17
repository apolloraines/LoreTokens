\# LoreTokens Compression (LT\_Compression)



LoreTokens are not “just another ZIP.”  

They are a \*\*semantic compression layer\*\* for AI systems: instead of compressing bytes, they compress \*\*meaning\*\*.



This document explains:



\- What LoreToken compression is

\- How it differs from traditional compression (ZIP, gzip, zstd, etc.)

\- How it interacts with models and SAIQL

\- How to think about compression ratios in a semantic world



> TL;DR: LoreTokens trade “more bytes” for “more understanding.”  

> Traditional codecs compress data. LoreTokens compress \*knowledge\* and \*behavior\*.



---



\## 1. What LoreToken Compression Actually Is



In the LoreToken stack, “compression” means:



> Representing \*\*large, reusable blocks of knowledge, structure, and behavior\*\* as \*\*compact symbolic tokens\*\* that models and engines can interpret directly, without expanding back to full natural language.



A LoreToken file (for example, `datasets/Schema-LoreTokenised.txt`) doesn’t store raw text like a .txt or .json file. Instead, it stores:



\- \*\*Symbolic identifiers\*\* (LoreTokens)  

\- \*\*Relations\*\* between those tokens (graph-like structure)

\- \*\*Roles and behaviors\*\* attached to tokens (what to do with them)

\- \*\*Context hooks\*\* so models can “unpack” only what they need, when they need it



From a model’s perspective:



\- A few hundred or thousand LoreTokens can stand in for:

&nbsp; - Hundreds of thousands of words of documentation

&nbsp; - Thousands of lines of spec / schema / narrative

&nbsp; - Deep historical and behavioral context that would normally blow up the context window



The key difference:  

\*\*Models can work directly on LoreTokens\*\* — they don’t need everything decompressed back into full natural language first.



---



\## 2. Semantic vs. Traditional Compression



\### 2.1 Traditional Compression (zip, gzip, zstd, etc.)



Traditional compression algorithms (ZIP, gzip, zstd, LZMA, bzip2, etc.) are:



\- \*\*Lossless\*\*: You can reconstruct the exact original bytes.

\- \*\*Syntactic\*\*: They operate on patterns of bits/bytes/characters, not meaning.

\- \*\*Entropy-focused\*\*: Their primary job is to approach the theoretical entropy limit of the data stream.



Characteristics:



\- Great at shrinking redundant text, logs, binaries, archives.

\- Useless to a model \*\*until fully decompressed\*\*.

\- Optimized for \*\*storage and bandwidth\*\*, not cognition.



\### 2.2 Semantic Compression (LoreTokens)



“Semantic compression” is different:



> Instead of compressing the \*surface form\* of data (bytes), we compress the \*\*underlying meaning and structure\*\*.



In practical terms:



\- A single LoreToken can reference:

&nbsp; - An entire concept (e.g., “short-term trend evaluation logic for crypto markets”)

&nbsp; - A set of rules or behaviors

&nbsp; - A subsystem of an AI (identity, ethics, strategy, memory schema, etc.)

\- A small LoreToken file can represent:

&nbsp; - Tens of thousands of pages of human-readable explanation, architecture, and history (if expanded back to prose)

&nbsp; - A complete operational blueprint of an AI system



\*\*Important difference:\*\*  

Traditional compression must be \*\*fully decompressed\*\* before use.  

LoreTokens are designed so AI systems (LLMs, SAIQL, custom engines) can \*\*use them while compressed\*\* – only expanding details as needed.



---



\## 3. How LoreToken Compression Works at a High Level



LoreTokens implement semantic compression in three main ways:



\### 3.1 Symbolic Snapshots



LoreTokens capture \*\*snapshots of knowledge and behavior\*\* using compact symbolic patterns, for example:



```text

LORETOKEN.CONCEPT.DEFINITION:\[self\_compressing\_self\_referencing\_ai\_system+symbolic\_memory\_snapshots+meaning\_compression\_not\_entropy>>cognitive\_framework\_compression,CLAIMED]



\## 10. How LoreTokens Cut GPU Compute (and Power) by ~70%



LoreTokens reduce GPU usage in three main ways:



1\. \*\*Shorter prompts (fewer tokens per call)\*\*  

2\. \*\*Fewer calls (less repeated reasoning)\*\*  

3\. \*\*Smarter division of labor between SAIQL (CPU) and the model (GPU)\*\*  



Taken together, this is what drives \*\*~70% less LLM-side compute\*\* in our reference pipelines, which shows up directly as lower GPU power draw.



---



\### 10.1 Where GPU Time Actually Goes in an LLM



For a transformer-style model, most of the heavy GPU work scales with:



\- \*\*Sequence length `n`\*\* (number of tokens in the context)

\- \*\*Hidden dimension \& layers\*\* (fixed for a given model)

\- \*\*Number of calls\*\* you make



Roughly:



\- Attention cost scales as \*\*O(n²)\*\* per layer  

\- Feed-forward / MLP cost scales as \*\*O(n)\*\* per layer  

\- Total generation cost ≈ \*layers × (attention + MLP) × tokens\*



So if you:



\- Cut the \*\*number of tokens\*\* per request,  

\- And cut the \*\*number of requests\*\*,  



you reduce both the \*\*time\*\* and \*\*energy\*\* the GPU spends per task.



---



\### 10.2 How LoreTokens Shorten Contexts



Without LoreTokens, a typical “smart agent” stack does something like:



1\. Fetch a lot of previous chat history, notes, and docs.

2\. Chunk them, embed them, retrieve top-K.

3\. Stuff the top-K chunks back into the LLM as raw text.

4\. Let the model re-read and re-interpret all of that every time.



This inflates `n` (context length) constantly.



With LoreTokens:



1\. Long-term knowledge is periodically \*\*compressed into LoreToken form\*\*:

&nbsp;  - Concepts, entities, rules, history, schemas, preferences.

2\. On each request:

&nbsp;  - SAIQL queries a small \*\*LoreToken subset\*\* (graph of meaning, not huge text blobs).

&nbsp;  - The model sees a \*\*short symbolic scaffold\*\* instead of pages of prose.



\## 11. Meaning vs Description: The Stop Sign in Plain Terms



The easiest way to understand LoreTokens is to think about a \*\*stop sign\*\*.



\### 11.1 How we normally explain a stop sign



If you \*can’t\* show someone a stop sign, you have to describe it with words:



> “It’s a red, octagon-shaped sign with white letters that say STOP, usually placed at intersections. When you see it, you must come to a complete stop, check for traffic, then proceed according to right-of-way rules…”



That’s a lot of text just to communicate one simple idea:  

\*\*“When you see this thing, you must stop here.”\*\*



LLMs work the same way with plain natural language:



\- You burn many tokens \*\*describing\*\* the thing.

\- Each time, the model has to re-read and re-interpret that description.



\### 11.2 What LoreTokens do differently



With LoreTokens, you don’t keep re-describing the stop sign.



Instead, you give the model a \*\*single compact handle\*\* that already \*means\*:



> “This is a stop sign. Vehicles must stop here, follow right-of-way rules, and bad things happen if they ignore it.”



In human terms:



\- Natural language = \*\*explaining\*\* a stop sign over and over.

\- LoreToken = \*\*showing\*\* the stop sign once, then just pointing at it.



Once the model has learned what that LoreToken stands for, you no longer need the whole paragraph.  

You just reference the one symbol, and the model can:



\- Reason about what a driver should do

\- Simulate different traffic situations

\- Explain the rule in English, Spanish, etc.



…without you paying for the big explanation every time.



\### 11.3 Why that saves so many tokens (and power)



For the model, this is where the savings come from:



\- With plain text:

&nbsp; - Every context has to include long descriptions of concepts, rules, background, history, etc.

\- With LoreTokens:

&nbsp; - Those concepts are compressed into \*\*short, reusable symbols\*\*.

&nbsp; - The model sees a tiny symbol instead of a long paragraph.

&nbsp; - It only expands details when needed for the current answer.



So instead of:



> “Here are three paragraphs reminding you what a stop sign is, plus extra explanation about traffic law…”



you send:



> “Here is the STOP\_SIGN concept you already know. Use it in this situation.”



That’s the essence of semantic compression:



\- Traditional methods shrink the \*sentence\* that describes the sign.  

\- LoreTokens give the model a \*\*direct shortcut to the meaning\*\* of the sign, so you don’t need the sentence at all.



