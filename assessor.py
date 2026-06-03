import os
import sys
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from collector import collect_all
from config import MODEL_NAME, REPORTS_DIR

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)


@tool
def collect_osint_data(url: str) -> str:
	"""Collects OSINT data from Web-Check for a target URL.
	Returns DNS, SSL, headers, security, tech stack, and whois data.
	Always call this first before analyzing anything."""
	results = collect_all(url)
	return json.dumps(results, indent=2, default=str)


tools = [collect_osint_data]
agent = create_react_agent(model=llm, tools=tools)

AUDIT_PROMPT = """You are a professional cybersecurity auditor. Perform a complete
security audit on {target_url} and generate a professional audit report.

INSTRUCTIONS:
1. First, collect all OSINT data using the collect_osint_data tool.
2. Then analyze the data and write a professional security audit report.

YOUR REPORT MUST FOLLOW THIS EXACT STRUCTURE:

# Website Security Audit Report

**Target:** {target_url}
**Date:** {date}
**Auditor:** AI Security Assessor (Web-Check + GPT)

---

## 1. Basic Information
Present these in a clean table:
- Domain Name
- Organization Name (from whois)
- IP Address
- Registrar
- SSL Certificate Status (valid/expired, issuer, expiry date)
- Key DNS Records (A, MX, NS)

## 2. Security Audit Checklist
Check EACH of these and mark as PASS/FAIL with explanation:
- HTTPS Enabled
- Valid SSL Certificate
- HSTS Header present
- Content Security Policy (CSP)
- X-Frame-Options
- X-Content-Type-Options
- Secure Cookie flags (Secure, HttpOnly, SameSite)
- Login Page Presence
- Contact Information Exposure
- Email Address Exposure

## 3. Technology Stack
Identify and list:
- Web Server (e.g., nginx, Apache, IIS)
- CMS (e.g., WordPress, if any)
- Programming Language/Framework
- CDN Used (e.g., Cloudflare, Akamai)
- Third-Party Services detected

## 4. Findings (minimum 5)
For EACH finding, provide:
- **Finding title**
- **Risk Level:** Critical / High / Medium / Low
- **Description:** What the issue is
- **Evidence:** The specific data that proves this
- **Impact:** What could happen if exploited

## 5. Recommendations (minimum 5)
For EACH recommendation:
- **Title**
- **Priority:** Critical / High / Medium / Low
- **Action:** Specific steps to fix the issue
- **Example:** Config snippet or command if applicable

## 6. Overall Security Rating
Rate the website's security posture:
- Score: X/100
- Rating: Critical / Poor / Fair / Good / Excellent
- Summary: 2-3 sentences explaining the rating

IMPORTANT RULES:
- Base ALL findings on actual data from the scan, not assumptions
- If a check couldn't be completed, say "Unable to determine" — don't make things up
- Be specific — use actual values from the scan data
- Write like a professional security consultant
"""


def run_audit(target_url):
	print("=" * 60)
	print("  Web-Check AI Security Assessor")
	print(f"  Target: {target_url}")
	print(f"  Model:  {MODEL_NAME}")
	print("=" * 60)

	prompt = AUDIT_PROMPT.format(
		target_url=target_url,
		date=datetime.now().strftime("%Y-%m-%d %H:%M"),
	)

	print("\n[*] Starting AI security assessment...\n")
	response = agent.invoke(
		{"messages": [{"role": "user", "content": prompt}]}
	)

	report = response["messages"][-1].content

	os.makedirs(REPORTS_DIR, exist_ok=True)
	domain = target_url.replace("https://", "").replace("http://", "")
	domain = domain.replace("/", "").replace(":", "")
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"{domain}_{timestamp}"

	json_path = os.path.join(REPORTS_DIR, f"{filename}.json")
	with open(json_path, "w") as f:
		json.dump({
			"target": target_url,
			"date": datetime.now().isoformat(),
			"model": MODEL_NAME,
			"report": report,
		}, f, indent=4)

	md_path = os.path.join(REPORTS_DIR, f"{filename}.md")
	with open(md_path, "w") as f:
		f.write(report)

	print("\n" + "=" * 60)
	print("  SECURITY AUDIT REPORT")
	print("=" * 60)
	print(report)
	print("\n" + "=" * 60)
	print(f"  Report saved to:")
	print(f"  ├─ {json_path}")
	print(f"  └─ {md_path}")
	print(f"\n  To convert to PDF:")
	print(f"  pip install md2pdf && md2pdf {md_path}")
	print("=" * 60)

	return report


if __name__ == "__main__":
	default_target = "https://microsoft.com"

	if len(sys.argv) > 1:
		target = sys.argv[1]
	else:
		target = default_target
		print(f"[*] No URL provided. Using default: {target}")
		print(f"[*] Usage: python assessor.py https://example.com\n")

	if not target.startswith("http"):
		target = f"https://{target}"

	run_audit(target)
