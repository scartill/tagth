import pytest
import re

from tagth.tagth import _normalize_resource, TagthValidationError


def test_valid_resource():
    r = _normalize_resource('content:read, metadata:write')
    assert r == [('content', 'read'), ('metadata', 'write')]

    r = _normalize_resource('content:read')
    assert r == [('content', 'read')]

    r = _normalize_resource('me:all,anyone:all,content:read')
    assert r == [('me', 'all'), ('anyone', 'all'), ('content', 'read')]


def test_empty_resource():
    r = _normalize_resource(None)
    assert r == []

    r = _normalize_resource('')
    assert r == []

    r = _normalize_resource(' ')
    assert r == [('void', 'all')]


def test_invalid_type_resource():
    with pytest.raises(TagthValidationError, match='Bad resource 1'):
        _normalize_resource(1)

    with pytest.raises(
        TagthValidationError, match=re.escape('Bad resource [\'content:read\']')
    ):
        _normalize_resource(['content:read'])


def test_invalid_resource_with_no_comma():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content:read metadata:write (tag and action required)'
        )
    ):
        _normalize_resource('content:read metadata:write')


def test_resource_with_whitespace():
    r = _normalize_resource(' ,content:read')
    assert r == [('void', 'all'), ('content', 'read')]

    r = _normalize_resource('content:read, ')
    assert r == [('content', 'read'), ('void', 'all')]

    r = _normalize_resource(' ,resource_tag:{action_1, action_2}')
    assert r == [
        ('void', 'all'),
        ('resource_tag', 'action_1'),
        ('resource_tag', 'action_2')
    ]

    r = _normalize_resource('resource_tag:{action_1, action_2}, ')
    assert r == [
        ('resource_tag', 'action_1'),
        ('resource_tag', 'action_2'),
        ('void', 'all')
    ]


def test_resource_without_colon():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content (tag and action required)'
        )
    ):
        _normalize_resource('content, read')


def test_not_isidentifier_resource():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content read (tag and action required)'
        )
    ):
        _normalize_resource('content read')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content;read (tag and action required)'
        )
    ):
        _normalize_resource('content;read')

    with pytest.raises(
        TagthValidationError,
        match='Special characters in resource tag: content@'
    ):
        _normalize_resource('content@:read')

    with pytest.raises(
        TagthValidationError,
        match='Special characters in resource tag: 11content'
    ):
        _normalize_resource('11content:read')

    with pytest.raises(
        TagthValidationError,
        match='Special characters in resource tag: 11'
    ):
        _normalize_resource('11:read')

    with pytest.raises(
        TagthValidationError,
        match='Special characters in resource action: read@'
    ):
        _normalize_resource('content:read@')

    with pytest.raises(
        TagthValidationError,
        match='Special characters in resource action: 11read'
    ):
        _normalize_resource('content:11read')

    with pytest.raises(
        TagthValidationError,
        match='Special characters in resource action: 11'
    ):
        _normalize_resource('content:11')


def test_resource_with_invalid_actions():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content:read:write (tag and action required)'
        )
    ):
        _normalize_resource('content:read:write')


def test_resource_special_values():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: :read (tag required)'
        )
    ):
        _normalize_resource(':read')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content: (action required)'
        )
    ):
        _normalize_resource('content:')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: : (tag required)'
        )
    ):
        _normalize_resource(':')


def test_multiple_empty_resources():
    r = _normalize_resource(',')
    assert r == [
        ('void', 'all'),
        ('void', 'all'),
    ]

    r = _normalize_resource(', ,')
    assert r == [
        ('void', 'all'),
        ('void', 'all'),
        ('void', 'all'),
    ]


