
目录
- [Dockerfile](#Dockerfile)  
  - [概念 & 流程](#概念-流程)
  - [指令](#指令)
  - [构建过程](#构建)
  - [运行容器](#运行)
- [Docker Network](#Docker-Network)
  - [网络模式](#网络模式)
     - [bridge模式](#bridge)
     - [host模式](#host) 
     - [none模式](#none)
     - [container模式](#container)
     - [自定义网络](#自定义网络)
- [Docker Compose](#Docker-Compose)
  - [概念 & 流程](#概念-流程-1)
  - [常用指令](#常用命令)
- [Portainer](#Portainer)
- [Docker 监控](#Docker-监控)


# Dockerfile

## 概念 流程
Dockerfile是用来构建Docker镜像的文本文件，是由一条条构建镜像所需的指令和参数构成的脚本

构建三步骤：
1. 编写Dockerfile文件
2. docker build命令构建镜像
3. docker run 依镜像运行容器

docker 执行dockerfile的大致流程：
- docker从基础镜像运行一个容器
- 执行一条指令并对容器作出修改执行类似dockercommit的操作提交一个新的镜像层
- docker再基于刚提交的镜像运行一个新容器
- 执行dockerfle中的下一条指令直到所有指令都执行完成

## 指令
FROM 
- 基础镜像，当前新镜像是基于哪个镜像的，指定一个已经存在的镜像作为模板，第一条必须是from

MAINTAINER
- 镜像维护者的姓名和邮箱地址【信息】

RUN
- 容器构建时需要运行的命令
- RUN 两种格式
  - shell
  - exec

- RUN是在 docker build时运行

EXPOSE
- 当前容器对外暴露的端口

WORKDIR
- 指定在创建容器后，终端默认登录进来的工作目录，一个落脚点

USER
- 指定在创建容器后，终端默认登录进来的用户, 默认是root用户

ENV
- 用来在构建镜像过程中设置环境变量

VOLUME
- 用来指定容器中一个或多个挂载点，使容器中的一个或多个目录具有持久化存储数据的功能

ADD
- 将宿主机目录下的文件拷贝进镜像且ADD命令会自动处理URL和解压tar压缩包

COPY
- 类似ADD，拷贝文件和目录到镜像中。将从构建上下文目录中 <源路径> 的文件/目录复制到新的一层 <目标路径> 中
  - COPY src dest 
  - COPY ["src", "dest"]
  - 源路径是相对被构建的源目录的路径，可以是文件或目录的路径，也可以是一个远程的文件URL
  - COPY src1 src2 dest

CMD
- 指定一个容器启动时要运行的命令
- Dockerfile中可以有多个CMD指令，但只有最后一个生效，CMD会被docker run之后的参数替换
  - RUN 是在构建镜像（docker build）时运行
  - CMD 是在容器启动（dokcer run）时运行

ENTRYPOINT
- 指定一个容器启动时要运行的命令
- ENTRYPOINT的目的和CMD一样，都是在指定容器启动程序及参数
- ENTRYPOINT和CMD的区别：
  - ENTRYPOINT可以指定多个参数，CMD只能指定一个参数
  - ENTRYPOINT可以修改，CMD不可以修改
  - ENTRYPOINT不会被docker run之后的参数替换覆盖，而CMD会，

## 构建
docker build -t 镜像名:标签 .

- -t 镜像名:标签
  - 指定要创建的目标镜像名，通常名称跟项目名一样，标签可选
  - 注意：最后的点表示Dockerfile文件所在的路径，绝对路径或者相对路径

## 运行
docker run -it 镜像名:标签 /bin/bash

- -it 表示启动交互式终端
- /bin/bash 表示进入容器后执行的命令

虚悬镜像
- 仓库名、标签都是<none>的镜像
- 构建完成后不会被使用
- 查看
  - docker image ls -f dangling=true
- 删除
  - docker image prune

# Docker Network

容器间的互联和通信以及端口映射，容器IP变动时候可以通过服务名直接网络通信而不受到影响

## 网络模式

Docker 网络模式
- bridge: 默认的网络模式，每个容器都有自己的IP地址，容器之间可以通过IP地址通信，并将容器连接到一个`docker0`虚拟网桥
  - `--network=bridge` 
- host: 容器和主机共享网络，容器和主机之间可以通过主机IP地址通信，容器不会虚拟出自己的网卡，而是使用宿主机的IP地址和端口
  - `--network=host`  
- none: 容器没有网络接口，需要自己配置网络。容器有自己独立的`network namespace`，但是没有进行任何网络配置，如：`--network=none`
  - `--network none` 
- container: 容器和另外一个容器共享网络，两个容器之间可以通过`localhost`通信。新创建的容器不会创建自己的网卡，配置自己的IP地址，而是和一个指定的容器共享IP地址和端口范围。两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。
  -  `--network container:<name or id>` 

  
```shell
docker network ls # 查看网络模式
docker network create --driver bridge my_bridge_network # 创建桥接网络
# docker network create <newt_work name>

docker network inspect <my_bridge_network> # 查看网络详情

docker network rm <my_bridge_network> # 删除网络
```

**docker 容器内的IP是会变动，所以不能直接通过IP地址通信，需要通过服务名或者容器名**

### bridge
- docker 服务默认会创建一个docker0网桥，docker0网桥是一个虚拟网桥，所有的docker容器都连接到docker0网桥上。
- ```
  docker network inpect bridge | grep name # 查看docker0网桥名称
  docker network inpect bridge | grep gateway # 查看docker0网桥网关
  ```
- 每一个bridge都是成双成对的，一个bridge网桥对应一个docker0网桥，`veth pair` 成对出现的虚拟设备，一端连接到容器中，一端连接到docker0网桥上。
  
### host
- 直接使用宿主机的IP地址与外界通信，不需要额外的NAT转换，速度快。通过`-p`设置的参数没用，可以直接通过宿主机IP地址+端口访问到容器。

### none
- Docker 没有网卡、IP、路由等信息，只有一个lo，需要自己配置。

### container
- 新建的容器和指定的容器共享网络，包括网络设备、IP、路由等。两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。

### 自定义网络

**自定义网络本身就维护好了主机名和ip的对应关系(ip和域名都能通)**

```shell
docker network create my_network

# 新建容器 自定义网络
docker run -it -p 8081:80 --network my_network --name my_nginx nginx
docker run -it -p 8082:80 --network my_network --name my_nginx2 nginx

# 测试
docker exec -it my_nginx 
  ping my_nginx2
docker exec -it my_nginx2 
  ping my_nginx
```

# Docker Compose

## 概念 流程
Docker-Compose是Docker官方的开源项目，负责实现对Docker容器集群的快速编排。

可以管理多个Docker容器组成一个应用。在docker-compose.yml文件中定义一个多容器的应用，写好多个容器之间的调用，然后使用一个命令，就可以同时启动/关闭这些容器。

compose 允许用户通过一个docker-compose.yml（YAML格式）来定义一组相关联的应用容器为一个项目。可以很容易地用一个配置文件定义一个多容器的应用，然后使用一条指令安装这个应用的所有依赖，完成构建。

**核心概念**
- **一文件** 
  - docker-compose.yml

- **两要素**
  - 服务（service）一个应用容器实例，比如订单微服务、库存微服务、mysql容器
  - 工程（project）由一组关联的应用容器组成的一个`完整业务单元`，在docker-compose.yml文件中定义。

**步骤**
- 编写Dockerfile定义各个微服务应用并构建出对应的镜像文件
- 使用 docker-compose.yml定义一个完整业务单元，安排好整体应用中的各个容器服务
- 最后，执行docker-compose up命令来启动并运行整个应用程序，完成一键部署上线

## 常用命令
```shell
docker-compose -h                   # 查看帮助
docker-compose up                   # 启动所有docker-compose服务
docker-compose up -d                # 启动所有docker-compose服务并后台运行
docker-compose down                 # 停止并删除容器、网络、卷、镜像。
docker-compose exec yml里面的服务id   # 进入容器实例内部 
  docker-compose exec docker-compose.yml文件中写的服务id /bin/bash
docker-compose ps                   # 展示当前docker-compose编排过的运行的所有容器
docker-compose top                  # 展示当前docker-compose编排过的容器进程
docker-compose logs yml里面的服务id   # 查看容器输出日志
docker-compose config               # 检査配置
docker-compose config-q             # 检查配置，有问题才有输出
docker-compose restart              # 重启服务
docker-compose start                # 启动服务
docker-compose stop                 # 停止服务
```

# Portainer

Portainer 是一个开源的 Docker 管理界面，提供状态显示面板、应用模板快速部署、容器镜像网络数据卷的基本操作（包括上传下载镜像，创建容器等操作）、事件日志显示、容器控制台操作、Swarm集群和服务等集中管理和操作、登录用户认证等。

# Docker 监控

CAdvisor 是一个用于监控 Docker 容器和宿主机的工具。

InfluxDB 是一个开源的时序数据库，可以存储和查询时间序列数据。

Grafana 是一个开源的监控可视化工具，可以基于 InfluxDB 和 Prometheus 等数据源展示监控数据。
