# 指定Python环境
FROM python:3.8.16
# 拷贝Python依赖库requirements文件到当前目录下
ADD requirements.txt /
# 安装依赖库
RUN pip install -r /requirements.txt

# 拷贝所有文件到app目录下
ADD . /app
# 指定app为工作目录
WORKDIR /app
# 声明端口
EXPOSE 5000
# docker容器启动
CMD [ "python" , "app.py"]