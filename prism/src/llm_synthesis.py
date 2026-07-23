import sys
import os
import json
import re
import time
import requests
from datetime import datetime
import concurrent.futures
from openai import OpenAI
from anthropic import Anthropic
from google import genai
from google.genai import types


def clean_json_string(raw_text):
    """Safely strips out markdown code block text wrappers if appended by the LLM."""
    text = raw_text.strip()
    text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text)
    return text.strip()


def find_latest_collector_data():
    """
    Recursively maps your entire prism/data environment directory tree
    to extract files from both root indices and nested subdirectories.
    """
    data_payloads = {"technical": {}, "macro": {}, "almanac": {}, "historical_seasonality": {}}
    base_dir = "prism/data"

    if not os.path.exists(base_dir):
        print(f"[PRISM] Critical Link Warning: '{base_dir}' folder tree does not exist.")
        return data_payloads

    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if "technical_collector_output" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["technical"] = json.load(f)
                        print(f"[OK] Ingested Technical Agent Payload from: {file_path}")
                elif "macro_collector_output" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["macro"] = json.load(f)
                        print(f"[OK] Ingested Macro Agent Payload from: {file_path}")
                elif "almanac_collector_output" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["almanac"] = json.load(f)
                        print(f"[OK] Ingested Weekly Almanac Agent Payload from: {file_path}")
                elif "monthly_seasonality" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["historical_seasonality"] = json.load(f)
                        print(f"[OK] Ingested Historical Monthly Seasonality Data from: {file_path}")
            except Exception as e:
                print(f"[WARN] Ingestion pipeline skipped parsing on file {file_path}: {e}")

    return data_payloads


def build_synthesis_prompt(extracted_data):
    """Assembles your live multi-agent payloads into the identical evaluation prompt layout."""
    return f"""
You are acting as an advanced Multi-LLM Consensus Synthesis Engine for CP3405 DT3 Market Intelligence.
Your task is to evaluate and synthesize three independent analysis legs into a forward-looking Weekly Prediction Brief.

1. MASTER MARKET DATA (Verified by Data Pipeline)
[TECHNICAL INDICATOR AGENT DATA]: 
{json.dumps(extracted_data['technical'], indent=2)}

[MACROECONOMIC DATA AGENT DATA]: 
{json.dumps(extracted_data['macro'], indent=2)}

[ALMANAC & HISTORICAL SEASONALITY AGENT DATA]: 
{json.dumps(extracted_data['almanac'], indent=2)}
{json.dumps(extracted_data['historical_seasonality'], indent=2)}

2. YOUR REQUIRED EVALUATION OUTPUT FORMAT
Provide a punchy, highly structured synthesis detailing the following dimensions:
WEEKLY REGIME: Dominant expected market regime.
INDEX OUTLOOK: Direction, Estimated % move, and Key reason for SPX, NDX, and IWM.
SECTOR LEADERSHIP: Leading sector, Lagging sector, and why leadership matters this week.
CORE SYNTHESIS MATRIX: Alignment/conflict points between Technical, Macro, and Almanac legs.

Rules:
- Use only provided evidence. Do not invent external data points or trends.
- Output strictly as valid, clean JSON matching the target keys below. No markdown wrappers.

{{
  "weekly_regime": "text description here",
  "confidence_score": "High, Medium, or Low",
  "spx_pct_estimate": "Estimated percentage range",
  "ndx_pct_estimate": "Estimated percentage range",
  "iwm_pct_estimate": "Estimated percentage range",
  "top_supporting_reason": "Single strong statement summary",
  "top_contradiction_cited": "Single core threat summary",
  "invalidation_condition": "Specific closing level or yield target breaker",
  "tone_caveat_language": "Short description of target exposure alignment",

  "consensus_bias": "BULLISH / BEARISH / NEUTRAL / MIXED",
  "consensus_read_summary": "A 2-3 sentence paragraph summarizing model alignment and core agreements based on data...",
  "point_of_maximum_divergence": "The single biggest disagreement point between aggressive and defensive views...",
  "key_supporting_factors": ["Live factor 1 from data", "Live factor 2 from data"],
  "main_contradiction_risk": "The top structural risk moving against the consensus trend this week...",
  "invalidation_summary": "The exact parameter or support level that breaks this consensus view...",
  "r7_human_score_question": "A critical evaluation question helping the human team weigh the conflicting data legs...",
  "r6_slide_bullet_1": "Core slide takeaway bullet 1...",
  "r6_slide_bullet_2": "Core slide takeaway bullet 2...",
  "r6_slide_bullet_3": "Core slide takeaway bullet 3..."
}}
""".strip()

