import os
from pathlib import Path
import logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "reseach/trials.ipynb"
]

for files in list_of_files:
    files = Path(files)
    filedir, filename = os.path.split(files)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")
        
    if (not os.path.exists(filename) or os.path.getsize(filename) == 0) and filename != "":
        with open(files, 'w') as f:
            pass 
        logging.info(f"Created file: {filename}")
    else:
        logging.info(f"Directory already exists: {filedir}")

        