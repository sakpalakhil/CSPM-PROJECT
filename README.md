# AI-Powered Cloud Security Posture Monitor (CSPM)

An automated security scanner that audits Azure cloud infrastructure 
for misconfigurations and uses AI to generate plain-English risk 
explanations and Terraform remediation code.

## Architecture
- Azure SDK scans cloud resources for misconfigurations
- Groq LLaMA3 AI analyzes each finding and generates fixes
- GitHub Actions runs scanner automatically daily
- Prometheus + Grafana visualizes security score over time
- Docker containerizes the entire stack

## Tech Stack
- Cloud: Microsoft Azure
- IaC: Terraform
- Language: Python 3.10
- AI: Groq API (LLaMA3-70b-versatile)
- CI/CD: GitHub Actions
- Containers: Docker + Docker Compose
- Monitoring: Prometheus + Grafana

## Quick Start
```bash
git clone https://github.com/sakpalakhil/CSPM-PROJECT
cd CSPM-PROJECT/scanner
pip install -r requirements.txt
cp .env.example .env
# Fill in your credentials in .env
python scanner.py

