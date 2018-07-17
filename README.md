# Pouriya's commit handler
I use this script in coding time to have structured Git commit messages and a nice changelog (history of project changes). This script does two things; commit changes, generate changelog file.


# Commit changes
```sh
$ git init
...
$ touch foo.bar
$ git add foo.bar # don't forget this
$ pcommit -m
Insert commit type ('init', 'fix', 'feat', 'ref', 'test', 'doc', 'build', 'style', 'ci', 'ver'): init
Insert commit main description (between 10-65 characters): add project source code
Insert changed files separated by comma (Enter to skip): foo.bar
Insert commit long description (Enter to skip): I have just added one file because of X and Y
$ # ...
```
As you can see, each commit MUST have a type part which can be one of:  
* **init:** for initial commits.
* **fix:** for fixing bugs.
* **feat:** for adding features.
* **ref:** for refactoring code.
* **test:** for adding, fixing, improving test codes.
* **doc:** for adding or updating documentation.
* **build:** for updating Makefiles, etc for build process.
* **style:** for fixing indentation or line breakings, etc.
* **ci:** for updating CI files, for example `.travis.yml` file.
* **ver:** for versioning.

After type part, each commit has a short description and after that it CAN has a changed file list and also CAN has a long description. This part of scripts makes commit message in form of:  
```txt
<type>: <short description>\n[<files: list, of, changed, files, for, this, commit, separated, with, comma>][<long description>]
```

# Generate changelog
I have 10 commit types, but actually I dont want a changelog for all types. Personally I prefer seeing just `fix`, `feat`, `ref` and `test` commits with its details. If you want more or less, there are some flags for changing output and finally you can simply edit the code for your own changelog.  
Suppose that I have a project with following commits:  
```sh
$ git log --oneline
b98906f init: add files\nFiles: hello_world.c, Makefile, test/test.py\nThis is initial commit of project
69ffd51 fix: api function foo(bar, baz)\nFiles: hello_world.c\nBug X was generated because Y and fixed
6698b7a ver: 0.10.2
7789086 doc: improve\n New functions usage has been documented well using markdown in code
17fa611 build: change gcc flags\nFiles: Makefile\nAdded -O2 and -pipe
12434ab ref: use new X library API 
28006e4 style: fix indentation 
67b57af ver: 1.0.0
3be3d51 feat: CI using travis service
fed846b ci: add redis server
0d122a4 ci: add code coverage
ca38cea style: fix line breaking
f851753 ref: improve speed\nfiles: hello_world.c\nSupport threading using pthread library
484b053 ver: 2.0.0
```
and I want to generate a changelog. Just run:  
```sh
$ pcommit -c
```
and I have new file named `CHANGELOG.md`.  
```sh
$ cat CHANGELOG.md
### 0.10.2
* **Fix(es):**
    * api function foo(bar, baz)  
        >Bug X was generated because Y and fixed  
...
    * improve speed  
        >Support threading using pthread library  

        Files changed: hello_world.c  

Generated at 2018-07-18 00:00
```
It's nice Markdown file. I copied the output bellow.  

# Changelog output example
### 0.10.2
* **Fix(es):**
    * api function foo(bar, baz)  
        >Bug X was generated because Y and fixed  

        Files changed: hello_world.c  
### 1.0.0
* **Refactor(s):**
    * use new X library API  
### 2.0.0
* **Feature(s):**
    * CI using travis service  
* **Refactor(s):**
    * improve speed  
        >Support threading using pthread library  

        Files changed: hello_world.c  

Generated at 2018-07-18 00:00

# Notes
You can use `-s` or `--since` to generating changelog only after specified version.  
If you have a repository with lots of different commit messages and want to use this script for next commits, don't worry. By default it skip unknown commit messages. If you want to stop on unknown commit message, use `--no-unknown-commits`.  
If you want to generate changelog in other formats for example HTML page, This script is your friend, Just edit `MarkdownChangeLogGenerator` class.  

# Install on a *nix OS
Assuming that python 2 or 3 is installed.  
```sh
$ chmod a+x pcommit.py
$ sudo ln -s $PWD/pcommit.py /usr/local/bin/pcommit
```
