import numpy as np
from pettingzoo.butterfly import knights_archers_zombies_v10

from supersuit import vectorize_aec_env_v0


def recursive_equal(info1, info2):
    if info1 == info2:
        return True
    return False


def test_identical():
    def env_fn():
        return knights_archers_zombies_v10.env()  # ,20)

    n_envs = 2
    # single threaded
    env1 = vectorize_aec_env_v0(knights_archers_zombies_v10.env(), n_envs)
    env2 = vectorize_aec_env_v0(knights_archers_zombies_v10.env(), n_envs, num_cpus=1)
    env1.reset(seed=42)
    env2.reset(seed=42)

    def policy(obs, agent):
        return [env1.action_space(agent).sample() for i in range(env1.num_envs)]

    envs_done = 0
    for agent in env1.agent_iter(200000):
        assert env1.agent_selection == env2.agent_selection
        agent = env1.agent_selection
        (
            obs1,
            rew1,
            agent_term1,
            agent_trunc1,
            env_term1,
            env_trunc1,
            agent_passes1,
            infos1,
        ) = env1.last()
        (
            obs2,
            rew2,
            agent_term2,
            agent_trunc2,
            env_term2,
            env_trunc2,
            agent_passes2,
            infos2,
        ) = env2.last()
        assert np.all(np.equal(obs1, obs2))
        assert np.all(np.equal(agent_term1, agent_term2))
        assert np.all(np.equal(agent_trunc1, agent_trunc2))
        assert np.all(np.equal(agent_passes1, agent_passes2))
        assert np.all(np.equal(env_term1, env_term2))
        assert np.all(np.equal(env_trunc1, env_trunc2))
        assert np.all(np.equal(obs1, obs2))
        assert all(
            np.all(np.equal(r1, r2))
            for r1, r2 in zip(env1.rewards.values(), env2.rewards.values())
        )
        assert recursive_equal(infos1, infos2)
        actions = policy(obs1, agent)
        env1.step(actions)
        env2.step(actions)
        # env.envs[0].render()
        for j in range(2):
            # if agent_passes[j]:
            #     print("pass")
            if rew1[j] != 0:
                print(j, agent, rew1, agent_term1[j], agent_trunc1[j])
            if env_term1[j] or env_trunc1[j]:
                print(j, "done")
                envs_done += 1
                if envs_done == n_envs + 1:
                    print("test passed")
                    return
