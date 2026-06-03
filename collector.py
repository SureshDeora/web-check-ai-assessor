import json
import requests
from config import (
	WEB_CHECK_URL,
	INFO_ENDPOINTS,
	SECURITY_ENDPOINTS,
	TECH_ENDPOINTS,
	REQUEST_TIMEOUT,
)


def call_endpoint(endpoint, target_url):
	"""Call a single Web-Check API endpoint."""
	api_url = f"{WEB_CHECK_URL}/api/{endpoint}?url={target_url}"
	try:
		response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
		return response.json()
	except requests.exceptions.Timeout:
		return {"error": f"Timeout after {REQUEST_TIMEOUT}s"}
	except requests.exceptions.ConnectionError:
		return {"error": "Cannot connect to Web-Check. Is Docker running?"}
	except Exception as e:
		return {"error": str(e)}


def collect_all(target_url):
	"""Run all security checks on a target website."""
	all_endpoints = INFO_ENDPOINTS + SECURITY_ENDPOINTS + TECH_ENDPOINTS
	results = {}

	print(f"\n[*] Scanning {target_url}...")
	print(f"[*] Running {len(all_endpoints)} checks...\n")

	for endpoint in all_endpoints:
		print(f"  ├─ {endpoint}...", end=" ", flush=True)
		results[endpoint] = call_endpoint(endpoint, target_url)

		if "error" in results[endpoint]:
			print(f"✗ {results[endpoint]['error']}")
		else:
			print("✓")

	print(f"\n[✓] Data collection complete.\n")
	return results


if __name__ == "__main__":
	data = collect_all("https://microsoft.com")
	print(json.dumps(data, indent=2, default=str)[:3000])
