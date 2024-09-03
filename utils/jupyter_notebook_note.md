
# Jupyter Notebook Note

在 Pycharm 专业版中使用 jupyter notebook

1. 按照正常的创建项目环境的步骤创建一个项目，选择你想要的环境
2. 在Terminal中输入以下命令，启动`jupyter notebook`
    ```shell
   jupyter notebook
   # jupyter notebook --no-browser
   ```
   以上命令会在浏览器中打开一个jupyter notebook的页面，选择一个文件夹，即可在浏览器中打开一个jupyter notebook的页面
3. 复制执行命令时，复制 `copy and paste one of these URLs:`下的链接其中一个
4. 在Pycharm中，选择`Settings`->`Languages & Frameworks`->`Jupyter`->`Jupyter server`->`Configured server`，输入刚刚复制的链接，并点击`Apply`
5. jupyter notebook项目配置密码：
    ```shell
   jupyter notebook --generate-config 
   # 打开生成的文件 ~/.jupyter/jupyter_notebook_config.py
   ```
6. 配置密码
   ```python
   # 关闭上面打开的jupyter notebook (ctr c + ctr c)
   # 打开python，执行下面的代码，并输入密码
   # 进入Python解释器
   
    from notebook.auth import passwd
    passwd()
   # 输入两次密码之后，会得到一个加密后的密码，复制下来
   ```
   找到并修改c.NotebookApp.password = ''，将加密后的密码粘贴进去
7. jupyter notebook 项目使用本地的Python环境，由于本地使用的是conda 环境，所以在terminal中执行以下命令
   ```shell
   python -m ipykernel install --user --name=myenv
   ```
   配置完成后，重启jupyter notebook
8. 然后就可以在pycharm中的jupyter notebook中使用本地环境了
   
   

















