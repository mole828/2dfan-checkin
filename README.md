# 2dfan 自动签到

基于 git action 的自动签到

目前不可用(旧的签到逻辑有问题)

## usage

### 用户区分

设置 浏览器 "_project_hgc_session" 到仓库的 "SESSIONS" 中

### 人机验证

这里使用了 ez-captcha.com 的 api 作为案例，通过人机验证

使用其他平台的，需要自行完善一个 recaptcha.py 下的 CaptchaInterface

## 补充说明

有能力的话，请支持2dfan的运营，这一项目更多是用来学习尝试的