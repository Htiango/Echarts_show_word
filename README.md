# 问题画像可视化展示 (The display of the visualization of problem figure)

## 简介

问题画像可视化展示，展示的是轻问诊中用户提问中，关于用药、症状以及疾病着三个类别两两之间的高频关键词组合，以及对应的关键词组合所在的句子。目前覆盖的科目有男科、妇科、减肥、皮肤科，同时也添加了新增科室的入口。

通过下列命令在79服务器上运行，如果要更换服务器请在setting中进行修改

```shell
$ python manage.py runserver 0.0.0.0:8800
```

由于数据量较小，目前的数据暂时通过文件的形式读取，后期随着数据量的增大，可能需要转到数据库。目前的文件路径都是以绝对路径的方法进行读写。

## 运行环境

基于django的框架，采用Echart实现数据可视化，前端开发框架为bootstrap，工程的运行环境如下：

+ Django (1.10.4)
+ Echarts 3.0
+ Python 2.7.5

## 数据预处理

数据的预处理都在 data_processing/ 文件夹下，预处理过程中的所需如下所示：

+ 预处理的用户提问文件，每条提问为一行
+ 停用词表、专业词表
+ 药品、症状、疾病各种对应的关键词的词表

接下来首先运行：

```shell
$ python get_corpus.py -h
```

根据说明生成语料corpus

然后运行：

```shell
$ python get_relation.py -h
```

根据说明生成用于数据可视化展示的json文件

## Echarts数据可视化

采用官方文档中的Graph Webkit Dep模型进行展示，为力学图结构，共有三层结构：第一层为所属的类别（比如用药与症状词的组合），第二层为第一类中的高频词（比如所有提问中用药的高频关键词），第三层为第二类中的和第二层中的词组合出现的高频词（比如关于症状词和之前出现的用药高频词组合在一起高频出现的关键词），通过点击第二层和第三层的节点，我们还可以看到对应的用户提问句子。

可视化界面如下所示：

![WebImg](djangoImg1.png?raw=true "Optional Title")

## 工程解析

工程相关的脚本文件主要位于目录 graph/ 下，其中：

+ create_fig_data.py 文件中是用于存放数据的类，里面有关于节点、连接、类别之类的信息
+ get_fig_info.py 文件中是用于将从json文件中读取的数据表示为create_fig_data.py 文件中的类
+ html框架在目录 templates/ 下
+ Echarts相关的数据可视化通过js文件来实现，路径为 static/js/fig.js




=======================ENGLISH VERSION====================

## Introduction
This is about the display of visualization of the problem figur. It reveals the relationship among the words from medicine, disease and symptom from the massive dialogs between doctors and patients. It not only represents the relationship between words, but also show the relavant sentenses from the dialogs. It now covers the type on Andrology, Gynecological, Obesity and Dermatology. And it is easy to add a new department through the remain entrance.

Run the following command on the 79 server. If you want to replace the server, make changes in the setting

```shell
$ python manage.py runserver 0.0.0.0:8800
```

Since the amount of data is small now, we temporarily read files to get the data, with the increasing in the amount of data, we will migrate it to the database. The current file path is based on the absolute path to read and write.


## Enviroment
Based on the framework of django, the project uses Echart to achieve data visualization. It uses bootstrap. The project's operating environment is as follows:

+ Django (1.10.4)
+ Echarts 3.0
+ Python 2.7.5

## Data pre-processiong
Data preprocessing part is in the data_processing/ folder. The preprocessing process is as follows:

+ Preprocessing user question file, each question for one line
+ Disable vocabulary as well as professional vocabulary
+ Build a vocabulary of drugs, symptoms, and diseases based on the analysis. 

Next run first:

`` `shell
$ python get_corpus.py -h
`` ``

Generate corpus according to the help function. 

Then run:

`` `shell
$ python get_relation.py -h
`` ``

Generate json files for data visualization based on the instructions

## Visualiza data using Echarts
Using the Graph Webkit Dep model in the Echarts' official document to display. It looks like a force graph with three layers: the first layer represents the category (such as the combination of medication and symptom words), the second layer represents the first category of high-frequency (For example, all the high frequency keywords used in the question), the third layer represents the second category and the second layer of the word combination of high frequency words. By clicking the second and third level nodes, we can also see the corresponding questions from patients.

The visual interface is as follows:

! [WebImg] (djangoImg1.png? Raw = true "Optional Title")

