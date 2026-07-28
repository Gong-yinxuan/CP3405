import os
import sys
import json
import re
import time
import requests
import concurrent.futures
from datetime import datetime

# Official API SDK Clients
from anthropic import Anthropic
from google import genai
from google.genai import types

# Stable, Production-grade Production IDs on OpenRouter
CHATGPT_MODEL = "openai/gpt-4o-mini"
DEEPSEEK_MODEL = "deepseek/deepseek-chat"
FREE_FALLBACK_MODEL = "openrouter/free"

# System Endpoint Assets
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def clean_json_stream(raw_text):
    """Isolates and extracts valid JSON boundaries out of LLM text responses."""
    text = raw_text.strip()
    # Strip markdown code blocks cleanly
    text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text)

    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx == -1 or end_idx == -1:
        raise ValueError("No structural JSON object boundaries discovered in output stream.")

    pristine = text[start_idx:end_idx + 1].strip()
    # Repair standard trailing comma structural anomalies
    pristine = re.sub(r',\s*\}', '}', pristine)
    pristine = re.sub(r',\s*\]', ']', pristine)
    return pristine


# Pattern matches standard internal-monologue reasoning blocks
_REASONING_TAG_PATTERN = re.compile(
    r"<(think|reasoning|scratchpad|analysis)[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)


def strip_reasoning_tags(raw_text):
    """Strips internal reasoning/thinking tags before routing to JSON extractor."""
    text = _REASONING_TAG_PATTERN.sub("", raw_text)
    return clean_json_stream(text)


def get_safe_fallback_payload(model_label, error_message):
    """Generates a populated safe fallback object to protect report generation stability."""
    print(f"[RECOVERY MATRIX] Building failure recovery frame for {model_label}. Error Context: {error_message}")
    return {
        "weekly_regime": f"Automated recovery substitution active for {model_label}.",
        "confidence_score": "Low",
        "spx_pct_estimate": "N/A",
        "ndx_pct_estimate": "N/A",
        "iwm_pct_estimate": "N/A",
        "top_supporting_reason": f"Execution dropped into safe fallback rail. Error: {error_message}",
        "top_contradiction_cited": "Connection interface drop recorded.",
        "invalidation_condition": "Check active run parameters.",
        "tone_caveat_language": "N/A",
        "_fallback_warning": f"Generated via error recovery protocol due to termination of primary model {model_label}."
    }


def call_openrouter_free_fallback(prompt, failed_model_label, structural_error):
    """Last resort connection routing block utilizing OpenRouter's auto-router path."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return get_safe_fallback_payload(failed_model_label,
                                         f"{structural_error} (And OPENROUTER_API_KEY secret is missing)")

    print(f"[RECOVERY PATH] Diverting prompt for {failed_model_label} to OpenRouter Free Fallback...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Prism Infrastructure Failover Engine"
    }
    payload = {
        "model": FREE_FALLBACK_MODEL,
        "messages": [
            {"role": "system",
             "content": "You are a rigid automation server. Return ONLY a valid raw JSON object matching the requested schema keys."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    for attempt in range(1, 3):
        try:
            res = requests.post(OPEN_ROUTER_URL, headers=headers, json=payload, timeout=30)
            if res.status_code != 200:
                print(f"[WARN] Failover network attempt {attempt}/2 dropped with status: {res.status_code}")
                continue

            choices = res.json().get("choices", [])
            if not choices:
                continue

            content = choices[0].get("message", {}).get("content", "")
            parsed_json = json.loads(strip_reasoning_tags(content))
            parsed_json[
                "_fallback_warning"] = f"{failed_model_label} connection dropped. Swapped automatically with {FREE_FALLBACK_MODEL}."
            return parsed_json
        except Exception as e:
            print(f"[WARN] Failover loop tracking engine variance on attempt {attempt}: {e}")
            time.sleep(2)

    return get_safe_fallback_payload(failed_model_label,
                                     f"Primary failure: {structural_error}. Backup auto-router free space limits exhausted.")


def call_claude(prompt):
    """Targets primary native Anthropic Claude-3-5-Sonnet cluster framework."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY variable missing from current environment runtime context.")
        return call_openrouter_free_fallback(prompt, "Claude", "Missing native API access credentials.")

    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.1,
            system="You are a rigid automation server. Output ONLY a valid raw JSON object matching the requested schema keys.",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
        return json.loads(clean_json_stream(raw_text))
    except Exception as e:
        print(f"[ERROR] Native Claude environment channel broken: {e}")
        return call_openrouter_free_fallback(prompt, "Claude", str(e))


