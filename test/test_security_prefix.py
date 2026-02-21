from tagth.tagth import allowed, _resolve

def test_strict_prefix_matching_tags():
    """Test that tags are matched strictly (exact or prefix + '_')."""
    # Exact match
    assert allowed("admin", "admin:read", "read")

    # Prefix match with underscore
    assert allowed("admin", "admin_user:read", "read")

    # Prefix match without underscore (should fail)
    assert not allowed("admin", "administrator:read", "read")
    assert not allowed("me", "meme:read", "read")
    assert not allowed("dev", "device:read", "read")

def test_strict_prefix_matching_actions():
    """Test that actions are matched strictly (exact or prefix + '_')."""
    # Exact match
    assert allowed("user", "user:read", "read")

    # Prefix match with underscore
    assert allowed("user", "user:read", "read_all")

    # Prefix match without underscore (should fail)
    assert not allowed("user", "user:read", "reading")
    assert not allowed("user", "user:create", "created")

def test_resolve_strictness():
    """Test _resolve function for strict matching."""
    # admin matches admin_user
    assert _resolve("admin", "admin_user:read") == {"read"}

    # admin does NOT match administrator
    assert _resolve("admin", "administrator:read") == set()

    # multiple tags
    p = "admin"
    r = "admin_user:read, administrator:write"
    assert _resolve(p, r) == {"read"}
