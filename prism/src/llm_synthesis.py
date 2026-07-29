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
OPEN_ROUTER_URL = "https://openrouter.ai"


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
                print(
                    f"[WARN] Fallback network attempt {attempt}/2 dropped with status: {res.status_code} | Raw text: {res.text}")
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
            print(f"[WARN] Fallback loop tracking engine variance on attempt {attempt}: {e}")
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
                    print(f"[RETRY] Gemini congestion drop active (Attempt {attempt + 1}/{max_retries}). Retrying with backoff...")
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
            {"role": "system", "content": "You are a rigid automation server. Output ONLY a valid raw JSON object matching requested schema keys."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    try:
        response = requests.post(OPEN_ROUTER_URL, headers=headers, json=payload, timeout=45)
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter provider cluster error: {response.status_code} | Payload: {response.text}")
        choices = response.json().get("choices", [])
        if not choices:
            raise ValueError("OpenRouter response payload contains empty choice arrays.")
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
    """Assembles pipeline telemetry and structures rigid search instructions
    ordering models to perform real-time verification and spot collector omissions.
    """
    # Extract the forward-looking calendar watch details parsed by macro_collector.py
    fed_and_data_watch = extracted_data.get('macro', {}).get('fed_and_data_watch', {})

    return f"""
You are acting as an advanced Multi-LLM Consensus Synthesis Engine for CP3405 DT3 Market Intelligence.
Your task is to evaluate three independent retrospective analysis legs, cross-reference them with live internet research, and deliver a forward-looking Weekly Prediction Brief.

1. LOCAL SOURCE DATA PAYLOADS (Retrospective Pipeline Ingestion)
[TECHNICAL INDICATOR AGENT DATA]:
{json.dumps(extracted_data['technical'], indent=2)}

[ALMANAC & HISTORICAL SEASONALITY AGENT DATA]:
{json.dumps(extracted_data['almanac'], indent=2)}
{json.dumps(extracted_data['historical_seasonality'], indent=2)}

[PIPELINE ECONOMIC CALENDAR CAPTURE]:
{json.dumps(fed_and_data_watch, indent=2)}

2. MANDATORY INDEPENDENT REAL-TIME RESEARCH INSTRUCTIONS
Our local economic macro data collectors may have missed critical market events, unscheduled central bank updates, or breaking macroeconomic catalysts. 
YOU ARE EXPLICITLY ORDERED TO USE YOUR WEB-SEARCH, LIVE-RETRIEVAL, AND PARAMETRIC KNOWLEDGE INFRASTRUCTURE TO PERFORM AN INDEPENDENT AUDIT OF CURRENT LIVE SECTORS AND EVENTS:
- Research current breaking macroeconomic catalysts, geopolitical shifts, or sudden volatility vectors affecting broad market indices (SPX, NDX, IWM) for the upcoming tracking week.
- Cross-reference the 'PIPELINE ECONOMIC CALENDAR CAPTURE' against actual public economic calendars to identify high-importance missing events (e.g., unscheduled central bank speeches, flash PMI data, emergency updates, or unexpected global inventory revisions).
- Identify current consensus estimates for any major upcoming indicators to evaluate trend acceleration or trend exhaustion conditions.

3. YOUR REQUIRED EVALUATION OUTPUT FORMAT
Provide a punchy, highly structured synthesis detailing your findings. 

Rules for Synthesis Compilation:
- Do not invent past historical price metrics.
- INTEGRATE YOUR INDEPENDENT RESEARCH FINDINGS directly into your index outlooks and regime evaluations to enhance accuracy beyond our local data collectors.
- Explicitly log any discovered data collection gaps, omitted events, or missed macroeconomic parameters inside the dedicated 'pipeline_omissions_discovered' array key so we can update our collectors.

Output strictly as valid, clean JSON matching the target keys below. No markdown wrappers.
{{
"weekly_regime": "text description detailing expected market regime, incorporating both pipeline telemetry and your independent live research discoveries",
"confidence_score": "High, Medium, or Low",
"spx_pct_estimate": "Estimated percentage range",
"ndx_pct_estimate": "Estimated percentage range",
"iwm_pct_estimate": "Estimated percentage range",
"top_supporting_reason": "Single strong statement detailing your top core macro/technical catalyst trigger discovered",
"top_contradiction_cited": "The primary scheduled risk or discovered missing calendar anomaly that could break this trend",
"invalidation_condition": "Specific closing level or yield target breaker level",
"tone_caveat_language": "Short description of target exposure alignment based on the complete risk calendar",
"consensus_bias": "BULLISH / BEARISH / NEUTRAL / MIXED",
"consensus_read_summary": "A 2-3 sentence paragraph summarizing model alignment, agreements, and specific missing market developments highlighted via your independent live search...",
"point_of_maximum_divergence": "The single biggest disagreement point between aggressive and defensive views regarding upcoming event impacts...",
"key_supporting_factors": ["Live factor from local data", "Macro driver or missed calendar event surfaced via independent search"],
"main_contradiction_risk": "The top structural risk moving against the consensus trend this week...",
"invalidation_summary": "The exact parameter or support level that breaks this consensus view...",
"pipeline_omissions_discovered": ["List specific high-importance calendar events, indicators, central bank releases, or macro data points missed by our local macro/technical collectors that you discovered via real-time research"],
"r7_human_score_question": "A critical evaluation question helping the human team weigh the conflicting data legs against discovered external elements...",
"r6_slide_bullet_1": "Core slide takeaway bullet 1 incorporating live research context...",
"r6_slide_bullet_2": "Core slide takeaway bullet 2 incorporating live research context...",
"r6_slide_bullet_3": "Core slide takeaway bullet 3 incorporating live research context..."
}}
""".strip()


def generate_markdown_report(c, gpt, gem, ds, raw_data, week_suffix_file="W08"):
    """Human-scannable dashboard briefing report compiler.

    Programmatically calculates the most credible model of the week using
    a mathematical majority alignment matrix to eliminate chatbot guesswork.
    """
    almanac_window = raw_data.get("almanac", {}).get("forecast_window", {})
    start_date_str = almanac_window.get("start", datetime.now().strftime("%Y-%m-%d"))
    try:
        dt_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        display_date = dt_obj.strftime('%d %B %Y')
        current_week_label = f"Week {almanac_window.get('sprint_week', '31')}"
    except Exception:
        display_date = datetime.now().strftime('%d %B %Y')
        current_week_label = "Week 31"

    # --- ADVANCED LOGICAL RESOLVER: CONFLUENCE SCORING ENGINE ---
    models_dict = {"Claude": c, "ChatGPT": gpt, "Gemini": gem, "DeepSeek": ds}

    # 1. Track and calculate the majority market bias
    bias_votes = []
    for m_name, m_obj in models_dict.items():
        if isinstance(m_obj, dict) and "_fallback_warning" not in m_obj:
            bias = str(m_obj.get("consensus_bias", "")).upper()
            if bias in ["BULLISH", "BEARISH", "NEUTRAL", "MIXED"]:
                bias_votes.append(bias)
    calculated_majority_bias = max(set(bias_votes), key=bias_votes.count) if bias_votes else "NEUTRAL"

    # 2. Score each model based on structural consistency and alignment
    model_scores = {}
    for m_name, m_obj in models_dict.items():
        if not isinstance(m_obj, dict):
            model_scores[m_name] = -100
            continue
        if "_fallback_warning" in m_obj:
            model_scores[m_name] = -50
            continue
        score = 0
        if str(m_obj.get("consensus_bias", "")).upper() == calculated_majority_bias:
            score += 40
        if m_obj.get("invalidation_condition") and "N/A" not in str(m_obj.get("invalidation_condition")):
            score += 30
        omissions = m_obj.get("pipeline_omissions_discovered", [])
        if isinstance(omissions, list) and len(omissions) > 0 and "List specific" not in str(omissions):
            score += 30
        model_scores[m_name] = score

    most_credible_model = max(model_scores, key=model_scores.get)
    highest_score = model_scores[most_credible_model]

    if highest_score <= 0:
        credibility_justification = "All primary models encountered service disruptions. System defaulted to basic structural fallback tracks."
    else:
        credibility_justification = f"Successfully matched the calculated majority market framework ({calculated_majority_bias}) while introducing active validation parameters and discovering uncaptured macro pipeline anomalies."

    # --- RETROSPECTIVE LOCAL DATA EVIDENCE CHECK ---
    tech_instruments = raw_data.get("technical", {}).get("instruments", {})
    bullish_count = sum(1 for inst in tech_instruments.values() if "Bullish" in inst.get("technical_bias", ""))
    bearish_count = sum(1 for inst in tech_instruments.values() if "Bearish" in inst.get("technical_bias", ""))
    tech_read, tech_align = ("Bullish", "Aligned") if bullish_count > bearish_count else (
        ("Bearish", "Aligned") if bearish_count > bullish_count else ("Neutral", "Mixed"))

    macro_instruments = raw_data.get("macro", {}).get("instruments", {})
    vix_direction = macro_instruments.get("VIX", {}).get("direction", "Flat")
    macro_read, macro_align = ("Slightly Bearish / Defensive", "Mixed") if vix_direction == "Up" else (
        "Stable / Supportive", "Aligned")

    almanac_flags = raw_data.get("almanac", {}).get("calendar_flags", {})
    has_weakness = almanac_flags.get("june_seasonal_weakness_flag", False) or almanac_flags.get("midterm_year_flag",
                                                                                                False)
    almanac_read, almanac_align = ("Neutral-Cautious (Flags Active)", "Mixed") if has_weakness else (
        "Neutral-Neutral (Clear Calendar)", "Aligned")

    # --- STANDARD BASE FIELD RESOLVERS ---
    def get_consensus_field(key, fallback="Dynamic text calculation pending across matrix paths..."):
        for model_obj in [c, gpt, gem, ds]:
            if isinstance(model_obj, dict) and "_fallback_warning" not in model_obj:
                val = model_obj.get(key)
                if val and "Error" not in str(val):
                    return str(val).strip()
        return fallback

    def get_consensus_list(key):
        for model_obj in [c, gpt, gem, ds]:
            if isinstance(model_obj, dict) and "_fallback_warning" not in model_obj:
                items = model_obj.get(key, [])
                if isinstance(items, list) and items and not any("Error" in str(i) for i in items):
                    return "\n".join([f"* {str(item).strip()}" for item in items])
        return "* Multi-engine matrix research sequence ongoing across active collector branches."

    def get_model_cell(model_obj, key):
        if not isinstance(model_obj, dict): return "N/A (Missing Payload)"
        val = model_obj.get(key, "N/A")
        return "⚠️ Fallback Active" if "Error loading" in str(val) else str(val).strip()

    # --- COMPILE BRIEFING REPORT ---
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
        f"| **Weekly Regime** | {get_model_cell(c, 'weekly_regime')} | {get_model_cell(gpt, 'weekly_regime')} | {get_model_cell(gem, 'weekly_regime')} | {get_model_cell(ds, 'weekly_regime')} |",
        f"| **Confidence Score** | {get_model_cell(c, 'confidence_score')} | {get_model_cell(gpt, 'confidence_score')} | {get_model_cell(gem, 'confidence_score')} | {get_model_cell(ds, 'confidence_score')} |",
        f"| **SPX % estimate** | {get_model_cell(c, 'spx_pct_estimate')} | {get_model_cell(gpt, 'spx_pct_estimate')} | {get_model_cell(gem, 'spx_pct_estimate')} | {get_model_cell(ds, 'spx_pct_estimate')} |",
        f"| **NDX % estimate** | {get_model_cell(c, 'ndx_pct_estimate')} | {get_model_cell(gpt, 'ndx_pct_estimate')} | {get_model_cell(gem, 'ndx_pct_estimate')} | {get_model_cell(ds, 'ndx_pct_estimate')} |",
        f"| **IWM % estimate** | {get_model_cell(c, 'iwm_pct_estimate')} | {get_model_cell(gpt, 'iwm_pct_estimate')} | {get_model_cell(gem, 'iwm_pct_estimate')} | {get_model_cell(ds, 'iwm_pct_estimate')} |",
        f"| **Top supporting reason** | {get_model_cell(c, 'top_supporting_reason')} | {get_model_cell(gpt, 'top_supporting_reason')} | {get_model_cell(gem, 'top_supporting_reason')} | {get_model_cell(ds, 'top_supporting_reason')} |",
        f"| **Top contradiction cited** | {get_model_cell(c, 'top_contradiction_cited')} | {get_model_cell(gpt, 'top_contradiction_cited')} | {get_model_cell(gem, 'top_contradiction_cited')} | {get_model_cell(ds, 'top_contradiction_cited')} |",
        f"| **Invalidation condition** | {get_model_cell(c, 'invalidation_condition')} | {get_model_cell(gpt, 'invalidation_condition')} | {get_model_cell(gem, 'invalidation_condition')} | {get_model_cell(ds, 'invalidation_condition')} |",
        f"| **Tone / caveat language** | {get_model_cell(c, 'tone_caveat_language')} | {get_model_cell(gpt, 'tone_caveat_language')} | {get_model_cell(gem, 'tone_caveat_language')} | {get_model_cell(ds, 'tone_caveat_language')} |",
        "",
    ]

    fallback_notes = []
    for label, model_result in (("Claude", c), ("ChatGPT", gpt), ("Gemini", gem), ("DeepSeek", ds)):
        if isinstance(model_result, dict) and model_result.get("_fallback_warning"):
            fallback_notes.append(f"* ⚠️ **{label}:** {model_result.get('_fallback_warning')}")

    if fallback_notes:
        lines.append("### ⚠️ Fallback Notices");
        lines.append("");
        lines.extend(fallback_notes);
        lines.append("")

    lines += [
        "## Consensus Read",
        "",
        "**Models in agreement summary (Blended Analysis Matrix):**",
        f"{get_consensus_field('consensus_read_summary')}",
        "",
        "**Point of maximum divergence:**",
        f"{get_consensus_field('point_of_maximum_divergence')}",
        "",
        "**Most credible model this week:**",
        f"**{most_credible_model}**",
        "",
        "**Why:**",
        f"{credibility_justification}",
        "",
        "---",
        "",
        "## Final Team Interpretation",
        "",
        "### Consensus Bias",
        f"**{calculated_majority_bias}**",
        "",
        "### Confidence",
        f"**{get_consensus_field('confidence_score', 'Medium')}**",
        "",
        "### Key Supporting Factors (Combined Local & Discovered Elements)",
        f"{get_consensus_list('key_supporting_factors')}",
        "",
        "### Main Contradiction / Risk Horizon",
        f"{get_consensus_field('main_contradiction_risk')}",
        "",
        "### Invalidation Condition Boundaries",
        f"{get_consensus_field('invalidation_summary')}",
        "",
        "---",
        "",
        "## R6 Handoff to R7 Human Score",
        "",
        "### Key Human Score Question",
        f"{get_consensus_field('r7_human_score_question')}",
        "",
        "## Evidence Confluence Check",
        "",
        "| Evidence Leg | Current Read | Alignment |",
        "| ------------ | ----------------------------- | --------------------------------- |",
        f"| Technical | {tech_read} | {tech_align} |", f"| Macro | {macro_read} | {macro_align} |",
        f"| Almanac | {almanac_read} | {almanac_align} |",
        "",
        "---",
        "",
        "## 🛠️ Data Collector Audit Ledger",
        "",
        "The following omissions or missing event constraints were surfaced by the multi-engine matrix research pass. Use this log to update upstream data collector modules in future sprint iterations:",
        "", f"{get_consensus_list('pipeline_omissions_discovered')}", "", "---", "", "## R6 Slide Text", "",
        f"* {get_consensus_field('r6_slide_bullet_1')}",
        f"* {get_consensus_field('r6_slide_bullet_2', 'Macro layers generate visible divergence relative to valuations.')}",
        f"* {get_consensus_field('r6_slide_bullet_3', 'Dynamic execution sequence completed across matrix tracks.')}",
        "", "---", "### Raw responses saved as:", f"* synthesis_chatgpt_{week_suffix_file}.json",
        f"* synthesis_claude_{week_suffix_file}.json", f"* synthesis_gemini_{week_suffix_file}.json",
        f"* synthesis_deepseek_{week_suffix_file}.json", ]
    return "\n".join(lines)


