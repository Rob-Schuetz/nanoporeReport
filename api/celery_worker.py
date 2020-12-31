from celery import Celery
from werkzeug.utils import secure_filename
import sys
import os
import subprocess
from datetime import datetime
sys.path.append(os.path.join(os.getcwd(), '..', 'build_report', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), 'build_report', 'scripts'))
from genomics import get_config

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

@celery.task(bind=True)
def long_pdf_task(self):
    # Initialize state
    self.update_state(state='IN PROGRESS')

    # Background task that runs a long function
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

        self.update_state(state='Complete')
        return send_file(
            output_path,
            as_attachment=True,
            attachment_filename=output_filename)
            #attachment_filename=filename)

    except FileNotFoundError:
        abort(404)