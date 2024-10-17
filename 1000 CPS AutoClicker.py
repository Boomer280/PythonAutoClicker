import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

print('Welcome')

# Setup, you can modify it as you wish
delay = 0.0001
button = Button.left
start_key = KeyCode(char='z')
emsstop_key = KeyCode(char='s')
exit_key = KeyCode(char='x')

# This function calculates clicks per second 
def calculate_cps(delay):
    return 1 / delay

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                start_time = time.time()
                mouse.click(self.button)
                
                # This ensures that delay isn't too small so it can register key
                time_spent = time.time() - start_time
                if time_spent < self.delay:
                    time.sleep(self.delay - time_spent)

    def update_delay(self, new_delay):
        self.delay = new_delay

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

def print_cps():
    while click_thread.program_running:
        if click_thread.running:
            cps = calculate_cps(click_thread.delay)
            print(f"Current CPS: {cps:.2f}")
        time.sleep(1)

cps_thread = threading.Thread(target=print_cps)
cps_thread.start()

def runtime_counter(duration):
    time.sleep(duration)
    click_thread.stop_clicking()
    print("Auto Stop")

def on_press(key):
    global runtime_thread  # Declare this as global
    try:
        if key == start_key:
            click_thread.start_clicking()
            print("Starting")
            # DO NOT SET THE TIME HIGHER THAT 25 SECONDS, IT WILL LAG THE APPLICATION YOUR CLICKING IN
            runtime_thread = threading.Thread(target=runtime_counter, args=(15,))
            runtime_thread.start()
        elif key == emsstop_key:
            click_thread.stop_clicking()
            print("Emergency Stop")
        elif key == exit_key:
            click_thread.exit()
            print("Goodbye!")
            return False  # Stop the listener and exit the program
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure proper thread termination if program is no longer running
        if not click_thread.program_running:
            listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()
