## 2025-02-17 - [Internal Placeholder Collision]
**Vulnerability:** Found that the string "void" was used both as an internal placeholder for empty/whitespace resources AND as a potential user-controlled principal string. The library's prefix-matching logic allowed a principal named "v" (or "void") to access resources with empty ACLs because "void" starts with "v".
**Learning:** Internal sentinel values must be distinct from the domain of user inputs. Reusing a valid identifier ("void") for a special meaning is risky when coupled with broad matching rules like `startswith`.
**Prevention:** Use characters invalid in user input (like `@` or `$`) for internal sentinel values (e.g., `@empty`), or ensure strict type checking where sentinels are objects, not strings.

## 2025-02-18 - [Intended Insecure Prefix Matching]
**Vulnerability:** Identified that the library uses loose string prefix matching (e.g., `admin` matches `administrator`), which can lead to unintended privilege escalation if tag names are not chosen carefully.
**Learning:** This behavior is an **intended feature** of the library, not a bug to be fixed by code changes. The library relies on simple `startswith` logic for "supertags".
**Prevention:** Do NOT attempt to change the matching logic to be stricter (e.g., delimiter-based). Instead, document this behavior clearly so users can design their tag schemas accordingly (e.g., avoiding overlapping prefixes for distinct roles).

## 2024-05-18 - [Privilege Escalation via Prefix Matching of Special Actions]
**Vulnerability:** A user granted an action tag that is a prefix of a special internal action like `all` (e.g., `a` or `al`) is erroneously granted full system access because the authorization library evaluates `action.startswith(allowed_action)`.
**Learning:** When using prefix-based string matching for authorization tags or actions, special values that represent full access (e.g., `all`, `*`) must be explicitly excluded from being matched as a suffix to a user's tag.
**Prevention:** Always check for an exact match against special reserved actions before falling back to prefix matching for regular actions.
