import pytest

from tagth.tagth import _normalize_principal, TagthValidationError


def test_valid_tags():
    p = _normalize_principal('tag_1, tag_2')
    assert p == (['tag_1', 'tag_2'], [])

    p = _normalize_principal('tag_1')
    assert p == (['tag_1'], [])

    p = _normalize_principal('tag_1,tag_2, tag_3')
    assert p == (['tag_1', 'tag_2', 'tag_3'], [])


def test_empty_tag():
    p = _normalize_principal('')
    assert p == (['void'], [])


def test_whitespace_tag():
    p = _normalize_principal(' ')
    assert p == (['void'], [])


def test_invalid_tag_int():
    with pytest.raises(TagthValidationError, match='Bad principal: expected a string'):
        _normalize_principal(4)


def test_invalid_tag_list():
    with pytest.raises(TagthValidationError, match='Bad principal: expected a string'):
        _normalize_principal(['tag_1', 'tag_2'])


def test_not_isidentifier_tag():
    with pytest.raises(TagthValidationError):
        _normalize_principal('1tag')

    with pytest.raises(TagthValidationError):
        _normalize_principal('20')

    with pytest.raises(TagthValidationError):
        _normalize_principal('tag-1')

    with pytest.raises(TagthValidationError):
        _normalize_principal('1tag, tag_2')

    with pytest.raises(TagthValidationError):
        _normalize_principal('tag@')

    with pytest.raises(TagthValidationError):
        _normalize_principal('tag_1 tag_2')


def test_with_whitespaces():
    p = _normalize_principal('tag_1, tag_2, ')
    assert p == (['tag_1', 'tag_2', 'void'], [])

    p = _normalize_principal(' ,tag_1')
    assert p == (['void', 'tag_1'], [])

    p = _normalize_principal(' , ')
    assert p == (['void', 'void'], [])

    p = _normalize_principal(',')
    assert p == (['void', 'void'], [])


def test_with_multiple_commas():
    p = _normalize_principal('tag_1,,,tag_2')
    assert p == (['tag_1', 'void', 'void', 'tag_2'], [])


def test_global_actions_section():
    assert _normalize_principal('# read') == ([], ['read'])
    assert _normalize_principal('# read, export') == ([], ['read', 'export'])
    assert _normalize_principal('# all') == ([], ['all'])


def test_global_actions_with_tags():
    assert _normalize_principal('campaign_42 # read') == (['campaign_42'], ['read'])
    assert _normalize_principal('tag_1, tag_2 # read, write') == (
        ['tag_1', 'tag_2'],
        ['read', 'write'],
    )


def test_global_actions_whitespace_insensitive():
    assert _normalize_principal('campaign_42#read') == (['campaign_42'], ['read'])
    assert _normalize_principal('campaign_42 # read') == (['campaign_42'], ['read'])
    assert _normalize_principal('a#read,export') == (['a'], ['read', 'export'])


def test_global_actions_errors():
    # Two '#' sections.
    with pytest.raises(TagthValidationError):
        _normalize_principal('# read # write')

    # '#' with no actions.
    with pytest.raises(TagthValidationError):
        _normalize_principal('campaign_42 #')

    # Bare '#'.
    with pytest.raises(TagthValidationError):
        _normalize_principal('#')

    # Explicit void combined with a non-empty global section.
    with pytest.raises(TagthValidationError):
        _normalize_principal('void # read')
