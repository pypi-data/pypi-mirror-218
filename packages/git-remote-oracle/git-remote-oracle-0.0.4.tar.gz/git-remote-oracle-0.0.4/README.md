# git-remote-oracle

Source can be found on https://github.com/TheCrazyT/git-remote-oracle.

Can be used in combination with git to view made changes in packages.

It is **NOT** intended to be a full backup of the database structure.

## Requirements
* python 3
* git
* pip-packages:
   * pexpect
   * oracle

## Usage

usage example can be found here:

https://github.com/TheCrazyT/git-remote-oracle/blob/main/tests/google_colab_docker_oracle_xe.ipynb

for example you can do:

```
git clone oracle://127.0.0.1:1521/XEPDB1/JOHN
```

this will ask for credentials and create a folder called JOHN.

But it works only if that scheme exists and you have access to it!

(There is currently no validation, so you won't get a proper error message).

## Environment variables

| Name        | Description |
| ----------- | ----------- |
|GR_ORACLE_DEBUG|Debug informations|
|GR_ORACLE_DEBUG_GIT|Output of all internal output to git itself to the console|
|GR_ORACLE_SYSDBA|Set flag that you run as sys user|