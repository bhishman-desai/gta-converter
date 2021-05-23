import os
import zipfile

from flask import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def basic():
    global path
    if "data.zip" in os.listdir():
        os.remove("data.zip")
    dire = 'downloads'
    for f in os.listdir(dire):
        os.remove(os.path.join(dire, f))
    if request.method == 'POST':

        if request.files:
            snap_upload = request.files.getlist('upload[]')
            for snap in snap_upload:
                path = os.path.join('downloads', snap.filename)
                with open(path + '.jpg', 'wb') as out_file:
                    out_file.write(snap.stream.read()[292:])

        zip_folder = zipfile.ZipFile('data.zip', 'w', compression=zipfile.ZIP_STORED)
        for root, dirs, files in os.walk(dire):
            if len(files) <= 1:
                return send_file(path + '.jpg', as_attachment=True)

            for file in files:
                zip_folder.write(dire + '/' + file)
            zip_folder.close()

        return send_file('data.zip',
                         mimetype='zip',
                         attachment_filename='data.zip',
                         as_attachment=True)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