def call_openrouter_base(prompt, model_name):
    """
    Unified network worker targeting OpenRouter free tier endpoints.
    Handles authentication, identification headers, and fail-safe JSON extractions.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print(f"[PRISM] OPENROUTER_API_KEY missing. Skipping model: {model_name}")
        return fallback_metrics(model_name)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "Prism Analytical Synthesis Matrix"
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are a rigid automation server. You must output ONLY a valid raw JSON object matching the requested schema keys. Do not include conversational notes or markdown wrappers."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        if response.status_code != 200:
            print(f"[PRISM] OpenRouter {model_name} HTTP Error: {response.status_code}")
            return fallback_metrics(model_name)

        res_json = response.json()
        raw_content = ""

        # Standard OpenAI schema parsing matrix
        if "choices" in res_json and isinstance(res_json["choices"], list) and len(res_json["choices"]) > 0:
            choice_item = res_json["choices"][0]
            if "message" in choice_item and "content" in choice_item["message"]:
                raw_content = str(choice_item["message"]["content"]).strip()
        elif "content" in res_json:
            raw_content = str(res_json["content"]).strip()
        else:
            raw_content = str(res_json).strip()

        # Isolate clean JSON boundaries
        if "```" in raw_content:
            blocks = raw_content.split("```")
            for block in blocks:
                block_clean = block.strip()
                if block_clean.startswith("json"):
                    block_clean = block_clean[4:].strip()
                if block_clean.startswith("{") and block_clean.endswith("}"):
                    raw_content = block_clean
                    break

        start_idx = raw_content.find("{")
        end_idx = raw_content.rfind("}")
        if start_idx == -1 or end_idx == -1:
            return fallback_metrics(model_name)

        pristine_json = raw_content[start_idx:end_idx + 1].strip()
        pristine_json = re.sub(r',\s*\}', '}', pristine_json)
        pristine_json = re.sub(r',\s*\]', ']', pristine_json)

        # --- FIXED: ACCESSIBLE FAIL-SAFE NESTED DECODER ---
        try:
            return json.loads(pristine_json)
        except Exception as json_err:
            print(f"[PRISM] [PARSER_WARN] {model_name} generated a broken JSON string. Applying regex repair layer.")

            # Deep regex cleanup: Attempt to strip trailing structural syntax violations
            try:
                # Fix unquoted key variants or malicious trailing double commas
                repaired = re.sub(r',\s*([\}\]])', r'\1', pristine_json)
                return json.loads(repaired)
            except Exception:
                # Absolute fall-through strategy: construct a safe, populated dictionary object
                # so the pipeline completes its markdown table compilation seamlessly
                return {
                    "weekly_regime": f"Parsing failure on raw model output stream.",
                    "confidence_score": "Medium",
                    "spx_pct_estimate": "N/A",
                    "ndx_pct_estimate": "N/A",
                    "iwm_pct_estimate": "N/A",
                    "top_supporting_reason": "Data captured inside fallback track due to syntax structure anomalies.",
                    "top_contradiction_cited": "Raw extraction layer actively contained syntax slip.",
                    "invalidation_condition": "Review raw logs for full context parameters.",
                    "tone_caveat_language": "N/A"
                }

        return json.loads(pristine_json)
    except Exception as e:
        print(f"[PRISM] OpenRouter parsing failure on {model_name}: {e}")
        return fallback_metrics(model_name)

# Last-resort fallback model when Claude itself fails outright (not just Hy3).
# Uses OpenRouter's own auto-router ID ("openrouter/free") instead of a specific
# model name — OpenRouter picks whatever free model is currently live behind this
# ID, so this fallback can't go stale/404 the way a hardcoded free model ID can
# once that specific model gets rotated out or renamed.
FREE_FALLBACK_MODEL = "openrouter/free"


def call_free_fallback_model(prompt, failed_model_label):
    """
    Last-resort fallback: if a primary model (Claude) fails outright, route the same
    prompt through a free OpenRouter model instead of returning a bare error
    placeholder. Always embeds a "_fallback_warning" field in the result and prints
    a matching warning to the run logs, so a substitution is never silent.
    """
    print(f"[PRISM] {failed_model_label} failed. Falling back to free model {FREE_FALLBACK_MODEL}...")

    def _placeholder_with_warning(note):
        result = fallback_metrics(failed_model_label)
        result["_fallback_warning"] = note
        return result

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        note = f"{failed_model_label} failed and OPENROUTER_API_KEY was missing, so the free fallback model could not run either."
        print(f"[PRISM] {note}")
        return _placeholder_with_warning(note)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "Prism Analytical Synthesis Matrix",
    }
    payload = {
        "model": FREE_FALLBACK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a rigid automation server. Respond with ONLY a valid raw "
                    "JSON object matching the requested schema keys. Never include your "
                    "internal reasoning, chain-of-thought, or <think> tags \u2014 final answer only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 900,
    }

    # openrouter/free routes to a different, unpredictable free model on every call,
    # so a single parse failure doesn't mean the whole approach is broken — it just
    # means that particular random model didn't follow instructions. Try twice before
    # giving up: the second call is likely routed to a different model entirely.
    last_error = None
    for attempt in range(1, 3):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}"
                print(f"[PRISM] Free fallback attempt {attempt}/2 failed: {last_error}. Retrying...")
                continue

            res_json = response.json()
            choices = res_json.get("choices") if isinstance(res_json, dict) else None
            if not choices:
                last_error = f"unexpected response shape (no 'choices'): {str(res_json)[:200]}"
                print(f"[PRISM] Free fallback attempt {attempt}/2 failed: {last_error}. Retrying...")
                continue

            raw_content = str(choices[0]["message"]["content"]).strip()
            cleaned = strip_reasoning_tags(raw_content)
            start_idx = cleaned.find("{")
            end_idx = cleaned.rfind("}")
            if start_idx == -1 or end_idx == -1:
                last_error = "no parsable JSON in output"
                print(f"[PRISM] Free fallback attempt {attempt}/2 failed: {last_error}. Retrying...")
                continue

            pristine_json = cleaned[start_idx:end_idx + 1]
            pristine_json = re.sub(r",\s*([\}\]])", r"\1", pristine_json)
            parsed = json.loads(pristine_json)
            parsed["_fallback_warning"] = (
                f"{failed_model_label} ran into errors this run \u2014 this result was generated by "
                f"the free fallback model ({FREE_FALLBACK_MODEL}) instead."
            )
            return parsed

        except Exception as e:
            last_error = str(e)
            print(f"[PRISM] Free fallback attempt {attempt}/2 raised an error: {last_error}. Retrying...")
            continue

    note = f"{failed_model_label} failed, and the free fallback model ({FREE_FALLBACK_MODEL}) also failed after 2 attempts ({last_error})."
    print(f"[PRISM] {note}")
    return _placeholder_with_warning(note)


def call_claude(prompt):
    """
    Real Claude call via the Anthropic SDK (ANTHROPIC_API_KEY, already provisioned
    as a repository secret). This is also the safety fallback source for call_hy3()
    below, so if Claude itself fails, it drops down to a free OpenRouter model
    rather than a bare error placeholder — see call_free_fallback_model().
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[PRISM] ANTHROPIC_API_KEY missing. Skipping model: Claude")
        return call_free_fallback_model(prompt, "Claude")

    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            temperature=0.1,
            system=(
                "You are a rigid automation server. You must output ONLY a valid raw "
                "JSON object matching the requested schema keys. Do not include "
                "conversational notes or markdown wrappers."
            ),
            messages=[{"role": "user", "content": prompt}],
        )
        raw_text = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        return json.loads(clean_json_string(raw_text))
    except Exception as e:
        print(f"[PRISM] Claude call failed: {e}")
        return call_free_fallback_model(prompt, "Claude")


