# SF-002 — Content Security Policy (CSP) Header Not Set

## Status

Open

## Severity

Medium

## Category

Security Misconfiguration

## Detection

OWASP ZAP DAST

## OWASP ZAP Alert

Content Security Policy (CSP) Header Not Set

## Affected Endpoint

GET /

## Description

OWASP ZAP identified that the application does not currently
define a Content Security Policy (CSP) response header.

A Content Security Policy provides a browser-enforced layer of
protection that can restrict the sources from which scripts,
styles, images, and other resources may be loaded.

## Security Impact

Without an appropriate Content Security Policy, the application
has less browser-side protection against certain classes of
content injection and cross-site scripting attacks.

The practical impact depends on the application's resource
loading behavior and the presence of other security controls.

## Evidence

The issue was detected during the automated OWASP ZAP DAST
baseline scan.

OWASP ZAP reported:

`Content Security Policy (CSP) Header Not Set`

Affected endpoint:

`GET /`

## Remediation Plan

Implement an application-appropriate Content Security Policy
rather than applying an unnecessarily restrictive policy that
could break legitimate application functionality.

The policy should be reviewed against the application's actual
JavaScript, CSS, image, font, API, and external resource
requirements.

## Validation

After remediation, the application will be re-scanned using the
OWASP ZAP DAST pipeline.

The remediation will be considered validated when the relevant
CSP finding is no longer reported or has been appropriately
reviewed and documented.

## Security Engineering Notes

This finding demonstrates the importance of validating automated
scanner results against real application requirements.

Security headers should be implemented deliberately and tested
for application compatibility rather than added solely to
eliminate scanner alerts.

## Remediation Status

Pending remediation.
