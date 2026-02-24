from src.infisical_manager import InfisicalManager


def test_infisical_manager_no_creds(clear_infisical_env):
    mgr = InfisicalManager()
    assert mgr.is_connected is False
    assert mgr.get_secret("any") is None
