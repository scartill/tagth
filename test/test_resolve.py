from tagth.tagth import _resolve


def test_with_root_principal():
    p = "root, user"
    r = "content:read"
    a = _resolve(p, r)
    assert a == {"all"}


def test_epmpty_resource():
    p = "user"
    r = ""
    a = _resolve(p, r)
    assert a == set()

    p = "root"
    r = ""
    a = _resolve(p, r)
    assert a == {"all"}


def test_empty_principle():
    p = ""
    r = "user:read"
    a = _resolve(p, r)
    assert a == set()

    # check the expected result
    p = ""
    r = "anyone:read"
    a = _resolve(p, r)
    assert a == {"read"}

    p = ""
    r = "admin:all"
    a = _resolve(p, r)
    assert a == set()


def test_with_void_principal():
    p = "void"
    r = "content:read, metadata:write"
    a = _resolve(p, r)
    assert a == set()

    p = "void"
    r = "anyone:read, anyone:write"
    a = _resolve(p, r)
    assert a == {"read", "write"}


def test_with_matching_tags():
    p = "admin"
    r = "admin:read, admin:write"
    a = _resolve(p, r)
    assert a == {"read", "write"}

    p = "admin"
    r = "anyone:read, admin:write"
    a = _resolve(p, r)
    assert a == {"read", "write"}

    p = "admin"
    r = "user:read, admin:write"
    a = _resolve(p, r)
    assert a == {"write"}

    p = "me"
    r = "me:all"
    a = _resolve(p, r)
    assert a == {"all"}

    p = "me"
    r = "meme_me:all"
    a = _resolve(p, r)
    assert a == {"all"}

    p = "me"
    r = "xmememe:ro, meme:rw"
    a = _resolve(p, r)
    assert a == {"rw"}


def test_with_no_matching_tags():
    p = "user"
    r = "admin:write"
    a = _resolve(p, r)
    assert a == set()


def test_with_supertag_match():
    p = "admin"
    r = "admin_user:read"
    a = _resolve(p, r)
    assert a == {"read"}

    p = "admin"
    r = "admin_user:read, admin_content:delete"
    a = _resolve(p, r)
    assert a == {"read", "delete"}

    p = "user"
    r = "admin_user:read"
    a = _resolve(p, r)
    assert a == set()


def test_with_any_resource_tag():
    p = "user"
    r = "anyone:read"
    a = _resolve(p, r)
    assert a == {"read"}

    p = "user"
    r = "anyone:read, content:write"
    a = _resolve(p, r)
    assert a == {"read"}


def test_with_all_action_tag():
    p = "user"
    r = "content:all"
    a = _resolve(p, r)
    assert a == set()

    p = "content"
    r = "content:all"
    a = _resolve(p, r)
    assert a == {"all"}


def test_with_multiple_principle():
    p = "admin, user"
    r = "admin:write, user:read"
    a = _resolve(p, r)
    assert a == {"read", "write"}


def test_with_root_and_void_principal():
    p = "void, root"
    r = "content:read, content:write"
    a = _resolve(p, r)
    assert a == {"all"}


def test_with_special_format():
    p = "user"
    r = "anyone:all"
    a = _resolve(p, r)
    assert a == {"all"}

    p = "user"
    r = "anyone:read"
    a = _resolve(p, r)
    assert a == {"read"}

    p = "user"
    r = "user:all"
    a = _resolve(p, r)
    assert a == {"all"}


def test_principal_tags_and_supertags():
    p = "admin"
    r = "admin_user:write, admin_content:delete"
    a = _resolve(p, r)
    assert a == {"write", "delete"}


# failed tests, need checking
def test_principal_tag_start_with_resource_1():
    p = "user, content_viewer"
    r = "content:read, metadata:write"
    a = _resolve(p, r)
    assert a == {"write", "read"}


def test_principal_tag_start_with_resource_2():
    p = "content_viewer"
    r = "content:view"
    a = _resolve(p, r)
    assert a == {"view"}


def test_principal_multiple_actions():
    p = "content_viewer"
    r = "content:view, content:edit"
    a = _resolve(p, r)
    assert a == {"view", "edit"}


def test_principal_multiple_tags():
    p = "content_viewer, admin"
    r = "content:view, admin:manage"
    a = _resolve(p, r)
    assert a == {"view", "manage"} 
