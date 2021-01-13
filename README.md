# nanoporeReport
Basic layout for a web application that takes as it's inputs a list of gene panel targets (targets.bed) and a summary of variants (variants.vcf) derived from an aggregation of nanopore sequencing reads.

## Dependencies

### install_dependecies.sh
The install_dependencies.sh file located in the root directory can be utilized to install all dependencies.  You will be prompted by sourced installation scripts, accept all defaults when available and answer Y|y|yes to prompts where no default is available.  The only exceptions are the directories, when prompted by conda, provide the following path: /home/ubuntu/miniconda3.  When prompted by jasperserver, provide the following path: /home/ubuntu/jasperserver.  If you would be more comfortable installing the dependencies individually, refer to each dependency below and refer to the conda_environment.yml file located in the root directory.

PATCH, run the following commands after running install_dependencies.sh:
conda activate nanoporeReport
conda install redis


### Conda Environment
The conda_environment.yml configuration file contains all of the necessary conda packages.  Ensure that conda is installed and available in the path variable and run the following to create the conda environment:
conda env create -f nanoporeReport.yml -n nanoporeReport

### Node.js
The front-end of the application utilizes the react framework (create-react-app), which lives on a node.js server.  To initiate the node, ensure node.js (with npm) is installed and navigate into the directory of the freshly cloned repository.  Running 'npm install' will result in the installation of all dependencies, at which time 'npm start' can be called to start the development server (runs on port 3000).

### Jasperserver
A jasperserver instance is required to generate the pdf that is ultimately returned to the end user.  Detailed jasperserver installation instructions are provided at https://community.jaspersoft.com/documentation/tibco-jasperreports-server-installation-guide/v780/introduction.

### PostgreSQL
A database instance is necessary in this application to prepare the report data and store data pertaining to each report execution.  The Jasperserver instance by default includes a postgres database.  You may chose your own database if you'd like, but I found it easiest to utilize the existing postgres instance and add your own database.  The build_report/scripts/make_tables.sql script is used to build all necessary tables.  It is called in install_dependencies.sh, but if you choose to use another database simply update syntax to match your flavor of sql and execute in an IDE.

### Upload jasper.zip
Once the jasperserver is up and running, login by navigating to http://{your_ip}:8080/jasperserver/login.html in your preferred web browser. The default admin login credentials are jasperadmin/jasperadmin.  Navigate to the jasperserver repository (Navbar > Manage > Server Settings).  In the left hand margin, select the "Import" tab.  Upload the jasper.zip file located in build_report/jrxml directory, select the "Server Key" radio button, accept the defaults in the "Import options:" section and select the "Import" button.

## Configuration
The build_report/config/config.yaml file contains several items that can be utilized to alter the behavior of the nanoporeReport application.  Default ports for the jasperserver and flaskAPI are set to 8080 and 5000, respectively.  Credentials are stored here, so if you choose to change the default users for either jasperserver or postgres be sure to change the credential values.

## Initializing
Before initializing any components, the conda environment must be activated:
conda activate nanoporeReport

Execute each of the following commands to initialize the necessary components of nanoporeReport.  I prefer to execute these in individual panes to monitor traffic, but they can also be batched together in a bash script if desired:

bash {jasperserver location}/ctlscript.sh start  #jasperserver  
redis-server  #message broker  
npm start   #react front-end  
python api/api.py  #Flask API  
celery -A api/api.celery worker  #celery worker  

## Use
Navigate to http://{your_ip}:3000 in your preferred web browser. The application takes as it's inputs a .vcf file resulting from nanopore sequencing and a .bed file indicating targets of interest for the sequenced tumor sample.  Invalid vcf's will be rejected as long as .bed files that do not meet the following format (*chr*, *pos-1*, *pos*, *target_description*).  The final output is a summary of the mutational status at each provided target.

