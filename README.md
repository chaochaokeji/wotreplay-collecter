# wotreplay collecter

> 坦克世界录像信息收集器

## 说明

应用可通过wotreplay文件获取相关信息

应用包含2个类：

Wotreplay 录像信息类

Download 下载录像类

## 用法

应用使用 Docker 进行部署

* 第一步

使用 Dockerfile 文件生成 wotpython 镜像

```
docker build -f ./Dockerfile -t wotpython .

```

* 第二步

执行 docker-compose.yml 文件启动容器

```
docker-compose up -d

```

* 第三步

检查是否运行

```
docker ps

```

列表中显示 wotpython wotmongo 两个容器说明运行成功

* 第四步

容器 wotpython 执行完成后会退出容器

再次启动执行

```
docker ps -a  # 查看容器id

docker start 容器id  # 启动容器

```

## 其他

配置说明：

数据库中 configs 集合

```
`server`： 网站后缀

`version`： 录像版本号

`page`： 每次查询页数量

```

录像版本号获取方式，点击网站录像列表页下一页，在url参数中可查看当前坦克世界版本对应version值

网站地址：

```
`RU 俄服` ： wotreplays.ru

`EU 欧服` ： wotreplays.eu

~~`NA 北美服 ` ： wotreplays.na~~

~~`ASIA 亚服` ： wotreplays.asia~~
```


## 更新日志

* 2019-11-29 第一个版本
