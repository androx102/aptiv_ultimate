# aptiv_ultimate

## 1. Requirements
- git
- curl
- python 

## 2. Installation

2.1 Clone repo:

```bash
git clone https://github.com/androx102/aptiv_ultimate.git
```

2.2A If you don't have python - install conda and create env:
```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash ~/Miniconda3-latest-Linux-x86_64.sh

source ~/.bashrc
```
2.2B
Create new enviroment and activate it:
```bash
conda create -n django_env django
conda activate django_env
```

2.3
To install python requirements:
```bash
pip install -r requirements.txt
```

## 3. Running application

To start application
```bash
python manage.py runserver
```
