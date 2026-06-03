# Web-Check AI Security Assessor — Interview Prep Guide

This document explains every part of the project so you can confidently discuss it in interviews.

---

## How to Explain This Project in 30 Seconds

> "I built an AI-powered security audit tool that extends the open-source Web-Check OSINT platform.
> It runs 10 security checks against any website — DNS, SSL, headers, cookies, open ports,
> tech stack detection — and then uses a LangGraph AI agent to automatically interpret the results
> and generate a professional audit report with findings, risk ratings, and remediation recommendations."

---

## The 3 Files and What They Do

### `config.py` (11 lines)
Stores all settings: Web-Check URL, AI model name, which API endpoints to call, timeouts.

**Why a separate config?** So you can change the model or add endpoints without touching the main code. Shows good software engineering practice.

### `collector.py` (48 lines)
Does ONE thing: calls the Web-Check API and returns raw data.

**Two functions:**
- `call_endpoint(endpoint, url)` — calls a single API endpoint (e.g., `/api/ssl?url=microsoft.com`)
- `collect_all(url)` — loops through all endpoints and collects everything

**Why separate from assessor.py?** Separation of concerns. Data collection is independent from AI analysis. You could swap Web-Check with Nmap or Shodan without changing the AI code.

### `assessor.py` (120 lines)
The main script. Three parts:

1. **Tool definition** — `collect_osint_data()` is decorated with `@tool` so the AI agent can call it
2. **Agent creation** — `create_react_agent(model=llm, tools=tools)` creates a ReAct agent
3. **Audit prompt** — A detailed prompt that tells the AI exactly what report structure to produce
4. **Report generation** — Saves output as Markdown and JSON

---

## Key Concepts You Must Know

### What is a ReAct Agent?
ReAct = **Reasoning + Acting**. A loop where the AI:
1. **Thinks** — "I need to collect data first"
2. **Acts** — Calls the `collect_osint_data` tool
3. **Observes** — Reads the returned JSON
4. **Thinks** — "Now I need to analyze this for vulnerabilities"
5. **Acts** — Writes the analysis (no tool needed, just generates text)
6. Repeats until done

**Interview phrasing:** "The agent autonomously decides which tools to use and in what order, following a think-act-observe loop."

### What is LangGraph?
LangGraph is built on top of LangChain. It adds **stateful, graph-based workflows**.

- **LangChain** = the building blocks (LLM wrapper, tool definitions, prompts)
- **LangGraph** = the engine that manages the agent loop (think → act → observe)

`create_react_agent()` creates a graph with two nodes: "call LLM" and "execute tool", connected by edges that loop until the AI says "I'm done."

### What is the `@tool` Decorator?
It does 3 things:
1. Registers the function so the AI can call it
2. Uses the **docstring** as the tool's description (AI reads this to decide when to use it)
3. Uses the **function signature** (parameter types) to tell the AI what arguments to pass

### Why `temperature=0`?
Controls randomness. `0` = deterministic (same input → same output). For security audits, we want consistent, factual results. Not creative writing.

### Why `gpt-4o-mini` instead of `gpt-4o`?
Cost. `gpt-4o-mini` is ~10x cheaper and performs well enough for structured analysis. You can change it in `config.py`.

---

## How the Data Flows

```
1. User runs: python assessor.py https://microsoft.com

2. assessor.py creates the audit prompt and sends it to the AI agent

3. AI agent THINKS: "I need to collect data first"
   AI agent ACTS: calls collect_osint_data("https://microsoft.com")

4. collect_osint_data() → calls collector.py → collect_all()

5. collector.py calls 10 Web-Check API endpoints:
   GET http://localhost:3000/api/dns?url=https://microsoft.com
   GET http://localhost:3000/api/whois?url=https://microsoft.com
   GET http://localhost:3000/api/ssl?url=https://microsoft.com
   ... (7 more)

6. Web-Check (Docker) performs the actual scans and returns JSON

7. collector.py combines all results into one big dict → returns to agent

8. AI agent OBSERVES: reads all the scan data

9. AI agent THINKS: "Now I'll analyze this and write the report"
   AI agent ACTS: generates the structured audit report following the prompt template

10. assessor.py saves the report as .md and .json files
```

---

