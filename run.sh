https://www.daterangepicker.com


ssh -i "shaman_aws_key.pem" ubuntu@ec2-3-142-254-179.us-east-2.compute.amazonaws.com


conda env export --no-builds > environment.yml

# update and install packeges from the environment file
conda env update --file environment.yml --prune

# ------- update solution on the server
git pull
systemctl daemon-reload
sudo systemctl restart nhc.service

# --------   for installation 
conda create -p neuro_health_env_prod python==3.8
conda activate neuro_health_env_prod
conda install --force-reinstall -y -q -c conda-forge --file requirements_conda.txt
...
conda deactivate

# ---------- for local debug
# source .venv/bin/activate
conda activate /home/ubuntu/neuro_health_env_prod
# flask run --host=0.0.0.0 &
# uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app &
uwsgi --enable-threads --lazy-apps --ini neuro_health_uat.ini

# for text wsgi
uwsgi --ini neuro_health.ini &

# ----------- for production wsgi
# sudo systemctl start cd_lab.service

# upload files to rhe server
#scp clang+llvm-8.0.1-powerpc64le-linux-ubuntu-16.04.tar.xz dafanasev@138.201.200.174:/home/dafanasev/

#llvm-config --version

# envirimental variables

#1DMC hadoop client
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

export HADOOP_HOME=/home/shaman/Soft/hadoop-2.7.7
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
export HADOOP_CONF_DIR=/media/psf/Dropbox/Devs/cd_lab/cd_lab/config/1dmc_hadoop_client/hadoop-conf



# --------
conda install -c anaconda flask
conda install -c anaconda flask-login
conda install -c conda-forge uwsgi

#conda install -c anaconda requests
#conda install -c anaconda pandas
#conda install -c menpo pathlib
#conda install -c anaconda beautifulsoup4
#conda install -c conda-forge fastparquet
#conda install -c conda-forge python-ldap
#conda install -c conda-forge swifter
#conda install -c conda-forge python-snappy
#conda install -c conda-forge apscheduler
#conda install -c conda-forge pyarrow
#conda install -c conda-forge hdfs3
#conda install -c anaconda psycopg2
#conda install -c conda-forge flask-mail

# hdfs test

hdfs dfs -ls /user/cleverdata/data/incoming/
hdfs dfs -copyToLocal /user/cleverdata/data/incoming/cid=4fd755f2-9075-4379-8640-12ee75c358ef/data_type=cookiesync/dt=2020-09-11/cookie-nc-events.1599845420642.avro

# copy to remote server
#scp -i ../../_aws/shaman_aws_key.pem ubuntu@app.neurohealth.care:/home/ubuntu/_exchange/prod_data_300622.zip
scp -i ../../_aws/shaman_aws_key.pem course_1.zip ubuntu@app.neurohealth.care:/home/ubuntu/_exchange/

# copy from remote
scp -i ../../_aws/shaman_aws_key.pem ubuntu@app.neurohealth.care:/home/ubuntu/_exchange/prod_data_300622.zip .

# setup cert to nginx
https://marcosantonocito.medium.com/steps-to-install-a-go-daddy-ssl-certificate-on-nginx-on-ubuntu-14-04-ff942b9fd7ff
