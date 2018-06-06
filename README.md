## 运维客户端接口程序
* 基于flask插件式开发
* 用法
    * 在api目录下加入开发好的模块,
    * 配置config/ApiConfig.json，加入模块的请求方法及url
      如： {"func":"SendMail.SendMail","url":"SendMail","endpoint":"mailapi"}

* 启动客户端程序

 sh ops_agent_cli.sh start