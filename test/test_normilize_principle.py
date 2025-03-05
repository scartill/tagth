import pytest
import re

from tagth.tagth import _normalize_principal, TagthValidationError


def test_valid_tags():
    p = _normalize_principal("tag_1, tag_2")
    assert p == ["tag_1", "tag_2"]

    p = _normalize_principal("tag_1")
    assert p == ["tag_1"]

    p = _normalize_principal("tag_1,tag_2, tag_3")
    assert p == ["tag_1", "tag_2", "tag_3"]


def test_empty_tag():
    p = _normalize_principal("")
    assert p == ["void"]


def test_empty_string_tag():
    p = _normalize_principal(" ")
    assert p == ["void"]


def test_invalid_tag_int():
    with pytest.raises(TagthValidationError, match="Bad principal 4"):
        _normalize_principal(4)


def test_invalid_tag_list():
    with pytest.raises(
        TagthValidationError, match=re.escape("Bad principal ['tag_1', 'tag_2']")
    ):
        _normalize_principal(["tag_1", "tag_2"])


def test_not_isidentifier_tag():
    with pytest.raises(
        TagthValidationError, match="Special characters in principal tag: 1tag"
    ):
        _normalize_principal("1tag")

    with pytest.raises(
        TagthValidationError, match="Special characters in principal tag: 20"
    ):
        _normalize_principal("20")

    with pytest.raises(
        TagthValidationError, match="Special characters in principal tag: tag-1"
    ):
        _normalize_principal("tag-1")

    with pytest.raises(
        TagthValidationError, match="Special characters in principal tag: 1tag"
    ):
        _normalize_principal("1tag, tag_2")

    with pytest.raises(
        TagthValidationError, match="Special characters in principal tag: tag@"
    ):
        _normalize_principal("tag@")


def test_with_whitespaces():
    p = _normalize_principal("tag_1, tag_2, ")
    assert p == ["tag_1", "tag_2", "void"]

    p = _normalize_principal(" ,tag_1")
    assert p == ["void", "tag_1"]

    p = _normalize_principal(" , ")
    assert p == ["void", "void"]


def test_with_multiple_commas():
    p = _normalize_principal("tag_1,,,tag_2")
    assert p == ["tag_1", "void", "void", "tag_2"]
