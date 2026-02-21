from tagth.tagth import allowed, _resolve

def test_strict_prefix_matching_principal_resource():
    # Verify that 'me' does NOT match 'meme'
    p = 'me'
    r = 'meme:read'
    assert _resolve(p, r) == set()
    assert not allowed(p, r, 'read')

    # Verify that 'me' DOES match 'me'
    p = 'me'
    r = 'me:read'
    assert _resolve(p, r) == {'read'}
    assert allowed(p, r, 'read')

    # Verify that 'me' DOES match 'me_stuff'
    p = 'me'
    r = 'me_stuff:read'
    assert _resolve(p, r) == {'read'}
    assert allowed(p, r, 'read')

    # Verify that 'admin' DOES match 'admin_user'
    p = 'admin'
    r = 'admin_user:read'
    assert _resolve(p, r) == {'read'}
    assert allowed(p, r, 'read')

    # Verify that 'admin' does NOT match 'administrator'
    p = 'admin'
    r = 'administrator:read'
    assert _resolve(p, r) == set()
    assert not allowed(p, r, 'read')


def test_strict_prefix_matching_action():
    # Verify that 'up' does NOT match 'update'
    p = 'user'
    r = 'user:up'
    # allowed(p, r, 'update')
    # principal 'user' has access to action 'up'.
    # Does 'up' grant 'update'? No.
    assert not allowed(p, r, 'update')

    # Verify that 'update' DOES match 'update_password' (standard hierarchy with underscore)
    r = 'user:update'
    assert allowed(p, r, 'update_password')

    # Verify that 'read' does NOT match 'reader'
    r = 'user:read'
    assert not allowed(p, r, 'reader')

    # Verify that 'create' DOES match 'create_asset' (superaction with underscore)
    r = 'user:create'
    assert allowed(p, r, 'create_asset')

    # Verify that 'create' DOES match 'create'
    assert allowed(p, r, 'create')
