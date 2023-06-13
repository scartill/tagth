from tagth import _normalize_principal, _normalize_resource


def test_normalize_principal():
    p = _normalize_principal('me')
    assert list(p) == ['me']

    p = _normalize_principal(lambda: 'these')
    assert list(p) == ['these']

    p = _normalize_principal(['this', 'that', lambda: 'those'])
    assert list(p) == ['this', 'that', 'those']


def test_normalize_resource():
    s = _normalize_resource('me')
    print(list(s))

    s = _normalize_resource(lambda: ['this', 'that:ro'])
    print(list(s))


test_normalize_resource()
