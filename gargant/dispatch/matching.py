class NotMetched(Exception):
    pass


def method_matching(method):
    def _matching(environ):
        environ_method = environ.get('REQUEST_METHOD', 'GET')
        return environ_method.lower() == method
    return _matching


def brace_match(s):
    if s.startswith('{') and s.endswith('}'):
        return s.strip('{}')


def path_matching(matching_list):
    def _matching(environ):
        url_kwargs = {'matching_list': matching_list}
        path_info = environ.get('PATH_INFO', '')
        path_list = path_info.split('/')[1:]

        if len(path_list) != len(matching_list):
            return None

        for path, matching in map(None, path_list, matching_list):
            key = brace_match(matching)
            if key:
                url_kwargs[key] = path
                continue
            else:
                if path != matching:
                    return None
                else:
                    continue
        else:
            return url_kwargs
    return _matching
