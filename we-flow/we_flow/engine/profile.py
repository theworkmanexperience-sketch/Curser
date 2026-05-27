"""
W.E. FLOW — Config Profile System (Phase 1-C)

Profile resolution order (last wins):
  1. config.yaml                     — base defaults
  2. profiles/{name}.yaml            — project-level client profile
  3. ~/.weflow/profiles/{name}.yaml  — user-local override

Usage:
  python3 main.py --profile ryderz
  python3 main.py --profile google_drive
"""

import yaml
from pathlib import Path
from typing import Optional


# ── Profile directories ───────────────────────────────────────────────────────
SYSTEM_PROFILES_DIR = Path(__file__).parent.parent / 'profiles'
USER_PROFILES_DIR   = Path.home() / '.weflow' / 'profiles'


def deep_merge(base: dict, override: dict) -> dict:
    """
    Recursively merge override into base.
    Only keys present in override are changed.
    All other base keys are preserved unchanged.
    """
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class ProfileLoader:

    def __init__(self):
        self.system_dir = SYSTEM_PROFILES_DIR
        self.user_dir   = USER_PROFILES_DIR

    def load(self, profile_name: str, base_config: dict) -> dict:
        """
        Load and merge a named profile over base_config.
        Returns the merged config dict.
        Raises FileNotFoundError if profile not found in either location.
        """
        system_path = self.system_dir / f'{profile_name}.yaml'
        user_path   = self.user_dir / f'{profile_name}.yaml'

        system_profile = self._load_file(system_path)
        user_profile   = self._load_file(user_path)

        if system_profile is None and user_profile is None:
            searched = [str(system_path), str(user_path)]
            raise FileNotFoundError(
                f"Profile '{profile_name}' not found.\n"
                f"Searched:\n" +
                '\n'.join(f"  {p}" for p in searched) +
                f"\n\nAvailable profiles: {self._list_available()}"
            )

        merged = dict(base_config)
        if system_profile:
            merged = deep_merge(merged, self._strip_metadata(system_profile))
        if user_profile:
            merged = deep_merge(merged, self._strip_metadata(user_profile))

        # Preserve profile metadata in the merged config for logging
        active = user_profile or system_profile
        merged['_active_profile'] = {
            'name':        active.get('profile_name', profile_name),
            'version':     active.get('profile_version', 'unknown'),
            'client':      active.get('client', ''),
            'description': active.get('description', ''),
            'source':      str(user_path) if user_profile else str(system_path),
        }
        return merged

    def list_profiles(self) -> list[dict]:
        """Return all available profiles with their metadata."""
        profiles = {}
        for path in sorted(self.system_dir.glob('*.yaml')):
            data = self._load_file(path)
            if data and 'profile_name' in data:
                profiles[data['profile_name']] = {
                    'name': data['profile_name'],
                    'client': data.get('client', ''),
                    'description': data.get('description', ''),
                    'source': 'system',
                    'path': str(path),
                }
        for path in sorted(self.user_dir.glob('*.yaml')):
            data = self._load_file(path)
            if data and 'profile_name' in data:
                name = data['profile_name']
                profiles[name] = {
                    'name': name,
                    'client': data.get('client', ''),
                    'description': data.get('description', ''),
                    'source': 'user (overrides system)',
                    'path': str(path),
                }
        return list(profiles.values())

    @staticmethod
    def _load_file(path: Path) -> Optional[dict]:
        """Load a YAML profile file. Returns None if file does not exist."""
        if not path.exists():
            return None
        try:
            data = yaml.safe_load(path.read_text())
            return data if isinstance(data, dict) else None
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in profile {path}: {e}")

    @staticmethod
    def _strip_metadata(profile: dict) -> dict:
        """Remove profile metadata keys before merging into config."""
        META_KEYS = {'profile_name', 'profile_version', 'client',
                     'description', 'created', 'base_profile'}
        return {k: v for k, v in profile.items() if k not in META_KEYS}

    def _list_available(self) -> str:
        profiles = self.list_profiles()
        if not profiles:
            return 'none found'
        return ', '.join(p['name'] for p in profiles)
