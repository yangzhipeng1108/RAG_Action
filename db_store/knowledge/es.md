https://blog.csdn.net/smilehappiness/article/details/118466378

https://blog.csdn.net/u014553029/article/details/110572632


wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.2-linux-x86_64.tar.gz
tar -zxvf elasticsearch-7.13.2-linux-x86_64.tar.gz -C /usr/local

useradd user-es


chown user-es:user-es -R /usr/local/elasticsearch-7.13.2
su user-es

cd /usr/local/elasticsearch-7.13.2/bin

./elasticsearch

vim /usr/local/elasticsearch-7.13.2/config/elasticsearch.yml

pip  install  elasticsearch==7.13.2  版本对应

#默认只允许本机访问，修改为0.0.0.0后则可以远程访问
# 绑定到0.0.0.0，允许任何ip来访问
network.host: 0.0.0.0 

初始化节点名称

cluster.name: elasticsearch 
node.name: es-node0
cluster.initial_master_nodes: ["es-node0"]

修改端口号（非必须）

http.port: 19200


xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true


/usr/local/elasticsearch-7.13.2/bin/elasticsearch-setup-passwords interactive