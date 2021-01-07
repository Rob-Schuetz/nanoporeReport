# Ensure Conda is installed
if conda | grep -q "conda is a tool"; then
    echo "conda already installed"

else
    echo "installing conda"
    echo wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    echo Miniconda3-latest-Linux-x86_64.sh
fi

# conda create --name myenv
echo conda env create -n nanporeReport -f nanoporeReport_environment.yml
# conda activate nanporeReport


# Ensure Node.js is installed
if npm | grep -q "Usage: npm <command>"; then
    echo "node.js already installed"
    
else
    echo installing nodejs
    echo apt install nodejs
fi

# Install node dependencies.
echo npm install

# Install jasperserver
echo wget https://sourceforge.net/projects/jasperserver/files/JasperServer/JasperReports%20Server%20Community%20edition%207.8.0/TIB_js-jrs-cp_7.8.0_linux_x86_64.run
echo chmod +x TIB_js-jrs-cp_7.8.0_linux_x86_64.run
echo TIB_js-jrs-cp_7.8.0_linux_x86_64.run

