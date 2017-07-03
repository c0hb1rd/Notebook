# 目录
* [环境配置](#环境配置)
* [创建本地仓库](#创建本地仓库)

# 环境配置
* 安装
```bash
$ sudo apt install git -y
```

* 配置用户名和邮箱
```bash
### 如果只想当前环境下生效，可以把--global参数去掉
$ git config --global user.name "你的姓名"        #配置全局用户名
$ git config --global user.email "你的邮箱"       #配置全局邮箱
```

# 创建仓库
* 实验流程
  * 在 [Github](/https://github.com) 上注册用户
  * 把本地的 `SSH` 公钥关联到用户下
  * 创建一个空的仓库，仓库名自拟
  * 在任意路径下，用 `git init` 初始化一个本地仓库
  * 创建一个 `README.md` 文件作为这个仓库的描述文件，一开始可以只写项目名等作为一个简单的介绍就可以
  * 用 `git add <path>` 命令将指定文件添加到索引库中
  * 用 `git commit -m 'your note'` 命令为这一次或者批次的改动做批注
  * 最后就是推送本地仓库中的更新到远程仓库里做同步
* 具体操作
```bash
$ mkdir "项目文件夹"                        #创建项目文件夹
$ cd "项目文件夹"                           #切换目录到项目文件夹下
$ git init                                #初始化本地仓库
$ echo '# 项目名称' > README.md             #创建项目描述文件
$ git add README.md                       #添加
$ git commit -m "这一次或这一批次的操作批注"   #添加改动批注
$ git push origin master                  #同步的远程仓库的主分支
```

版本查看：git status查有无change，git diff查change的content
git status：查看当前git repository的当前status，可以再指令之间自由穿插来看看what happens和which steps
git diff <fileName>：查看某文件的difference，也就是所做的改动有什么，可以在commit前来一发，确保做了什么change再commit

版本回退相关：git log查看日志返回对应的版本commit_id，git reset commit_id回退到id指向的版本,git reflog可以看到未来的版本
git log：无参时返回内容比较detail，粗略查看可以加--pretty=oneline
git reset：在git中，HEAD表示current version，对应的上一个version则是HEAD^，再上一个则是HEAD^，再退的话，用HEAD~numbers来指定退到numbers执行的那个版本，用法git reset --hard HEAD^ / git reset --hard HEAD~12，也可以通过接log返回的commit_id来回退，用法git reset --hard commit_id
git relog：log无法显示回退的那个version之前的log，这时就要用reflog来查看commit_id，并回退到所要的版本

工作区：就是目录
版本库：init的那个目录，也就是有隐藏的.git文件那个目录，就是版本库
暂存区：可以理解为buffer area，add指令就是把工作区的内容add到暂存区，再用commit把内容提交到版本库的某个分支上，在创建版本库时会defaule一个master分支，所以content就被add到这个default branch上

管理修改：git管理的是修改而不是文件，可以理解为以文件修改的内容为基准来查看区别
查看区别命令：git diff HEAD -- fileNAme，可以查看当前文件与库中文件的区别
git reset HEAD fileName：撤销暂存区中文件修改，使之与库中文件相同
git checkout -- fileNAme：撤销工作区中文件修改，使之与上一次提交前内容一致
ps：前提条件是没有commit，如果commit。。。do not ask me how to save urself~_~

删除文件：rm是删除文件，但是库中如果有文件，那么可以用git checkout -- fileName撤销删除，而要永远删除库中的文件，则用git rm
git rm fileName：删除库中文件
git checkout -- fileName：撤销用rm删除的文件，但是无法撤销git rm指令删除的文件，因为本质上是从库中的当前版本拉回来，而不是完全撤销，因此一切改动已库中file为基准

连接GitHub：首先linux很方便，利用远程登录协议，也就是ssh
step如下：
1.设置邮箱：ssh-keygen -t rsa -C "your email"
2.接下来是一些设置，还有密码设置什么的，我也没仔细看
3.成功后会在user根目录下创建.ssh目录，里面有公钥和私钥
4.上GitHub->Setting->SSH Keys->add key：title随便填，key里面把公钥的内容复制进去，然后提交，输入Github的帐号密码，ok

关联远程库：首先在GitHub上Create一个repository，输入名字后提交，会返回对应的ssh地址，在本地的git库目录下，用remote指令关联，再用push推送到Github上

关联本地库与github库：在本地库下用指令git remote add origin ssh_address
格式: git remote add origin git@github.com:githubUserName/repositoryName.git
ps：第一次使用会提示验证Key指纹信息，输入yes就ok，以后不会出现

推送本地库到github库：在本地库下用指令git push -u origin master
格式：git push -u origin branchName(default is master)
ps：第一次使用推送时加上-u参数，可以关联并推送本地的branch与远程库的branch，下一次使用push就不需要加-u，会默认推送到上一次使用-u关联的branch

克隆库：从github把库拉到本地，用clone命令
格式：git clone ssh_address
比如：git clone git@github.com:userName/path.git
ps：clone支持https和ssh协议，但是https速度慢，所以使用ssh，当然有的公司内部只开了https端口，就只能使用https_address来把库拉到本地

文件管理：
添加文件到暂存区：git add <fileName>
将所有待提交文件文件提交的库中：git commit -m "blablabla"
同步本地库与远程库中的文件：git push <repositoryName> <branchName>
同时删除本地文件与库中文件：git rm <fileName>，git commit -m "blablabla"
删除库中文件不删除本地文件：git rm --cached <fileName>，git commit -m "blablabla"

分支管理：Git把每一次提交都把它们串成一条时间线，这条时间线就是一个分支，在git分支里，master叫主分支
查看分支：git branch
创建分支：git branch <name>
删除分支：git branch -d <name>
切换分支：git checkout <name>
创建+切换分支：git checkout -b <name>
合并某分支到当前分支：git merge <name>
强行删除没合并的分支：git branch -D <name>

多分支管理策略：团队合作时，各自create一个分支工作用，把master独立开来单独作为同步更新项目用，在工作分支做好相应的工作后与master merge后提交就ok

Bug分支：bug分支专门用来调bug，临时建立，bug修复后再合并，简直方便nice，再切到bug分支前，用stash记录下当前工作的status，修复完bug回来工作时可以再stash恢复工作的status
command：
git stash    //记录工作区
git stash apply    //恢复工作区但不删除记录
git stash drop    //删除记录
git stash pop    //恢复工作区并删除记录

多人协作：当从远程库clone库时，会自动把本地的master与github中的master对应，并且默认远程库名字是origin，可以用remote查看远程库信息
查看：git remote
detail查看：git remote -v
ps：默认情况下clone的库的branch只有master，要在本地对应dev可以用command：git checkout -b dev origin/dev

提交冲突：当最新提交和推送的提交有冲突时，用pull抓取最新提交，在本地很并之，再推送就可以解决
step：
git pull
git push repositoryName branchNAme
ps：推送错误根据pull提示一步一步整就行，上面只是一个小例子，还有建立local branch与远程branch关联，command：git branch --set-upstream branchName origin/branchName

标签管理：发布版本时，可以在版本库中打一个标签，例如，v1.0，这样在将来想调用版本库的某个历史版本，直接选择标签就可以
创建标签：git tag <name>
为某个版本打标签：git tag <name> commit_id
查看现已有标签：git tag
查看标签信息：git show <tagName>
创建带有说明的标签：git tag -a <tagName> -m "hint text"
用私钥绑定标签：git -s <tagName> -m "blablabla"

标签操作：
推送标签：git push origin <tagName>
推送所有未推送的标签：git push origin --tags
删除一个本地标签：git tag -d <tagName>
删除远程库标签：git push origin :refs/tags/<tagName>

Github上的开源项目，想参与的话先fork到自己的库中，然后clone到本地并关联，然后do anything what u wanna do，然后pull request，如果审核过的话就会合并你的那部分

自定义git：例如git config --global color.ui true，ui显色
-------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------配置有很多，占坑，有时间再补充0.0----------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------

忽略特殊文件：在.gitgnore文件中可以定义要忽略的文件，就是无视掉的文件，比如*.pyc，*.pyo，*.obj，*.class等一些编译过程生成的文件，没必要提交到远程库中的文件，就可以在.gitnore中配置忽略之

配置命令别名：用alias可以为指令配置别名，类似C中的macro，还可以把某部分组合指令缩减成一个别名
查看别名：git alias list，git config --get-regexp alias
指令别名：git config --global alias.newCommandName <SourceCommandName>
组合指令别名：git config --global alias.<newCommandName> <'combinCommandiName'>
取消别名：git config --global --unset alias.<commandName>

搭建自己的Github服务器：
step(root)：
1、安装git：apt-get install git
2、创建git用户来运行服务：adduser git    
3、收集公钥，放到/home/git/.ssh/authorized_keys文件里，一行一个
4、选定目录为Git仓库：在选定的库目录下敲git init --bare sample.git
5、把owner改为git：chown -R git:git sample.git
6、禁用shell登录：安全起见，创建git的用户不允许登录shell，通过编辑/etc/passwd文件，找到这样的一行：git:x:1001:1001:,,,:/home/git:/bin/bash，改为：git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
7、clone库的地址为：git@server:<repositoryPath>sample.git

That's all.
