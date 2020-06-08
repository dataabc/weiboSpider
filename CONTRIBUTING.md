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
本建议是可选的，如果你觉得不合理，可以按自己的方式编写代码。建议每次提交都是代码改动较少的提交，如果新功能需要大量修改代码，除非不得已，否则建议将新功能分成几个小模块，每个模块提交一次。原因是这样更容易管理代码。比如，一个新功能包含几个模块。其中大部分模块都写的很多，但是有一个模块有bug。分模块提交只需要单独处理出问题的模块，其他模块不受影响。
## Python之linter
本项目使用flake8。
## Python之formatter
本项目使用yapf。
## 引号的使用
代码中**建议使用单引号**，只有在特殊情况下使用双引号如类、方法、函数等开头的注释使用6个双引号包括（注释左边三个双引号，右边三个双引号），或者字符串中中已经包含单引号了，则要用双引号包裹。
## 避免过多的模块依赖
除非有必要，尽量少使用非内置的模块，因为会增加用户的安装成本，当然如果该模块能够为本项目或用户带来很多便利，则可以使用。