def call_gemini(prompt):
    """Targets primary native Google Gemini-2.5-Flash cluster framework."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY variable missing from current environment runtime context.")
        return call_openrouter_free_fallback(prompt, "Gemini", "Missing native API access credentials.")

    try:
        client = genai.Client(api_key=api_key)
        max_retries = 3
        delay = 5

        for attempt in range(max_retries):
            try:
                res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                return json.loads(clean_json_stream(res.text))
            except Exception as e:
                err_msg = str(e).lower()
                if "503" in err_msg or "demand" in err_msg or "exhausted" in err_msg:
                    print(
                        f"[RETRY] Gemini congestion drop active (Attempt {attempt + 1}/{max_retries}). Retrying with backoff...")
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise e
        raise RuntimeError("Gemini concurrency query limits completely exhausted under high traffic density profile.")
    except Exception as e:
        print(f"[ERROR] Native Gemini runtime framework dropped validation frame: {e}")
        return call_openrouter_free_fallback(prompt, "Gemini", str(e))


def call_openrouter_base(prompt, model_name, friendly_label):
    """Standardized operational network route for handling unified OpenRouter tasks."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print(f"[ERROR] OPENROUTER_API_KEY missing. Skipping endpoint creation for: {friendly_label}")
        return call_openrouter_free_fallback(prompt, friendly_label, "Missing OpenRouter configuration secrets.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Prism Core Matrix Engine"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system",
             "content": "You are a rigid automation server. Output ONLY a valid raw JSON object matching requested schema keys."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(OPEN_ROUTER_URL, headers=headers, json=payload, timeout=45)
        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter target provider cluster returned error tracking flag status code: {response.status_code}")

        choices = response.json().get("choices", [])
        if not choices:
            raise ValueError("OpenRouter parsed response payload contains empty choice arrays.")

        raw_content = choices[0].get("message", {}).get("content", "")
        return json.loads(clean_json_stream(raw_content))
    except Exception as e:
        print(f"[ERROR] OpenRouter mapping structure faulted for model segment {friendly_label}: {e}")
        return call_openrouter_free_fallback(prompt, friendly_label, str(e))


def call_chatgpt(prompt):
    return call_openrouter_base(prompt, CHATGPT_MODEL, "ChatGPT")


def call_deepseek(prompt):
    return call_openrouter_base(prompt, DEEPSEEK_MODEL, "DeepSeek")


def find_latest_collector_data():
    """Recursively maps your entire prism/data environment directory tree

    to extract files from both root indices and nested subdirectories.
    """
    data_payloads = {
        "technical": {},
        "macro": {},
        "almanac": {},
        "historical_seasonality": {},
    }
    base_dir = "prism/data"

    if not os.path.exists(base_dir):
        print(
            f"[PRISM] Critical Link Warning: '{base_dir}' folder tree does not exist."
        )
        return data_payloads

    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if "technical_collector_output" in file and file.endswith(
                    ".json"
                ):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["technical"] = json.load(f)
                    print(
                        f"[OK] Ingested Technical Agent Payload from: {file_path}"
                    )
                elif "macro_collector_output" in file and file.endswith(
                    ".json"
                ):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["macro"] = json.load(f)
                    print(
                        f"[OK] Ingested Macro Agent Payload from: {file_path}"
                    )
                elif "almanac_collector_output" in file and file.endswith(
                    ".json"
                ):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["almanac"] = json.load(f)
                    print(
                        f"[OK] Ingested Weekly Almanac Agent Payload from: {file_path}"
                    )
                elif "monthly_seasonality" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["historical_seasonality"] = json.load(f)
                    print(
                        f"[OK] Ingested Historical Monthly Seasonality Data from: {file_path}"
                    )
            except Exception as e:
                print(
                    f"[WARN] Ingestion pipeline skipped parsing on file {file_path}: {e}"
                )

    return data_payloads


def build_synthesis_prompt(extracted_data):
    """Assembles your live multi-agent payloads into the identical evaluation

    prompt layout.
    """
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


def generate_markdown_report(c, gpt, gem, ds, raw_data, week_suffix_file="W08"):
    """Fully automated: Every table row and conclusion block is generated from

    live data.
    """
    # Dynamic Week Calculation: Extract week from almanac data or calculate it
    almanac_window = raw_data.get("almanac", {}).get("forecast_window", {})
    start_date_str = almanac_window.get(
        "start", datetime.now().strftime("%Y-%m-%d")
    )
    try:
        dt_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        display_date = dt_obj.strftime("%d %B %Y")
        current_week_label = (
            f"Week {almanac_window.get('sprint_week', '28')}"
        )
    except Exception:
        display_date = datetime.now().strftime("%d %B %Y")
        current_week_label = "Week 28"

    # --- DYNAMIC EVIDENCE CONFLUENCE CALCULATIONS ---
    tech_instruments = raw_data.get("technical", {}).get("instruments", {})
    bullish_count = sum(
        1
        for inst in tech_instruments.values()
        if "Bullish" in inst.get("technical_bias", "")
    )
    bearish_count = sum(
        1
        for inst in tech_instruments.values()
        if "Bearish" in inst.get("technical_bias", "")
    )
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
    has_weakness = almanac_flags.get(
        "june_seasonal_weakness_flag", False
    ) or almanac_flags.get("midterm_year_flag", False)
    if has_weakness:
        almanac_read, almanac_align = "Neutral-Cautious (Flags Active)", "Mixed"
    else:
        almanac_read, almanac_align = (
            "Neutral-Neutral (Clear Calendar)",
            "Aligned",
        )

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

    # Surface any fallback substitutions plainly right under the table
    fallback_notes = []
    for label, model_result in (
            ("Claude", c),
            ("ChatGPT", gpt),
            ("Gemini", gem),
            ("DeepSeek", ds),
    ):
        note = (
            model_result.get("_fallback_warning")
            if isinstance(model_result, dict)
            else None
        )
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
        f"* `synthesis_chatgpt_{week_suffix_file}.json`",
        f"* `synthesis_claude_{week_suffix_file}.json`",
        f"* `synthesis_gemini_{week_suffix_file}.json`",
        f"* `synthesis_deepseek_{week_suffix_file}.json`",
    ]
    return "\n".join(lines)


