## 2025-02-17 - [Internal Placeholder Collision]
**Vulnerability:** Found that the string "void" was used both as an internal placeholder for empty/whitespace resources AND as a potential user-controlled principal string. The library's prefix-matching logic allowed a principal named "v" (or "void") to access resources with empty ACLs because "void" starts with "v".
**Learning:** Internal sentinel values must be distinct from the domain of user inputs. Reusing a valid identifier ("void") for a special meaning is risky when coupled with broad matching rules like `startswith`.
**Prevention:** Use characters invalid in user input (like `@` or `$`) for internal sentinel values (e.g., `@empty`), or ensure strict type checking where sentinels are objects, not strings.

## 2025-05-15 - [Broad Prefix Authorization Bypass]
**Vulnerability:** The library used `startswith()` for tag matching, allowing a principal `user` to access resources tagged `username`, `user_admin`, or `users`. This unintentional "supertag" behavior violated the principle of least privilege.
**Learning:** Prefix matching without delimiters is inherently ambiguous and insecure for authorization. It creates overlapping namespaces where short tags accidentally grant access to longer, unrelated tags.
**Prevention:** Always enforce a delimiter (e.g., `_` or `:`) or require exact matches for authorization tags. Use strict matching logic: `tag == target OR tag.startswith(target + delimiter)`.
