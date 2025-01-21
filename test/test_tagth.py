from tagth.tagth import _normalize_principal, _normalize_resource, _resolve, allowed


def test_normalize_principal():
    p = _normalize_principal('me')
    assert list(p) == ['me']

    p = _normalize_principal('this,that, those')
    assert list(p) == ['this', 'that', 'those']


def test_normalize_resource():
    s = _normalize_resource('me')
    assert list(s) == [('me', 'all')]

    s = _normalize_resource('here:admin, there, nowhere:user')
    assert list(s) == [('here', 'admin'), ('there', 'all'), ('nowhere', 'user')]

    s = _normalize_resource('my,:,:ro')
    assert list(s) == [('my', 'all'), ('any', 'all'), ('any', 'ro')]


def test_resolve():
    r = _resolve('me', 'me')
    assert r == {'all'}

    r = _resolve('me', 'meme_me')
    assert r == {'all'}

    r = _resolve('mememe', 'me')
    assert r == set()

    r = _resolve('me', 'mememe:ro, meme:rw')
    assert r == {'ro', 'rw'}

    r = _resolve('me', 'xmememe:ro, meme:rw')
    assert r == {'rw'}


def test_allowed():
    a = allowed('me', 'me', 'all')
    assert a

    a = allowed('me', 'me', 'ro')
    assert a

    a = allowed('me', ':ro', 'ro')
    assert a

    a = allowed('me', 'any:ro', 'ro')
    assert a

    a = allowed('me', 'they:ro, meme:rw', 'rw')
    assert a

    a = allowed('me', 'ther:ro, meme:rw', 'ro')
    assert not a


def test_root():
    a = allowed('a', 'a:ro', 'ro')
    assert a

    a = allowed('a', 'a:ro', 'rw')
    assert not a

    a = allowed('a,root', 'a:ro', 'rw')
    assert a


def test_emply_resource():
    a = allowed('root', '', 'all')
    assert a

    a = allowed('nonroot', '', 'all')
    assert not a


def test_emply_principal():
    a = allowed('', 'resource', 'action')
    assert not a

    a = allowed(',', 'resource', 'action')
    assert not a

    a = allowed(',res', 'resource', 'action')
    assert a

    a = allowed(',res', 'other,resource', 'action')
    assert a

    a = allowed('other,another', 'other,resource', 'action')
    assert a

    a = allowed('other,another', 'another:action', 'action')
    assert a

    a = allowed('other,another', 'another:inaction', 'action')
    assert not a


def test_void():
    a = allowed('resource', 'resource', 'action')
    assert a

    a = allowed('void', 'void', 'action')
    assert not a


def test_empty_anyoune():
    a = allowed('', 'any:action', 'action')
    assert a

    a = allowed('', 'any:action', 'inaction')
    assert not a

    a = allowed('', 'any:all', 'action')
    assert a

    a = allowed('', 'any', 'inaction')
    assert a

    a = allowed('', '', 'action')
    assert not a


def test_normalize_emply():
    n = _normalize_resource('')
    assert not n


def test_action_prefixes():
    assert allowed('user', 'user:a_class_action', 'a_class_action')
    assert allowed('user', 'user:a_class', 'a_class_one')
    assert allowed('user', 'user:a_class', 'a_class_two')
    assert not allowed('user', 'user:b_class', 'a_class_action')
    assert not allowed('user', 'user:a_class', 'b_class_action')
