# dm_control2gym

dm_control2gym is a small wrapper to make [DeepMind Control Suite](https://github.com/deepmind/dm_control) environments available for [OpenAI Gym](https://github.com/openai/gym).

## Installation

```shell
$ git clone https://github.com/martinseilair/dm_control2gym/
$ cd dm_control2gym
$ pip install .
```

Tested with Python 3.5.2 and Ubuntu 16.04.

## Quick start

```python
import gym
import dm_control2gym

# make the dm_control environment
env = dm_control2gym.make(domain_name="cartpole", task_name="balance")

# use same syntax as in gym
env.reset()
for t in range(1000):
    observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
    env.render()

```

## Short documentation

### Spaces and Specs

The dm_control specs are converted to spaces. If there is only one entity in the observation dict, the original shape is used for the corresponding space. Otherwise, the observations are vectorized and concatenated.
Note, that the pixel observation is processed separately through the render routine.

The difference between the `Discrete` and the corresponding `ArraySpec` with type `np.int`, is that the domain `ArraySpec` is arbitrary and of that the domain of `Discrete` always starts at 0. Therefore, the domain is shifted  to obtain a valid `Discrete` space.

### Rendering
Three rendering modes are available:

* `human`: Render scene and show it
* `rgb_array`: Render scene and return it as rgb array
* `human_rgb_array`: Render scene, show and return it

