from pyparsing import (
    Literal, Word, alphas,
    alphanums, OneOrMore, Suppress,
    ZeroOrMore, ParseException,
    StringEnd, Empty)


TAG_LIST_DELIMETER = ','
ACTION_DELIMETER = ':'
ANYONE_PRINCIPAL = 'anyone'
FULL_ACCESS_ACTION = 'all'
ROOT_PRINCIPAL = 'root'
VOID_PRINCIPAL = 'void'
VOID_RESOURCE = ''
ACTIONS_START_BRACE = '{'
ACTIONS_END_BRACE = '}'


class TagthException(Exception):
    pass


class TagthValidationError(TagthException):
    pass


def _normalize_principal(principal: str) -> list[str]:
    def norm_item(item: str) -> str:
        tag = item.strip()

        if not tag:
            tag = VOID_PRINCIPAL

        if not tag.isidentifier():
            raise TagthValidationError(f'Special characters in principal tag: {tag}')

        return tag

    if not isinstance(principal, str):
        raise TagthValidationError(f'Bad principal {principal}')

    principal_list = principal.split(TAG_LIST_DELIMETER)
    return list(map(norm_item, principal_list))


def _normalize_resource(resource: str) -> list[tuple[str, str]]:
    if not resource:
        return []
    if not isinstance(resource, str):
        raise TagthValidationError(f'Bad resource {resource}')

    separator = Literal(',')
    resource_tag = (Word(alphas + '_', alphanums + '_'))('resource_tag')
    action = (Word(alphas + '_', alphanums + '_'))('action')
    actions = OneOrMore((action + Suppress((',')) + action))('actions')

    single_action_module = (resource_tag + Suppress(':') + action).setParseAction(
        lambda t: (t.resource_tag, t.action)
    )

    multiple_actions_module = (
        resource_tag + Suppress(':') + Suppress('{') + actions + Suppress('}')
    ).setParseAction(
        lambda t: [(t.resource_tag, act) for act in t.actions]
    )

    empty_module = (Empty()).setParseAction(lambda _: [('void', 'all')])

    resource_module = single_action_module | multiple_actions_module | empty_module

    parser = ZeroOrMore(resource_module + Suppress(separator)) + resource_module + StringEnd()

    try:
        result = parser.parseString(resource)
        return result.asList()
    except ParseException as e:
        raise TagthValidationError(f"Invalid resource: {e}")


def _resolve_internal(principal: list[str], resource: list[tuple[str, str]]) -> set[str]:
    actions = set()

    for pr_tag in principal:
        if pr_tag == ROOT_PRINCIPAL:
            actions.add(FULL_ACCESS_ACTION)

    if not resource:
        return actions

    for (res_tag, action) in resource:
        if res_tag == ANYONE_PRINCIPAL:
            actions.add(action)

    for pr_tag in principal:
        if pr_tag == VOID_PRINCIPAL:
            continue

        for (res_tag, action) in resource:
            if res_tag.startswith(pr_tag):
                actions.add(action)

    return actions


def _resolve(principal: str, resource: str) -> set[str]:
    principal_list = _normalize_principal(principal)
    resource_list = _normalize_resource(resource)
    return _resolve_internal(principal_list, resource_list)


def allowed(principal: str, resource: str, action: str) -> bool:
    actions = _resolve(principal, resource)

    if FULL_ACCESS_ACTION in actions:
        return True

    for allowed_action in actions:
        if action.startswith(allowed_action):
            return True

    return False


def validate_principal(principal: str) -> bool:
    try:
        _normalize_principal(principal)
    except TagthValidationError:
        return False

    return True


def validate_resource(resource: str) -> bool:
    try:
        _normalize_resource(resource)
    except TagthValidationError:
        return False

    return True
