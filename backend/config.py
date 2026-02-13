import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get(self, key, default=None):
        return self._config.get(key, default)

    def reload_config(self):
        print(f"Reloading configuration from {self.config_path}...")
        try:
            self._config = self._load_config()
            print("Configuration reloaded successfully.")
        except Exception as e:
            print(f"Error reloading config: {e}")
            # Potentially revert to old config or use fallbacks

class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, config_loader):
        self.config_loader = config_loader

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.config_loader.config_path:
            self.config_loader.reload_config()

if __name__ == "__main__":
    # Create a dummy config file
    with open('app_config.json', 'w') as f:
        json.dump({"feature_x_enabled": False, "threshold": 60}, f)

    config_loader = ConfigLoader('app_config.json')
    print(f"Initial config: {config_loader.get('feature_x_enabled')}, {config_loader.get('threshold')}")

    observer = Observer()
    event_handler = ConfigFileHandler(config_loader)
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
            # In a real app, you'd use config_loader.get() here
            # print(f"Current config (every 5s): {config_loader.get('feature_x_enabled')}, {config_loader.get('threshold')}")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # To test: modify app_config.json while the script is running
    # e.g., change "feature_x_enabled": true, "threshold": 80