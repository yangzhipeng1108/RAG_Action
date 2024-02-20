from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts=["http://elastic:123456@0.0.0.0:19200/"])
# response = es.cluster.health()

#有密码
# es = Elasticsearch(['10.10.13.12'], http_auth=('xiao', '123456'), timeout=3600)

es.indices.delete(index='es_subdocument_store', ignore=[400, 404])
#
es.indices.create(index="es_subdocument_store",ignore=400)


Subdocument_result_dict = {'文件存储': ['银汉智算平台采用 CephFS 作为后端存储系统，CephFS是一个支持POSIX接口的文件系统，它使用ceph存储集群来存储数据。', '文件系统对于客户端来说可以方便的挂载至本地使用。CephFS构建在RADOS之上，继承RADOS的容错性和扩展性，支持多副本，保障数据的高可靠性。'],

 '文件存储 目录结构': ['目录 /    名称 系统盘    容量限制 20GB    说明 一般系统依赖以及python安装包都会安装在系统盘下，也可以存放代码等小容量的数据。系统盘数据可通过“固化为镜像”操作，保存至自有镜像中。注意：请不要在“/”目录下创建文件夹和文件，否则重启后文件会消失。',
 '目录 /root/tmp    名称 缓存盘    容量限制 20GB    说明 可存放读写IO要求高的缓存数据。实例关机数据保留七天，连续关机七天后将删除缓存数据。在有效期内重新开机，也可能会因为原容器实例所在节点的资源不足等原因（例如GPU卡不足），而导致缓存盘数据丢失。',
 '目录 /root/nas-private    名称 个人网盘    容量限制 100GB    说明 持久化数据盘，用户级独享。在同一个区域，个人网盘对该用户的不同实例可见，并且文件可读可写。', '目录 /root/nas-share    名称 共享网盘    容量限制 500GB    说明 持久化数据盘，客户级共享。在同一个区域，共享网盘对该客户下所有用户的不同实例可见，并且文件可读可写。',
 '目录 /root/nas-public    名称 公共数据盘    容量限制 无    说明 平台常用公共数据集的存放目录。文件只读。']}

#插入多条数据
action = []
i = 1
for key in Subdocument_result_dict.keys():
    if len(Subdocument_result_dict[key]) > 1:
        doc_inter = []
        for  context in Subdocument_result_dict[key]:
            doc_inter.append({"_index":"es_subdocument_store","_type":"doc","_id":i,"_source":{"title":key,"content":context}})
            i += 1
        action.extend(doc_inter)
    else:
        action.append({"_index":"es_subdocument_store","_type":"doc","_id":i,"_source":{"title":key,"content":Subdocument_result_dict[key][0]}})
        i += 1

print(action)
helpers.bulk( es, action )



es.indices.delete(index='es_document_store', ignore=[400, 404])
es.indices.create(index="es_document_store",ignore=400)


result_dict = {'文件存储': '银汉智算平台采用 CephFS 作为后端存储系统，CephFS是一个支持POSIX接口的文件系统，它使用ceph存储集群来存储数据。文件系统对于客户端来说可以方便的挂载至本地使用。CephFS构建在RADOS之上，继承RADOS的容错性和扩展性，支持多副本，保障数据的高可靠性。',
               '文件存储 目录结构': '目录 /    名称 系统盘    容量限制 20GB    说明 一般系统依赖以及python安装包都会安装在系统盘下，也可以存放代码等小容量的数据。系统盘数据可通过“固化为镜像”操作，保存至自有镜像中。注意：请不要在“/”目录下创建文件夹和文件，否则重启后文件会消失。 目录 /root/tmp    名称 缓存盘    容量限制 20GB    说明 可存放读写IO要求高的缓存数据。实例关机数据保留七天，连续关机七天后将删除缓存数据。在有效期内重新开机，也可能会因为原容器实例所在节点的资源不足等原因（例如GPU卡不足），而导致缓存盘数据丢失。 目录 /root/nas-private    名称 个人网盘    容量限制 100GB    说明 持久化数据盘，用户级独享。在同一个区域，个人网盘对该用户的不同实例可见，并且文件可读可写。 目录 /root/nas-share    名称 共享网盘    容量限制 500GB    说明 持久化数据盘，客户级共享。在同一个区域，共享网盘对该客户下所有用户的不同实例可见，并且文件可读可写。 目录 /root/nas-public    名称 公共数据盘    容量限制 无    说明 平台常用公共数据集的存放目录。文件只读。'}

# 插入多条数据
action = []
i = 1
for key in result_dict.keys():
    action.append({"_index":"es_document_store","_type":"doc","_id":i,"_source":{"title":key,"content":result_dict[key]}})
    i += 1

print(action)
helpers.bulk( es, action )
