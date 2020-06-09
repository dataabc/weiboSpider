# 为本项目做贡献
本项目使用**Python3**编写，感谢大家对项目的支持，也欢迎大家为开源项目做贡献。鉴于大家拥有不同的技能、经验、认知、时间等，每个人可以根据自身的情况为本项目贡献力量。我们不会因为贡献者写的代码少或者提的建议不好而失去感恩之心，每一个乐于奉献的人都值得并且应该被尊重。所以，如果您觉得自己的代码或建议不好，而不好意思去贡献，这样可能就让本项目失去了一次变得更好的机会。所以，如果您有好的想法、建议，或者发现了bug，欢迎通过issue提出来，这也是一种贡献方式。如果您想要为本项目贡献代码，我们也非常欢迎。最开始您可以通过pull request方式提交代码，如果我们发现您的代码质量非常高，或者非常有想法等，我们会邀请您请成为本项目的协作者（[Collaborator](https://help.github.com/cn/github/setting-up-and-managing-your-github-user-account/permission-levels-for-a-user-account-repository#collaborator-access-on-a-repository-owned-by-a-user-account)），这样您就可以直接向本项目提交代码了。在您贡献代码之前，请先阅读下面的说明，这会让您更好的贡献代码。

## 贡献代码之前
如果要开发新功能或者其它需要大量编写代码的修改，在开发之前最好发Issue说明一下。比如，“我准备开发xx新功能”或者“我想修改xx功能”之类的。因为要开发的功能不一定适合本项目，所以提前说明讨论，判断新功能或修改是否有必要。否则，费时费力写了很多代码，结果最后没有被采纳，可能会做一些无用功。
## Python风格规范（建议Python新手阅读）
参考[Python风格规范](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)
或者[Python风格规范](https://github.com/zh-google-styleguide/zh-google-styleguide/blob/master/google-python-styleguide/python_style_rules.rst)
二者内容是一样的。
## git提交规范
参考[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
或者[Git提交规范](https://zhuanlan.zhihu.com/p/67804026)，commit描述中文英文皆可，只要符合规范就好。
## git提交建议（可选）
本建议是可选的，如果你觉得不合理，可以按自己的方式编写代码。建议每次提交都是代码改动较少的提交，如果新功能需要大量修改代码，建议将新功能分成几个小模块，每个模块提交一次。原因是这样更容易管理代码。比如，一个新功能包含几个模块。其中大部分模块都写的很好，但是有一个模块有bug。分模块提交只需要单独处理出问题的模块，其他模块不受影响。
## Python之linter
本项目使用flake8。
## Python之formatter
本项目使用yapf。
## 引号的使用
代码中**建议使用单引号**，只有在特殊情况下使用双引号，如类、方法、函数等开头的注释使用6个双引号包裹（注释左边三个双引号，右边三个双引号），或者字符串中中已经包含单引号了，则要用双引号包裹。
## 避免过多的模块依赖
除非有必要，尽量少使用非内置的模块，因为会增加用户的安装成本，当然如果该模块能够为本项目或用户带来很多便利，则可以使用。
