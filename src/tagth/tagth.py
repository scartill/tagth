import re


TAG_LIST_DELIMETER = ','
ACTION_DELIMETER = ':'
ANYONE_PRINCIPAL = 'anyone'
FULL_ACCESS_ACTION = 'all'
ROOT_PRINCIPAL = 'root'
VOID_PRINCIPAL = 'void'
VOID_RESOURCE = ''
ACTION_OPEN_BRACE = '{'
ACTION_CLOSE_BRACE = '}'


class TagthException(Exception):
    pass


class TagthValidationError(TagthException):
    pass


def resolve_multiple_actions(item):
    item_list = item.split(ACTION_DELIMETER)

    if len(item_list) != 2:
        raise TagthValidationError(f'Invalid resource tag: {item} (tag and action required)')

    resourse_tag = item_list[0]

    action_list = item_list[1].split(TAG_LIST_DELIMETER)
    result = []

    for action in action_list:
        action.strip()
        action = action.replace(ACTION_OPEN_BRACE, '', 1).replace(ACTION_CLOSE_BRACE, '', 1)
        result.append(f'{resourse_tag}: {action}')

    return result


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

    principal = principal.split(TAG_LIST_DELIMETER)
    return list(map(norm_item, principal))


def _normalize_resource(resource: str) -> list[tuple[str, str]]:
    def norm_item(item):
        item = item.strip()

        if not item:
            return (VOID_PRINCIPAL, FULL_ACCESS_ACTION)

        pair = item.split(ACTION_DELIMETER)

        if len(pair) != 2:
            raise TagthValidationError(f'Invalid resource tag: {item} (tag and action required)')

        tag = pair[0]
        tag = tag.strip()

        if not tag:
            raise TagthValidationError(f'Invalid resource tag: {item} (tag required)')

        action = pair[1]
        action = action.strip()

        if not action:
            raise TagthValidationError(f'Invalid resource tag: {item} (action required)')

        if not tag.isidentifier():
            raise TagthValidationError(f'Special characters in resource tag: {tag}')

        if not action.isidentifier():
            raise TagthValidationError(f'Special characters in resource action: {action}')

        return (tag, action)

    if not resource:
        return []

    if not isinstance(resource, str):
        raise TagthValidationError(f'Bad resource {resource}')

    resource_list = re.split(r',\s*(?![^{}]*\})', resource)
    result = []

    for resource in resource_list:
        if ACTION_OPEN_BRACE in resource and ACTION_CLOSE_BRACE in resource:
            result.extend(resolve_multiple_actions(resource))
        else:
            result.append(resource)

    return list(map(norm_item, result))


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
    principal = _normalize_principal(principal)
    resource = _normalize_resource(resource)
    return _resolve_internal(principal, resource)


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
