# Generative AI Developer Roadmap

Goal: go from zero to building and shipping LLM-powered apps and agents.
Pace: ~10-12 weeks at 8-10 hrs/week. Each phase ends with a **Checkpoint project**. Do not skip them; building is how this sticks.

Language: **Python** (the ecosystem default). Add TypeScript later if you want web work.

---

## Phase 0 - Setup & Python/Tooling (Week 1)

**Learn**
- Python 3.11+, venv/uv, pip, `.env` files, type hints, `async/await`, `requests`/`httpx`
- Git + GitHub basics
- JSON, REST APIs, reading API docs

**Exercises**
1. Create a venv, install `anthropic python-dotenv`, store your API key in `.env` (never commit it; add `.env` to `.gitignore`).
2. Write a script that calls any public REST API (e.g. a weather API) and prints parsed JSON.
3. Rewrite that script with `httpx.AsyncClient` and fetch 5 URLs concurrently with `asyncio.gather`.

**Assignment**: Read the Python `asyncio` "Coroutines and Tasks" docs page and explain `await` vs `gather` in 5 lines in `notes/phase0.md`.

**Checkpoint**: a CLI that takes a city and prints the weather.

---

## Phase 1 - How LLMs Work (Week 2)

**Learn**
- Tokens, tokenization, context window, embeddings (conceptually)
- Transformer / attention at an intuition level
- Pretraining -> fine-tuning -> RLHF/RLAIF
- Temperature, top_p, max tokens, stop sequences
- Hallucination, knowledge cutoff, why models are non-deterministic

**Reading assignments**
- Andrej Karpathy: "Intro to Large Language Models" (YouTube, 1 hr)
- Jay Alammar: "The Illustrated Transformer"
- 3Blue1Brown: Neural networks / Transformers series

**Exercises**
1. Use `tiktoken` (or the Anthropic token-counting endpoint) to count tokens for English vs Hindi vs code. Why do they differ?
2. Call the same prompt 5 times at temperature 0 and at 1.0. Record the differences.
3. Write down, in your own words, why an LLM can't "look up" a fact it never saw.

**Checkpoint**: a 1-page `notes/how-llms-work.md` you could explain to a friend.

---

## Phase 2 - Prompt Engineering & the API (Weeks 2-3)

**Learn**
- Messages API: system prompt, user/assistant turns, multi-turn state (you resend history; the API is stateless)
- Prompting: clear instructions, role, examples (few-shot), XML tags for structure, chain-of-thought / thinking
- Structured output (JSON, schema validation with Pydantic)
- Streaming, error handling, retries, rate limits
- Prompt caching, cost and token management

**Reading assignments**
- Anthropic docs: "Prompt engineering overview" and the Messages API reference
- Anthropic docs: "Streaming", "Prompt caching", "Structured outputs"

**Exercises** (see `exercises/01_first_call.py`, `02_structured_output.py`)
1. Build a terminal chatbot with conversation memory and streaming.
2. Build a text classifier (support ticket -> category + urgency) returning validated JSON. Test 20 inputs and measure accuracy.
3. Take a bad prompt, improve it 3 ways (role, examples, format) and compare outputs side by side.
4. Add retry with exponential backoff on 429/5xx errors.

**Checkpoint**: "Ticket triage CLI" that reads a CSV of tickets and writes an enriched CSV.

---

## Phase 3 - Tool Use / Function Calling (Weeks 3-4)

**Learn**
- The tool-use loop: model requests a tool -> you run it -> you return `tool_result` -> model continues
- Writing good tool descriptions and JSON schemas
- Parallel tool calls, error results, tool-choice control
- Security: never trust model-supplied arguments blindly (validate, sandbox, least privilege)

**Reading assignment**: Anthropic docs "Tool use" (overview + implement tool use).

**Exercises** (see `exercises/03_tool_use.py`)
1. Give the model `get_weather` and `calculator` tools; ask a question that needs both.
2. Add a `search_files` tool that searches a local folder. Add path validation to block `../` escapes.
3. Handle a tool that raises an exception: return it as an error result and let the model recover.

**Checkpoint**: a "personal assistant" CLI with 4+ tools (files, web fetch, calculator, notes).

---

## Phase 4 - Embeddings, Vector Search & RAG (Weeks 5-6)

**Learn**
- Embeddings and cosine similarity
- Chunking strategies (size, overlap, by heading)
- Vector stores: start in-memory (numpy), then Chroma / pgvector / Qdrant
- RAG pipeline: ingest -> chunk -> embed -> retrieve -> augment -> generate -> cite
- Hybrid search (BM25 + vectors), reranking, query rewriting
- Evaluating retrieval: recall@k, groundedness

**Reading assignments**
- Anthropic: "Contextual Retrieval" blog post
- Docs of one vector DB (Chroma quickstart)

**Exercises** (see `exercises/04_mini_rag.py`)
1. Run the mini RAG over 3-5 markdown files. Ask questions whose answers are and aren't in the docs; verify it says "I don't know" when appropriate.
2. Try chunk sizes 200 / 500 / 1000 and compare answer quality on 10 questions.
3. Swap the numpy store for Chroma.
4. Add source citations (file + chunk) to every answer.