def test_multiple_actions_for_one_resource():
    r = _normalize_resource('resource_tag:{action_1, action_2}')
    assert r == [('resource_tag', 'action_1'), ('resource_tag', 'action_2')]

    r = _normalize_resource('resource_tag_1:{action_1, action_2}, resource_tag_2: action_3')
    assert r == [('resource_tag_1', 'action_1'), ('resource_tag_1', 'action_2'), ('resource_tag_2', 'action_3')]

    r = _normalize_resource(
        'resource_tag_2: action_3, resource_tag_1:{action_1, action_2}'
    )
    assert r == [
        ('resource_tag_2', 'action_3'),
        ('resource_tag_1', 'action_1'),
        ('resource_tag_1', 'action_2')
    ]

    r = _normalize_resource(
        'resource_tag_1:{action_1, action_2}, resource_tag_2: action_3, resource_tag_3:{action_4, action_5}'
    )
    assert r == [
        ('resource_tag_1', 'action_1'),
        ('resource_tag_1', 'action_2'),
        ('resource_tag_2', 'action_3'),
        ('resource_tag_3', 'action_4'),
        ('resource_tag_3', 'action_5')
    ]

    r = _normalize_resource('resource_tag_1:{action_1, action_2},,')
    assert r == [
        ('resource_tag_1', 'action_1'),
        ('resource_tag_1', 'action_2'),
        ('void', 'all'),
        ('void', 'all')
    ]

    r = _normalize_resource('resource_tag_1:{action_1, action_2}, ')
    assert r == [
        ('resource_tag_1', 'action_1'),
        ('resource_tag_1', 'action_2'),
        ('void', 'all'),
    ]

    r = _normalize_resource(' , resource_tag_2: action_3, resource_tag_1:{action_1, action_2}')
    assert r == [
        ('void', 'all'),
        ('resource_tag_2', 'action_3'),
        ('resource_tag_1', 'action_1'),
        ('resource_tag_1', 'action_2'),
    ]


def test_invalid_multiple_actions_and_empty_tag():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag:  (action required)'
        )
    ):
        _normalize_resource('resource_tag:{}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag_1:  (action required)'
        )
    ):
        _normalize_resource('resource_tag_1:{}, reosurse_tag_2: action_2')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag:  (action required)'
        )
    ):
        _normalize_resource('resource_tag: {}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: a{'
        )
    ):
        _normalize_resource('p:a{}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: p:  (action required)'
        )
    ):
        _normalize_resource('p:{,}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag:  (action required)'
        )
    ):
        _normalize_resource('resource_tag:{ ,action}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag:  (action required)'
        )
    ):
        _normalize_resource('resource_tag:{,,}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag:  (action required)'
        )
    ):
        _normalize_resource('resource_tag:{action, }')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag:  (action required)'
        )
    ):
        _normalize_resource('resource_tag:{ ,action}')


def test_nested_braces():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: {action_1'
        )
    ):
        _normalize_resource('resource_tag: {{action_1, action_2}}')


    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: content:{read, write:{delete}}'
        )
    ):
        _normalize_resource('content:{read, write:{delete}}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: a{1'
        )
    ):
        _normalize_resource('p:a{1,s}}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: a{{1'
        )
    ):
        _normalize_resource('p:a{{1,s}}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: e (tag and action required)'
        )
    ):
        _normalize_resource('p:{a1, {b, c}, d}, e')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: f}'
        )
    ):
        _normalize_resource('p_1:{a, b}, p_2:c, p_3:{d, {e, f}}')


def test_invalid_multiple_actions_structure():

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag: {action_1, resource_tag: action_2} (tag and action required)'
        )
    ):
        _normalize_resource('resource_tag: {action_1, resource_tag: action_2}')
    
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: {action1, action2} (tag and action required)'
        )
    ):
        _normalize_resource('{action1, action2}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: a{1'
        )
    ):
        _normalize_resource('p:a{1,s}2')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: }action1'
        )
    ):
        _normalize_resource('resource_tag: }action1, action2{')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag{action} (tag and action required)'
        )
    ):
        _normalize_resource('resource_tag{action}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: s3 (tag and action required)'
        )
    ):
        _normalize_resource('p:{a1, a2}, s3')


def test_single_brace():
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: {action_1'
        )
    ):
        _normalize_resource('resource_tag: {action_1')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: a{1'
        )
    ):
        _normalize_resource('p:a{1,s')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: s} (tag and action required)'
        )
    ):
        _normalize_resource('p:a,s}')
    
    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Special characters in resource action: action}'
        )
    ):
        _normalize_resource('resource_tag:action}')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: resource_tag{action (tag and action required)'
        )
    ):
        _normalize_resource('resource_tag{action')

    with pytest.raises(
        TagthValidationError,
        match=re.escape(
            'Invalid resource tag: s3} (tag and action required)'
        )
    ):
        _normalize_resource('p:{a1, a2}, s3}')



