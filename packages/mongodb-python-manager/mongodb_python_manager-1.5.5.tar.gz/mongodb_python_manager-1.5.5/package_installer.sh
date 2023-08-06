#!/bin/bash
source .venv/bin/activate
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip setuptools wheel
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org structlog pandas==1.5.3
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org pymongo python-dotenv tqdm pytest
python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org certifi

#python setup.py test --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host 

# cat ~/ca_certs/IS_INFRA_ROOT_CRT.crt >> $(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)
export SSL_CERT_FILE=$(python -m certifi)
export CERT_PATH=$(python -m certifi)
