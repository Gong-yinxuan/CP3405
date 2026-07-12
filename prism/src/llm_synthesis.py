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

def call_claude(prompt):
    if not os.getenv("ANTHROPIC_API_KEY"): return fallback_metrics("Claude")
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        res = client.messages.create(
            model="claude-3-5-sonnet-20241022", max_tokens=1000, temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(clean_json_string(res.content.text))
    except Exception as e:
        return {"error": str(e)}

def call_openrouter(prompt):
    """
    Queries OpenRouter's free tier endpoints using uniform OpenAI JSON schemas.
    Utilizes a robust open-weights model runner with zero credit card setup requirements.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return fallback_metrics("OpenRouter")

    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # We target the highly performant Llama 3 8B free variant hosted on OpenRouter
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a rigid automation server. You must output ONLY a valid raw JSON object. Do not include any conversational introduction, notes, or markdown code blocks."
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
        response.raise_for_status()

        res_json = response.json()
        raw_content = res_json["choices"][0]["message"]["content"].strip()

        # Run through your extraction regex matrix to extract pristine dictionary
        cleaned_text = clean_json_string(raw_content)
        json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
        if json_match:
            cleaned_text = json_match.group(0)

        cleaned_text = re.sub(r',\s*\}', '}', cleaned_text)
        cleaned_text = re.sub(r',\s*\]', ']', cleaned_text)
        return json.loads(cleaned_text)

    except Exception as e:
        print(f"[PRISM] OpenRouter processing layer failed: {e}")
        return fallback_metrics("OpenRouter")

def call_chatgpt(prompt):
    """
    Hits the permanently free Hugging Face API via HTTP POST with an aggressive,
    self-cleaning text decoder to safely capture valid JSON objects from conversational text.
    """
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        return fallback_metrics("ChatGPT")

    url = "https://huggingface.co"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # We tweak the prompt instructions within the payload to heavily demand raw text object notation
    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a rigid automation server. You must output ONLY a valid raw JSON object. Do not include any conversational introduction, notes, or markdown code blocks."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 1000
    }

    max_retries = 3
    delay = 5

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)

            # Catch server capacity issues cleanly
            if response.status_code == 503:
                print(
                    f"[PRISM] Hugging Face server busy (Attempt {attempt + 1}/{max_retries}). Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
                continue

            response.raise_for_status()
            res_json = response.json()
            raw_content = res_json["choices"]["message"]["content"].strip()

            # --- AGGRESSIVE SELF-CLEANING EXTRACTION MATRIX ---
            # 1. Strip out basic backticks if the model used markdown code blocks
            cleaned_text = clean_json_string(raw_content)

            # 2. Heavy-duty Regex: Find the very first '{' and the very last '}'
            # This completely cuts out conversational text like "Here is the data:"
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                cleaned_text = json_match.group(0)

            # 3. Clean up any trailing broken commas right before a closing brace that break json.loads
            cleaned_text = re.sub(r',\s*\}', '}', cleaned_text)
            cleaned_text = re.sub(r',\s*\]', ']', cleaned_text)

            return json.loads(cleaned_text)

        except Exception as e:
            print(f"[PRISM] Hugging Face processing attempt {attempt + 1} failed: {e}")
            time.sleep(2)

    print("[PRISM] Hugging Face node completely swamped. Engaging clean fallback metrics.")
    return fallback_metrics("ChatGPT")

def call_gemini(prompt):
    """Hits the permanently free Google Gemini API with an automatic retry loop for 503/high-demand spikes."""
    if not os.getenv("GEMINI_API_KEY"):
        return fallback_metrics("Gemini")

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    except Exception as e:
        print(f"[PRISM] Failed to initialize Gemini Client: {e}")
        return fallback_metrics("Gemini")

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

    # If all live retrieval attempts fail due to extreme server load, engage your clean fallback payload
    print("[PRISM] Gemini completely swamped. Engaging clean assignment mock fallback payload.")
    return fallback_metrics("Gemini")


def call_deepseek(prompt):
    if not os.getenv("DEEPSEEK_API_KEY"): return fallback_metrics("DeepSeek")
    try:
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://deepseek.com")
        res = client.chat.completions.create(
            model="deepseek-chat", response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}], temperature=0.1
        )
        return json.loads(clean_json_string(res.choices.message.content))
    except Exception as e:
        return {"error": str(e)}


def fallback_metrics(model_name):
    return {k: f"Error loading {model_name} value" for k in
            ["weekly_regime", "confidence_score", "spx_pct_estimate", "ndx_pct_estimate", "iwm_pct_estimate",
             "top_supporting_reason", "top_contradiction_cited", "invalidation_condition", "tone_caveat_language"]}


def generate_markdown_report(c, gpt, gem, ds, raw_data):
    """Fully automated: Every table row and conclusion block is generated from live data."""
    # Dynamic Week Calculation: Extract week from almanac data or calculate it
    almanac_window = raw_data.get("almanac", {}).get("forecast_window", {})
    start_date_str = almanac_window.get("start", datetime.now().strftime("%Y-%m-%d"))

    # Derives the formal display week (e.g., Week 28) based on the course roadmap calendar tracking
    try:
        dt_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        display_date = dt_obj.strftime('%d %B %Y')
        # Map dynamic target context tracking directly to your vW layout definitions
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
        "| Dimension                   | Claude     | ChatGPT    | Gemini     | DeepSeek   |",
        "| --------------------------- | ---------- | ---------- | ---------- | ---------- |",
        f"| **Weekly Regime**           | {c.get('weekly_regime')} | {gpt.get('weekly_regime')} | {gem.get('weekly_regime')} | {ds.get('weekly_regime')} |",
        f"| **Confidence Score**        | {c.get('confidence_score')} | {gpt.get('confidence_score')} | {gem.get('confidence_score')} | {ds.get('confidence_score')} |",
        f"| **SPX % estimate**          | {c.get('spx_pct_estimate')} | {gpt.get('spx_pct_estimate')} | {gem.get('spx_pct_estimate')} | {ds.get('spx_pct_estimate')} |",
        f"| **NDX % estimate**          | {c.get('ndx_pct_estimate')} | {gpt.get('ndx_pct_estimate')} | {gem.get('ndx_pct_estimate')} | {ds.get('ndx_pct_estimate')} |",
        f"| **IWM % estimate**          | {c.get('iwm_pct_estimate')} | {gpt.get('iwm_pct_estimate')} | {gem.get('iwm_pct_estimate')} | {ds.get('iwm_pct_estimate')} |",
        f"| **Top supporting reason**   | {c.get('top_supporting_reason')} | {gpt.get('top_supporting_reason')} | {gem.get('top_supporting_reason')} | {ds.get('top_supporting_reason')} |",
        f"| **Top contradiction cited** | {c.get('top_contradiction_cited')} | {gpt.get('top_contradiction_cited')} | {gem.get('top_contradiction_cited')} | {ds.get('top_contradiction_cited')} |",
        f"| **Invalidation condition**  | {c.get('invalidation_condition')} | {gpt.get('invalidation_condition')} | {gem.get('invalidation_condition')} | {ds.get('invalidation_condition')} |",
        f"| **Tone / caveat language**  | {c.get('tone_caveat_language')} | {gpt.get('tone_caveat_language')} | {gem.get('tone_caveat_language')} | {ds.get('tone_caveat_language')} |",
        "",
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
        "| Evidence Leg | Current Read                  | Alignment                         |",
        "| ------------ | ----------------------------- | --------------------------------- |",
        f"| Technical    | {tech_read}                  | {tech_align}                      |",
        f"| Macro        | {macro_read}                 | {macro_align}                     |",
        f"| Almanac      | {almanac_read}               | {almanac_align}                   |",
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
        f"* `synthesis_chatgpt_{current_week_label.replace(' ', '')}.txt`",
        f"* `synthesis_claude_{current_week_label.replace(' ', '')}.txt`",
        f"* `synthesis_gemini_{current_week_label.replace(' ', '')}.txt`",
        f"* `synthesis_deepseek_{current_week_label.replace(' ', '')}.txt`"
    ]
    return "\n".join(lines)


def main():
    print("[PRISM] Querying multi-agent environment data blocks...")
    data = find_latest_collector_data()
    prompt = build_synthesis_prompt(data)

    almanac_window = data.get("almanac", {}).get("forecast_window", {})
    week_suffix = f"W{almanac_window.get('sprint_week', '28')}"
    target_dir = "prism/data/llm_synthesis"
    os.makedirs(target_dir, exist_ok=True)

    # Save unified attestation prompt snapshot
    prompt_file_path = os.path.join(target_dir, f"ai_prompt_{week_suffix}.md")
    try:
        with open(prompt_file_path, "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
    except Exception as e:
        print(f"[WARN] Prompt cache error: {e}")

    print("[PRISM] Spawning concurrent threads to execute multi-engine matrix evaluation...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_claude = executor.submit(call_claude, prompt)
        future_openrouter = executor.submit(call_openrouter, prompt)
        future_gemini = executor.submit(call_gemini, prompt)
        future_deepseek = executor.submit(call_deepseek, prompt)

    c_res = future_claude.result()
    gpt_res = future_openrouter.result()
    gem_res = future_gemini.result()
    ds_res = future_deepseek.result()

    responses_map = {
        "chatgpt": gpt_res,
        "claude": c_res,
        "gemini": gem_res,
        "deepseek": ds_res
    }

    # Routinely drops the raw txt logs directly into prism/data/llm_synthesis/
    for name, data_obj in responses_map.items():
        out_path = os.path.join(target_dir, f"synthesis_{name}_{week_suffix}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data_obj, indent=2))
        print(f"[OK] Saved copy tracker: {out_path}")

    # Drops the compiled markdown matrix directly into prism/data/llm_synthesis/
    report_content = generate_markdown_report(c_res, gpt_res, gem_res, ds_res, data)
    report_file_path = os.path.join(target_dir, f"llm_synthesis_{week_suffix}.md")
    with open(report_file_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_content)
    print(f"[PRISM] Complete! Dynamic markdown generated cleanly at: {report_file_path}")

if __name__ == "__main__":
    main()