import pytest
from gmi.config import load_local_env


def test_env_load_is_literal_allowlisted_and_does_not_override_terminal(tmp_path):
    path = tmp_path/'.env'
    path.write_text('# private config\nGEMINI_API_KEY="fixture=secret"\n'
                    'GEMINI_MODEL=local-model\nGMI_BUDGET_NOTE=literal $(command) ${HOME}\n'
                    'PATH=/malicious\n')
    env = {'GEMINI_MODEL':'terminal-model'}
    assert load_local_env(path, env) is None
    assert env['GEMINI_API_KEY']=='fixture=secret'
    assert env['GEMINI_MODEL']=='terminal-model'
    assert env['GMI_BUDGET_NOTE']=='literal $(command) ${HOME}'
    assert 'PATH' not in env


def test_invalid_secret_line_does_not_leak_or_partially_load(tmp_path):
    path = tmp_path/'.env'
    path.write_text('GEMINI_API_KEY=fixture-secret\nGEMINI_MODEL="secret-broken\n')
    env = {}
    with pytest.raises(ValueError) as caught:
        load_local_env(path, env)
    assert 'secret' not in str(caught.value)
    assert env == {}


def test_missing_env_is_ok(tmp_path):
    env = {}
    load_local_env(tmp_path/'missing', env)
    assert env == {}
