# diz

目前开源的大模型项目普遍来说都有如下问题：
1. 安装环境复杂，需要安装大量依赖包，而且依赖包版本之间有冲突，导致安装失败
2. 模型往往存放在 huggeface 上，下载速度慢，且不符合国情，使用 git lfs 也不方便

本项目重点解决上述 2 个问题，提供一个简单的模型下载和使用的框架，方便大家快速使用。
总结一句话来说就是：目标就是干出一个大模型的 homebrew。

## 安装

```bash
pip install diz
```

系统依赖：
1. tmux
2. git
3. git lfs

## 使用

```bash
diz setup
```
根据提示输入你要安装的目录和模型的 url
当前支持的模型有：
- ChatGLM2-6B: https://gist.githubusercontent.com/mjason/a616dcb8f9fd09fb2c7fb18ff3bb6279/raw/bb530a7d4101edf8aa474883d1f54a6aef58bc44/chatglm2-6b.yml

也可以一句话安装：
```bash
diz setup --path /root/autodl-tmp/chatglm2 --pkg https://gist.githubusercontent.com/mjason/a616dcb8f9fd09fb2c7fb18ff3bb6279/raw/bb530a7d4101edf8aa474883d1f54a6aef58bc44/chatglm2-6b.yml
```

```bash
diz install ChatGLM2-6B --path /root/autodl-tmp/chatglm2
```
即可完成安装，安装完成后会自动进入虚拟环境，可以直接使用。

- diz shell 进入虚拟环境
- diz shell --mode o 退出虚拟环境，环境进入后台
- diz shell --mode k 退出虚拟环境，环境进入后台，且 kill 掉原来的进程

```bash

## 路线图
- [x] 提供 install 命令，统一安装源
- [x] 提供 venv 指令，快速进入对应的虚拟环境
- [ ] 提供 generate 命令，根据生成本地模型调用代码