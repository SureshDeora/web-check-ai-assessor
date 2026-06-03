# Web-Check AI Security Assessor

AI-powered security assessment engine built on top of [Web-Check](https://github.com/lissy93/web-check) (22k+ ⭐). Automates website security audits by collecting OSINT data and using GPT to interpret vulnerabilities and generate remediation recommendations.

## What It Does

1. **Collects** — Scans target website using 10 Web-Check API endpoints (DNS, SSL, headers, cookies, ports, tech stack, WAF, whois, HSTS, HTTP security)
2. **Analyzes** — AI agent interprets raw scan data to identify security misconfigurations
3. **Reports** — Generates a professional security audit report with findings, risk ratings, and specific remediation steps

## Architecture

```
User → assessor.py → Web-Check API (Docker) → Raw OSINT Data
                   → LangGraph ReAct Agent (GPT) → Security Report (MD/JSON)
```

## Setup

### Prerequisites
- Docker
- Python 3.10+
- OpenAI API key

### Installation

```bash
# 1. Start Web-Check
sudo docker run -d -p 3000:3000 --name web-check lissy93/web-check

# 2. Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Run

```bash
# Scan a website
python assessor.py https://microsoft.com

# Scan any target
python assessor.py https://zoho.com
```

### Output

Reports are saved to `reports/` as both Markdown and JSON:
```
reports/
├── microsoft.com_20260603_120000.md    ← Human-readable report
└── microsoft.com_20260603_120000.json  ← Structured data
```

Convert to PDF:
```bash
pip install md2pdf
md2pdf reports/microsoft.com_20260603_120000.md
```

## Report Structure

| Section | Content |
|---|---|
| Basic Information | Domain, IP, registrar, SSL status, DNS records |
| Security Checklist | HTTPS, HSTS, CSP, X-Frame-Options, cookie flags |
| Technology Stack | Web server, CMS, CDN, frameworks, third-party services |
| Findings | 5+ findings with risk level, evidence, and impact |
| Recommendations | 5+ actionable fixes with config examples |
| Overall Rating | Security score (0-100) with summary |

## Tech Stack

- **Python** — Core language
- **LangGraph** — AI agent orchestration (ReAct pattern)
- **LangChain** — LLM integration (OpenAI GPT)
- **Web-Check** — OSINT data collection (30+ security checks)
- **Docker** — Web-Check deployment

## Project Structure

```
web-check-ai-assessor/
├── assessor.py        # Main script — AI agent + report generation
├── collector.py       # Web-Check API data collection
├── config.py          # Configuration (endpoints, model, URLs)
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed)
├── .env.example       # API key template
├── .gitignore
├── reports/           # Generated audit reports
└── docs/              # Interview prep documentation
```
