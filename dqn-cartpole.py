from src.gyms.cartpole import CartPole
from src.agents import Agent
from src.utils import uniform

env = CartPole()
observe = env.appearance()

# Q function is appproximated by depth-2 MLP
action_space = [[-1.0], [1.0]]
inp_dim = len(observe) + len(action_space[0])
MLP_dims = (inp_dim, 4, 1)
cart = Agent(MLP_dims, action_space)

total = int(1e5)
save_every = int(1500)
eps_max = .4; eps_min = .1

print('Press [ESC] to stop')
for count in range(total):
    epsilon = max(eps_max - count * 1.0 / total, eps_min)
    #epsilon = .1
    action, q_val = cart.act(observe, epsilon)
    if action is None: # exploration
        action = action_space[round(uniform())]
    
    reward = env.react(action)
    new_observe = env.appearance()
    transition = [observe + action, reward, new_observe]
    cart.store_and_learn(transition)
    observe = new_observe
    
    if (count + 1) % 8 == 0:
        cart.update()
        if q_val: print('Q = ', q_val)
    
    if (count + 1) % save_every == 0:
        cart.save('cart_{}'.format(count + 1))

    # Visualize and wait for [ESC]
    if env.viz(1) == 27: break