import os
import time
os.system('')

print("\x1b[2J\x1b[H", end="")
print("="*20 + " JARVIS " + "="*20)
print("System loaded.")
print("\x1b[3;r", end="")
print("\x1b[3;1H", end="")

for i in range(50):
    print(f"Line {i}")
    time.sleep(0.05)
