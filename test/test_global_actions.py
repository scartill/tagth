import pytest

from tagth.tagth import allowed, validate_principal, TagthValidationError


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
        ('campaign_42', 'campaign_42:write', 'write', True),
        ('campaign_42#read', 'campaign_42:write', 'write', True),
        ('campaign_42#read', 'other:read', 'read', True),
        ('campaign_42#read', 'other:write', 'write', False),
        ('# stats_read', 'content:stats_write', 'stats_write', False),
        ('# read, export', 'content:delete', 'delete', False),
        ('# read', '', 'write', False),
        ('# all', '', 'anything', True),
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
        '# read,',
        '# ,read',
        '# read,,export',
        'campaign_42 read',
    ],
)
def test_conformance_validation_errors(principal):
    with pytest.raises(TagthValidationError):
        allowed(principal, 'content:read', 'read')


@pytest.mark.parametrize(
    'principal',
    [
        '# read',
        '# read, export',
        '# all',
        'campaign_42 # read',
        'campaign_42#read',
        'tag_1, tag_2 # read, write',
        '  campaign_42  #  read , export  ',
        'tag_1,tag_2#read',
    ],
)
def test_validate_principal_accepts_valid_global_actions(principal):
    assert validate_principal(principal) is True


@pytest.mark.parametrize(
    'principal',
    [
        '# read # write',
        'campaign_42 #',
        '#',
        'void # read',
        '##',
        '##read',
        '# #',
        '#read##write',
        'campaign_42##read',
        '# read,',
        '# ,read',
        '# read,,export',
        'campaign_42 read',
    ],
)
def test_validate_principal_rejects_invalid_global_actions(principal):
    assert validate_principal(principal) is False


def test_void_principal_is_valid():
    assert validate_principal('void')


def test_void_cannot_be_combined_with_global_actions():
    assert not validate_principal('void#read')


def test_void_does_not_grant_access():
    assert not allowed('void', 'content:read', 'read')

@pytest.mark.parametrize(
    'resource, action',
    [
        ('content:read', 'read'),
        ('content:write', 'write'),
        ('meta:delete', 'delete'),
        ('', 'anything'),
    ],
)
def test_global_all_is_equivalent_to_root(resource, action):
    assert allowed('#all', resource, action) == allowed('root', resource, action)

def test_global_action_applies_to_empty_resource():
    assert allowed('#read', '', 'read')


def test_global_action_does_not_grant_unlisted_action_on_empty_resource():
    assert not allowed('#read', '', 'write')


def test_global_all_applies_to_empty_resource():
    assert allowed('#all', '', 'anything')

@pytest.mark.parametrize(
    'principal, action, expected',
    [
        ('# stats_read', 'stats_read_daily', True),
        ('# stats_read', 'stats_write', False),
        ('# read, export', 'read', True),
        ('# read, export', 'export', True),
        ('# read, export', 'delete', False),
        ('# all', 'anything', True),
    ],
)
def test_global_actions_boundaries(principal, action, expected):
    assert allowed(principal, 'content:read', action) is expected


@pytest.mark.parametrize(
    'principal',
    [
        '##',
        '##read',
        '# #',
        '#read##write',
        'campaign_42##read',
        'campaign_42#read##write',
    ],
)
def test_allowed_raises_for_consecutive_global_delimiters(principal):
    with pytest.raises(TagthValidationError):
        allowed(principal, 'content:read', 'read')

def test_global_actions_allow_whitespace():
    assert allowed(
        '  campaign_42  #  read , export  ',
        'content:read',
        'export',
    )

@pytest.mark.parametrize(
    'resource, action',
    [
        ('campaign_42:write', 'read'),
        ('other:write', 'read'),
        ('content:delete', 'read'),
    ],
)
def test_global_action_applies_to_unrelated_resources(resource, action):
    assert allowed('campaign_42#read', resource, action)