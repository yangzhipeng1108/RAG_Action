import  os

# f = open("document_result_dict.txt",encoding='utf-8')               # 返回一个文件对象
# line = f.readlines()               # 调用文件的 readline()方法
#
# for value  in line :
#     document_result_dict = eval(value)
#     print(document_result_dict)
#     print(type(document_result_dict))



base = 'E:/python/yovole/NLP/pre-train/ai_project/yovole/source/'
for root, ds, fs in os.walk(base):
    for f in fs:
        if f.endswith('.md'):
            fullname = os.path.join(root, f)
            print(fullname)