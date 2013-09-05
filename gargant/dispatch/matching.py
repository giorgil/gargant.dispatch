def method_matching(method, picker=lambda condition: condition):
    def _matching(condition):
        environ = picker(condition)
        environ_method = environ.get('REQUEST_METHOD', 'GET')
        return environ_method.lower() == method
    return _matching


PATH_MATCHING_LIST_NAME = 'gargant.dispatch.path_matching_list'


def path_matching(matching_list, picker=lambda condition: condition):
    def _matching(condition):
        environ = picker(condition)

        url_kwargs = {'matching_list': matching_list}
        path_list = environ.get(PATH_MATCHING_LIST_NAME)
        if not path_list:
            path_info = environ.get('PATH_INFO', '')
            path_list = path_info.split('/')
        print path_list
        if path_list < matching_list:
            return None

        for path, matching in zip(path_list, matching_list):
            if matching.startswith('{') and matching.endswith('}'):
                key = matching.strip('{}')
                url_kwargs[key] = path
            else:
                if path != matching:
                    return None

        environ[PATH_MATCHING_LIST_NAME] = path_list[len(matching_list):]

        return url_kwargs
    return _matching
