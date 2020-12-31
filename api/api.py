from flask import Flask, send_file, send_from_directory, safe_join, abort, request, flash, url_for
from werkzeug.utils import secure_filename
import sys
import time
import os
import json
import shlex
import subprocess
import get_percentage
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
def run_snakemake(self, my_id):
    # Initialize state
    self.update_state(state='IN PROGRESS')

    # Run Snakemake
    command = ['bash', get_config.main("flaskAPI", "sub_command")]
    os.chdir(os.path.dirname(get_config.main("flaskAPI", "sub_command")))

    with open(os.path.join(get_config.main("flaskAPI", "log_dir"), my_id + '.txt'), 'w') as f:
        process = subprocess.run(command, stderr=f)



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




################################
#         FLASK ROUTES         #
################################



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
    report_name = report_name.replace(" ","_")
    my_id = report_name + '-' + str(datetime.now())
    task = run_snakemake.delay(my_id)
    return {
        'taskUrl': url_for('taskstatus', task_id=task.id),
        'reportName': report_name,
        'my_id': my_id
    }


@app.route('/status/<task_id>',  methods=['GET', 'POST'])
def taskstatus(task_id):
    percentage = get_percentage.main(request.json['my_id'] + '.txt')
    task = run_snakemake.AsyncResult(task_id)
    if task.state == 'IN PROGRESS':
        response = {
            'status': 'Pending...',
            'percentage': percentage
        }   
    elif task.state == 'SUCCESS':
        response = {
            'status': 'Complete!',
            'percentage': percentage
        }
        
    else:
        # something went wrong in the background job
        response = {
            'status': task.state,
            'percentage': percentage
        }
    return response

@app.route("/get-pdf", methods=['GET', 'POST'])
def get_pdf():
    output_filename = '%s.pdf' % request.json['reportName'].replace(" ","_")
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