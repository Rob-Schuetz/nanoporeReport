# nanoporeReport
Basic layout for a web applicationi that takes as it's inputs a list of gene panel targets (targets.bed) and a summary of variants (variants.vcf) derived from an aggregation of nanopore sequencing reads.

## Dependencies
### Conda Environment
The nanoporeReport.yml configuration file contains all of the necessary conda packages.  Ensure that conda is installed and available in the path variable and run the following to create the conda environment:
conda env create -f nanoporeReport.yml -n nanoporeReport

### Node.js
The front-end of the application utilizes the react framework (create-react-app), which lives on a node.js server.  To initiate the node, ensure node.js (with npm) is installed and navigate into the directory of the freshly cloned repository.  Running 'npm install' will result in the installation of all dependencies, at which time 'npm start' can be called to start the development server (runs on port 3000).

### Jasperserver
A jasperserver instance is required to generate the pdf that is ultimately returned to the end user.  Detailed jasperserver installation instructions are provided at https://community.jaspersoft.com/documentation/tibco-jasperreports-server-installation-guide/v780/introduction. All defaults can be accepted when installing.

### PostgreSQL
A database instance is necessary in this application to prepare the report data and store data pertaining to each report execution.  The Jasperserver instance by default includes a postgres database.  You may chose your own database if you'd like, but I found it easiest to utilize the existing postgres instance and add your own database.  The build_report/scripts/make_tables.sql script is used to build all necessary tables, simply execute from your preferred database IDE.

## Configuration
The build_report/config/config.yaml file contains several items that can be utilized to alter the behavior of the nanoporeReport application.  Default ports for the jasperserver and flaskAPI are set to 8080 and 5000, respectively.  Credentials are stored here, so if you choose to change the default users for either jasperserver or postgres be sure to change the credential values.

## Initializing
Execute each of the following commands to initialize the necessary components of nanoporeReport.  I prefer to execute these in individual panes to monitor traffic, but they can also be batched together in a bash script if desired:
  
bash {jasperserver location}/ctlscript.sh start  #jasperserver  
redis-server  #message broker  
npm start   #react front-end  
python api/api.py  #Flask API  
celery -A api/api.celery worker  #celery worker  


## Use
This application takes as it's inputs a .vcf file resulting from nanopore sequencing and a .bed file indicating targets of interest for the sequenced tumor sample.  Invalid vcf's will be rejected as long as .bed files that do not meet the following format (*chr*, *pos-1*, *pos*, *target_description*).  The final output is a summary of the mutational status at each provided target.

