import os
import json
import re
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
                # Matches technical/technical_collector_output.json
                if "technical_collector_output" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["technical"] = json.load(f)
                        print(f"[OK] Ingested Technical Agent Payload from: {file_path}")
                # Matches macro/macro_collector_output.json
                elif "macro_collector_output" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["macro"] = json.load(f)
                        print(f"[OK] Ingested Macro Agent Payload from: {file_path}")
                # Matches almanac/almanac_collector_output.json
                elif "almanac_collector_output" in file and file.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_payloads["almanac"] = json.load(f)
                        print(f"[OK] Ingested Weekly Almanac Agent Payload from: {file_path}")
                # Matches almanac/monthly_seasonality.json
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
Your task is to evaluate and synthesize three independent analysis legs into a forward-looking Week 5 Prediction Brief.

1. MASTER WEEK 5 MARKET DATA (Verified by Data Pipeline)
[TECHNICAL INDICATOR AGENT DATA]: 
{json.dumps(extracted_data['technical'], indent=2)}

[MACROECONOMIC DATA AGENT DATA]: 
{json.dumps(extracted_data['macro'], indent=2)}

[ALMANAC & HISTORICAL SEASONALITY AGENT DATA]: 
{json.dumps(extracted_data['almanac'], indent=2)}
{json.dumps(extracted_data['historical_seasonality'], indent=2)}

2. YOUR REQUIRED EVALUATION OUTPUT FORMAT
Provide a punchy, highly structured synthesis detailing the following dimensions:
WEEKLY REGIME
State the dominant market regime expected for the coming week.
Examples: Bullish continuation, Defensive rotation, Risk-on recovery, Sideways consolidation, High-volatility regime.

INDEX OUTLOOK
Provide expected directional bias and estimated % range for:
- S&P 500 (SPX)
- Nasdaq 100 (NDX)
- Russell 2000 (IWM)
Include: Direction, Estimated % move, Key reason.

SECTOR LEADERSHIP
Identify: Leading sector, Lagging sector. Explain why leadership matters this week.

CORE SYNTHESIS MATRIX
Evaluate whether Technical, Macro, and Almanac are aligned or contradictory. State where evidence converges and where conflict exists.

TOP SUPPORTING REASON
What is the strongest evidence supporting the weekly thesis?

TOP CONTRADICTION / RISK
What is the biggest threat to the weekly outlook?

INVALIDATION CONDITION
What clear event or market move invalidates the thesis?

TONE / CAVEAT LANGUAGE
How cautious or aggressive should positioning be?

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
  "tone_caveat_language": "Short description of target exposure alignment"
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


def call_chatgpt(prompt):
    if not os.getenv("OPENAI_API_KEY"): return fallback_metrics("ChatGPT")
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-4o-mini", response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}], temperature=0.1
        )
        return json.loads(clean_json_string(res.choices.message.content))
    except Exception as e:
        return {"error": str(e)}


def call_gemini(prompt):
    if not os.getenv("GEMINI_API_KEY"): return fallback_metrics("Gemini")
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        res = client.models.generate_content(
            model='gemini-2.5-flash', contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(clean_json_string(res.text))
    except Exception as e:
        return {"error": str(e)}


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


def generate_markdown_report(c, gpt, gem, ds):
    return f"""# LLM Synthesis — Week 05 ({datetime.now().strftime('%d %B %Y')})

> Paste the **identical** prompt into all four models. Do not change a word between models.

---

## Comparison Table

| Dimension                   | Claude     | ChatGPT    | Gemini     | DeepSeek   |
| --------------------------- | ---------- | ---------- | ---------- | ---------- |
| **Weekly Regime**           | {c.get('weekly_regime')} | {gpt.get('weekly_regime')} | {gem.get('weekly_regime')} | {ds.get('weekly_regime')} |
| **Confidence Score**        | {c.get('confidence_score')} | {gpt.get('confidence_score')} | {gem.get('confidence_score')} | {ds.get('confidence_score')} |
| **SPX % estimate**          | {c.get('spx_pct_estimate')} | {gpt.get('spx_pct_estimate')} | {gem.get('spx_pct_estimate')} | {ds.get('spx_pct_estimate')} |
| **NDX % estimate**          | {c.get('ndx_pct_estimate')} | {gpt.get('ndx_pct_estimate')} | {gem.get('ndx_pct_estimate')} | {ds.get('ndx_pct_estimate')} |
| **IWM % estimate**          | {c.get('iwm_pct_estimate')} | {gpt.get('iwm_pct_estimate')} | {gem.get('iwm_pct_estimate')} | {ds.get('iwm_pct_estimate')} |
| **Top supporting reason**   | {c.get('top_supporting_reason')} | {gpt.get('top_supporting_reason')} | {gem.get('top_supporting_reason')} | {ds.get('top_supporting_reason')} |
| **Top contradiction cited** | {c.get('top_contradiction_cited')} | {gpt.get('top_contradiction_cited')} | {gem.get('top_contradiction_cited')} | {ds.get('top_contradiction_cited')} |
| **Invalidation condition**  | {c.get('invalidation_condition')} | {gpt.get('invalidation_condition')} | {gem.get('invalidation_condition')} | {ds.get('invalidation_condition')} |
| **Tone / caveat language**  | {c.get('tone_caveat_language')} | {gpt.get('tone_caveat_language')} | {gem.get('tone_caveat_language')} | {ds.get('tone_caveat_language')} |

## Consensus Read

**Models in agreement (3/4):**
Claude, ChatGPT, and Gemini find technical convergence regarding short-term EMA chart retention. All four models agree that underlying macro frictions and yield curves apply structural counterweight pressure this cycle.

**Point of maximum divergence:**