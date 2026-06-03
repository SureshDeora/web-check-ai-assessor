# Website Security Audit Report

**Target:** https://microsoft.com  
**Date:** 2026-06-03 09:05  
**Auditor:** AI Security Assessor (Web-Check + GPT)

---

## 1. Basic Information

| Item | Details |
|---|---|
| Domain Name | microsoft.com |
| Organization Name (from whois) | Microsoft Corporation |
| IP Address | 13.107.226.48 |
| Registrar | MarkMonitor Inc. |
| SSL Certificate Status | Valid; Issuer: Microsoft Corporation / Microsoft TLS G2 RSA CA OCSP 16; Expires: 2026-11-08 23:30:11 GMT |
| Key DNS Records (A, MX, NS) | A: 13.107.253.48, 13.107.226.48<br>MX: microsoft-com.mail.protection.outlook.com (priority 10)<br>NS: ns1-39.azure-dns.com, ns2-39.azure-dns.net, ns3-39.azure-dns.org, ns4-39.azure-dns.info |

---

## 2. Security Audit Checklist

| Control | Status | Explanation |
|---|---|---|
| HTTPS Enabled | PASS | The site is served over HTTPS and the response indicates TLS 1.3 in use. |
| Valid SSL Certificate | PASS | Certificate validity is confirmed: `isValid: true`, valid from 2026-05-12 to 2026-11-08. |
| HSTS Header present | PASS | `strict-transport-security: max-age=31536000; includeSubDomains` is present. Note: scan also reports the HSTS configuration as not fully compatible because the header does not include all subdomains in the scanner’s assessment. |
| Content Security Policy (CSP) | FAIL | No CSP header was detected (`contentSecurityPolicy: false`). |
| X-Frame-Options | FAIL | No `X-Frame-Options` header was detected (`xFrameOptions: false`). |
| X-Content-Type-Options | FAIL | No `X-Content-Type-Options` header was detected (`xContentTypeOptions: false`). |
| Secure Cookie flags (Secure, HttpOnly, SameSite) | FAIL | One cookie includes `Secure` and `SameSite=None` (`CAS_PROGRAM=echo`), but `HttpOnly` was not observed in the header data. Another cookie (`bStore=Y`) lacks security attributes in the observed response. |
| Login Page Presence | Unable to determine | The scan data does not include page discovery or endpoint enumeration results for login functionality. |
| Contact Information Exposure | Unable to determine | The collected data does not provide page content or contact pages. |
| Email Address Exposure | Unable to determine | No page-body analysis was included in the scan output. |

---

## 3. Technology Stack

| Component | Detected Value |
|---|---|
| Web Server | Unable to determine from the collected scan data |
| CMS | Unable to determine from the collected scan data |
| Programming Language/Framework | Unable to determine from the collected scan data |
| CDN Used | Likely Microsoft/Azure edge delivery based on `x-azure-ref` and Azure DNS, but a specific CDN product was not explicitly identified in the scan output |
| Third-Party Services detected | Microsoft 365/Outlook mail protection, Azure DNS, plus multiple verification tokens indicating services such as 1Password, Adobe/Marketo (`d365mktkey`), Zoom, Anthropic, Atlassian, OpenAI, HubSpot, DocuSign, Workplace, Linear, Mixpanel, Sitecore, Airtable, Facebook, Google, Liveramp, and HPE GreenLake |

---

## 4. Findings (minimum 5)

### 1) Missing Content Security Policy
- **Risk Level:** Medium
- **Description:** The response does not include a Content Security Policy header.
- **Evidence:** `http-security.contentSecurityPolicy: false`
- **Impact:** If any injection flaw exists in the site or downstream content, the absence of CSP increases the likelihood of successful XSS and content injection abuse.

### 2) Missing X-Frame-Options Header
- **Risk Level:** Low
- **Description:** The site does not send an `X-Frame-Options` header.
- **Evidence:** `http-security.xFrameOptions: false`
- **Impact:** The site may be more exposed to clickjacking if other frame-busting controls are not implemented.

