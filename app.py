from flask import Flask, render_template, request, jsonify
from PIL import Image
import io, base64, os
from datetime import datetime

app = Flask(__name__)

SAVE_DIR = os.path.join(os.getcwd(), "saved_photos")
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/')
def titlepage():
    return render_template('titlepage.html')

@app.route('/layout')
def layout_selection():
    return render_template('layout.html')

@app.route('/frame')
def frame_selection():
    return render_template('frame.html')

@app.route('/photobooth')
def photobooth_page():
    return render_template('photobooth.html')

@app.route('/save_photos', methods=['POST'])
def save_photos():
    data = request.json
    images = data.get("images", [])
    layout = int(data.get("layout", 1))
    frame_color = data.get("frameColor", "#FFFFFF")

    if not images:
        return jsonify({"error": "No images received"}), 400

    # Layout settings
    slot_size = (300, 200)
    padding = 10

    if layout == 1:
        final_width = slot_size[0] + padding * 2
        final_height = slot_size[1] + padding * 2
    elif layout == 2:
        final_width = slot_size[0] + padding * 2
        final_height = slot_size[1] * 2 + padding * 3
    elif layout == 4:
        final_width = slot_size[0] + padding * 2
        final_height = slot_size[1] * 4 + padding * 5
    else:
        return jsonify({"error": "Invalid layout"}), 400

    # Create the background frame
    final_img = Image.new("RGB", (final_width, final_height), frame_color)

    for idx, img_data in enumerate(images):
        img_data = img_data.split(",")[1]
        img_bytes = base64.b64decode(img_data)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize(slot_size)

        if layout == 1:
            x, y = padding, padding
        elif layout == 2:
            x = padding
            y = padding + idx * (slot_size[1] + padding)
        elif layout == 4:
            x = padding
            y = padding + idx * (slot_size[1] + padding)

        final_img.paste(img, (x, y))

    filename = f"photobooth_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(SAVE_DIR, filename)
    final_img.save(filepath)

    return jsonify({"filename": filename})

if __name__ == '__main__':
    app.run(debug=True)
