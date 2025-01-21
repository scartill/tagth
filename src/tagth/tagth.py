TAG_LIST_DELIMETER = ','
ACTION_DELIMETER = ':'
ANYONE_PRINCIPAL = 'any'
FULL_ACCESS_ACTION = 'all'
ROOT_PRINCIPAL = 'root'
VOID_PRINCIPAL = 'void'
VOID_RESOURCE = ''


class TagthException(Exception):
    pass


class TagthValidationError(TagthException):
    pass


def _normalize_principal(principal):
    def norm_item(item):
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


def _normalize_resource(resource):
    def norm_item(item):
        item = item.strip()

        if not item:
            return (VOID_PRINCIPAL, FULL_ACCESS_ACTION)

        pair = item.split(ACTION_DELIMETER)

        if len(pair) > 2:
            raise TagthValidationError(f'Too many fields on a resource tag: {item}')

        tag = pair[0]

        if not tag:
            tag = ANYONE_PRINCIPAL

        action = None

        if len(pair) == 2:
            action = pair[1]

        if not action:
            action = FULL_ACCESS_ACTION

        tag = tag.strip()
        action = action.strip()

        if not tag.isidentifier():
            raise TagthValidationError(f'Special characters in resource tag: {tag}')

        if not action.isidentifier():
            raise TagthValidationError(f'Special characters in resource action: {action}')

        return (tag, action)

    if not resource:
        return []

    if not isinstance(resource, str):
        raise TagthValidationError(f'Bad principal {resource}')

    resource = resource.split(TAG_LIST_DELIMETER)
    return list(map(norm_item, resource))


def _resolve_internal(principal, resource):
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


def _resolve(principal, resource):
    principal = _normalize_principal(principal)
    resource = _normalize_resource(resource)
    return _resolve_internal(principal, resource)


def allowed(principal, resource, action):
    actions = _resolve(principal, resource)

    if FULL_ACCESS_ACTION in actions:
        return True

    for allowed_action in actions:
        if action.startswith(allowed_action):
            return True

    return False


def validate_principal(principal):
    try:
        _normalize_principal(principal)
    except TagthValidationError:
        return False

    return True


def validate_resource(resource):
    try:
        _normalize_resource(resource)
    except TagthValidationError:
        return False

    return True
