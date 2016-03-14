# regulations-stub

[eRegulations](http://eregs.github.io/) is a web-based tool that makes regulations easier to find, read and understand with features such as inline official interpretations, highlighted defined terms, and a revision comparison view.

eRegs is made up of three core components:

* [regulations-parser](https://github.com/cfpb/regulations-parser): Parse regulations
* [regulations-core](https://github.com/cfpb/regulations-core): Regulations API
* [regulations-site](https://github.com/cfpb/regulations-site): Display the regulations

This repository contains JSON that corresponds to CFPB regulations that
have been parsed by [regulations-parser](https://github.com/cfpb/regulations-parser) 
and which can be loaded into [regulations-core](https://github.com/cfpb/regulations-core)
with the scripts included in this responsitory. This allows a working
eRegulations setup to be created without needing to run the parser. 

To get the rest of the eRegulations stack up and working, please see the 
[regulations-bootstrap](https://github.com/cfpb/regulations-bootstrap)
repository.

## Requirements

Requirements for the [`send_to.py`](send_to.py) script can be satisfied with `pip`:

```shell
$ pip install -r requirements.txt
```

- [Requests](http://docs.python-requests.org/en/latest/) for accessing
  the [regulations-core](https://github.com/cfpb/regulations-core) API
- [boto](https://boto.readthedocs.org/en/latest/) for Amazon S3 support

## Usage

This repository includes a [`send_to.py`](send_to.py) script which can
send  the JSON in the [`stub`](stub) folder to either a running instance 
of [regulations-core](https://github.com/cfpb/regulations-core) or to an
Amazon S3 bucket. It can send either all of the JSON for a particular
regulation or a single JSON file.

`send_to.py` requires one of the following options that specify where
the JSON should be sent:

* `-a`, `--api-base`: The regulations-core API URL, used to 
  [send a regulation to regulations-core](#sending-a-regulation-to-regulations-core)
* `-b`, `--s3-bucket`: An S3 bucket name, used to 
  [send a regulation to S3](#sending-a-regulation-to-s3)

It requires one of the following options that specify what JSON should
be sent:

* `-r`, `--regulation`: The specific regulation part number to upload (eg. 1026).
* `-f`, `--files`: Specific JSON files to upload.

If you want to send JSON that does not live in the same directory as the
`send_to.py` script you can specify that:

* `-s`, `--stub-base`: The base filesystem path for the JSON to be sent (default: ./stub).

### Sending a regulation to regulations-core

To send a particular regulation to a running regulations-core instance,
you can use the `send_to.py` from the root of regulations-stub like so:

```shell
./send_to.py -a http://localhost:7000 -r 1005
```

This will look in the [`stub/`](stub) subfolder of regulations-stub for
all JSON files related to the regulation with part number 1005 (CFPB
Regulation E) and upload them to regulations-core running at
http://localhost:7000.

### Sending a regulation to S3

To send a particular regulation to an Amazon S3 bucket you will need to
create the S3 bucket and then set the environment variables 
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with the appropriate
accesss credentials. Then you can use the `send_to.py` from the root 
of regulations-stub like so:

```shell
./send_to.py -b a-regulations-bucket -r 1005
```

This will look in the [`stub/`](stub) subfolder of regulations-stub for
all JSON files related to the regulation with part number 1005 (CFPB
Regulation E) and upload them to the S3 bucket named
`a-regulations-bucket`.

### Sending specific JSON files

To send a specific JSON file or files, you can use `send_to.py` like so:

```shell
./send_to.py -a http://localhost:7000 -f regulation/1005/2011-31725
```

This will send the file `regulation/1005/2011-31725` in the [`stub/`](stub) 
subfolder of regulations-stub to the regulations-core API running at 
http://localhost:7000.

### Configuring regulations-parser

To write new JSON files to regulations-stub, you'll need to configure
regulations-parser accordingly. This is relatively straight-forward;
modify `API_BASE` and `OUTPUT_DIR` in regulations-parser's 
`local_settings.py` file like so:

```python
API_BASE=""
OUTPUT_DIR="../regulations-stub/stub"
```

With the path to regulations-stub in `OUTPUT_DIR` reflecting its actual
location on the filesystem. `API_BASE` can also be commented-out
entirely by placing a `#` in front of it.

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


