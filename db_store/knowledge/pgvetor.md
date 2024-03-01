
https://blog.csdn.net/Steven_yang_1/article/details/133648327
https://blog.csdn.net/buluxianfeng/article/details/119868702?spm=1001.2014.3001.5506


sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt install postgresql postgresql-contrib postgresql-server-dev-14
sudo apt install  postgresql-server-dev-16

# 检查运行状态
sudo systemctl status postgresql.service

# 安装pgvector插件
# https://github.com/pgvector/pgvector
cd /tmp
git clone --branch v0.5.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install


sudo -u postgres psql # 使用用户 postgres 登录数据库
create database vector_demo; # 创建数据库
\c vector_demo # 切换到数据库

CREATE EXTENSION vector; # 在当前数据库启用插件

CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

\q # 退出数据库终端

sudo apt-get -y install postgresql
sudo apt-get upgrade libpq-dev


ALTER USER postgres PASSWORD '123456';


wget http://es.archive.ubuntu.com/ubuntu/pool/main/libf/libffi/libffi7_3.3-4_amd64.deb
sudo dpkg -i libffi7_3.3-4_amd64.deb