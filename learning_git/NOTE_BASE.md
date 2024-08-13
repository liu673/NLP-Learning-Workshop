
# 一起学Git

# Git

## 简介

[Git](https://git-scm.com/) 是一个免费的开源分布式版本控制系统，能够有效的从个人开发过渡到团队协作

Git是由Linus Torvalds于2005年创建的，因此Linux的好多相似性语句是可用的！

**版本管理系统：**

| 集中式版本控制工具 | 分布式版本控制工具 |
| ------------------ | ------------------ |
| CVS                | Git                |
| SVN                | Mercurial          |
| VSS                | Bazaar             |
| ...                | ...                |

**优点**

1. 分布式版本控制：每个开发者都可以在本地拥有完整的代码仓库，不必依赖中央服务器
2. 强大的分支管理：创建、合并和切换分支非常快速和高效，这为团队的协同开发和并行工作提供了便利。
3. 本地化操作：Git的所有操作都是本地化的，无需联网即可进行版本控制操作。这使得Git的速度非常快，开发者可以快速地提交、切换分支和查看历史记录
4. 数据集完整性：Git中的所有数据都以SHA-1哈希值存储，这意味着每个文件和版本都有唯一的标识，并保证数据的完整性和安全性。
5. 多种工作流支持：Git适用于多种开发工作流程，可以根据团队的需求和开发模式来选择合适的工作流。


![Git工作流程.png](images%2Fimg.png)

## Git 常用命令

| 命令名称                                | 作用                                                  |
| --------------------------------------- | ----------------------------------------------------- |
| `git config--global user.name <用户名>` | 设置用户签名                                          |
| `git config --global user.email <邮箱>` | 设置用户签名                                          |
|                                         | windows用户可以在`C:/用户/.gitconfig`查看上面两个设置 |
| `git init`                              | 初始化本地库                                          |
| `git status`                            | 查看本地库状态                                        |
| `git add <文件名>`                      | 添加到暂存区                                          |
| `git rm --cached <文件名>`              | 将添加到暂存区的文件记录删除，本地文件依旧存在        |
| `git commit -m "日志信息" <文件名>`     | 提交到本地库                                          |
| `git reflog`                            | 查看历史记录                                          |
| `git log`                               | 查看详细日志记录                                      |
| `git reset --hard <版本号>`             | 版本穿梭                                              |
|                                         |                                                       |
| `git remote -v`                         | 查看远程仓库信息                                      |
| `git remote add <shortname> <url>`      | 添加一个新的远程 Git 仓库，同时指定一个方便使用的简写 |

> 在文件中查看当前指针（HEAD），可以在`git init`初始化之后产生的`.git/HEAD`文件中查看
> 在文件中查看当前版本号，可以查看`.git/refs/heads/main`
>
> **Git切换版本，底层是移动的HEAD指针**

![Git 常用命令速查表.jpg](https://www.runoob.com/wp-content/uploads/2015/02/011500266295799.jpg)



## Git 分支

在版本控制过程中，同时推进多个任务，为每个任务，我们就可以创建每个任务的单独使用分支意味着程序员可以把自己的工作从开发主线上分离开来，开发自己分支的时候，不会影响主线分支的运行。

对于初学者而言，分支可以简单理解为副本，一个分支就是一个单独的副本。(分支底层其实也是指针的引用)

**优点**

- 同时并行推进多个功能开发，提高开发效率。
- 各个分支在开发过程中，如果某一个分支开发失败，不会对其他分支有任何影响。失败的分支删除重新开始即可。

| 命令名称                | 作用                         |
| ----------------------- | ---------------------------- |
| `git branch <分支名>`   | 创建分支                     |
| `git branch -v`         | 查看分支                     |
| `git checkout <分支名>` | 切换分支                     |
| `git merge <分支名>`    | 把指定的分支合并到当前分支上 |

**Git 合并分支产生冲突**

冲突产生的原因:

- 合并分支时，两个分支在同一个文件的同一个位置有两套完全不同的修改。Git 无法替我们决定使用哪一个。
- 必须人为决定新代码内容。

解决冲突：

- 当你的`master`分支和`fix`分支都对代码进行修改，都进行了`add`、`commit`操作之后，在`master`分支合并`fix`分支时（`git merge fix`），回出现冲突，你的`master`分支变成了`master|MERGING`

- `git status`查看冲突的代码，手动修改冲突的地方，如`vim hello.py`，将代码中`<<<<HEAD`、`=====`、`>>>>FIX`这些都删除，并对两者需要保留的代码进行删除保留

- 执行`git add <文件名>`

- 执行`git commit -m "日志信息"` 

  > 注意，在日志信息之后，不要再加 文件名

- 此时分支将会变成 `master`，说明冲突已经解决了

  > 合并完成之后，代码只修改了 master 上的代码，在另一个分支 fix 上的代码没有修改

## 远程仓库

| 命令名称                                 | 作用                                                     |
| ---------------------------------------- | -------------------------------------------------------- |
| `git remote -v`                          | 查看当前所有远程地址别名                                 |
| `git remote add <别名> <远程地址>`       | 起别名                                                   |
| `git push <远程仓库别名> <本地分支名>`   | 推送本地分支上的内容到远程仓库                           |
| `git clone <远程地址/别名>`              | 将远程仓库的内容克隆到本地                               |
| `git pull <远程库地址别名> <远程分支名>` | 将远程仓库对于分支最新内容拉下来后与当前本地分支直接合并 |
|                                          |                                                          |

>  “origin” 并无特殊含义远程仓库名字 “origin” 与分支名字 “master” 一样，在 Git 中并没有任何特别的含义一样。 同时 “master” 是当你运行 `git init` 时默认的起始分支名字，原因仅仅是它的广泛使用， “origin” 是当你运行 `git clone` 时默认的远程仓库名字。 如果你运行 `git clone -o booyah`，那么你默认的远程分支名字将会是 `booyah/master`。



# GitHub SSH免密登录

- [GitHub Docs](https://docs.github.com/zh)

- [生成新的 SSH 密钥并将其添加到 ssh-agent - GitHub 文档](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## 生成SSH公钥

默认情况下，用户的 SSH 密钥存储在其 `~/.ssh` 目录下。 进入该目录并列出其中内容，你便可以快速确认自己是否已拥有密钥

需要寻找一对以 `id_dsa` 或 `id_rsa` 命名的文件，其中一个带有 `.pub` 扩展名。 

- `.pub` 文件是你的公钥，另一个则是与之对应的私钥。

-  如果找不到这样的文件（或者根本没有 `.ssh` 目录），你可以通过在`CMD`或者`powershell`运行 `ssh-keygen` 程序来创建它们。
  ```she
  ssh-keygen
  ```

- `ssh-keygen` 会确认密钥的存储位置（默认是 `.ssh/id_rsa`），然后它会要求你输入两次密钥口令。 如果你不想在使用密钥时输入口令，将其留空即可。 然而，如果你使用了密码，那么请确保添加了 `-o` 选项，它会以比默认格式更能抗暴力破解的格式保存私钥。 你也可以用 `ssh-agent` 工具来避免每次都要输入密码。

## 添加公钥到GitHub

- [新增 SSH 密钥到 GitHub 帐户 - GitHub 文档](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?tool=webui)

**步骤：**

1. 在 GitHub 任意页的右上角，单击个人资料照片，然后单击“**设置**”。
2. 在边栏的“访问”部分中，单击 “SSH 和 GPG 密钥”。
3. 单击“新建 SSH 密钥”或“添加 SSH 密钥” 。
4. 在 "Title"（标题）字段中，为新密钥添加描述性标签。 例如，如果使用的是个人笔记本电脑，则可以将此密钥称为“个人笔记本电脑”。
5. 选择密钥类型（身份验证或签名）。 有关提交签名的详细信息，请参阅“[关于提交签名验证](https://docs.github.com/zh/authentication/managing-commit-signature-verification/about-commit-signature-verification)”。
6. 在“密钥”字段中，粘贴公钥。
7. 单击“添加 SSH 密钥”。
8. 如果出现提示，请确认你的帐户是否拥有 GitHub 访问权限。 有关详细信息，请参阅“[Sudo 模式](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/sudo-mode)”。



