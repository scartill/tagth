import pytest

from tagth.tagth import allowed, TagthValidationError


@pytest.mark.parametrize(
    'principal, resource, action, expected',
    [
        ('# read', 'content:read, meta:write', 'read', True),
        ('# read', 'content:read, meta:write', 'write', False),
        ('# read', 'content:read, meta:write', 'read_all', True),
        ('# read', '', 'read', True),
        ('# read', 'anyone:write', 'write', True),
        ('# read', 'content:read', 'all', False),
        ('# all', 'content:read', 'anything', True),
        ('# read, export', 'c:read', 'export_csv', True),
        ('campaign_42 # read', 'campaign_42:write', 'write', True),
        ('campaign_42 # read', 'campaign_42:write', 'read', True),
        ('campaign_42#read', 'other:write', 'read', True),
        ('root', 'content:read', 'write', True),
        ('void', 'content:read', 'read', False),
    ],
)
def test_conformance_vectors(principal, resource, action, expected):
    assert allowed(principal, resource, action) == expected


@pytest.mark.parametrize(
    'principal',
    [
        '# read # write',
        'campaign_42 #',
        '#',
        'void # read',
    ],
)
def test_conformance_validation_errors(principal):
    with pytest.raises(TagthValidationError):
        allowed(principal, 'content:read', 'read')
