# CAS服务
本服务提基于CAS协议,实现简易SSO功能(Single Sign On, 单点登录)。可提供跨域名的统一身份认证。本服务基于flask框架实现，运行环境为python3.6.5。

## CAS服务规程描述

CAS服务规程共计三个，分别为:
1. 用户登录过程
2. 已登录用户认证过程
3. 用户登出过程（暂未实现）

### 用户登录过程规程描述
参与本规程的实体包含三个：
1. 用户 user
2. CAS服务 cas
3. 他方应用 app

规程描述如下：
1. user 发送请求到 app， 以请求获取相关资源;
2. app 获取到 user 发来的请求，判断该用户是否已通过认证。若通过认证，则结束规程，否则将返回给 user 状态码为302的响应报文，
报文携带 app 与 cas 事先商议好的 domain，domain用于标记app身份。使用户跳转到 cas，进行cas认证;
3. user 将携带由 app 返回的 domain，发送认证请求到 cas;
4. cas 判别是否已经颁发给 user 票证授予票证 tgt，若未颁发tgt或tgt过期失效，则返回 user 登录页面，要求用户进行登录;
5. user 将自身身份凭证及口令发送给 cas 请求身份认证;
6. cas 判别用户身份，若通过身份认证，将 domain 查询与 app 事先商议好的回调地址 callback_url，颁发给user的tgt，以及服务票证 st 返回给用户;
7. 用户将携带 st 访问 cas 发回的回调地址。
8. app 将在回调地址处获取到 st, 当app需要获取 user 的相关信息或权限声明时， 需要携带 st 访问 cas 的 server_validate 服务;
9. cas 接收到 server_validate 的服务请求时， 判断 st 是否存在、是否过期。当符合一切约束要求时，将返回与 st 绑定的 user 相关数据。

在已登录 cas 的 user 执行该规程时，即已经获得尚未过期的 tgt。不需要用户再次输入用户凭证及口令，cas可直接颁发st。
