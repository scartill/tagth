
ACTION_DELIMETER = ':'
ANYONE_PRINCIPAL = 'any'
FULL_ACCESS_ACTION = 'all'


class TagthException(Exception):
    pass


class TagthValidationError(TagthException):
    pass


class TagthNoAccess(TagthException):
    pass


def _normalize_principal(principal):
    def norm_item(item):
        item = item() if callable(item) else item

        if not isinstance(item, str):
            raise TagthValidationError(f'Bad principal tag {item}')

        return item

    principal = principal() if callable(principal) else principal
    principal = principal if isinstance(principal, list) else [principal]
    return map(norm_item, principal)


def _normalize_resource(resource):
    def norm_item(item):
        item = item() if callable(item) else item

        if not isinstance(item, str):
            raise TagthValidationError(f'Bad resource tag {item}')

        pair = item.split(ACTION_DELIMETER)

        if len(pair) > 2:
            raise TagthValidationError(f'Too many fields on a resource tag: {item}')

        tag = pair[0]

        if not tag:
            tag = ANYONE_PRINCIPAL

        if len(pair) == 2:
            action = pair[1]
        else:
            action = FULL_ACCESS_ACTION

        return (tag, action)

    resource = resource() if callable(resource) else resource
    resource = resource if isinstance(resource, list) else [resource]
    return map(norm_item, resource)


def _resolve_internal(principal, resource):
    actions = set()

    if not resource:
        return

    for (res_tag, action) in resource:
        if res_tag == ANYONE_PRINCIPAL:
            actions.add(action)

    if not principal:
        return

    for pr_tag in principal:
        if not pr_tag:
            continue

        for (res_tag, action) in resource:
            if res_tag.startswith(pr_tag):
                actions.add(action)

    return actions
