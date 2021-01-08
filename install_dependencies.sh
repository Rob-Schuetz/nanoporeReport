export PATH=$PATH:$(pwd)

# Ensure Conda is installed
if conda | grep -q "conda is a tool"; then
    echo "conda already installed"

else
    echo "installing conda"
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    Miniconda3-latest-Linux-x86_64.sh
fi

export PATH=$PATH:/home/ubuntu/miniconda3/bin/
conda env create -n nanoporeReport -f nanoporeReport_environment.yml


# Ensure Node.js is installed
if npm | grep -q "Usage: npm <command>"; then
    echo "node.js already installed"
    
else
    echo installing nodejs
    apt update
    apt install nodejs
    apt install npm
fi

# Install node dependencies.
npm install

# Install jasperserver
wget https://sourceforge.net/projects/jasperserver/files/JasperServer/JasperReports%20Server%20Community%20edition%207.8.0/TIB_js-jrs-cp_7.8.0_linux_x86_64.run
chmod +x TIB_js-jrs-cp_7.8.0_linux_x86_64.run
TIB_js-jrs-cp_7.8.0_linux_x86_64.run

# Remove installers
rm Miniconda3-latest-Linux-x86_64.sh
rm TIB_js-jrs-cp_7.8.0_linux_x86_64.run


# Set up SQL tables
bash /home/ubuntu/jasperserver/ctlscript.sh start
cd /home/ubuntu/projects/nanoporeReport/build_report/scripts
sudo -S -u postgres PGPASSWORD=postgres /home/ubuntu/jasperserver/postgresql/bin/createdb -p 5432 -h localhost -e nanopore
sudo -S -u postgres PGPASSWORD=postgres /home/ubuntu/jasperserver/postgresql/bin/psql -U postgres -d nanopore -a -f make_tables.sql

# Install ANNOVAR resources
cd /home/ubuntu/projects/nanoporeReport/build_report/annovar
mkdir humandb && cd humandb
wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz
# wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/hg19_cosmic68.txt.idx
# wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/hg19_cosmic68.txt
# wget http://www.openbioinformatics.org/annovar/download/hg19_cosmic68.txt
# annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene humandb/