# workers/ai_engine.py
from utils.language_detect import detect_language_from_file
from utils.json_parse import clean_llm_json_safe
import json
#from config import AppConfig
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from utils.functional_test.functional_test_case_generator_svc import run_functional_test_case_generation
from utils.unit_test.unit_test_case_generator_svc import run_unit_test_case_generation
from utils.priority_summary import summarize_test_case_priorities
from pydantic import BaseModel, HttpUrl
#load from 
#cfg = AppConfig()
import os
#from utils.priority_summary import summarize_test_case_priorities
# ------------ Helpers ------------

def _map_framework_label_to_key(label: str) -> str:
    framework_map = {
        "Java + Selenium": "java_selenium",
        "JavaScript + TestComplete": "js_testcomplete",
        # keep same mapping as your Streamlit app
    }
    return framework_map.get(label, label)

def _clean_llm_json(raw_output: str) -> Any:
    """
    Try to clean LLM JSON outputs (strip code fences, etc.) and parse JSON.
    Falls back to returning the raw string if parsing fails.
    """
    if not raw_output:
        return {}
    # remove triple-backticks and language hints
    cleaned = raw_output.strip()
    # common patterns
    for prefix in ("```json", "```js", "```java", "```python", "```"):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    # try to parse
    try:
        return json.loads(cleaned)
    except Exception:
        # try custom JSON cleaner if available
        try:
            return clean_llm_json_safe(cleaned)
        except Exception:
            # last resort: return cleaned string
            return cleaned
        

class FunctionalTestResponse(BaseModel):
    test_cases: List[Dict[str, Any]]
    automation_scripts: Dict[str, Any]

        
def generate_functional_tests(payload: dict) -> dict:
    """
    Given a payload with user story, acceptance criteria, and framework choice,
    call the AI engine to generate functional test cases and automation script.
    Returns a dict with 'test_cases' and optional 'automation_script'.
    """
    user_story = payload.get("user_story", "")
    acceptance_criteria = payload.get("acceptance_criteria", "")
    framework_choice = payload.get("framework_choice", "")

    if not user_story or not acceptance_criteria:
        raise HTTPException(status_code=400, detail="user_story and acceptance_criteria are required")

    # api_key = cfg.api_key
    # model_name =cfg.model_name
    api_key = os.environ["api_key"]
    model_name = os.environ["model_name"]
    # map label to internal framework key expected by service
    selected_framework = _map_framework_label_to_key(framework_choice)
    # Here you would integrate with your AI engine (e.g., OpenAI, etc.)
    # For demonstration, we'll return a mock response
    try:
        raw_output = run_functional_test_case_generation(
            user_story,
            acceptance_criteria,
            api_key=api_key,
            model_name=model_name,
            framework_choice=selected_framework
        )
        parsed = _clean_llm_json(raw_output)

        # normalize outputs to expected structure
        test_cases = []
        automation_scripts = {}
        if isinstance(parsed, dict):
            test_cases = parsed.get("test_cases", []) or []
            automation_scripts = parsed.get("automation_scripts", {}) or {}
        elif isinstance(parsed, list):
            test_cases = parsed
            automation_scripts = {}
        elif isinstance(parsed, str):
            # If LLM returned plain text, wrap it
            test_cases = []
            automation_scripts = {"raw_output": parsed}

        # summary = summarize_test_case_priorities(test_cases)
        # print(summary)

        return FunctionalTestResponse(
            test_cases=test_cases,
            automation_scripts=automation_scripts
        )
    except Exception as e:
        print(f"Error in AI engine call: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI engine error: {str(e)}")

    