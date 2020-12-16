from flask import Flask, send_file, send_from_directory, safe_join, abort, request
from werkzeug.utils import secure_filename
import sys
import time
import os
import json
import shlex
import subprocess
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), '..', 'build_report', 'scripts'))
from genomics import get_config

app = Flask(__name__)
app.config["CLIENT_PDF"] = "/home/ubuntu/projects/nanoporereport_ui/nanoporeReport/build_report/results/final_source"
app.config['UPLOAD_FOLDER'] = "/home/ubuntu/projects/nanoporereport_ui/nanoporeReport/build_report/input"

@app.route('/time')
def get_something ():
    return {"info": "Go Bucks!!!"}

@app.route("/time1")
def get_something_else ():
    return {"info": "Michigan Sucks!!!"}

@app.route("/get-pdf", methods=['GET', 'POST'])
def get_pdf():

    path, filename = '', ''
    if request.method == 'POST':
          for f in [request.files['file'], request.files['target_file']]:
            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)

    command = ['bash', get_config.main("flaskAPI", "sub_command")]
    os.chdir(os.path.dirname(get_config.main("flaskAPI", "sub_command")))

    with open(os.path.join(get_config.main("flaskAPI", "log_dir"), str(datetime.now())), 'w') as f:
        process = subprocess.run(command, stdout=f)
        print(process)



    sample_id, ext = os.path.splitext(filename)
    output_filename = '%s.pdf' % sample_id
    #output_filename = '%s.pdf' % 'sample_variants'
    output_path = os.path.join(app.config["CLIENT_PDF"], output_filename)

    try:

        return send_file(
            output_path,
            as_attachment=True,
            attachment_filename=output_filename)
            #attachment_filename=filename)

    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)