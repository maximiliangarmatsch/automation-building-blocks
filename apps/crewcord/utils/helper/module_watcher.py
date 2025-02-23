import os
import sys
import importlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            reload_modules()

def reload_modules():
    module_names = [
        "components.pyautogui.gmail",
        "finance_crew.execute_finance_crew",
        "invoice_crew.execute_invoice_crew",
    ]
    for module_name in module_names:
        if module_name in sys.modules:
            print(f"Reloading module: {module_name}")
            importlib.reload(sys.modules[module_name])

# Start the observer for watching file changes
def start_observer():
    event_handler = ReloadHandler()
    watch_path = os.path.abspath(".")
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()
    return observer