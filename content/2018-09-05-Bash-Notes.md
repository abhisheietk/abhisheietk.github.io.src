Title: Bash-Notes
Date: 2018-09-05
Category: notes
Tags: bash
Slug: 
Authors: Abhishek Bajpai
Summary: Notes on BASH

# Yum via socks5 proxy

## Creating socks5 proxy

To start such a connection, run the following command in your terminal.

```bash
$ ssh -D 1337 -q -C -N user@server.com
```
Add this line to /etc/yum.conf

```bash
proxy=socks5://ip:port
```

In case host name resolution through proxy is required.

```bash
proxy=socks5h://ip:port
```