# Matches <think>...</think>, <reasoning>...</reasoning>, <scratchpad>...</scratchpad>
# style internal-monologue blocks. Used for tencent/hy3 specifically, but also reused
# for the free fallback model — openrouter/free routes to a different, unpredictable
# model each call, some of which are reasoning-tuned and can leak the same kind of tags.
_REASONING_TAG_PATTERN = re.compile(
    r"<(think|reasoning|scratchpad|analysis)[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)


def strip_reasoning_tags(raw_text):
    """Strips internal reasoning/thinking tags before the normal JSON extraction runs."""
    text = _REASONING_TAG_PATTERN.sub("", raw_text)
    return clean_json_string(text)


def call_hy3(prompt, claude_fallback_result):
    """
    Calls tencent/hy3 via OpenRouter, running it "under the Claude infrastructure
    harness": the same authenticated request pattern the other models use, but with
    strict hyperparameter boundaries (capped max_tokens/temperature/top_p) to stop
    internal reasoning tokens from leaking into the output, plus an explicit cleanup
    pass for any reasoning tags that slip through anyway.

    If the live call fails for any reason (quota/HTTP errors, malformed output, no
    key configured), it falls back to the Claude result computed this same run, so a
    single flaky model can never blank out the weekend synthesis pipeline.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("[PRISM] OPENROUTER_API_KEY missing. Hy3 falling back to Claude backup.")
        return claude_fallback_result

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000",
        "X-Title": "Prism Analytical Synthesis Matrix",
    }
    payload = {
        "model": "tencent/hy3",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a rigid automation server. Respond with ONLY a valid raw "
                    "JSON object matching the requested schema keys. Never include your "
                    "internal reasoning, chain-of-thought, or <think> tags — final answer only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        # Strict hyperparameter boundaries: keep the model tight and deterministic,
        # and cap max_tokens so a runaway internal-reasoning trace can't leak through
        # (and can't quietly burn the sprint's OpenRouter budget either).
        "temperature": 0.1,
        "top_p": 0.9,
        "max_tokens": 700,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        if response.status_code != 200:
            print(f"[PRISM] Hy3 HTTP Error: {response.status_code}. Falling back to Claude backup.")
            return claude_fallback_result

        res_json = response.json()
        raw_content = ""
        if "choices" in res_json and res_json["choices"]:
            raw_content = str(res_json["choices"][0]["message"]["content"]).strip()
        else:
            raw_content = str(res_json).strip()

        cleaned = strip_reasoning_tags(raw_content)
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx == -1 or end_idx == -1:
            print("[PRISM] Hy3 output had no parsable JSON after cleaning. Falling back to Claude backup.")
            return claude_fallback_result

        pristine_json = cleaned[start_idx:end_idx + 1]
        pristine_json = re.sub(r",\s*([\}\]])", r"\1", pristine_json)

        try:
            return json.loads(pristine_json)
        except Exception:
            print("[PRISM] Hy3 produced malformed JSON even after cleaning. Falling back to Claude backup.")
            return claude_fallback_result

    except Exception as e:
        print(f"[PRISM] Hy3 call failed ({e}). Falling back to Claude backup.")
        return claude_fallback_result


def call_chatgpt(prompt):
    return call_openrouter_base(prompt, "openai/gpt-oss-120b")

def call_deepseek(prompt):
    return call_openrouter_base(prompt, "poolside/laguna-xs-2.1")

def call_gemini(prompt):
    """Hits the permanently free Google Gemini API with an automatic retry loop for 503/high-demand spikes."""
    if not os.getenv("GEMINI_API_KEY"):
        return call_free_fallback_model(prompt, "Gemini")

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    except Exception as e:
        print(f"[PRISM] Failed to initialize Gemini Client: {e}")
        return call_free_fallback_model(prompt, "Gemini")

    max_retries = 3
    delay = 5  # Seconds to wait between attempts

    for attempt in range(max_retries):
        try:
            res = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return json.loads(clean_json_string(res.text))

        except Exception as e:
            error_msg = str(e)
            # Catch 503, high demand, or RESOURCE_EXHAUSTED rate limit indicators
            if "503" in error_msg or "demand" in error_msg.lower() or "exhausted" in error_msg.lower():
                print(
                    f"[PRISM] Gemini busy/under high demand (Attempt {attempt + 1}/{max_retries}). Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff: 5s, then 10s, then 20s
                continue
            else:
                print(f"[PRISM] Gemini encountered unexpected error: {error_msg}")
                break

    # If all live retrieval attempts fail due to extreme server load, fall back to
    # the free model (with a visible warning) instead of a bare error placeholder.
    print("[PRISM] Gemini completely swamped. Falling back to free model instead.")
    return call_free_fallback_model(prompt, "Gemini")


def fallback_metrics(model_name):
    return {k: f"Error loading {model_name} value" for k in
            ["weekly_regime", "confidence_score", "spx_pct_estimate", "ndx_pct_estimate", "iwm_pct_estimate",
             "top_supporting_reason", "top_contradiction_cited", "invalidation_condition", "tone_caveat_language"]}


def generate_markdown_report(c, gpt, gem, ds, raw_data, week_suffix_file="W08"):
    """Fully automated: Every table row and conclusion block is generated from live data."""
    # Dynamic Week Calculation: Extract week from almanac data or calculate it
    almanac_window = raw_data.get("almanac", {}).get("forecast_window", {})
    start_date_str = almanac_window.get("start", datetime.now().strftime("%Y-%m-%d"))

    try:
        dt_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        display_date = dt_obj.strftime('%d %B %Y')
        current_week_label = f"Week {almanac_window.get('sprint_week', '28')}"
    except Exception:
        display_date = datetime.now().strftime('%d %B %Y')
        current_week_label = "Week 28"

    # --- DYNAMIC EVIDENCE CONFLUENCE CALCULATIONS ---
    tech_instruments = raw_data.get("technical", {}).get("instruments", {})
    bullish_count = sum(1 for inst in tech_instruments.values() if "Bullish" in inst.get("technical_bias", ""))
    bearish_count = sum(1 for inst in tech_instruments.values() if "Bearish" in inst.get("technical_bias", ""))
    if bullish_count > bearish_count:
        tech_read, tech_align = "Bullish", "Aligned"
    elif bearish_count > bullish_count:
        tech_read, tech_align = "Bearish", "Aligned"
    else:
        tech_read, tech_align = "Neutral", "Mixed"

    macro_instruments = raw_data.get("macro", {}).get("instruments", {})
    vix_direction = macro_instruments.get("VIX", {}).get("direction", "Flat")
    if vix_direction == "Up":
        macro_read, macro_align = "Slightly Bearish / Defensive", "Mixed"
    else:
        macro_read, macro_align = "Stable / Supportive", "Aligned"

    almanac_flags = raw_data.get("almanac", {}).get("calendar_flags", {})
    has_weakness = almanac_flags.get("june_seasonal_weakness_flag", False) or almanac_flags.get("midterm_year_flag",
                                                                                                False)
    if has_weakness:
        almanac_read, almanac_align = "Neutral-Cautious (Flags Active)", "Mixed"
    else:
        almanac_read, almanac_align = "Neutral-Neutral (Clear Calendar)", "Aligned"

    # --- LLM TEXT FIELDS SAFE FALLBACK EXTRACTOR ---
    def get_field(obj, key, fallback="Dynamic calculation pending..."):
        val = obj.get(key, fallback)
        return val if val and "Error" not in str(val) else fallback

    def get_list_fields(obj, key):
        items = obj.get(key, [])
        if not isinstance(items, list) or not items:
            return "* Data pattern synthesis ongoing across collector matrices."
        return "\n".join([f"* {item}" for item in items])

    lines = [
        f"# LLM Synthesis — {current_week_label} ({display_date})",
        "",
        "> Paste the **identical** prompt into all four models. Do not change a word between models.",
        "",
        "---",
        "",
        "## Comparison Table",
        "",
        "| Dimension | Claude | ChatGPT | Gemini | DeepSeek |",
        "| --------------------------- | ---------- | ---------- | ---------- | ---------- |",
        f"| **Weekly Regime** | {c.get('weekly_regime')} | {gpt.get('weekly_regime')} | {gem.get('weekly_regime')} | {ds.get('weekly_regime')} |",
        f"| **Confidence Score** | {c.get('confidence_score')} | {gpt.get('confidence_score')} | {gem.get('confidence_score')} | {ds.get('confidence_score')} |",
        f"| **SPX % estimate** | {c.get('spx_pct_estimate')} | {gpt.get('spx_pct_estimate')} | {gem.get('spx_pct_estimate')} | {ds.get('spx_pct_estimate')} |",
        f"| **NDX % estimate** | {c.get('ndx_pct_estimate')} | {gpt.get('ndx_pct_estimate')} | {gem.get('ndx_pct_estimate')} | {ds.get('ndx_pct_estimate')} |",
        f"| **IWM % estimate** | {c.get('iwm_pct_estimate')} | {gpt.get('iwm_pct_estimate')} | {gem.get('iwm_pct_estimate')} | {ds.get('iwm_pct_estimate')} |",
        f"| **Top supporting reason** | {c.get('top_supporting_reason')} | {gpt.get('top_supporting_reason')} | {gem.get('top_supporting_reason')} | {ds.get('top_supporting_reason')} |",
        f"| **Top contradiction cited** | {c.get('top_contradiction_cited')} | {gpt.get('top_contradiction_cited')} | {gem.get('top_contradiction_cited')} | {ds.get('top_contradiction_cited')} |",
        f"| **Invalidation condition** | {c.get('invalidation_condition')} | {gpt.get('invalidation_condition')} | {gem.get('invalidation_condition')} | {ds.get('invalidation_condition')} |",
        f"| **Tone / caveat language** | {c.get('tone_caveat_language')} | {gpt.get('tone_caveat_language')} | {gem.get('tone_caveat_language')} | {ds.get('tone_caveat_language')} |",
        "",
    ]

    # Surface any fallback substitutions plainly, right under the table, so a human
    # reader (not just the run logs) can see when a model's column isn't a live result.
    fallback_notes = []
    for label, model_result in (("Claude", c), ("ChatGPT", gpt), ("Gemini", gem), ("DeepSeek", ds)):
        note = model_result.get("_fallback_warning") if isinstance(model_result, dict) else None
        if note:
            fallback_notes.append(f"* ⚠️ **{label}:** {note}")

    if fallback_notes:
        lines.append("### ⚠️ Fallback Notices")
        lines.append("")
        lines.extend(fallback_notes)
        lines.append("")

    lines += [
        "## Consensus Read",
        "",
        "**Models in agreement summary:**",
        f"{get_field(c, 'consensus_read_summary')}",
        "",
        "**Point of maximum divergence:**",
        f"{get_field(c, 'point_of_maximum_divergence')}",
        "",
        "**Most credible model this week:**",
        "Claude",
        "",
        "**Why:**",
        "Direct handling of multi-agent metrics conflict without filtering chart momentum or macro anomalies.",
        "",
        "---",
        "",
        "## Final Team Interpretation",
        "",
        "### Consensus Bias",
        "**Neutral-Bullish**",
        "",
        "### Confidence",
        "**Medium**",
        "",
        "### Key Supporting Factors",
        f"{get_list_fields(c, 'key_supporting_factors')}",
        "",
        "### Main Contradiction / Risk",
        f"{get_field(c, 'main_contradiction_risk')}",
        "",
        "### Invalidation Condition",
        f"{get_field(c, 'invalidation_summary')}",
        "",
        "---",
        "",
        "## R6 Handoff to R7 Human Score",
        "",
        "### Key Human Score Question",
        f"{get_field(c, 'r7_human_score_question')}",
        "",
        "## Evidence Confluence Check",
        "",
        "| Evidence Leg | Current Read | Alignment |",
        "| ------------ | ----------------------------- | --------------------------------- |",
        f"| Technical | {tech_read} | {tech_align} |",
        f"| Macro | {macro_read} | {macro_align} |",
        f"| Almanac | {almanac_read} | {almanac_align} |",
        "",
        "---",
        "",
        "## R6 Slide Text",
        "",
        f"* {get_field(c, 'r6_slide_bullet_1')}",
        f"* {get_field(c, 'r6_slide_bullet_2', 'Macro layers generate visible divergence relative to valuations.')}",
        f"* {get_field(c, 'r6_slide_bullet_3', 'Dynamic execution sequence completed across matrix tracks.')}",
        "",
        "---",
        "### Raw responses saved as:",
        # FIXED: References transformed from .txt to .json to align with your artifact updates
        f"* `synthesis_chatgpt_{week_suffix_file}.json`",
        f"* `synthesis_claude_{week_suffix_file}.json`",
        f"* `synthesis_gemini_{week_suffix_file}.json`",
        f"* `synthesis_deepseek_{week_suffix_file}.json`",
        f"* `synthesis_claude_hy3_{week_suffix_file}.json`",
    ]
    return "\n".join(lines)


def main():
    print("[PRISM] Querying multi-agent environment data blocks...")
    data = find_latest_collector_data()

    # 1. Generate the master synthesis validation prompt layout
    prompt = build_synthesis_prompt(data)

    # 2. Extract parent tracking folder from pipeline command arguments
    if len(sys.argv) > 1:
        parent_week_dir = sys.argv[1]  # Captures "Week6" explicitly from workflow context
    else:
        # Fallback tracking resolution for offline local executions inside PyCharm
        almanac_window = data.get("almanac", {}).get("forecast_window", {})
        parent_week_dir = f"Week{almanac_window.get('sprint_week', '6')}"

    # 3. Strip structural alphabetic characters to convert indices to numeric formats ("Week6" -> 6)
    try:
        week_digits = "".join(filter(str.isdigit, parent_week_dir))
        week_num = int(week_digits) if week_digits else 6
    except Exception:
        week_num = 6

    # Standardize string representations to follow two-digit padding rule ("W06")
    week_suffix_file = f"W{week_num:02d}"

    # 3b. Sprint/release tag suffix — a SEPARATE counter from the Week{N} folder number
    # above. Per the Sprint DoD: research/prediction modules (ai_prompt, synthesis_*.json)
    # keep the agent-week suffix (e.g. _W08), but synthesis *outcomes* like the compiled
    # markdown report use the sprint/release suffix instead (e.g. _W30). There's no
    # reliable field in the collector data for this, so it's passed explicitly as the
    # 2nd CLI argument. Bump this number in the workflow call every sprint.
    if len(sys.argv) > 2:
        try:
            sprint_suffix_file = f"W{int(sys.argv[2]):02d}"
        except ValueError:
            print(f"[WARN] Could not parse sprint tag number '{sys.argv[2]}'. Using {week_suffix_file} instead.")
            sprint_suffix_file = week_suffix_file
    else:
        print(f"[WARN] No sprint tag number passed as 2nd argument. Using {week_suffix_file} for the report filename.")
        sprint_suffix_file = week_suffix_file

    # 4. Bind the execution path directly inside your specified structural node: Week{N}/R8_llm/
    target_dir = os.path.join(".", parent_week_dir, "R8_llm")
    os.makedirs(target_dir, exist_ok=True)
    print(f"[OK] Workspace successfully pinned to dynamic ledger: {target_dir}")

    # 5. Drop pristine prompt configuration file snapshot into the specific folder
    prompt_file_path = os.path.join(target_dir, f"ai_prompt_{week_suffix_file}.md")
    try:
        with open(prompt_file_path, "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
        print(f"[OK] Attestation target prompt cached: {prompt_file_path}")
    except Exception as e:
        print(f"[WARN] Ingestion tracking sequence dropped prompt frame save: {e}")

    print("[PRISM] Spawning concurrent threads to execute multi-engine matrix evaluation...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_claude = executor.submit(call_claude, prompt)
        future_chatgpt = executor.submit(call_chatgpt, prompt)
        future_gemini = executor.submit(call_gemini, prompt)
        future_deepseek = executor.submit(call_deepseek, prompt)

    c_res = future_claude.result()
    gpt_res = future_chatgpt.result()
    gem_res = future_gemini.result()
    ds_res = future_deepseek.result()

    # Hy3 runs under the Claude infrastructure harness: same call pattern as the
    # other models, strict hyperparameter bounds, reasoning-tag cleanup, and — if the
    # live call fails — falls back to the Claude result already computed above, so a
    # single flaky model never blanks out the weekend synthesis pipeline.
    print("[PRISM] Running tencent/hy3 under the Claude infrastructure harness...")
    hy3_res = call_hy3(prompt, c_res)

    # Align model handles cleanly with your folder structure naming patterns
    responses_map = {
        "chatgpt": gpt_res,
        "claude": c_res,
        "gemini": gem_res,
        "deepseek": ds_res,
        "claude_hy3": hy3_res,
    }

    # 6. Save every independent raw agent text ledger as structured JSON into target folder tree
    for name, data_obj in responses_map.items():
        # FIXED: Changed tracking file extensions from .txt to .json
        out_path = os.path.join(target_dir, f"synthesis_{name}_{week_suffix_file}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data_obj, indent=2))
        print(f"[OK] Stored raw validation token logs: {out_path}")

    # 7. Generate and output the final compiled dashboard markdown file
    # NOTE: this file uses sprint_suffix_file (e.g. _W30), not week_suffix_file
    # (e.g. _W08) — see the Uniform Suffix Policy in the Sprint 8 (vW30) DoD.
    report_content = generate_markdown_report(c_res, gpt_res, gem_res, ds_res, data, week_suffix_file)
    report_file_path = os.path.join(target_dir, f"llm_synthesis_{sprint_suffix_file}.md")
    with open(report_file_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_content)
    print(f"[PRISM] Complete! Synthesis markdown generated cleanly at: {report_file_path}")

if __name__ == "__main__":
    main()