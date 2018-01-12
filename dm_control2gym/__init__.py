from gym.envs.registration import register
from string import Template
import gym
import os
from dm_control2gym import wrapper

def make(domain_name, task_name):

    #create class file
    path = os.path.dirname(os.path.abspath(__file__))
    envpath = os.path.join(path,'envs')

    class_name = wrapper.getClassName(domain_name, task_name)
    gym_id = wrapper.getGymId(domain_name, task_name)
    class_file = os.path.join(envpath, class_name + '.py')


    if not os.path.exists(envpath):
        os.makedirs(envpath)
        with open(os.path.join(envpath,'__init__.py'), "w+") as f:
            pass

    with open(os.path.join(path,'template.py')) as f:
        src = Template(f.read())
        d = {'domainname': domain_name, 'taskname': task_name, 'classname': class_name}
        code = src.substitute(d)

    with open(class_file,"w") as f:
        f.write(code)

    # register enviroment
    register(
        id=gym_id,
        entry_point='dm_control2gym.envs.'+ class_name + ':' + class_name
    )

    # make the Open AI env
    return gym.make(gym_id)

