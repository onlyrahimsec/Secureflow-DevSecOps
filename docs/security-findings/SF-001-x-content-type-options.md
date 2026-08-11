# SF-001 — Missing X-Content-Type-Options Header

## Status

Open

## Severity

Low

## Category

Security Misconfiguration

## Detection

OWASP ZAP DAST

## OWASP ZAP Alert

X-Content-Type-Options Header Missing

## Affected Endpoint

GET /

## Evidence

OWASP ZAP identified that the application response does not include
the `X-Content-Type-Options` HTTP security header.

Detected response:

```http
HTTP/1.1 200 OK
