from flask import Flask, render_template, request, jsonify
import base64
from PIL import Image
import piexif
import io

app = Flask(__name__)

# Enable template auto-reload
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def upload_image():
    return render_template("image.html", filetype="Image")

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Read original image
        original_img = Image.open(image)
        original_bytes = io.BytesIO()
        original_img.save(original_bytes, format='JPEG')
        original_encoded_img = base64.b64encode(original_bytes.getvalue()).decode('utf-8')

        # Remove EXIF metadata
        exif_data = original_img.info.get('exif')
        if exif_data:
            cleaned_exif = piexif.remove(exif_data)
            original_img.save(image, exif=cleaned_exif)

        # Convert processed image to base64
        processed_bytes = io.BytesIO()
        original_img.save(processed_bytes, format='JPEG')
        processed_encoded_img = base64.b64encode(processed_bytes.getvalue()).decode('utf-8')

        # Get original and processed image metadata
        original_metadata = original_img.info.get('exif', {})
        processed_metadata = original_img.info.get('exif', {})

        return render_template('output_img.html', 
                               original_image=original_encoded_img, 
                               processed_image=processed_encoded_img, 
                               original_metadata=original_metadata, 
                               processed_metadata=processed_metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the application in debug mode on port 5001
    app.run(debug=True, port=5001)
