import pdf2image
import zipfile
import os

from io import BytesIO
from flask import Flask, request, redirect, url_for, abort, send_file

app = Flask(__name__, static_url_path='')

@app.route('/pdf2img')
def main():
    return """
<html>
    <head></head>
    <body>
        <form action="/pdf2img/convert" method="post" enctype="multipart/form-data">
            <div
                style="
                    display: flex;
                    flex-direction: column;
                    align-items: start;
                    row-gap: 10px;
                "
            >
                <input type="file" name="file" id="file" multiple>
                <div id="filenames">
                </div>
                <input type="submit" value="Convert PDF to images" name="submit" accept=".pdf">
            </div>
        </form>
        <script>
            document.querySelector('#file').addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    const filenames = e.target.files;
                    const filenamesDiv = document.querySelector('#filenames');
                    filenamesDiv.innerHTML = '';
                    for (let i = 0; i < filenames.length; i++) {
                        const filenameDiv = document.createElement('div');
                        filenameDiv.innerHTML = filenames[i].name;
                        filenamesDiv.appendChild(filenameDiv);
                    }
                }
            })
        </script>
    </body>
</html>
"""

@app.route('/pdf2img/convert', methods = ['GET', 'POST'])
def convert():
    if request.method == 'POST':
        if 'file' not in request.files:
            print(request.files)
            return redirect('/')

        files = request.files.getlist('file')
        # return abort(400) if any file's filename is empty
        if any(file.filename == '' for file in files):
            return abort(400)

        zip_file_bytes = BytesIO()
        zip_file = zipfile.ZipFile(zip_file_bytes, 'w')

        for file in files:
            pdf_basename = os.path.splitext(file.filename)[0]
            pdf_images_folder = os.path.join(app.root_path, pdf_basename)
            os.makedirs(pdf_images_folder, exist_ok=True)

            images = pdf2image.convert_from_bytes(file.read(), size=(1280, None), dpi=300)
            for i, im in enumerate(images, start=1):
                im_bytesio = BytesIO()
                im.save(im_bytesio, format='JPEG')
                image_filename = str(i) + '.jpg'
                image_filepath = os.path.join(pdf_images_folder, image_filename)
                im.save(image_filepath, format='JPEG')
                zip_file.write(image_filepath, arcname=os.path.join(pdf_basename, image_filename))

        zip_file.close()
        zip_file_bytes.seek(0)
        return send_file(zip_file_bytes, as_attachment=True, download_name='images.zip')
    else:
        return abort(404)

if __name__=='__main__':
    app.run(host="0.0.0.0")
