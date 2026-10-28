<!--
Owner: project-maintainer
Last Reviewed: 2026-10-25
Status: Accepted
-->

# ADR 010: BNBU-Only Institutional Auth

## Context

The local teaching deployment is intended for BNBU users. Retaining legacy
institution-specific domains in validation, interface copy, and product
documentation creates misleading sign-in guidance.

## Decision

Weak local authentication accepts exactly the BNBU email domains `bnbu.edu.cn`
and `mail.bnbu.edu.cn`. The student-mail domain was added on 2026-10-25 after
the local deployment user confirmed their institutional email uses that domain.
This is an additive correction to institutional coverage, not a wildcard rule
for all subdomains. Registration and login use the same domain check.
Existing role and token response shapes remain unchanged; accepted BNBU accounts
use the `teacher` role, which retains full phase-1 generation capability.

All active product copy, tests, reference slide branding, and governance material
use BNBU terminology.

## Consequences

- Accounts from other domains cannot register or log in.
- Previously created sessions remain usable until expiry because bearer-token
  validation is unchanged.
- Previously created accounts from other domains cannot create a new session.
- A future domain expansion must update the auth contract, implementation, and
  focused tests together.
