import os, json, re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_finding(finding: dict) -> dict:
    prompt = f"""You are a cloud security expert. Analyze this Azure security misconfiguration.
Respond ONLY in valid JSON with exactly these keys, no extra text, no markdown:
{{
    "risk_explanation": "plain English explanation in 2-3 sentences",
    "severity_reasoning": "why this severity level was assigned",
    "remediation_steps": ["step 1", "step 2", "step 3"],
    "terraform_fix": "the exact terraform code to fix this",
    "cvss_score": 7.5
}}

Finding details:
Resource: {finding['resource']}
Type: {finding['type']}
Issue: {finding['finding']}
Severity: {finding['severity']}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = re.sub(r'json|', '', raw).strip()

    try:
        analysis = json.loads(clean)
    except json.JSONDecodeError:
        analysis = {"raw_response": raw}

    return {**finding, 'ai_analysis': analysis}

def analyze_all_findings(findings: list) -> list:
    enriched = []
    for i, finding in enumerate(findings):
        print(f'Analyzing finding {i+1}/{len(findings)}: {finding["resource"]}...')
        enriched.append(analyze_finding(finding))
    return enriched
