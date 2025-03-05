from tagth.tagth import allowed


def test_regular_user_with_basic_permission_1():
    p = "user, content_view"
    r = "content:read, metatdata:write"

    a = allowed(p, r, "delete")
    assert not a


def test_regular_user_with_basic_permission_2():
    p = "user, content_view"
    r = "content:read, metatdata:write"
    a = allowed(p, r, "read")
    assert a


def test_regular_user_with_basic_permission_3():
    p = "content_viewer"
    r = "content:view"
    a = allowed(p, r, "view")
    assert a


def test_principal_with_partial_action_match():
    p = "content_viewer"
    r = "content:view"
    a = allowed(p, r, "view_more")
    assert not a


def test_empty_resource():
    p = "content_viewer"
    r = ""
    a = allowed(p, r, "view")
    assert not a


def test_principal_empty():
    p = ""
    r = "content:view"
    a = allowed(p, r, "view")
    assert not a


def test_invalid_resource():
    p = "content:viewer"
    r = "content:view@"
    a = allowed(p, r, "view")
    assert not a


def test_multiple_actions_on_resource():
    p = "admin"
    r = "admin:view, admin:edit"
    a = allowed(p, r, "edit")
    assert a


def test_different_actions_on_resources_1():
    p = "content_viewer"
    r = "user:view, content:edit"
    a = allowed(p, r, "edit")
    assert a


def test_different_actions_on_resources_2():
    p = "admin"
    r = "user:view, admin:edit"
    a = allowed(p, r, "edit")
    assert a


def test_principal_multiple_actions():
    p = "content_viewer"
    r = "content:view, content:edit"
    a = allowed(p, r, "edit")
    assert a


def test_principal_multiple_tags_1():
    p = "content_viewer, admin"
    r = "content:view, admin:manage"
    a = allowed(p, r, "manage")
    assert a


def test_principal_exact_match_on_resource():
    p = "admin"
    r = "admin:manage"
    a = allowed(p, r, "manage")
    assert a


def test_root_has_full_access():
    p = "root"
    r = "content:read, metadata:write"

    a = allowed(p, r, "anything")
    assert a

    a = allowed(p, r, "write")
    assert a

    r = "content:all"
    a = allowed(p, r, "all")
    assert a

    r = "any:read"
    a = allowed(p, r, "read")
    assert a

    r = "anyone:read"
    a = allowed(p, r, "write")
    assert a


def test_void_principal():
    p = "void"
    r = "anyone:read"

    a = allowed(p, r, "read")
    assert a

    a = allowed(p, r, "write")
    assert not a

    r = "content:read"
    a = allowed(p, r, "read")
    assert not a

    r = "content:all"
    a = allowed(p, r, "read")
    assert not a


def test_principal_tags_and_supertags():
    p = "admin"
    r = "admin_user:write, admin_content:delete"

    a = allowed(p, r, "write")
    assert a

    a = allowed(p, r, "delete")
    assert a

    a = allowed(p, r, "read")
    assert not a


def test_superactions_1():
    p = "content_viewer"
    r = "content:create"

    a = allowed(p, r, "create")
    assert a

    a = allowed(p, r, "create_assest")
    assert a


def test_superactions_2():
    p = "admin"
    r = "admin:create"

    a = allowed(p, r, "create")
    assert a

    a = allowed(p, r, "create_assest")
    assert a


def test_any_resource():
    p = "user"
    r = "anyone:read"

    a = allowed(p, r, "read")
    assert a

    a = allowed(p, r, "delete")
    assert not a


def test_all_actions_allow_all():
    p = "user"
    r = "user:all"

    a = allowed(p, r, "read")
    assert a

    a = allowed(p, r, "all")
    assert a

    p = "content"
    a = allowed(p, r, "read")
    assert not a

    a = allowed(p, r, "all")
    assert not a


def test_special_format_any():
    p_root = "root"
    p_void = "void"
    p_user = "user"

    r = ":read"
    a = allowed(p_root, r, "read")
    assert not a

    a = allowed(p_void, r, "read")
    assert not a

    a = allowed(p_user, r, "read")
    assert not a

    a = allowed(p_root, r, "write")
    assert not a

    a = allowed(p_void, r, "write")
    assert not a

    a = allowed(p_user, r, "write")
    assert not a


def test_special_format_all():
    p_root = "root"
    p_void = "void"
    p_user = "user"
    p = "another"

    r = "user:"
    a = allowed(p_root, r, "read")
    assert not a

    a = allowed(p_void, r, "read")
    assert not a

    a = allowed(p_user, r, "read")
    assert not a

    a = allowed(p, r, "read")
    assert not a


def test_special_format_any_and_all():
    p_root = "root"
    p_void = "void"
    p_user = "user"

    r = ":"
    a = allowed(p_root, r, "read")
    assert not a

    a = allowed(p_void, r, "read")
    assert not a

    a = allowed(p_user, r, "read")
    assert not a

    a = allowed(p_root, r, "all")
    assert not a

    a = allowed(p_void, r, "all")
    assert not a

    a = allowed(p_user, r, "all")
    assert not a
