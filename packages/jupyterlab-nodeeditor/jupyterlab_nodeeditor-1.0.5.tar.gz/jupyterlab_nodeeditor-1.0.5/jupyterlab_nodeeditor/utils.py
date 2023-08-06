import json
# import re
# import import_ipynb
# import sys
# import os


def get_instance_info(v):
    from .select import select, mselect
    t = type(v)
    d = None
    if isinstance(v, int) \
            or isinstance(v, float) \
            or isinstance(v, str) \
            or isinstance(v, bool):
        d = v
    if isinstance(v, select) \
            or isinstance(v, mselect):
        d = v.get_show_options()

    return json.dumps({"type": str(t), "value": d})


def get_urls(urls):
    if isinstance(urls, str):
        try:
            ret = json.loads(urls)
            if not isinstance(ret, list):
                raise TypeError('Expecting a list')
            return json.dumps(ret)
        except ValueError as e:
            return json.dumps([urls])
        except TypeError as e:
            raise TypeError('Invalid input type')
    elif isinstance(urls, list):
        return json.dumps(urls)
    elif isinstance(urls, dict):
        return json.dumps(list(urls.values()))
    else:
        raise TypeError('Invalid input type')


def get_boolean_value(v):
    if v:
        return True
    else:
        return False


def has_var(vars):
    vars = json.loads(vars)
    ret = {}
    for v in vars:
        ret[v] = v in globals()
    return json.dumps(ret)


# def importNodeTypesFromNotebook(path):
#     ret = {}
#     with open(path) as fp:
#         data = json.load(fp)
#     for cell in data['cells']:
#         code = ""
#         for line in cell['source']:
#             code += line + "\n"
#         code = code[:-1]
#         m: re.Match = re.search("#\[nodes_(.*?)\]\[\S*?\](.*)", code)
#         if m is not None:
#             nodesData = json.loads(m.group(2))
#             nodeTypes = nodesData.get("nodeTypes")
#             if nodeTypes is not None:
#                 ret.update(nodeTypes)
#     return ret


# loadCache = {}


# def importNotebook(path):
#     if not os.path.exists(path):
#         return
#     ret = loadCache.get(path)
#     if ret:
#         return ret
#     cache = import_ipynb.find_notebook
#     import_ipynb.find_notebook = lambda fullname, path: fullname
#     loader = import_ipynb.NotebookLoader()
#     try:
#         ret = loader.load_module(path)
#         loadCache[path] = ret
#     except ... as e:
#         raise e
#     finally:
#         import_ipynb.find_notebook = cache
#     return ret


# def loadNotebook(path):
#     importNotebook(path)
#     nodeTypes = importNodeTypesFromNotebook(path)


# if __name__ == "__main__":
#     path = "test_ext/testlib.ipynb"
#     loadNotebook(path)