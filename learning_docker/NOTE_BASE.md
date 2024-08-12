# 一起学习Docker



| List                                  | SubDirectory                                                 | Description                                                  | **Notes** |
| ------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | --------- |
| [镜像](#镜像)                         |                                                              | Image，简单来说从Docker图标上来解释，即可认为是下面的蓝鲸鱼  |           |
|                                       | - [基本命令](#基本命令)<br />- [本地镜像](#本地镜像)<br />- [阿里云Docker Registry](#阿里云Docker-Registry)<br />- [私服Docker Registry](#私服Docker-Registry) |                                                              |           |
| [容器](#容器)                         | - [基本命令](#基本命令-2)                                    | Container，简单来说可认为是蓝鲸鱼上面的集装箱，互相独立，互不影响 |           |
| [容器卷（数据卷）](#容器卷（数据卷）) | - [基本命令](#基本命令-3)                                    | 将docker容器中的文件挂载到本地                               |           |



# 镜像

## 基本命令

```shell
docker search <image_name> # 搜索镜像
docker pull <image_name> # 下载镜像
dpcker push <image_name> # 上传镜像

docker images  # 列出所有镜像
docker images -a  # 列出所有镜像
docker images -q  # 列出所有镜像的id
docker images -qa  # 列出所有镜像的id
docker system df # 列出镜像、容器、数据卷所占用的空间

docker rmi <image_id> # 删除镜像
docker rmi -f $(docker images -q) # 删除所有镜像
docker rmi -f <image_id1> <image_id2> # 删除多个镜像
```
## 本地镜像

将容器提交为本地镜像（本地镜像生产）

```shell
docker commit -m="description" -a="author" <container_id> <image_name>:<tag> # 提交容器为镜像
example:
   下载一个vim
   apt-get update
   apt-get -y install vim 
```
## 阿里云Docker Registry

将镜像提交到阿里云Docker Registry \
（aliyun.com -> 控制台 -> 容器镜像服务）

```shell
docker login --username=<your_name> registry.cn-hangzhou.aliyuncs.com

docker tag [ImageId] registry.cn-hangzhou.aliyuncs.com/jensen_docker_test/my_docker:[镜像版本号]

docker push registry.cn-hangzhou.aliyuncs.com/jensen_docker_test/my_docker:[镜像版本号]

docker pull registry.cn-hangzhou.aliyuncs.com/jensen_docker_test/my_docker:[镜像版本号]
```
## 私服Docker Registry

```shell
docker pull registry

docker run -d -p 5000:5000 --privileged=true registry
#docker run -d -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock registry:2
# -v 挂载数据卷 默认挂载到/var/lib/registry

docker commit -m="description" -a="author" <container_id> <image_name>:<tag> # 提交容器为镜像

# 查看私服库是否有 镜像
curl -XGET http://192.168.96.1:5000/v2/_catalog
# win 可用 Invoke-WebRequest -Uri http://127.0.0.1:5000/v2/_catalog -Method GET 

docker tag <image_name>:<tag> <本地IP:映射的端口5000>/<image_name>:<tag>
# docker tag myubuntu_if:1.0 192.168.96.1:5000/myubuntu_if:1.0

# 修改配置文件 daemon.json中添加["insecure-registries": ["<本地IP:映射的端口5000>"]]
# ["insecure-registries": ["192.168.96.1:5000"]]
cat /etc/docker/daemon.json 

# 修改配置之后docker
systemctl restart docker
docker run -d -p 5000:5000 --privileged=true registry
docker push 192.168.96.1:5000/myubuntu_if:1.0

# 再次查看信息
curl -XGET http://192.168.96.1:5000/v2/_catalog
# Invoke-WebRequest -Uri http://192.168.96.1:5000/v2/_catalog -Method GET

# 测试
docker pull 192.168.96.1:5000/myubuntu_if:1.0

example:
  apt-get update
  apt-get install net-tools
  # ifconfig
Invoke-WebRequest -Uri http://127.0.0.1:5000/v2/_catalog -Method GET # 192.168.96.1
```

# 容器

## 基本命令
![img.png](images%2Fimg.png)
```shell
docker run 
  --name # 指定容器名称
  -it # 进入容器 (前台交互模式)
  -P # 随机映射端口
  -p # 指定端口(主机端口:容器端口)
  -d # 后台运行 (后台交互模式)

docker run -it ubuntu bash
```
**列出所有运行的容器实例**

```shell
docker ps
docker ps -a
docker ps -a -q
```
**退出容器**

```shell
exit # 退出容器

control + p + q  # 退出容器，不停止
```

**启动已停止的容器**

```shell
docker start <container_id or container_name>  # 启动容器
docker start -i <container_id or container_name>  # 启动并进入容器
docker restart <container_id or container_name>  # 重启容器

docker stop <container_id or container_name>  # 停止容器

docker rm <container_id or container_name>  # 删除容器

docker kill <container_id or container_name>  # 强制停止容器
docker rm -f <container_id or container_name>  # 强制删除容器
```
**查看容器信息**

```shell
docker logs <container_id or container_name> # 查看容器日志

docker top <container_id> # 查看容器进程

docker inspect <container_id> # 查看容器详细信息

```
**重新进入没有停止的容器**

```shell
# exec 重新进入容器,用exit退出不会停止容器
docker exec 
  -it <container_id or container_name> bash # 进入容器 
  
# attach 重新进入容器,用exit退出会停止容器
docker attach 
  -it <container_id or container_name> bash #  进入容器
```
**拷贝容器文件到本地**

```shell
docker cp <container_id or container_name>:<container_path> <local_path> # 从容器复制文件到本地
docker cp <local_path> <container_id or container_name>:<container_path> # 从本地复制文件到容器
```

```shell
docker export <container_id or container_name> > <file_name>.tar # 导出容器
cat <file_name>.tar | docker import - <image_name> # 导入容器
```

# 容器卷（数据卷）

**将docker容器中的文件挂载到本地**

## 基本命令

```shell
docker run -it -v <local_path>:<container_path> <image_name>:<tag>
  -v  # 表示挂载一个数据卷
    --privileged=true # 表示容器内的root拥有真正的root权限
    
docker run -it --name myvl_test --privileged=true -v /users/15534/appdata/docker_vl_test:/tmp/mydokcer_vl ubuntu bash

docker inspect myvl_test # 查看容器信息 数据卷是否挂载成功

# 读写 :rw（默认） 只读 :ro
docker run -it --privileged=true -v <local_path>:<container_path>:<rw|ro> <image_name>:<tag>

# 继承、共享容器卷
docker run -it --privileged=true --volumes-from <父类 container_name> --name <子类 container_name> <image_name>:<tag>
```







