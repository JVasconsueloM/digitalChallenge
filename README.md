install on local (to dev)


Instalamos Python 3, pip3, Postgres y otras dependencias

```
$ sudo apt-get update && sudo apt-get -y upgrade
$ sudo apt-get install python3
$ sudo apt-get install -y python3-pip
$ pip3 install --upgrade pip

$ sudo apt-get install -y libpq-dev postgresql postgresql-contrib 	
```
configuramos el usuario postgres, creamos el usuario digital, la base de datos digital y configuramos los permisos .
```
$ sudo passwd postgres
$ sudo su postgres
$ createdb digital
$ psql

ALTER ROLE postgres WITH PASSWORD '1234';
CREATE USER digital PASSWORD '1234';

ALTER ROLE postgres WITH SUPERUSER;
ALTER ROLE digital WITH SUPERUSER;

GRANT ALL PRIVILEGES ON DATABASE digital TO digital;
ALTER DATABASE digital OWNER TO digital;

\q
exit
```
instalamos el virtualenv  y lo configuramos
```
 $ sudo -H pip3 install virtualenv virtualenvwrapper
 $ mkdir ~/.virtualenvs
 $ export WORKON_HOME=~/.virtualenvs
 $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
 $ source ~/.bashrc
 $ mkvirtualenv digital
 $ workon digital
```
instalamos el proyecto
```
$ sudo apt-get install git
$ cd ~
$ sudo mkdir webapps
$ cd webapps
$ git clone https://github.com/JVasconsueloM/digitalChallenge digital
$ cd digital/
$ pip3 install -r requirements.txt
$ python3.5 manage.py migrate --settings=digital.settings
```
ahora podemos abrirlo con nuestro IDE y usar el entorno virtual digital para ejecutar el proyecto y/o modificarlo

