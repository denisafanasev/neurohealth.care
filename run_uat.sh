# ------- update solution on the server
git pull
#sudo systemctl restart cd_lab.service

# --------   for installation 
#conda create -p .venv_conda python==3.7
#conda install --force-reinstall -y -q -c conda-forge --file requirements_conda.txt
#conda activate .venv_conda
#...
#conda deactivate

# ---------- for local debug
# source .venv/bin/activate
conda activate /home/ubuntu/neuro_health_env_prod

#conda install -c anaconda flask
#conda install -c conda-forge fastavro
#conda install -c anaconda flask-login
#conda install -c conda-forge urllib3
#conda install -c anaconda requests
#conda install -c anaconda pandas
#conda install -c menpo pathlib
#conda install -c anaconda beautifulsoup4
#conda install -c conda-forge fastparquet
#conda install -c conda-forge python-ldap
#conda install -c conda-forge swifter
#conda install -c conda-forge uwsgi
#conda install -c conda-forge python-snappy
#conda install -c conda-forge apscheduler

# flask run --host=0.0.0.0 &
# uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app &
uwsgi --enable-threads --lazy-apps --ini nhc_uat.ini

# for text wsgi
#uwsgi --ini cd_lab.ini &

# ----------- for production wsgi
# sudo systemctl start cd_lab.service

# upload files to rhe server
#scp clang+llvm-8.0.1-powerpc64le-linux-ubuntu-16.04.tar.xz dafanasev@138.201.200.174:/home/dafanasev/

#llvm-config --version

