import gym
import dm_control2gym

# make the dm_control environment
env = dm_control2gym.make(domain_name="cartpole", task_name="balance")

# use same syntax as in gym
env.reset()
for t in range(10):
    observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
    img = env.render(mode="rgb_array")
    print(img.shape)