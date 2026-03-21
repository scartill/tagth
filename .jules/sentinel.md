## 2024-05-18 - [Privilege Escalation via Prefix Matching of Special Actions]
**Vulnerability:** A user granted an action tag that is a prefix of a special internal action like `all` (e.g., `a` or `al`) is erroneously granted full system access because the authorization library evaluates `action.startswith(allowed_action)`.
**Learning:** When using prefix-based string matching for authorization tags or actions, special values that represent full access (e.g., `all`, `*`) must be explicitly excluded from being matched as a suffix to a user's tag.
**Prevention:** Always check for an exact match against special reserved actions before falling back to prefix matching for regular actions.
