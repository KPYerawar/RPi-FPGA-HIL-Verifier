# RPi-FPGA-HIL-Verifier
Automated Hardware-in-the-Loop (HIL) testbench using Raspberry Pi Zero 2 W and Python to perform exhaustive functional testing on FPGA-based VLSI core logic.

# ⚡ RPi-FPGA-HIL-Verifier: Automated VLSI Core Testing (64-Test-Case HIL Regression)

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Project Highlights

This project demonstrates a robust, low-cost **Hardware-in-the-Loop (HIL)** verification environment by connecting a **Raspberry Pi Zero 2 W** to a physical **FPGA** board. The primary goal was to automate the exhaustive functional testing of a critical VLSI core.

- **Technology:** FPGA (Verilog/VHDL), Raspberry Pi Zero 2 W, Python, SPI/GPIO Interface.
- **Method:** Automated Regression Testing / Hardware-in-the-Loop (HIL).
- **Result:** Successfully validated all 64 possible input states in **seconds**, proving design correctness on the actual silicon.

---

## 🧠 The Verification Challenge

My core logic design, which can be abstracted as a **4-bit functional block controlled by a 4-to-1 MUX**, created a verification matrix of 64 unique states:

| Input Component | Width | Calculation | Total Combinations |
| :--- | :--- | :--- | :---: |
| **4-bit Data Input** | 4-bit | $2^4$ | 16 |
| **2-bit Select Control** | 2-bit | $2^2$ | 4 |
| **Total Test Space** | 6-bit | $16 \times 4$ | **64 unique states** |

Manually toggling switches and checking LEDs for all 64 test cases is unscalable and highly error-prone. This bottleneck requires a programmatic solution.

## 💡 The RPi HIL Solution: Why Hardware Testing is Crucial

While a traditional **Verilog/VHDL Testbench** (e.g., in Vivado) is necessary for initial **Behavioral Simulation** of the RTL code's *logic*, it is fundamentally **idealized**.

| Testing Method | Verilog Testbench (Simulation) | RPi HIL Testbench (Hardware) |
| :--- | :--- | :--- |
| **Purpose** | **Logic** verification (Pre-synthesis) | **Physical** verification (Post-implementation) |
| **Timing** | Ideal/Zero gate delays | **Real-world timing,** clock skew, and path delays |
| **I/O** | Abstract internal signals | **Actual electrical signals** (noise, impedance, voltage levels) |
| **Conclusion** | Confirms *what* the code says. | Confirms *how* the code behaves on **real silicon** (the final instance of testing). |

By moving to **HIL**, we bridge the gap between simulation and deployment.

### Implementation Details

#### **1. Interface (The Hardware Connection)**

The RPi Zero 2 W serves as the host computer.

* **Interface Used:** Standard **SPI** (Serial Peripheral Interface) or bit-banged **GPIO** was implemented for communication due to the RPi 02w's accessible 40-pin header.
* **Safety:** A **Level Shifter** was used to ensure compatible voltage signaling (RPi is 3.3V) between the boards.

#### **2. Software (The Python Script)**

The Python script (`src_rpi/automated_testbench.py`) manages the entire test flow:

```python
# Pseudo-code demonstrating the test loop
for data_input in range(16):
    for select_line in range(4):
        # 1. Generate & Send Input
        test_vector = build_vector(data_input, select_line)
        rpi_send_data(test_vector) 
        
        # 2. Read Output
        actual_output = rpi_read_data()
        expected_output = lookup_golden_model(test_vector)
        
        # 3. Log Result
        if actual_output == expected_output:
            log_result("PASS")
        else:
            log_result(f"FAIL: Expected {expected_output}, Got {actual_output}")
