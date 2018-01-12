import os
from dm_control2gym import wrapper
class $classname(wrapper.DmControlWrapper):
    def __init__(self):
        super().__init__(domain_name="$domainname", task_name="$taskname")

    def __del__(self):
        file = os.path.abspath(__file__)
        path = os.path.dirname(file)
        cache_path = os.path.join(path,'__pycache__')
        cache_files = os.listdir(cache_path)
        for cache_file in cache_files:
            if cache_file.startswith('$classname'):
                os.remove(os.path.join(cache_path,cache_file))

        os.remove(file)


