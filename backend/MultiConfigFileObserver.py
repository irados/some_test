import json
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MultiConfigLoader:
    """
    Manages loading and reloading multiple configuration files.
    Each configuration is identified by a logical name.
    """
    def __init__(self, config_files_map):
        # config_files_map: {'config1_name': 'path/to/config1.json', 'config2_name': 'path/to/config2.json'}
        self.config_files_map = config_files_map
        # Store the loaded configurations: {'config1_name': {'key': 'value'}, ...}
        self.configs = {}
        self._load_all_configs()

    def _load_single_config(self, config_path):
        """
        Helper method to load a single JSON configuration file.
        Returns the loaded dictionary or None if an error occurs.
        """
        if not os.path.exists(config_path):
            print(f"Warning: Configuration file '{config_path}' not found. Skipping.")
            return {} # Return empty dict, so the key still exists but is empty
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from '{config_path}': {e}. Keeping previous config for this file.")
            return None # Indicate error, so previous config is retained if any
        except Exception as e:
            print(f"Error reading config file '{config_path}': {e}. Keeping previous config for this file.")
            return None

    def _load_all_configs(self):
        """Loads all configurations specified in the map during initialization."""
        print("Loading all initial configurations...")
        for name, path in self.config_files_map.items():
            loaded_config = self._load_single_config(path)
            if loaded_config is not None: # Only update if no error during load
                self.configs[name] = loaded_config
            else:
                # If initial load fails, ensure the config name is at least in the dict,
                # perhaps with an empty dict, to prevent KeyError later.
                if name not in self.configs:
                    self.configs[name] = {}
        print("Initial configurations loaded.")

    def reload_config_by_path(self, file_path):
        """
        Reloads a specific configuration file based on its file path.
        Identifies which logical configuration name the path belongs to.
        """
        # Resolve the absolute path of the modified file for robust comparison
        absolute_modified_path = os.path.abspath(file_path)

        for name, path in self.config_files_map.items():
            # Compare absolute paths
            if os.path.abspath(path) == absolute_modified_path:
                print(f"Reloading configuration '{name}' from {file_path}...")
                loaded_config = self._load_single_config(file_path)
                if loaded_config is not None:
                    self.configs[name] = loaded_config
                    print(f"Configuration '{name}' reloaded successfully.")
                else:
                    print(f"Failed to reload configuration '{name}'. Previous version retained.")
                return # Found and processed, so exit

        print(f"Warning: File '{file_path}' was modified but is not a recognized configuration file.")

    def get(self, config_name, key, default=None):
        """
        Retrieves a value from a specific configuration by its logical name.
        Example: config_loader.get('app_settings', 'api_key')
        """
        if config_name not in self.configs:
            print(f"Warning: Configuration '{config_name}' not loaded or defined.")
            return default
        return self.configs[config_name].get(key, default)

    def get_all(self, config_name):
        """
        Returns the entire configuration dictionary for a given logical name.
        """
        return self.configs.get(config_name, {})

class MultiConfigFileHandler(FileSystemEventHandler):
    """
    Event handler for watchdog, notifies the MultiConfigLoader when files change.
    """
    def __init__(self, config_loader):
        self.config_loader = config_loader
        # Store absolute paths of all watched config files for efficient lookup
        self.watched_absolute_paths = {os.path.abspath(path) for path in config_loader.config_files_map.values()}

    def on_modified(self, event):
        """Called when a file or directory is modified."""
        if not event.is_directory: # Only interested in file modifications, not directory ones
            absolute_event_path = os.path.abspath(event.src_path)
            if absolute_event_path in self.watched_absolute_paths:
                self.config_loader.reload_config_by_path(absolute_event_path)
            # else: print(f"Ignored modified file: {event.src_path}") # Optional: uncomment to see ignored files

if __name__ == "__main__":
    pita with cheese

    # Define your multiple configuration files here, mapping a logical name to its path
    config_definitions = {
        'app_settings': 'app_config.json',
        'feature_flags': 'feature_flags.json'
    }

    # --- Create dummy config files for demonstration ---
    with open('app_config.json', 'w') as f:
        json.dump({"api_key": "some_secret_123", "log_level": "INFO", "max_retries": 3}, f, indent=2)
    with open('feature_flags.json', 'w') as f:
        json.dump({"new_dashboard_enabled": False, "discount_enabled": True, "beta_testers_group": "group_a"}, f, indent=2)

    # Instantiate our multi-config loader
    config_loader = MultiConfigLoader(config_definitions)

    # --- Initial print of configurations ---
    print("\n--- Initial Configurations ---")
    print(f"App Settings API Key: {config_loader.get('app_settings', 'api_key')}")
    print(f"App Settings Log Level: {config_loader.get('app_settings', 'log_level')}")
    print(f"Feature Flags New Dashboard Enabled: {config_loader.get('feature_flags', 'new_dashboard_enabled')}")
    print(f"Feature Flags Discount Enabled: {config_loader.get('feature_flags', 'discount_enabled')}")
    print("------------------------------\n")

    # --- Set up watchdog observer ---
    observer = Observer()
    event_handler = MultiConfigFileHandler(config_loader)

    # Schedule the observer to watch the directory where the config files are located.
    # For simplicity, we assume they are in the current directory ('.').
    # If config files are in different directories, you'd schedule for each relevant directory.
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5) # Periodically print status to see effects of changes
            print(f"\n--- Current Status (every 5s) ---")
            print(f"App Settings Log Level: {config_loader.get('app_settings', 'log_level')}")
            print(f"Feature Flags New Dashboard Enabled: {config_loader.get('feature_flags', 'new_dashboard_enabled')}")

            # Example of how you'd use the config values dynamically:
            if config_loader.get('feature_flags', 'new_dashboard_enabled'):
                print(">>> New Dashboard Feature is CURRENTLY ACTIVE! <<<")
            else:
                print(">>> New Dashboard Feature is CURRENTLY INACTIVE. <<<")

            print("----------------------------------\n")

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # --- Cleanup dummy files (optional, but good for testing) ---
    print("Stopping application and cleaning up dummy config files.")
    os.remove('app_config.json')
    os.remove('feature_flags.json')