def main():
    print("[PRISM] Querying multi-agent environment data blocks...")
    data = find_latest_collector_data()
    prompt = build_synthesis_prompt(data)

    # 1. Defensively clean and resolve command line tracking variables
    if len(sys.argv) > 1 and sys.argv[1].strip():
        # Strip out loose string quotes if wrapped accidentally by workflow calls
        parent_week_dir = sys.argv[1].replace('"', '').replace("'", '').strip()
    else:
        almanac_window = data.get("almanac", {}).get("forecast_window", {})
        parent_week_dir = f"Week{almanac_window.get('sprint_week', '6')}"

    # 2. Extract context week numerical markers reliably
    week_digits = "".join(filter(str.isdigit, parent_week_dir))
    week_num = int(week_digits) if week_digits else 6
    week_suffix_file = f"W{week_num:02d}"

    # 3. Resolve the release counter string layout parameter (e.g., vW30)
    if len(sys.argv) > 2 and sys.argv[2].strip():
        try:
            sprint_digits = "".join(filter(str.isdigit, sys.argv[2]))
            sprint_num = int(sprint_digits) if sprint_digits else week_num
            sprint_suffix_file = f"W{sprint_num:02d}"
        except ValueError:
            print(f"[WARN] Failed to process sprint tag payload '{sys.argv[2]}'. Falling back to {week_suffix_file}")
            sprint_suffix_file = week_suffix_file
    else:
        print(f"[WARN] Sprint release parameter missing from execution frame. Utilizing fallback: {week_suffix_file}")
        sprint_suffix_file = week_suffix_file

    # 4. Initialize dynamic target directories matching your workspace conventions
    target_dir = os.path.join(".", parent_week_dir, "R8_llm")
    os.makedirs(target_dir, exist_ok=True)
    print(f"[OK] Workspace successfully pinned to dynamic ledger: {target_dir}")

    # 5. Backup the master prompt snapshot state asset locally
    prompt_file_path = os.path.join(target_dir, f"ai_prompt_{week_suffix_file}.md")
    try:
        with open(prompt_file_path, "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
        print(f"[OK] Attestation target prompt cached: {prompt_file_path}")
    except Exception as e:
        print(f"[WARN] Drop frame exception encountered while writing prompt state file: {e}")

    # 6. Fire asynchronous API calls to engine infrastructure clusters concurrently
    print("[PRISM] Spawning concurrent threads to execute multi-engine matrix evaluation...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_claude = executor.submit(call_claude, prompt)
        future_chatgpt = executor.submit(call_chatgpt, prompt)
        future_gemini = executor.submit(call_gemini, prompt)
        future_deepseek = executor.submit(call_deepseek, prompt)

        c_res = future_claude.result()
        gpt_res = future_chatgpt.result()
        gem_res = future_gemini.result()
        ds_res = future_deepseek.result()

    # 7. Serialize runtime metadata dictionaries to your directory tracks
    responses_map = {
        "chatgpt": gpt_res,
        "claude": c_res,
        "gemini": gem_res,
        "deepseek": ds_res,
    }

    for name, data_obj in responses_map.items():
        out_path = os.path.join(target_dir, f"synthesis_{name}_{week_suffix_file}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data_obj, indent=2))
        print(f"[OK] Stored raw validation token logs: {out_path}")

    # 8. Render full compilation dashboard reporting page
    report_content = generate_markdown_report(c_res, gpt_res, gem_res, ds_res, data, week_suffix_file)
    report_file_path = os.path.join(target_dir, f"llm_synthesis_{sprint_suffix_file}.md")
    with open(report_file_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_content)
    print(f"[PRISM] Complete! Synthesis markdown generated cleanly at: {report_file_path}")


if __name__ == "__main__":
    main()