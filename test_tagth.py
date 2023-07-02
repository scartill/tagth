import pytest

from tagth import _normalize_principal, _normalize_resource, _resolve, allowed
from tagth import Authenticator, TagthNoAccess


def test_normalize_principal():
    p = _normalize_principal('me')
    assert list(p) == ['me']

    p = _normalize_principal(lambda: 'these')
    assert list(p) == ['these']

    p = _normalize_principal(['this', 'that', lambda: 'those'])
    assert list(p) == ['this', 'that', 'those']

    p = _normalize_principal('this,that, those')
    assert list(p) == ['this', 'that', 'those']


def test_normalize_resource():
    s = _normalize_resource('me')
    assert list(s) == [('me', 'all')]

    s = _normalize_resource(lambda: ['this', 'that:ro'])
    assert list(s) == [('this', 'all'), ('that', 'ro')]

    s = _normalize_resource(['here:admin', 'there', 'nowhere:user'])
    assert list(s) == [('here', 'admin'), ('there', 'all'), ('nowhere', 'user')]

    s = _normalize_resource('here:admin, there, nowhere:user')
    assert list(s) == [('here', 'admin'), ('there', 'all'), ('nowhere', 'user')]

    s = _normalize_resource('my,:,:ro')
    assert list(s) == [('my', 'all'), ('any', 'all'), ('any', 'ro')]


def test_resolve():
    r = _resolve('me', 'me')
    assert r == {'all'}

    r = _resolve('me', 'mememe')
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


def test_authenticator():
    auth = Authenticator('me', 'me:ro')
    a = auth.allowed('ro')
    assert a

    a = auth.allowed('all')
    assert not a


def test_authenticator_throw():
    auth = Authenticator('me', 'me:ro', throw=True)
    a = auth.allowed('ro')
    assert a

    with pytest.raises(TagthNoAccess):
        a = auth.allowed('all')
