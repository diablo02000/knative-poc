import glob
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename, send_from_directory
from PIL import Image
import cv2


app = Flask(__name__)
# Max file size is 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
# Define the upload folder
app.config['UPLOAD_FOLDER'] = '/tmp'

# Define extensions allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health')
def health():
    return jsonify({'status' : 'ok'}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message' : 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message' : 'No file selected for uploading'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message' : 'File successfully uploaded'}), 201
    else:
        return jsonify({'message' : f'Allowed file types are {ALLOWED_EXTENSIONS}' }), 400


@app.route('/list', methods=['GET'])
def list():
    # List the files in the upload folder
    images = [os.path.basename(f) for f in glob.glob(f"{app.config['UPLOAD_FOLDER']}/*") if allowed_file(f)]
    return jsonify({'images' : images}), 200

@app.route('/size', methods=['GET'])
def size():
    # List the files in the upload folder
    image_name = request.args.get('filename')
    if not image_name:
        return jsonify({'message' : 'filename is required'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if os.path.exists(filename):
        img = cv2.imread(filename)
        return jsonify({'size' : {'width' : img.shape[1], 'height' : img.shape[0]}}), 200
    else:
        return jsonify({'message' : 'File not found'}), 404

@app.route('/delete', methods=['DELETE'])
def delete():
    # List the files in the upload folder
    image_name = request.args.get('filename')
    if not image_name:
        return jsonify({'message' : 'filename is required'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if os.path.exists(filename):
        os.remove(filename)
        return jsonify({'message' : 'File deleted successfully'}), 200
    else:
        return jsonify({'message' : 'File not found'}), 404

@app.route('/delete-all', methods=['DELETE'])
def delete_all():
    # List the files in the upload folder
    files = [f for f in glob.glob(f"{app.config['UPLOAD_FOLDER']}/*") if allowed_file(f)]
    for f in files:
        os.remove(f)
    return jsonify({'message' : 'All files deleted successfully'}), 200

@app.route('/convert', methods=['GET'])
def convert():
    # List the files in the upload folder
    image_name = request.args.get('filename')
    if not image_name:
        return jsonify({'message' : 'filename is required'}), 400
    
    format= request.args.get('format')
    if format not in ALLOWED_EXTENSIONS:
        return jsonify({'message' : f'Convertion types are {ALLOWED_EXTENSIONS}' }), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if os.path.exists(filename):
        img = Image.open(filename)
        rgb_img = img.convert('RGB')
        rgb_img.save(f"{filename.rsplit('.', 1)[0]}.{format}")
        return jsonify({'message' : 'File converted successfully'}), 200
    else:
        return jsonify({'message' : 'File not found'}), 404

@app.route('/download', methods=['GET'])
def download():
    # List the files in the upload folder
    image_name = request.args.get('filename')
    if not image_name:
        return jsonify({'message' : 'filename is required'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if os.path.exists(filename):
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=image_name)
    else:
        return jsonify({'message' : 'File not found'}), 404

if __name__ == '__main__':
    app.run()
