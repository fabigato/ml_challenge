Example coding challenge

## Setup virtualenv and install dependencies

* Create a python 3 virtual environment
```bash    
virtualenv -p python3 ~/virtualenvs/codfish
```

* Start the environment
```bash
source ~/virtualenvs/codfish/bin/activate
```

* Install Dependencies
```bash
pip3 install -r requirements.txt
```

## Generate documentation

Install sphinx dependencies

    pip install sphinx sphinx_rtd_theme
    
Build the documentation

    cd docs && make html && cd build && python -m http.server 1234
    
View it in your browser

    http://0.0.0.0:1234/html
