TAG_LIST_DELIMETER = ','
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

        return item.strip()

    principal = principal() if callable(principal) else principal
    principal = principal.split(TAG_LIST_DELIMETER) if isinstance(principal, str) else principal
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

        action = None

        if len(pair) == 2:
            action = pair[1]

        if not action:
            action = FULL_ACCESS_ACTION

        return (tag.strip(), action.strip())

    resource = resource() if callable(resource) else resource
    resource = resource.split(TAG_LIST_DELIMETER) if isinstance(resource, str) else resource
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


def _resolve(principal, resource):
    principal = list(_normalize_principal(principal))
    resource = list(_normalize_resource(resource))
    return _resolve_internal(principal, resource)


def allowed(principal, resource, action):
    actions = _resolve(principal, resource)
    return action in actions or FULL_ACCESS_ACTION in actions


class Authenticator():
    def __init__(self, principal, resource, throw=False):
        self._principal = principal
        self._resource = resource
        self._throw = throw

    def allowed(self, action):
        is_allowed = allowed(self._principal, self._resource, action)

        if self._throw and not is_allowed:
            raise TagthNoAccess()

        return is_allowed