def main():
    print("[PRISM] Querying multi-agent environment data blocks...")
    data = find_latest_collector_data()
    prompt = build_synthesis_prompt(data)

    if len(sys.argv) > 1 and sys.argv[1].strip():
        parent_week_dir = sys.argv[1].replace('"', '').replace("'", '').strip()
    else:
        almanac_window = data.get("almanac", {}).get("forecast_window", {})
        parent_week_dir = f"Week{almanac_window.get('sprint_week', '6')}"

    week_digits = "".join(filter(str.isdigit, parent_week_dir))
    week_num = int(week_digits) if week_digits else 6
    week_suffix_file = f"W{week_num:02d}"

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

    target_dir = os.path.join(".", parent_week_dir, "R8_llm")
    os.makedirs(target_dir, exist_ok=True)
    print(f"[OK] Workspace successfully pinned to dynamic ledger: {target_dir}")

    prompt_file_path = os.path.join(target_dir, f"ai_prompt_{week_suffix_file}.md")
    try:
        with open(prompt_file_path, "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
        print(f"[OK] Attestation target prompt cached: {prompt_file_path}")
    except Exception as e:
        print(f"[WARN] Drop frame exception encountered while writing prompt state file: {e}")

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

    report_content = generate_markdown_report(c_res, gpt_res, gem_res, ds_res, data, week_suffix_file)
    report_file_path = os.path.join(target_dir, f"llm_synthesis_{sprint_suffix_file}.md")
    with open(report_file_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_content)
    print(f"[PRISM] Complete! Synthesis markdown generated cleanly at: {report_file_path}")


if __name__ == "__main__":
    main()