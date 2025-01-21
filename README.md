# Stateless Tag-Based Authorization Library

## Background

Traditional role-based authorization models are not flexible enough to cover all required use cases. On the other side, full-managed ACLs are too complex for account managers to handle. `tagth` is a simple and flexible authorization model that can be easily implemented and maintained.

## Tag-Based Authorization

A lightweight model that is based on three concepts:
* a principal and its associated tags,
* a resource and its associated tags,
* an action.

The model adheres to the following principles:
* the model is stateless and purely functional, and it has no internal persistence,
* the model does not interpret the tags or actions, besides the special values,
* the model produces a binary result: either the action is allowed or not.

### Principal and Principal Tags

A Principal is an acting entity. A Principal can be a user, a role, a group, or any other entity that can perform actions.

Principal’s auth tag string looks like a comma-separated list of tags: `tag_one, tag_two, tag_three`. Each tag should be a string that is a valid Python identifier.

A supertag is a tag that is a prefix of another tag. For example, `admin` is a supertag of `admin_user`.

A principal is said to possess a tag if the tag or its supertag exists in the principal’s auth tag string.

Special values:
* `void` (can only access resources with `any` access, see below),
* `root` (unlimited access).

### Resource and Resource Tags

A Resource is an object that can be accessed by a Principal. A Resource can be a user, a channel, a source asset, an extension, a tenant, a campaign, etc.

A resource tag is a string that is a valid Python identifier. *NB: there is no such thing as a supertag for a resource tag.*

An action is a string that is a valid Python identifier. A superaction is an action that is a prefix of another action. For example, `create` is a superaction of `create_asset`.

Resource auth tag string looks like a comma-separated of colon-separarted pairs of tags and actions: `tag_one:read, tag_two:write` (tags with associated actions).

An action is allowed for a principal if it possesses:
* a tag that is associated with the action
* a tag that is associated with the superaction of the action
* the `root` tag

Special values:
* `any` resource tag (any principal is allowed to perform action).
* `all` action (all action are allowed).

Actions may be omitted (`tag_one` is equivalent to `tag_one:all`), tags can be omitted (`:read` is equivalent to `any:read`), or both (`:` means `any:all` - unlimited access for all).

### Access Resolution

The model makes a decision based on the following three values **only**:
* the principal’s auth tag string
* the resource’s auth tag string
* the action to be performed

The resolution is binary: either the action is allowed or not.

## Examples

### Basic Usage

```python
from tagth import allowed

# A regular user with basic permissions
principal_tags = 'user, content_viewer'
resource_tags = 'content:read, metadata:write"

# Check if user can read content
allowed(principal_tags, resource_tags, "read")  # Returns True
# Check if user can delete content
allowed(principal_tags, resource_tags, "delete")  # Returns False

# Root user has unlimited access
principal_tags = "root"
allowed(principal_tags, resource_tags, "anything")  # Returns True

# Void user can only access 'any' resources
void_tags = "void"
allowed(void_tags, "any:read", "read")  # Returns True
allowed(principal_tags, "content:read", "read")  # Returns False
```

### Supertags and Superactions

```python
# Principal tags can be supertags
principal_tags = "admin"
resource_tags = "admin_user:write, admin_content:delete"

# 'admin' is a supertag of 'admin_user' and 'admin_content'
allowed(principal_tags, resource_tags, "write")  # Returns True
allowed(principal_tags, resource_tags, "delete")  # Returns True

# Actions can have superactions
principal_tags = "content_manager"
resource_tags = "content:create"

# 'create' is a superaction of 'create_asset'
allowed(principal_tags, resource_tags, "create_asset")  # Returns True
```

### Special Values

```python
# 'any' resource tag allows access to all principals
principal_tags = 'basic_user'
resource_tags = 'any:read'
allowed(principal_tags, resource_tags, 'read')  # Returns True

# 'all' action allows all actions
principal_tags = 'content'
resource_tags = 'content:all'
allowed(principal_tags, resource_tags, 'read')  # Returns True
allowed(principal_tags, resource_tags, 'write')  # Returns True

resource_tags = ":read"  # Equivalent to "any:read"
allowed(principal_tags, resource_tags, "read")  # Returns True

resource_tags = ":"  # Equivalent to "any:all"
allowed(principal_tags, resource_tags, "any_action")  # Returns True
```
