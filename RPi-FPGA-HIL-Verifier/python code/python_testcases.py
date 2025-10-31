import RPi.GPIO as GPIO
import time

# --- Pin Map ---
I_pins = [17, 27, 22, 23]  # I[3:0]  (to FPGA)
S_pins = [24, 25]          # S[1:0]  (to FPGA)
Y_pin = 18                 # Output from FPGA

GPIO.setmode(GPIO.BCM)

# Setup pins
for p in I_pins + S_pins:
    GPIO.setup(p, GPIO.OUT)
GPIO.setup(Y_pin, GPIO.IN)

print("\nTesting 4x1 MUX via FPGA...\n")
print(" I3 I2 I1 I0 | S1 S0 | Y ")
print("-----------------------------")

try:
    # Loop through all input combinations
    for i in range(16):
        # Convert i (0?15) to bits for I[3:0]
        I_vals = [(i >> b) & 1 for b in range(4)]
        for j, val in enumerate(I_vals):
            GPIO.output(I_pins[j], val)
        # Now loop through all 4 select values
        for s in range(4):
            GPIO.output(S_pins[0], s & 1)
            GPIO.output(S_pins[1], (s >> 1) & 1)
            time.sleep(0.05)
            y_val = GPIO.input(Y_pin)
            print(f"  {I_vals[3]}  {I_vals[2]}  {I_vals[1]}  {I_vals[0]}  |  {(s>>1)&1}  {s&1}  |  {y_val}")
        print("-----------------------------")
    print("\nTest Complete ?")

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
