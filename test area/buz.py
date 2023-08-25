
import machine
import utime

# Define the pin number for the piezo buzzer
BUZZER_PIN = 13

# Define the frequency of the sound to produce
SOUND_FREQ = 15000

# Define the duration of each sound pulse in milliseconds
SOUND_DURATION = 500

# Create a machine object for the piezo buzzer
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

# Define a function to produce a sound pulse
def sound_pulse():
    # Generate a square wave at the specified frequency for the specified duration
    buzzer.on()
    utime.sleep_ms(SOUND_DURATION)
    buzzer.off()

