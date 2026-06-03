import os
from dotenv import load_dotenv

load_dotenv()

WEB_CHECK_URL = os.getenv("WEB_CHECK_URL", "http://localhost:3000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INFO_ENDPOINTS = ["dns", "whois", "ssl", "get-ip"]
SECURITY_ENDPOINTS = ["headers", "http-security", "hsts", "cookies", "firewall"]
TECH_ENDPOINTS = ["tech-stack"]

REQUEST_TIMEOUT = 30
REPORTS_DIR = "reports"
