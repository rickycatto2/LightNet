import RPi.GPIO as GPIO
import time
import threading
import subprocess
import json
import paho.mqtt.publish as publish

CONFIG_FILE = "/home/lightmeup/config.json"
PIR_PIN = 17
BULBS = [
    "cmnd/light/Haze01/Backlog",
    "cmnd/light/Haze02/Backlog",
    "cmnd/light/Haze03/Backlog"
]
STAGGER_DELAY = 0.8  # seconds

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def trigger_bulbs(config):
    fade_time = int(config.get("fade_time", 6)) * 10  # Tasmota uses tenths of a second
    color_temp = config.get("color_temp", 153)
    commands = [
        f"Fade 1; Dimmer 20; Delay 5; Power 0; Delay 10; Dimmer 40; Power 1; Delay 5; Power 0; Delay 5; Power 1; Dimmer 60; CT {color_temp}; Delay 5; Dimmer 100; CT {color_temp}; FadeTime {fade_time}",
        "Delay 600",  # Hold full brightness for a minute
        "Fade 1; Dimmer 0; Power 0"
    ]
    for i, topic in enumerate(BULBS):
        def delayed_publish(topic=topic):
            for cmd in commands:
                publish.single(topic, cmd, hostname="localhost")
                time.sleep(0.1)
        threading.Timer(i * STAGGER_DELAY, delayed_publish).start()

def pir_callback(channel):
    global last_trigger_time
    current_time = time.time()
    if current_time - last_trigger_time >= cooldown:
        last_trigger_time = current_time
        config = load_config()
        trigger_bulbs(config)

if __name__ == "__main__":
    config = load_config()
    cooldown = int(config.get("fade_time", 6)) + int(config.get("off_delay", 60))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    last_trigger_time = 0

    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=pir_callback, bouncetime=300)

    subprocess.Popen(["python3", "/home/lightmeup/control_panel.py"])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