## The 10 API Endpoints Explained

| Endpoint | What It Checks | Why It Matters |
|---|---|---|
| `dns` | DNS records (A, MX, NS, CNAME) | Reveals mail servers, nameservers, subdomains |
| `whois` | Domain registration | Owner, registrar, expiry date, creation date |
| `ssl` | SSL/TLS certificate | Expired certs, weak algorithms, certificate chain |
| `get-ip` | Server IP address | Geolocation, hosting provider |
| `headers` | HTTP response headers | Missing security headers = vulnerabilities |
| `http-security` | Security-specific headers | HSTS, CSP, X-Frame-Options analysis |
| `hsts` | HSTS preload status | Whether HTTPS is enforced |
| `cookies` | Cookie attributes | Missing Secure/HttpOnly/SameSite flags |
| `firewall` | WAF detection | Whether a Web Application Firewall is present |
| `tech-stack` | Technologies used | Server software, CMS, CDN, frameworks |

---

## Common Interview Questions

### Q1: "Why did you use Web-Check instead of building your own scanner?"
"Web-Check is a battle-tested open-source OSINT tool with 22k+ GitHub stars. It already handles 30+ types of scans reliably. Instead of reinventing the wheel, I focused on the AI layer — the part that interprets results and generates actionable recommendations. This is the same approach used in enterprise security: collect data from existing tools, then use AI to automate the analysis."

### Q2: "How does the AI know what to look for?"
"The audit prompt provides a structured template that the AI must follow. It tells the AI to check specific things like HSTS, CSP, X-Frame-Options, and to format findings with risk levels. The AI then maps the raw scan data against these requirements. For example, if the headers scan shows no `Strict-Transport-Security` header, the AI marks HSTS as FAIL and recommends adding it."

### Q3: "What if the AI hallucinates or makes things up?"
"I set `temperature=0` for deterministic output, and the prompt explicitly says 'Base ALL findings on actual data from the scan, not assumptions' and 'If a check couldn't be completed, say Unable to determine.' The AI's analysis is grounded in real scan data, not hypotheticals."

### Q4: "What security headers are most important?"
- **HSTS (Strict-Transport-Security)** — Forces HTTPS, prevents SSL stripping
- **CSP (Content-Security-Policy)** — Prevents XSS by controlling script sources
- **X-Frame-Options** — Prevents clickjacking via iframe embedding
- **X-Content-Type-Options** — Prevents MIME sniffing attacks
- **Referrer-Policy** — Controls how much info is sent in the Referer header

### Q5: "What would you improve?"
- Add Nmap port scanning via `python-nmap` for deeper port analysis
- Add CVE lookup: cross-reference detected tech versions with NVD database
- Support local AI models (Ollama) for offline/private assessments
- Add historical tracking: compare reports over time to detect changes
- Export directly to PDF with proper formatting

### Q6: "Why separate collector.py from assessor.py?"
"Separation of concerns. The collector handles data gathering, the assessor handles AI analysis. If I want to swap Web-Check for Shodan or Nmap, I only change collector.py — the AI logic stays untouched. It also makes testing easier: I can test data collection independently."

### Q7: "Can this replace a human security auditor?"
"No — and it's not meant to. It automates the initial assessment and generates a draft report, but a human auditor still needs to verify findings, test for business logic flaws, and assess context-specific risks. Think of it as an assistant that handles the tedious data collection and initial analysis."

### Q8: "How does the Web-Check Docker container work?"
"Web-Check is a Node.js application that provides both a web dashboard and REST API. When you run it in Docker, it exposes port 3000. Each API endpoint accepts a URL parameter and returns JSON with scan results. My Python code simply makes HTTP GET requests to these endpoints."

---

## What Makes This Project Resume-Worthy

1. **Open-source integration** — Not a toy project; built on a real tool with 22k+ stars
2. **AI agent architecture** — Uses LangGraph ReAct pattern (cutting-edge AI engineering)
3. **Real output** — Generates actual professional security audit reports
4. **Security domain knowledge** — Shows you understand headers, SSL, DNS, OWASP concepts
5. **Clean architecture** — Config/Collector/Assessor separation shows software engineering skills
6. **Practical value** — Could actually be used in a real security assessment workflow
