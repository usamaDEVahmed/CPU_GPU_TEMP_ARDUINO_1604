# CPU_GPU_TEMP_ARDUINO_1604
Python program that will get the CPU and the GPU temperature &amp; usage and then send it to Arduino via serial communication. The Arduino will display that information on 1604 LCD display screen.

# Currently tested on Windows 10. 
To be modified to Linux (Ubuntu).

`**Python version == 3.8.10**`

**Python Modules:**
`pythonnet==3.0.1`
`msl-loadlib==0.10.0`
`pyserial==3.5`

For Arduino two libs are used:
`LiquidCrystal_I2C.h==1.2.1`
`Wire.h`


# **HOW TO RUN:**
run command `**"python sender.py"**`
It will send CPU/GPU Temperature/Usage to the connected Arduino. The port to which Aruduino is connected will be scanned automatically by the scripts.

# **Script that can be used individually:**
`**"stat_fetcher.py"**` script gets all the details and returns it as a dictionary like the one given in the below examply. 
Just run `**"python stat_fetcher.py"**`

`{'CPU': {'TEMPERATURE': '44C', 'USAGE': '2.4%'}, 'GPU': {'TEMPERATURE': '29C', 'USAGE': '5.0%'}}`

# Arduino's Code
Arduino's Code to update data on the 1604 LCD display is inside the directory **arduino_display_on_1604** in the `file arduino_display_on_1604.ino`

# Result
**While doing normal tasks:**
https://github.com/usamaDEVahmed/CPU_GPU_TEMP_ARDUINO_1604/assets/41208249/32ffe66d-57ac-4674-a5c2-89759911286d

**While Gaming!!!**
https://github.com/usamaDEVahmed/CPU_GPU_TEMP_ARDUINO_1604/assets/41208249/adedeec3-4d3b-42f9-ba41-5b94ee4f840d