### 3) Missing X-Content-Type-Options Header
- **Risk Level:** Low
- **Description:** The response does not include `X-Content-Type-Options: nosniff`.
- **Evidence:** `http-security.xContentTypeOptions: false`
- **Impact:** Browsers may perform MIME sniffing in some contexts, which can increase exposure to content-type confusion attacks.

### 4) Cookie Security Not Fully Hardened
- **Risk Level:** Medium
- **Description:** At least one cookie is set without a complete set of security attributes; `HttpOnly` was not observed, and one cookie appears to lack `Secure` and `SameSite`.
- **Evidence:** `set-cookie: bStore=Y; expires=...` and `set-cookie: CAS_PROGRAM=echo; ...; path=/; secure; SameSite=None`
- **Impact:** Cookies without strong flags are more susceptible to theft via client-side attacks or improper cross-site usage depending on application behavior.

### 5) HSTS Configuration Assessment Incomplete for Full Subdomain Coverage
- **Risk Level:** Low
- **Description:** HSTS is present, but the scanner flagged it as not compatible because the header does not include all subdomains according to its check.
- **Evidence:** `strict-transport-security: max-age=31536000; includeSubDomains` and `hsts.message: "HSTS header does not include all subdomains."`
- **Impact:** If any related subdomain is reachable without TLS enforcement, users may be exposed to downgrade or SSL-stripping risk.

### 6) Public Exposure of Extensive Third-Party Verification Records
- **Risk Level:** Low
- **Description:** The DNS TXT records contain many third-party verification tokens and service integrations.
- **Evidence:** TXT records for OpenAI, Zoom, Atlassian, DocuSign, HubSpot, Mixpanel, Sitecore, Airtable, Facebook, Google, 1Password, Anthropic, and others.
- **Impact:** This does not indicate a direct vulnerability, but it increases the external attack surface and provides useful intelligence about the organization’s SaaS footprint.

---

## 5. Recommendations (minimum 5)

### 1) Deploy a Strict Content Security Policy
- **Priority:** High
- **Action:** Add a restrictive CSP tailored to the site’s actual script, style, and frame requirements. Start in report-only mode if needed, then enforce.
- **Example:**
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'self' https: 'unsafe-inline'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';
  ```

### 2) Add Clickjacking Protections
- **Priority:** Medium
- **Action:** Configure `X-Frame-Options` and/or `frame-ancestors` in CSP to prevent unauthorized framing.
- **Example:**
  ```http
  X-Frame-Options: DENY
  ```
  or, preferred with CSP:
  ```http
  Content-Security-Policy: frame-ancestors 'none';
  ```

### 3) Enable MIME Sniffing Protection
- **Priority:** Medium
- **Action:** Add `X-Content-Type-Options: nosniff` on all HTML and static responses.
- **Example:**
  ```http
  X-Content-Type-Options: nosniff
  ```

### 4) Harden Cookie Flags
- **Priority:** High
- **Action:** Ensure all authentication and session-related cookies use `Secure`, `HttpOnly`, and an appropriate `SameSite` value. Review whether `SameSite=None` is truly required.
- **Example:**
  ```http
  Set-Cookie: sessionid=...; Path=/; Secure; HttpOnly; SameSite=Lax
  ```

### 5) Verify and Enforce HSTS Across the Full Domain Estate
- **Priority:** Medium
- **Action:** Confirm that every production subdomain is HTTPS-only before maintaining `includeSubDomains`. Consider adding `preload` if the domain meets preload requirements.
- **Example:**
  ```http
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  ```

### 6) Review and Minimize Public DNS Verification Records
- **Priority:** Low
- **Action:** Periodically audit TXT records and remove obsolete verification entries and unused service tokens.
- **Example:** No command required; use DNS management review and lifecycle cleanup for stale verification records.

---

## 6. Overall Security Rating

- **Score:** 82/100
- **Rating:** Good
- **Summary:** Microsoft’s main domain demonstrates strong baseline transport security with a valid certificate, HTTPS enforcement, and HSTS enabled. However, several important browser-side hardening headers are missing, and cookie security is not fully consistent across observed response headers, which prevents a higher rating.

