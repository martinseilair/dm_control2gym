# dm_control2gym

dm_control2gym is a small wrapper to make [DeepMind Control Suite](https://github.com/deepmind/dm_control) environments available for [OpenAI Gym](https://github.com/openai/gym).

## Installation

```shell
$ git clone https://github.com/martinseilair/dm_control2gym/
$ cd dm_control2gym
$ pip install .
```

Tested with
- Python 3.5.2 and Ubuntu 16.04.
- Python 3.6.8 and Ubuntu 18.04

## Quick start
You can directly run the file as below.

```shell
python3.6 sample.py
```


```python
import gym
import dm_control2gym

# make the dm_control environment
env = dm_control2gym.make(domain_name="cartpole", task_name="balance")

# use same syntax as in gym
env.reset()
for t in range(10):
    observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
    env.render()

```

## Short documentation

### Spaces and Specs

The dm_control specs are converted to spaces. If there is only one entity in the observation dict, the original shape is used for the corresponding space. Otherwise, the observations are vectorized and concatenated.
Note, that the pixel observation is processed separately through the render routine.

The difference between the `Discrete` and the corresponding `ArraySpec` with type `np.int`, is that the domain `ArraySpec` is arbitrary and of that the domain of `Discrete` always starts at 0. Therefore, the domain is shifted  to obtain a valid `Discrete` space.

### Rendering
Three rendering modes are available by default:

* `human`: Render scene and show it
* `rgb_array`: Render scene and return it as rgb array
* `human_rgb_array`: Render scene, show and return it

You can create your own rendering modes before making the environment by:

```python
dm_control2gym.create_render_mode(name, show=True, return_pixel=False, height=240, width=320, camera_id=-1, overlays=(),
             depth=False, scene_option=None)
```

* `name`: name of rendering mode
* `show`: rendered image is shown
* `return_pixel`: return the rendered image

It is possible to render in different render modes subsequently. Output of several render modes can be visualized at the same time.




### Procedurally generated environments

* `swimmer`: `swimmer_n`
    - `k`: number of links
* `stacker`: `stack_k`
    - `k`: number of boxes (max. 4)
* `lqr`: `lqr_n_m`
    - `n`: number of masses
    - `m`: number of actuated masses
* `cartpole`: `k_poles`
    - `k`: number of poles
    - `swing_up`: balance or swing_up task (default=TRUE)
    - `sparse`: use sparse reward variant (default=FALSE)
    

__Example__

```python
env = dm_control2gym.make(domain_name="cartpole", task_name="k_poles",task_kwargs={'k':10})
```

## What's new

- 2018-01-25: Optimized registering process (thanks to [rejuvyesh](https://github.com/rejuvyesh)), added access to procedurally generated environments, added render mode functionality
- 2019-09-25: Being compatible with MuJoCo200/gym=1.14.0 or later/dm_control=0.0.0
- 2019-10-2: fixed the tiny bug in `convertObservation` method in `wrapper.py`



## Known Error
As of 25/9/2019, with the current dm_control package(ver=0.0.0), you might be getting the error below.

```shell
Traceback (most recent call last):
  File "/dm_control2gym/tests/sample.py", line 12, in <module>
    env.render()
  File "/dm_control2gym/dm_control2gym/wrapper.py", line 116, in render
    self._get_viewer(mode).update(self.pixels)
  File "/dm_control2gym/dm_control2gym/viewer.py", line 20, in update
    self.window.clear()
  File "/python3.6/site-packages/pyglet/window/__init__.py", line 1228, in clear
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
  File "/python3.6/site-packages/pyglet/gl/lib.py", line 105, in errcheck
    raise GLException(msg)
pyglet.gl.lib.GLException: b'invalid operation'
```

