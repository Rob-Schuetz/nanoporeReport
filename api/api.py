from flask import Flask, send_file, send_from_directory, safe_join, abort, request, flash, url_for
from werkzeug.utils import secure_filename
import sys
import time
import os
import json
import shlex
import subprocess
from celery import Celery
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), '..', 'build_report', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), 'build_report', 'scripts'))
from genomics import get_config

app = Flask(__name__)
app.config["CLIENT_PDF"] = "/home/ubuntu/projects/nanoporereport_ui/nanoporeReport/build_report/results/final_source"
app.config['UPLOAD_FOLDER'] = "/home/ubuntu/projects/nanoporereport_ui/nanoporeReport/build_report/input"
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
app.config['result_backend'] = "redis://localhost:6379/0"

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


################################
#         CELERY TASKS         #
################################

@celery.task(bind=True)
def run_snakemake(self):
    print('HELLO')
    # Initialize state
    self.update_state(state='IN PROGRESS')

    # Run Snakemake
    command = ['bash', get_config.main("flaskAPI", "sub_command")]
    os.chdir(os.path.dirname(get_config.main("flaskAPI", "sub_command")))

    with open(os.path.join(get_config.main("flaskAPI", "log_dir"), str(datetime.now())), 'w') as f:
        process = subprocess.run(command, stdout=f)
        print(process)


@celery.task(bind=True)
def get_pdf(self, vcf_filename):
    sample_id, ext = os.path.splitext(filename)
    output_filename = '%s.pdf' % sample_id
    #output_filename = '%s.pdf' % 'sample_variants'
    output_path = os.path.join(app.config["CLIENT_PDF"], output_filename)

    try:

        self.update_state(state='Complete')
        return send_file(
            output_path,
            as_attachment=True,
            attachment_filename=output_filename)
            #attachment_filename=filename)

    except FileNotFoundError:
        abort(404)

@celery.task(bind=True)
def addition(self, num1, num2):
    time.sleep(5)
    return num1 + num2

@celery.task(bind=True)
def print_request(self, file):
    print(file)
    time.sleep(5)
    return {'msg': 'hello'}


################################
#         FLASK ROUTES         #
################################

@app.route('/get-info', methods=['GET', 'POST'])
def get_info ():
    if request.method == 'POST':
        print(request.__dict__)
    return {"info": "Yummy celery!"}


@app.route('/time')
def get_something ():
    return {"info": "Go Bucks!!!"}


@app.route('/longtask')
def get_somethings ():
    time.sleep(10)
    return {"info": "ayyyy"}


@app.route("/time1")
def get_something_else ():
    return {"info": "Michigan Sucks!!!"}


@app.route("/generate-report", methods=['GET', 'POST'])
def longpdf_task():
    files = {'files': []}
    for f in [request.files['test_bed'], request.files['test_vcf']]:
        filename = secure_filename(f.filename)
        files['files'].append([f.filename])
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
    #task = long_pdf_task.delay(request)
    report_name, ext = os.path.splitext(request.files['test_bed'].filename)
    task = run_snakemake.delay()
    return {
        'taskUrl': url_for('taskstatus', task_id=task.id),
        'reportName': report_name
    }


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = run_snakemake.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'status': 'Pending...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'status': 'Complete!'
        }
        
    else:
        # something went wrong in the background job
        response = {
            'status': task.state
        }
    return response

@app.route("/get-pdf", methods=['GET', 'POST'])
def get_pdf():
    output_filename = '%s.pdf' % request.json['reportName'].replace(" ","_")
    #output_filename = '%s.pdf' % 'sample_variants'
    output_path = os.path.join(app.config["CLIENT_PDF"], output_filename)

    try:
        print("I'll go ahead and send the file now")
        return send_file(
            output_path,
            as_attachment=True,
            attachment_filename=output_filename)
            #attachment_filename=filename)

    except FileNotFoundError:
        print('woah')
        abort(404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)