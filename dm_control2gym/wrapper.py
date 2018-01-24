from gym import core, spaces
from dm_control import suite
from dm_control.rl import specs
from gym.utils import seeding
import gym
from dm_control2gym.viewer import DmControlViewer
import numpy as np
import sys


class DmcDiscrete(gym.spaces.Discrete):
    def __init__(self, _minimum, _maximum):
        super().__init__(_maximum - _minimum)
        self.offset = _minimum


def convertSpec2Space(spec, clip_inf=False):
    if spec.dtype == np.int:
        # Discrete
        return DmcDiscrete(spec.minimum, spec.maximum)
    else:
        # Box
        if type(spec) is specs.ArraySpec:
            return spaces.Box(-np.inf, np.inf, shape=spec.shape)
        elif type(spec) is specs.BoundedArraySpec:
            _min = spec.minimum
            _max = spec.maximum
            if clip_inf:
                _min = np.clip(spec.minimum, sys.float_info.min, sys.float_info.max)
                _max = np.clip(spec.maximum, sys.float_info.min, sys.float_info.max)

            if np.isscalar(_min) and np.isscalar(_max):
                # same min and max for every element
                return spaces.Box(_min, _max, shape=spec.shape)
            else:
                # different min and max for every element
                return spaces.Box(_min + np.zeros(spec.shape),
                                  _max + np.zeros(spec.shape))
        else:
            raise ValueError('Unknown spec!')

def convertOrderedDict2Space(odict):
    if len(odict.keys()) == 1:
        # no concatenation
        return convertSpec2Space(list(odict.values())[0])
    else:
        # concatentation
        numdim = sum([np.int(np.prod(odict[key].shape)) for key in odict])
        return spaces.Box(-np.inf, np.inf, shape=(numdim,))


def convertObservation(spec_obs):
    if len(spec_obs.keys()) == 1:
        # no concatenation
        return list(spec_obs.values())[0]
    else:
        # concatentation
        numdim = sum([np.int(np.prod(spec_obs[key].shape)) for key in spec_obs])
        space_obs = np.zeros((numdim,))
        i = 0
        for key in spec_obs:
            space_obs[i:i+np.prod(spec_obs[key].shape)] = spec_obs[key].flatten()
            i += np.prod(spec_obs[key].shape)
        return space_obs

def getClassName(domain_name, task_name):
    return domain_name + task_name

def getGymId(domain_name, task_name):
    return 'dmc' + domain_name + '-' + task_name + '-v0'

class DmControlWrapper(core.Env):

    def __init__(self, domain_name, task_name, task_kwargs=None, visualize_reward=False):

        self.dmcenv = suite.load(domain_name=domain_name, task_name=task_name, task_kwargs=task_kwargs, visualize_reward=visualize_reward)

        # convert spec to space
        self.action_space = convertSpec2Space(self.dmcenv.action_spec(), clip_inf=True)
        self.observation_space = convertOrderedDict2Space(self.dmcenv.observation_spec())
        self.viewer = None

        self.metadata = {
            'render.modes': ['human', 'rgb_array', 'human_rgb_array'],
        }

        # set seed
        self._seed()

    def getObservation(self):
        return convertObservation(self.timestep.observation)

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _reset(self):
        self.timestep = self.dmcenv.reset()
        return self.getObservation()



    def _step(self, a):

        if type(self.action_space) == DmcDiscrete:
            a += self.action_space.offset
        self.timestep = self.dmcenv.step(a)

        return self.getObservation(), self.timestep.reward, self.timestep.last(), {}



    def _render(self, mode='human', close=False):

        self.pixels = self.dmcenv.physics.render()

        if close:
            if self.viewer is not None:
                self._get_viewer().close()
                self.viewer = None
            return
        elif mode.find('human') >= 0:
            self._get_viewer().update(self.pixels)

        if mode.find('rgb_array') >= 0:
            return self.pixels

    def _get_viewer(self):
        if self.viewer is None:
            self.viewer = DmControlViewer(self.pixels.shape[1], self.pixels.shape[0])
        return self.viewer