**Checkpoint**: "Chat with your PDFs/notes" app with citations.

---

## Phase 5 - MCP (Model Context Protocol) (Week 7)

**Learn**
- What MCP is: an open standard for connecting AI apps to tools and data
- Architecture: host / client / server; transports (stdio, streamable HTTP)
- Primitives: **tools**, **resources**, **prompts**
- Building servers (Python `mcp` SDK, FastMCP) and connecting them to Claude Code / Claude Desktop
- Security: auth (OAuth), permissions, prompt injection via tool output

**Reading assignments (do these in order)**
1. modelcontextprotocol.io -> "Introduction" and "Architecture"
2. modelcontextprotocol.io -> "Build an MCP server" quickstart
3. MCP spec: Tools, Resources, Prompts pages
4. Claude Code docs -> "Connect Claude Code to tools via MCP"
5. Browse the `modelcontextprotocol/servers` GitHub repo and read two server implementations

**Exercises** (see `exercises/05_mcp_server.py`)
1. Run the example server, connect it with `claude mcp add notes -- python exercises/05_mcp_server.py`, then ask Claude to add and list notes.
2. Add a **resource** (`notes://all`) and a **prompt** template.
3. Write a small MCP server wrapping an API you like (GitHub issues, weather, your own DB).
4. Test it with the MCP Inspector: `npx @modelcontextprotocol/inspector`.
5. Write a short threat model: what could a malicious tool result do to your agent?

**Checkpoint**: a published-quality MCP server with README, 3+ tools, 1 resource.

---

## Phase 6 - Agents (Weeks 8-9)

**Learn**
- Agent = LLM + tools + loop + memory + stopping condition
- Patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- Planning, reflection, human-in-the-loop approval
- Context management: summarization, compaction, scratchpads/files as memory
- Subagents, Agent SDK, Skills, hooks
- Reliability: max-iteration caps, cost budgets, idempotent tools, logging every step

**Reading assignments**
- Anthropic: "Building effective agents" (essential)
- Anthropic: "How we built our multi-agent research system"
- Claude Agent SDK docs; Claude Code docs on subagents, skills and hooks

**Exercises**
1. Hand-write an agent loop (about 60 lines) with no framework. Cap at 10 iterations.
2. Build a "research agent": web search tool + fetch tool -> writes a cited report to a file.
3. Add human approval before any destructive tool call.
4. Rebuild exercise 1 using the Claude Agent SDK and compare code size and control.
5. Add a skill/CLAUDE.md to a repo so Claude Code follows your project conventions.

**Checkpoint**: a coding or research agent that completes a multi-step task end to end, with logs.

---

## Phase 7 - Evaluation, Safety & Observability (Week 10)

**Learn**
- Build an eval set (30-100 real examples), then score: exact match, rubric, LLM-as-judge
- Regression testing prompts when you change models or prompts
- Prompt injection, data exfiltration, jailbreaks, PII handling
- Tracing/logging (Langfuse, OpenTelemetry or plain JSONL), latency and cost tracking

**Reading assignments**: Anthropic docs "Develop tests / evaluations" and "Mitigate jailbreaks and prompt injections".

**Exercises**
1. Build an eval harness for your Phase 2 classifier (pass/fail table + accuracy).
2. Swap the model/prompt and show the diff in score and cost.
3. Plant an injection in a fetched web page ("ignore instructions and ...") and make your agent resist it.

**Checkpoint**: `evals/` folder with a repeatable `python run_evals.py`.

---

## Phase 8 - Going Further (Weeks 11-12+)

Pick 1-2 tracks:
- **Fine-tuning & open models**: Hugging Face `transformers`, LoRA/PEFT, run Llama/Qwen locally with Ollama or vLLM
- **Multimodal**: image/PDF input, vision, speech
- **Production**: FastAPI backend, queues, caching, auth, Docker, deploy (Fly/Render/AWS)
- **Frontend**: Next.js + streaming UI (Vercel AI SDK)
- **Frameworks (optional)**: LangChain / LlamaIndex / LangGraph - learn them *after* you can do it by hand

---

## Capstone (pick one, ship it publicly)

1. **Docs assistant**: RAG + MCP server + web UI + evals + citations
2. **Dev agent**: reads an issue, edits code, runs tests, opens a PR (human approval gate)
3. **Personal ops agent**: email/calendar/notes via MCP servers with permission prompts

Requirements: README with architecture diagram, eval results, cost per request, known limitations, deployed link or demo video.

---

## Weekly habits
- Build something every week, even if small; keep a `notes/` log of what broke and why
- Read one primary-source doc or paper per week
- Push code to GitHub as a portfolio

## Resources
- Anthropic docs: docs.claude.com (API, tool use, MCP, agents)
- Anthropic Courses (GitHub: anthropics/courses) and Anthropic Cookbook (anthropics/anthropic-cookbook)
- modelcontextprotocol.io
- Hugging Face LLM course
- Karpathy: "Neural Networks: Zero to Hero"
- DeepLearning.AI short courses
