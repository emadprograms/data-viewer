from infisical_sdk import InfisicalSDKClient
import os
import toml
import threading

class InfisicalManager:
    _instance = None
    _cache_lock = threading.Lock()

    def __new__(cls):
        with cls._cache_lock:
            if cls._instance is None:
                cls._instance = super(InfisicalManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        
        self.client = None
        self.is_connected = False
        self._secrets_cache = {}
        
        # Load from Env or Secrets file
        client_id = os.getenv("INFISICAL_CLIENT_ID")
        client_secret = os.getenv("INFISICAL_CLIENT_SECRET")
        self.project_id = os.getenv("INFISICAL_PROJECT_ID")
        service_token = os.getenv("INFISICAL_TOKEN")
        
        if not client_id and not service_token:
            try:
                # Attempt to load from .streamlit/secrets.toml if env vars are missing
                secrets_path = ".streamlit/secrets.toml"
                if os.path.exists(secrets_path):
                    data = toml.load(secrets_path)
                    sec = data.get("infisical", {})
                    client_id = sec.get("client_id")
                    client_secret = sec.get("client_secret")
                    self.project_id = sec.get("project_id")
                    service_token = sec.get("token")
            except Exception:
                pass

        if not client_id and not service_token:
            try:
                # Streamlit Cloud injects secrets into st.secrets
                import streamlit as st
                if "infisical" in st.secrets:
                    client_id = st.secrets["infisical"].get("client_id")
                    client_secret = st.secrets["infisical"].get("client_secret")
                    self.project_id = st.secrets["infisical"].get("project_id")
                    service_token = st.secrets["infisical"].get("token")
            except Exception:
                pass

        try:
            # Must provide host for InfisicalSDKClient
            self.client = InfisicalSDKClient(host="https://app.infisical.com")
            
            if client_id and client_secret:
                # Universal Auth (Preferred)
                self.client.auth.universal_auth.login(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.is_connected = True
            elif service_token:
                # Service Token (Legacy)
                self.client.auth.login(token=service_token)
                self.is_connected = True

            if self.is_connected:
                self._initialized = True
        except Exception as e:
            # print(f"❌ Infisical Connection Failed: {e}")
            pass

    def get_secret(self, secret_name, environment="dev", path="/"):
        if not self.is_connected: 
            return None
        
        cache_key = f"{environment}:{path}:{secret_name}"
        if cache_key in self._secrets_cache:
            return self._secrets_cache[cache_key]
            
        try:
            # Use environment_slug and secret_path as per documentation
            secret = self.client.secrets.get_secret_by_name(
                secret_name=secret_name,
                project_id=self.project_id,
                environment_slug=environment,
                secret_path=path
            )
            # Based on inspection, the attribute is 'secretValue'
            val = secret.secretValue
            self._secrets_cache[cache_key] = val
            return val
        except Exception:
            return None
