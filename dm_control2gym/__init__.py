from gym.envs.registration import register
import gym
from dm_control2gym import wrapper
import hashlib
import dm_control2gym
from dm_control import suite

def make(domain_name, task_name, task_kwargs=None, visualize_reward=False):
    # register environment
    prehash_id = domain_name + task_name + str(task_kwargs) + str(visualize_reward)
    h = hashlib.md5(prehash_id.encode())
    gym_id = h.hexdigest()+'-v0'

    # avoid re-registering
    if gym_id not in gym_id_list:
        register(
            id=gym_id,
            entry_point='dm_control2gym.wrapper:DmControlWrapper',
            kwargs={'domain_name': domain_name, 'task_name': task_name, 'task_kwargs': task_kwargs, 'visualize_reward':visualize_reward}
        )
    # add to gym id list
    gym_id_list.append(gym_id)

    # make the Open AI env
    return gym.make(gym_id)



# add procedurally generated environments

@suite.swimmer.SUITE.add('proc')
def swimmer_k(**kwargs):
    return suite.swimmer.swimmer(**kwargs)

@suite.stacker.SUITE.add('proc')
def stack_k(k=2, observable=True, time_limit=suite.stacker._TIME_LIMIT, random=None):
    n_boxes = max(1, min(k, 4))
    if n_boxes != k:
        print('Input out of bounds. k set to: ',n_boxes)
    physics = suite.stacker.Physics.from_xml_string(*suite.stacker.make_model(n_boxes=n_boxes))
    task = suite.stacker.Stack(n_boxes, observable, random=random)
    return suite.control.Environment(
      physics, task, control_timestep=suite.stacker._CONTROL_TIMESTEP, time_limit=time_limit)

@suite.lqr.SUITE.add('proc')
def lqr_n_m(n=2, m=1, time_limit=suite.lqr._DEFAULT_TIME_LIMIT, random=None):
    _m = min(n, max(m,1))
    if _m != m:
        print('Input error. m should be <=n. m set to: ', _m)
    return suite.lqr._make_lqr(n_bodies=n,
                   n_actuators=_m,
                   control_cost_coef=suite.lqr._CONTROL_COST_COEF,
                   time_limit=time_limit,
                   random=random)

@suite.cartpole.SUITE.add('proc')
def k_poles(k=2, swing_up=True, sparse=False, time_limit=suite.cartpole._DEFAULT_TIME_LIMIT, random=None):
    physics = suite.cartpole.Physics.from_xml_string(*suite.cartpole.get_model_and_assets(num_poles=k))
    task = suite.cartpole.Balance(swing_up=swing_up, sparse=sparse, random=random)
    return suite.control.Environment(physics, task, time_limit=time_limit)


gym_id_list = []