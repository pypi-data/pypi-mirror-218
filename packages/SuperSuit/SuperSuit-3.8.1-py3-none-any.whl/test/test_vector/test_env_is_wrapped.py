import gymnasium
import pytest
from pettingzoo.mpe import simple_spread_v3

from supersuit import concat_vec_envs_v1, pettingzoo_env_to_vec_env_v1
from supersuit.generic_wrappers.frame_skip import frame_skip_gym


def test_env_is_wrapped_true():
    env = gymnasium.make("MountainCarContinuous-v0")
    env = frame_skip_gym(env, 4)
    num_envs = 3
    venv1 = concat_vec_envs_v1(env, num_envs)
    assert venv1.env_is_wrapped(frame_skip_gym) == [True] * 3


def test_env_is_wrapped_false():
    env = gymnasium.make("MountainCarContinuous-v0")
    num_envs = 3
    venv1 = concat_vec_envs_v1(env, num_envs)
    assert venv1.env_is_wrapped(frame_skip_gym) == [False] * 3


@pytest.mark.skip(
    reason="Wrapper depreciated, see https://github.com/Farama-Foundation/SuperSuit/issues/188"
)
def test_env_is_wrapped_cpu():
    env = gymnasium.make("MountainCarContinuous-v0")
    env = frame_skip_gym(env, 4)
    num_envs = 3
    venv1 = concat_vec_envs_v1(env, num_envs, num_cpus=2)
    assert venv1.env_is_wrapped(frame_skip_gym) == [True] * 3


def test_env_is_wrapped_pettingzoo():
    env = simple_spread_v3.parallel_env()
    venv1 = pettingzoo_env_to_vec_env_v1(env)
    num_envs = 3
    venv1 = concat_vec_envs_v1(venv1, num_envs)
    assert venv1.env_is_wrapped(frame_skip_gym) == [False] * 9
