import pytest

from tagth.tagth import allowed


@pytest.mark.parametrize(
    'p, r, action, expected',
    [
        ('user, content_view', 'content:read, metatdata:write', 'read', True),
        ('admin, content_view', 'content:read, admin:write', 'write', True),
        ('user, content_view', 'content:read, metatdata:write', 'delete', False),
        ('content_viewer', 'content:view', 'view', True),
        ('admin', 'admin:write', 'write', True),
        ('admin', 'admin:write', 'admin:write', False),
        ('content_viewer', 'content:view', 'view_more', False)

    ]
)
def test_regular_user_with_basic_permission(p, r, action, expected):
    assert allowed(p, r, action) == expected


@pytest.mark.parametrize(
    'p, r, action, expected',
    [
        ('content_viewer', 'content:create', 'create', True),
        ('content_viewer', 'content:create', 'create_assest', True),
        ('admin', 'admin:create', 'create', True),
        ('admin', 'admin:create', 'create_assest', True),
        ('admin', 'admin:create', 'write_message', False)
    ]
)
def test_superactions(p, r, action, expected):
    assert allowed(p, r, action) == expected


@pytest.mark.parametrize(
    'p, r, action, expected',
    [
        ('admin', 'admin:view, admin:edit', 'edit', True),
        ('content_viewer', 'content:view, content:edit', 'edit', True)
    ]
)
def test__multiple_actions(p, r, action, expected):
    assert allowed(p, r, action) == expected


def test_principal_with_partial_action_match():
    p = 'content_viewer'
    r = 'content:view'
    assert not allowed(p, r, 'view_more')


def test_empty_resource():
    p = 'content_viewer'
    r = ''
    assert not allowed(p, r, 'view')


def test_empty_principal():
    p = ''
    r = 'content:read'
    assert not allowed(p, r, 'read')

    p = ','
    r = 'content:read'
    assert not allowed(p, r, 'read')

    p = ', content'
    r = 'content:read'
    assert allowed(p, r, 'read')


def test_invalid_resource():
    p = 'content:viewer'
    r = 'content:view@'
    assert not allowed(p, r, 'view')


def test_root_has_full_access():
    p = 'root'
    r = 'content:read, metadata:write'

    assert allowed(p, r, 'anything')
    assert allowed(p, r, 'write')

    r = 'content:all'
    assert allowed(p, r, 'all')

    r = 'any:read'
    assert allowed(p, r, 'read')

    r = 'anyone:read'
    assert allowed(p, r, 'write')


def test_void_principal():
    p = 'void'
    r = 'anyone:read'

    assert allowed(p, r, 'read')
    assert not allowed(p, r, 'write')

    r = 'content:read'
    assert not allowed(p, r, 'read')

    r = 'content:all'
    assert not allowed(p, r, 'read')


def test_principal_tags_and_supertags():
    p = 'admin'
    r = 'admin_user:write, admin_content:delete'

    assert allowed(p, r, 'write')
    assert allowed(p, r, 'delete')
    assert not allowed(p, r, 'read')


def test_any_resource():
    p = 'user'
    r = 'anyone:read'

    assert allowed(p, r, 'read')
    assert not allowed(p, r, 'delete')


def test_anyone_resource():
    p_root = 'root'
    p_void = 'void'
    p_user = 'user'

    r = 'anyone:read'

    assert allowed(p_root, r, 'read')
    assert allowed(p_void, r, 'read')
    assert allowed(p_user, r, 'read')
    assert allowed(p_root, r, 'write')
    assert not allowed(p_void, r, 'write')
    assert not allowed(p_user, r, 'write')


def test_special_format_any():
    p_root = 'root'
    p_void = 'void'
    p_user = 'user'

    r = ':read'

    assert not allowed(p_root, r, 'read')
    assert not allowed(p_void, r, 'read')
    assert not allowed(p_user, r, 'read')
    assert not allowed(p_root, r, 'write')
    assert not allowed(p_void, r, 'write')
    assert not allowed(p_user, r, 'write')


def test_special_format_all():
    p_root = 'root'
    p_void = 'void'
    p_user = 'user'
    p = 'another'

    r = 'user:'

    assert not allowed(p_root, r, 'read')
    assert not allowed(p_void, r, 'read')
    assert not allowed(p_user, r, 'read')
    assert not allowed(p, r, 'read')


def test_all_resource():
    p_root = 'root'
    p_void = 'void'
    p_user = 'user'
    p = 'another'

    r = 'user:all'

    assert allowed(p_root, r, 'read')
    assert not allowed(p_void, r, 'read')
    assert allowed(p_user, r, 'read')
    assert not allowed(p, r, 'read')


def test_special_format_any_and_all():
    p_root = 'root'
    p_void = 'void'
    p_user = 'user'

    r = ':'

    assert not allowed(p_root, r, 'read')
    assert not allowed(p_void, r, 'read')
    assert not allowed(p_user, r, 'read')
    assert not allowed(p_root, r, 'all')
    assert not allowed(p_void, r, 'all')
    assert not allowed(p_user, r, 'all')
