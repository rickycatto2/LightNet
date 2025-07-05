from flask import Flask, render_template_string, request, redirect
import json

app = Flask(__name__)
config_path = "/home/lightmeup/config.json"

default_config = {
    "fade_time": 6,
    "color_temp": 6500,
    "off_delay": 60
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_config = {
            "fade_time": float(request.form["fade_time"]),
            "color_temp": int(request.form["color_temp"]),
            "off_delay": int(request.form["off_delay"])
        }
        with open(config_path, "w") as f:
            json.dump(new_config, f)
        return redirect("/")

    try:
        with open(config_path) as f:
            current = json.load(f)
    except:
        current = default_config

    return render_template_string("""
    <h2>Lighting Control Panel</h2>
    <form method="POST">
      Fade Time (s): <input name="fade_time" value="{{cfg['fade_time']}}"><br>
      Color Temp (K): <input name="color_temp" value="{{cfg['color_temp']}}"><br>
      Off Delay (s): <input name="off_delay" value="{{cfg['off_delay']}}"><br>
      <input type="submit" value="Save">
    </form>
    """, cfg=current)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)