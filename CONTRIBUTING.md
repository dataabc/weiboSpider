## Python风格规范（建议Python新手阅读）
参考[Python风格规范](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)
或者[Python风格规范](https://github.com/zh-google-styleguide/zh-google-styleguide/blob/master/google-python-styleguide/python_style_rules.rst)
二者内容是一样的。
## git提交规范
参考[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
或者[Git提交规范](https://zhuanlan.zhihu.com/p/67804026)，commit描述中文英文皆可，只要符号规范就好。
## Python之linter
本项目使用flake8。
## Python之formatter
本项目使用yapf。
## 引号的使用
代码中**建议使用单引号**，只有在特殊情况下使用双引号如类、方法、函数等开头的注释使用6个双引号包括（注释左边三个双引号，右边三个双引号），或者字符串中中已经包含单引号了，则要用双引号包裹。
## 避免过多的模块依赖
除非有必要，尽量少使用非内置的模块，因为会增加用户的安装成本，当然如果该模块能够为本项目或用户带来很多便利，则可以使用。
