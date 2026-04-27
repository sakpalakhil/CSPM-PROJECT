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

## Architecture Design
<img width="1079" height="644" alt="Screenshot_20260427_024644_Claude" src="https://github.com/user-attachments/assets/6ad793eb-447e-4e04-95e5-1f80dc9ab149" />


<img width="960" height="564" alt="report-sample" src="https://github.com/user-attachments/assets/97b51597-2360-4230-b615-35c2e1928d3a" />

<img width="960" height="564" alt="azure-resources" src="https://github.com/user-attachments/assets/53d30571-3882-4456-b4aa-1b20d6272199" />

<img width="960" height="564" alt="grafana-dashboard" src="https://github.com/user-attachments/assets/4d7bf63c-8311-4c39-9a53-8650d5526206" />


<img width="960" height="564" alt="pipeline-success" src="https://github.com/user-attachments/assets/ffb7fd3a-a674-40f9-b5ed-0dcaa2651376" />

## Quick Start
```bash
git clone https://github.com/sakpalakhil/CSPM-PROJECT
cd CSPM-PROJECT/scanner
pip install -r requirements.txt
cp .env.example .env
# Fill in your credentials in .env
python scanner.py

