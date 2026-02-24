from src.infisical_manager import InfisicalManager
import os


def test_infisical_manager_no_creds(clear_infisical_env, monkeypatch):
    # Reset singleton for clean test
    InfisicalManager._instance = None
    
    # Ensure no secrets.toml is found
    monkeypatch.setattr(os.path, "exists", lambda x: False)
    
    mgr = InfisicalManager()
    assert mgr.is_connected is False
    assert mgr.get_secret("any") is None
