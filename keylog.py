from pynput import keyboard
import datetime
import time

class KeyLogger:
    def __init__(self):
        self.start_time = None
        self.last_key_time = None
        self.keys = []

    def on_press(self, key):
        current_time = time.time()

        if self.start_time is None:
            self.start_time = current_time

        if self.last_key_time is not None:
            elapsed_time = current_time - self.last_key_time
            self.keys.append((key, elapsed_time))

        self.last_key_time = current_time

    def save_to_file(self):
        if self.start_time is not None:
            end_time = time.time()
            total_duration = end_time - self.start_time

            filename = f"registered_keys_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            
            with open(filename, "w") as file:
                file.write(f"Total Duration: {total_duration:.2f} seconds\n")
                file.write("Key\t\tDuration\n")

                for key, duration in self.keys:
                    file.write(f"{self.format_key(key)}\t\t{duration:.2f} seconds\n")

            print(f"Data saved to {filename}")

    def format_key(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char
        else:
            return str(key)

if __name__ == "__main__":
    key_logger = KeyLogger()

    with keyboard.Listener(on_press=key_logger.on_press) as listener:
        print("Keylogger started. Press 'Esc' to stop.")
        listener.join()

    key_logger.save_to_file()
