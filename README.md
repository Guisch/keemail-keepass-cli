# keemail-keepass-cli
Integrate Keemail into Keepass database (.kdbx) in Command line

- [keemail-keepass-cli](#keemail-keepass-cli)
  * [About / Synopsis](#about---synopsis)
  * [Installation](#installation)
      - [Env](#env)
      - [Requirements](#requirements)
  * [Run](#run)

## About / Synopsis

Keemail Keepass CLI is a command line tool that integrate Keemail into a Keepass DB. From command, it allows you to generate an entry for a given URL with a unique URL and 

## Installation

#### Env

You can set environement viariables or pass infos as arguments

| Name            | args               | Description                        |
| --------------- | ------------------ | ---------------------------------- |
| KEEMAILPASS_API | `--api`, `-a`      | URL to Keemail API (with token)    |
| KEEMAILPASS_DB  | `--database`, `-d` | Path to the Keepass db (file.kdbx) |



#### Requirements

Keemail Keepass CLI is tested for Python3. Python 2.7 and lower are not supported. To install required library, please use pip3

```bash
$ pip3 install -r requirements.txt
```



## Run

```bash
$ ./keemail.py --help
= Keemail-pass =
usage: keemail.py [-h] [--group GROUP] [--title TITLE] --url URL
                  [--password PASSWORD] [--api API] [--database DB]

Keemail-pass - Create Keepass entry with Keemail alias

optional arguments:
  -h, --help            show this help message and exit
  --group GROUP, -g GROUP
                        Set entry group (default=root_group)
  --title TITLE, -t TITLE
                        Set entry title (defaul=keemail)
  --url URL, -u URL     Set entry url
  --password PASSWORD, -p PASSWORD
                        Set entry password, random 20 ascii if empty
  --api API, -a API     Keemail API URL (default=None)
  --database DB, -d DB  Keepass database (default=None)
$ ./keemail.py -t "Google" -u "https://google.com" -a "http://keemailserver/api/generate_alias?token=xxx" -d "./db.kdbx"
= Keemail-pass =
Enter Keepass Password:
=Successfully created entry:
 - Email:    gmlrwgltjs@keemailserver
 - Password: 49rtIHBs7FHu6qqK66GU

See ya !
```

