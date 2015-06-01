#!/usr/bin/env python
from __future__ import print_function

import requests
import sys
import os
import argparse
import json
import urlparse
import logging
import boto

logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def find_regulation_files(stub_base, regulation):
    """
    Find all JSON files in the `stub_base` belonging to the given
    `regulation`. Returns a list of paths relative to stub_base.
    """

    # regulations-parser outputs JSON files in the following directory
    # structure:
    #   regulation/
    #       [regulation part number]/
    #           [notice number]
    #           ...
    #   notice/
    #       [notice number]
    #       ...
    #   layer/
    #       [layer name]/
    #           [regulation part number]/
    #               [notice number]
    #               ...
    #   diff/
    #       [regulation part number]/
    #           [notice number]/
    #               [notice number]
    #               ...
    # 

    regulation_files = []
    notice_names = None

    # Get the regulation/ JSON and notice numbers
    logger.info("getting files for regulation {}...".format(regulation))
    regulation_base = os.path.join(stub_base, 'regulation', regulation)
    if not os.path.isdir(regulation_base):
        logger.error("Can't find regulation JSON for {} at {}".format(regulation, regulation_base))
        return []
    for dirname, subdirs, files in os.walk(regulation_base):
        notice_names = files
        regulation_files.extend([os.path.join(dirname, f) for f in files])

    # Get notice JSON
    logger.info("getting notice files for regulation {}...".format(regulation))
    for dirname, subdirs, files in os.walk(os.path.join(stub_base, 'notice')):
        # Notices are not stored in a regulation-part-number
        # subdirectory. Use notice_names, from above, to just grab the
        # ones we want.
        notice_files = [os.path.join(dirname, f) for f in files if f in notice_names]
        regulation_files.extend(notice_files)

    # Get layer JSON
    logger.info("getting layer files for regulation {}...".format(regulation))
    for dirname, subdirs, files in os.walk(os.path.join(stub_base, 'layer')):
        # For layers, dig into each subdirectory of the layer path until
        # we find one with our regulation part number.
        if dirname.endswith(regulation):
            layer_files = [os.path.join(dirname, f) for f in files if f in notice_names]
            regulation_files.extend(layer_files)

    # Get diff JSON
    logger.info("getting diff files for regulation {}...".format(regulation))
    for dirname, subdirs, files in os.walk(os.path.join(stub_base, 'diff', regulation)):
        # For diffs, each regulation directory has a notice directory
        # with json files corrosponding to each other notice. 
        diff_files = [os.path.join(dirname, f) for f in files]
        regulation_files.extend(diff_files)

    return regulation_files


def send_to_s3(bucket, stub_base, path):
    """
    Send the JSON at the given `path` to the given Amazon S3 `bucket`.
    Path components will be appended to the bucket and will match the
    path beneith `stub_base`.
    """
    relative_path = os.path.relpath(path, stub_base)
    logger.info('sending {} to s3://{}/{}'.format(path, bucket.name, relative_path))

    data = json.dumps(json.load(open(path, 'r')))

    try:
        k = boto.s3.key.Key(bucket)
        k.key = relative_path
        k.set_contents_from_string(data)
    except boto.exception.S3ResponseError as e:
        logger.error("error sending", exc_info=True)


def send_to_server(api_base, stub_base, path):
    """
    Send the file at the given `path` to the given `api_base`. Path
    components will be appended to the `api_base` and are presumed to
    match.
    """
    relative_path = os.path.relpath(path, stub_base)
    url = urlparse.urljoin(api_base, relative_path)

    logger.info('sending {} to {}'.format(path, url))

    data = json.dumps(json.load(open(path, 'r')))
    r = requests.post(url, data=data,
                      headers={'content-type': 'application/json'})

    # regulations-core returns 204 on a successful POST
    if r.status_code != 204:
        logger.error("error sending {}: {}".format(r.status_code, r.reason))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # We can either send to the regulations-core API 
    parser.add_argument('-a', '--api-base', action='store',
            help='the regulations-core API URL')
    # Or to an Amazon S3 bucket
    parser.add_argument('-b', '--s3-bucket', action='store',
            help='an S3 bucket name')

    # We need to know where the JSON is coming from
    parser.add_argument('-s', '--stub-base', action='store',
            default=os.path.join(os.getcwd(), 'stub'), 
            help='the base filesystem path for regulations JSON (default: ./stub)')

    # We need to know what we're uploading, either a whole regulation's
    # worth of JSON or a specific file or files
    parser.add_argument('-r', '--regulation', nargs='?', action='store',
            help='the specific regulation part number to upload (eg: 1026)')
    parser.add_argument('-f', '--files', nargs='*', action='store',
            default=[], help='specific JSON files to upload')

    args = parser.parse_args()

    # We need a destination
    if args.api_base is None and args.s3_bucket is None:
        logger.error("ERROR: either -a api_base or -b s3_bucket is required.")
        parser.print_help()
        sys.exit(1)

    if args.regulation is not None:
        # If we're going to upload all the JSON for a single regulation, 
        # we need to fetch those files.
        args.files = find_regulation_files(args.stub_base, args.regulation)

    elif len(args.files) > 0:
        # We need to get the path to the files relative to stub_base
        args.files = [os.path.join(args.stub_base, f) for f in args.files]

    else:
        logger.error("no file or regulation to upload. Use -r or -f to specify.")
        parser.print_help()
        sys.exit(1)

    if args.api_base is not None:
        [send_to_server(args.api_base, args.stub_base, f) 
                for f in args.files]
    elif args.s3_bucket is not None:
        # Set up our S3 connection and get the bucket
        try:
            conn = boto.connect_s3()
            bucket = conn.get_bucket(args.s3_bucket)
        except boto.exception.S3ResponseError as e:
            logger.error("error connecting", exc_info=True)
            sys.exit(1)

        [send_to_s3(bucket, args.stub_base, f)
                for f in args.files]

 
