from tagth.tagth import allowed


def test_regular_user_with_basic_permission_1():
    p = "user, content_view"
    r = "content:read, metatdata:write"
    assert allowed(p, r, "read")


def test_regular_user_with_basic_permission_2():
    p = "admin, content_view"
    r = "content:read, admin:write"
    assert allowed(p, r, "write")


def test_regular_user_with_basic_permission_3():
    p = "user, content_view"
    r = "content:read, metatdata:write"
    assert not allowed(p, r, "delete")


def test_regular_user_with_basic_permission_4():
    p = "content_viewer"
    r = "content:view"
    assert allowed(p, r, "view")


def test_regular_user_with_basic_permission_5():
    p = "admin"
    r = "admin:write"
    assert allowed(p, r, "write")


def test_regular_user_with_basic_permission_6():
    p = "admin"
    r = "admin:write"
    assert not allowed(p, r, "delete")


def test_principal_with_partial_action_match():
    p = "content_viewer"
    r = "content:view"
    assert not allowed(p, r, "view_more")


def test_empty_resource():
    p = "content_viewer"
    r = ""
    assert not allowed(p, r, "view")


def test_empty_principal():
    p = ""
    r = "content:read"
    assert not allowed(p, r, "read")

    p = ","
    r = "content:read"
    assert not allowed(p, r, "read")

    p = ", content"
    r = "content:read"
    assert allowed(p, r, "read")


def test_invalid_resource():
    p = "content:viewer"
    r = "content:view@"
    assert not allowed(p, r, "view")


def test_multiple_actions_on_resource():
    p = "admin"
    r = "admin:view, admin:edit"
    assert allowed(p, r, "edit")


def test_principal_multiple_actions_1():
    p = "content_viewer"
    r = "content:view, content:edit"
    assert allowed(p, r, "edit")


def test_principal_multiple_actions_2():
    p = "user"
    r = "user:read, user:edit"
    assert allowed(p, r, "read")


def test_root_has_full_access():
    p = "root"
    r = "content:read, metadata:write"

    assert allowed(p, r, "anything")
    assert allowed(p, r, "write")

    r = "content:all"
    assert allowed(p, r, "all")

    r = "any:read"
    assert allowed(p, r, "read")
 

    r = "anyone:read"
    assert allowed(p, r, "write")


def test_void_principal():
    p = "void"
    r = "anyone:read"

    assert allowed(p, r, "read")
    assert not allowed(p, r, "write")

    r = "content:read"
    assert not allowed(p, r, "read")

    r = "content:all"
    assert not allowed(p, r, "read")


def test_principal_tags_and_supertags():
    p = "admin"
    r = "admin_user:write, admin_content:delete"

    assert allowed(p, r, "write")
    assert allowed(p, r, "delete")
    assert not allowed(p, r, "read")


def test_superactions_1():
    p = "content_viewer"
    r = "content:create"

    assert allowed(p, r, "create")
    assert allowed(p, r, "create_assest")


def test_superactions_2():
    p = "admin"
    r = "admin:create"

    assert allowed(p, r, "create")
    assert allowed(p, r, "create_assest")
    assert not allowed(p, r, "write_message")


def test_any_resource():
    p = "user"
    r = "anyone:read"

    assert allowed(p, r, "read")
    assert not allowed(p, r, "delete")


def test_anyone_resource():
    p_root = "root"
    p_void = "void"
    p_user = "user"

    r = "anyone:read"

    assert allowed(p_root, r, "read")
    assert allowed(p_void, r, "read")
    assert allowed(p_user, r, "read")
    assert allowed(p_root, r, "write")
    assert not allowed(p_void, r, "write")
    assert not allowed(p_user, r, "write")


def test_special_format_any():
    p_root = "root"
    p_void = "void"
    p_user = "user"

    r = ":read"

    assert not allowed(p_root, r, "read")
    assert not allowed(p_void, r, "read")
    assert not allowed(p_user, r, "read")
    assert not allowed(p_root, r, "write")
    assert not allowed(p_void, r, "write")
    assert not allowed(p_user, r, "write")


def test_special_format_all():
    p_root = "root"
    p_void = "void"
    p_user = "user"
    p = "another"

    r = "user:"

    assert not allowed(p_root, r, "read")
    assert not allowed(p_void, r, "read")
    assert not allowed(p_user, r, "read")
    assert not allowed(p, r, "read")


def test_all_resource():
    p_root = "root"
    p_void = "void"
    p_user = "user"
    p = "another"

    r = "user:all"

    assert allowed(p_root, r, "read")
    assert not allowed(p_void, r, "read")
    assert allowed(p_user, r, "read")
    assert not allowed(p, r, "read")


def test_special_format_any_and_all():
    p_root = "root"
    p_void = "void"
    p_user = "user"

    r = ":"

    assert not allowed(p_root, r, "read")
    assert not allowed(p_void, r, "read")
    assert not allowed(p_user, r, "read")
    assert not allowed(p_root, r, "all")
    assert not allowed(p_void, r, "all")
    assert not allowed(p_user, r, "all")
