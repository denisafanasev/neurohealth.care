# conda activate nhc_dev
conda env export --no-builds > environment.yml

zip -r data_backup.zip data

python -m coverage run tests/TestNeuroHealthApp.py
python -m coverage report

rm -r data
unzip data_backup.zip