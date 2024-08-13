#  一起学Git

# 配置忽略文件

> 问题1：为什么要忽略他们?
> 答:与项目的实际功能无关，不参与服务器上部署运行。把它们忽略掉能够屏蔽IDE 工具之间的差异。
>
> 问题 2：怎么忽略?
> 1)创建忽略规则文件 .xxxxignore(前缀名随便起，建议是 .gitignore)

```text
.gitignore  # 忽略文件，忽略一些不需要上传的文件

.idea       # idea的配置文件，不需要上传
.env        # 环境变量，不需要上传
```

## [为单个仓库配置忽略的文件](https://docs.github.com/zh/get-started/getting-started-with-git/ignoring-files#configuring-ignored-files-for-a-single-repository)

可以在存储库的根目录中创建 `.gitignore` 文件，指示 Git 在提交时要忽略哪些文件和目录。 要与克隆存储库的其他用户共享忽略规则，请将 `.gitignore` 文件提交到存储库。

GitHub 在“github/gitignore”公共存储库中维护建议用于许多常用操作系统、环境及语言的 `.gitignore` 文件的正式列表。 还可以使用 gitignore.io 创建 `.gitignore` 文件，以用于操作系统、编程语言或 IDE。 有关详细信息，请参阅“[github/gitignore](https://github.com/github/gitignore)”和“[gitignore.io](https://www.gitignore.io/)”站点。

1. 打开Git Bash。

2. 导航到 Git 仓库的位置。

3. 为存储库创建 `.gitignore` 文件。

   ```shell
   touch .gitignore
   ```

   如果命令成功，则不会有输出。

有关 `.gitignore` 文件的示例，请参阅 Octocat 存储库中的“[一些常见 .gitignore 配置](https://gist.github.com/octocat/9257657)”。

如果想要忽略已检入的文件，则必须在添加忽略该文件的规则之前取消跟踪它。 从终端取消跟踪文件。

```shell
git rm --cached FILENAME
```

## [为计算机上的所有存储库配置忽略的文件](https://docs.github.com/zh/get-started/getting-started-with-git/ignoring-files#configuring-ignored-files-for-all-repositories-on-your-computer)

在计算机上的任何 Git 存储库中提交时，可以指示 Git 始终忽略特定文件或目录。 例如，可以使用此功能忽略文本编辑器创建的任何临时备份文件。

要始终忽略特定文件或目录，请将其添加到目录 `~/.config/git` 中名为 `ignore` 的文件。 默认情况下，Git 会忽略全局配置文件 `~/.config/git/ignore` 中列出的任何文件和目录。 如果 `git` 目录和 `ignore` 文件尚不存在，可能需要创建它们。

## [排除本地文件而不创建 .gitignore 文件](https://docs.github.com/zh/get-started/getting-started-with-git/ignoring-files#excluding-local-files-without-creating-a-gitignore-file)

如果不想创建与其他人共享的 `.gitignore` 文件，可以创建不随存储库提交的规则。 您可以对不希望其他用户生成的本地生成文件使用此方法，例如编辑者创建的文件。

使用偏好的文本编辑器打开 Git 存储库根目录中名为 `.git/info/exclude` 的文件。 您在此处添加的任何规则都不会检入，并且只会对您的本地仓库忽略文件。

1. 打开Git Bash。
2. 导航到 Git 仓库的位置。
3. 使用偏好的文本编辑器打开文件 `.git/info/exclude`。

# IDEA

## IDEA集成Git
settings -> Version Control -> Git -> Git executable -> your_path\Program Files\Git\bin\git.exe -> OK

点击`test`之后出现 你的git版本号  说明配置成功
![配置Git.png](images%2Fimg_1.png)

## 步骤

1. 如果你是新建的项目，打开IDEA，点击VCS(Version Control) -> Import into Version Control -> Create Git Repository -> OK
   ![git初始化.png](images%2Fimg_2.png)
2. 如果你是已有项目，cd 到项目根目录，执行`git init`
3. 编写好代码之后, 选中整个项目，右键 -> Git -> Add
   ![git_add.png](images%2Fimg_3.png)
4. 同样的位置，右键 -> Git -> Commit。输入commit信息，点击Commit或者点击Commit and Push。如果代码颜色变为正常，说明提交成功
   ![git_commit.png](images%2Fimg_4.png)

   ![git_commit_2.png](images%2Fimg_5.png)
5. 如果点击Commit之后，你可以看到log信息，黄色的是`HEAD`,绿色的是`master`
   ![img_6.png](images%2Fimg_6.png)
6. 如果你想切换版本，选择你想要切换的版本，右键 -> Git -> Checkout Version，可以看到黄色的头指针到你选择的版本，与此同时，你的代码也会切换到这个版本

## 分支管理
- 选择项目，右键 -> Git -> Branches -> New Branch -> 输入分支名（默认切换到新分支） -> OK

  ![img_7.png](images%2Fimg_7.png)
- 如何确定自己当前在哪个分支？查看log信息中，查看黄色的`HEAD`在哪个分支上

  ![img_8.png](images%2Fimg_8.png)
- 解决分支冲突。如果你在另一个分支上`fix-hot`修改了代码，然后切换到`master`分支上，要合并`fix-hot`的修改，需要解决冲突。

  ![img_9.png](images%2Fimg_9.png)
  - 选中项目，右键 -> Git -> Merge -> 选择你想要合并的分支 -> Merge

    ![img_11.png](images%2Fimg_11.png)
  - 或者，在`fix-hot`分支上，右键 -> Merge 'fix-hot' into 'master'
  
    ![img_12.png](images%2Fimg_12.png)

- 分支上代码冲突。master分支和fix-hot分支都修改了同一个文件的同一行代码，解决冲突的方法是：
  
  在log中，右键`fix-hot` -> Merge 'fix-hot' into 'master' -> Merge -> 在出现代码中，留下的代码用`>>`，不留的代码用`X` -> Apply
  ![img_13.png](images%2Fimg_13.png)
  ![img_14.png](images%2Fimg_14.png)
  ![img_15.png](images%2Fimg_15.png)

- 如果Apply之后，代码没有颜色没有变为正常，需要`commit`，然后就变正常了

  ![img_16.png](images%2Fimg_16.png)

## GitHub设置

**现在账号密码登录比较难，需时刻全局科学，因此，本方法只展示设置Token登录**

setting -> Version Control -> GitHub -> 点击 + -> Log into Github Enterprise -> 输入Server:github.com -> 输入Token -> 点击Add Account
![img_17.png](images%2Fimg_17.png)

生成Token的方法：
Github settings -> Developer Settings -> Personal access tokens -> Generate new token -> 勾选repo -> 点击Generate token














