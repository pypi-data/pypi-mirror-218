import random

import numpy as np
from pettingzoo.butterfly import knights_archers_zombies_v10
from pettingzoo.classic import rps_v2
from pettingzoo.mpe import simple_world_comm_v3

from supersuit import vectorize_aec_env_v0


def test_all():
    NUM_ENVS = 5

    def test_vec_env(vec_env):
        vec_env.reset()
        (
            obs,
            rew,
            agent_term,
            agent_trunc,
            env_term,
            env_trunc,
            agent_passes,
            infos,
        ) = vec_env.last()
        print(np.asarray(obs).shape)
        assert len(obs) == NUM_ENVS
        act_space = vec_env.action_space(vec_env.agent_selection)
        assert np.all(np.equal(obs, vec_env.observe(vec_env.agent_selection)))
        assert len(vec_env.observe(vec_env.agent_selection)) == NUM_ENVS
        vec_env.step([act_space.sample() for _ in range(NUM_ENVS)])
        (
            obs,
            rew,
            agent_term,
            agent_trunc,
            env_term,
            env_trunc,
            agent_passes,
            infos,
        ) = vec_env.last(observe=False)
        assert obs is None

    def test_infos(vec_env):
        vec_env.reset()
        infos = vec_env.infos[vec_env.agent_selection]
        assert infos[1]["legal_moves"]

    def test_seed(vec_env):
        vec_env.reset(seed=4)

    def test_some_done(vec_env):
        vec_env.reset()
        act_space = vec_env.action_space(vec_env.agent_selection)
        assert not any(done for dones in vec_env.dones.values() for done in dones)
        vec_env.step([act_space.sample() for _ in range(NUM_ENVS)])
        assert any(rew != 0 for rews in vec_env.rewards.values() for rew in rews)
        any_done_first = any(done for dones in vec_env.dones.values() for done in dones)
        vec_env.step([act_space.sample() for _ in range(NUM_ENVS)])
        any_done_second = any(
            done for dones in vec_env.dones.values() for done in dones
        )
        assert any_done_first and any_done_second

    def select_action(vec_env, passes, i):
        my_info = vec_env.infos[vec_env.agent_selection][i]
        if False and not passes[i] and "legal_moves" in my_info:
            return random.choice(my_info["legal_moves"])
        else:
            act_space = vec_env.action_space(vec_env.agent_selection)
            return act_space.sample()

    for num_cpus in [0, 1]:
        test_vec_env(vectorize_aec_env_v0(rps_v2.env(), NUM_ENVS, num_cpus=num_cpus))
        test_vec_env(
            vectorize_aec_env_v0(
                knights_archers_zombies_v10.env(), NUM_ENVS, num_cpus=num_cpus
            )
        )
        test_vec_env(
            vectorize_aec_env_v0(
                simple_world_comm_v3.env(), NUM_ENVS, num_cpus=num_cpus
            )
        )
