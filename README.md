# transformers_en_zh中英互译
### 项目代码来源：https://github.com/huggingface/transformers

### 基于Flask的前端WEB编写
~~~Python
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/jquery/2.0.0/jquery-2.0.0.min.js"></script>
</head>
<body>
<div id="a">
    <h1>transformers中英互译</h1>
    <pre></pre>
    <select class="form-select" aria-label="Default select example" onchange="selectOnchang(this)">
        <option selected>选择翻译模式</option>
        <option value="1">英译中</option>
        <option value="2">中译英</option>
      </select>
    <form id="form1" class="row g-3" onsubmit="return false" method="post">
        <div>
            <div class="grid text-center">
                <div class="mb-3 g-col-6">
                    <textarea class="form-control" name="sentence" placeholder="请输入..." id="exampleFormControlTextarea1" rows="3"></textarea>
                </div>
                <div class="mb-3 g-col-6">
                    <textarea class="form-control"  readonly id="result" rows="3"></textarea>
                </div>
              </div>
       
    </div>
        <div class="col-auto">
            <button type="submit" class="btn btn-primary mb-3">提交</button>
        </div>

    </form>
</div>
</body>
</html>
<style>
    #a {
        margin: 100px;

    }
</style>
<script>
    var a = 0;
    function selectOnchang(obj){  
        //获取被选中的option标签选项 
        a = obj.selectedIndex
       }
    $("button").click(function () {
        if(a==1){
            $.ajax({
                url: "/en2zh",
                type: "POST",
                data: $('#form1').serialize(),
                success: function (result) {
                    // alert(result);
                    $('#result').html(result)
                }
            });
        }else if(a==2){
            $.ajax({
                url: "/zh2en",
                type: "POST",
                data: $('#form1').serialize(),
                success: function (result) {
                    // alert(result);
                    $('#result').html(result)
                }
            });
        }else{
            alert("请选择翻译模式！")
        }
        
    });
</script>
~~~

### 基于Flask的后端编写
~~~Python
from flask import Flask, Response, request, render_template
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

#加载en2zh模型
model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)

#加载zh2en模型
model2 = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
tokenizer2 = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
translation2 = pipeline("translation_zh_to_en", model=model2, tokenizer=tokenizer2)

app = Flask(__name__)


@app.route('/')
def r():
    return render_template('translation.html')
    
@app.route('/en2zh', methods=['POST'])
def en2zh():
# 英文翻译成中文
# AutoModelForSeq2SeqLM.from_pretrained
    text = request.form.get("sentence")
    translated_text = translation(text, max_length=40)[0]['translation_text']
    return translated_text

@app.route('/zh2en', methods=['POST'])
def zh2en():
    # 中文翻译成英文
    text2 = request.form.get("sentence")
    translated_text2 = translation2(text2, max_length=40)[0]['translation_text']
    return translated_text2

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
~~~

## Docker镜像配置


### Dockerfile的编写

Dockerfile是一个用来构建镜像的文本文件，文本内容包含了一条条构建镜像所需的指令和说明。主要代码如下：
~~~Dockerfile
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
~~~
项目部署代码存放的GitHub仓库地址：https://github.com/cancan520/transformers_en_zh

仓库地址截图：
![result](https://raw.githubusercontent.com/cancan520/transformers_en_zh/main/Snipaste_2022-12-13_00-28-54.jpg)

下载后，构建容器镜像：docker build . -t 容器名称

可用docker images命令查看打包完成的镜像文件信息

上传容器到DockerHub：

docker login -u cancan520

docker tag [ImageId] cancan520/transformers:1.0

docker push cancan520/transformers:1.0

查看DockerHub上传情况：
![result](https://github.com/cancan520/transformers_en_zh/blob/main/Snipaste_2022-12-13_00-11-51.jpg?raw=true)

## 应用服务运行

从DockerHub远程拉取镜像：

docker pull cancan520/transformers:1.0

运行镜像（将容器5000端口映射到宿主机的5000端口）：

docker run -p 5000:5000 cancan520/transformer:1.0

运行后等待加载模型后，在浏览器访问127.0.0.1:5000即可弹出使用界面，选择翻译模式，输入对应语言提交即可获取其翻译

使用界面如下：

![result](https://github.com/cancan520/transformers_en_zh/blob/main/Snipaste_2022-12-13_00-21-06.jpg?raw=true)

选择翻译模式：

![result](https://github.com/cancan520/transformers_en_zh/blob/main/Snipaste_2022-12-13_00-21-24.jpg?raw=true)

英译中成果展示如下：
![result](https://github.com/cancan520/transformers_en_zh/blob/main/Snipaste_2022-12-13_00-22-01.jpg?raw=true)

中译英成功展示如下：
![result](https://github.com/cancan520/transformers_en_zh/blob/main/Snipaste_2022-12-13_00-23-10.jpg?raw=true)

停止服务（该步骤耗时较长）：
docker stop cancan520/transformers:1.0
