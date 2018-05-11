#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Downloader for tesseract language files."""

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import argparse
import os
import sys

import requests

__author__ = "Zdenko Podobny <zdenop@gmail.com>"
__copyright__ = "Copyright 2018 Zdenko Podobny"
__version__ = "1.0"
__license__ = "Apache license 2"
__date__ = "11/05/2018"

PROJECT_URL = 'https://api.github.com/repos/tesseract-ocr/'
REPOSITORIES = ['tessdata', 'tessdata_fast', 'tessdata_best']


def get_repo_tags(project_url, repository):
    """Get list of tags for repository."""
    tags_url = '{0}{1}/tags'.format(project_url, repository)
    r = requests.get(tags_url)
    tags = dict()
    for item in r.json():
        tags[item['name']] = item['commit']['sha']
    return tags


def get_repository_lof(project_url, repository, tag):
    """Get list of files for repository."""
    if tag == "the_latest":
        tree_url = '{0}{1}/contents'.format(project_url, repository)
    else:
        tag_sha = get_sha_of_tag(repository, tag)
        if not tag_sha:
            print("Unknown tag '{0}' for repository '{1}'".format(
                tag, repository))
            return None
        tree_url = '{0}{1}/git/trees/{2}'.format(project_url, repository,
                                                 tag_sha)
    tree_content = requests.get(tree_url).json()
    if isinstance(tree_content, dict):
        tree = tree_content.get('tree')
    elif isinstance(tree_content, list):
        tree = tree_content
    else:
        print('Unexpected structure {0}'.format(type(tree)))
        return False
    list_of_files = []
    for item in tree:
        list_of_files.append(item['path'])
        # list_of_files.append({item['path']: (item['size'], item['sha'])})
    return list_of_files


def download_file(file_url, filename, file_size, output_dir):
    """Download file."""
    req = requests.get(
        file_url,
        allow_redirects=True,
        stream=True,
        headers={"Accept": "application/vnd.github.v3.raw"})
    content_length = req.headers.get('Content-Length')
    if content_length:
        file_size = int(content_length)
    block_size = 4096
    kb_size = int(file_size / 1024)
    dl = 0
    output = os.path.join(output_dir, filename)
    with open(output, "wb") as file:
        for chunk in req.iter_content(chunk_size=block_size):
            if chunk:
                dl += len(chunk)
                file.write(chunk)
                done = int(20 * dl / file_size)
                sys.stdout.write('\rDownloading {0:21} [{1}{2}] {3}KB'.format(
                    filename, '=' * done, ' ' * (20 - done), kb_size))
                sys.stdout.flush()
    sys.stdout.write('\n')


def list_of_repos():
    """List of know tesseract traineddata repositories."""
    print("Available tesseract traineddata repositories are:")
    for repository in REPOSITORIES:
        print('  "{}"'.format(repository))


def get_list_of_tags():
    """Retrieve tags from know repositories."""
    project_url = PROJECT_URL
    for repository in REPOSITORIES:
        tags = get_repo_tags(project_url, repository)
        if tags:
            print("Following tags were found for repository "
                  '"{0}":'.format(repository))
            for tag in tags:
                print('  "{}"'.format(tag))
        else:
            print('No tag was found for repository "{0}"!'.format(repository))


def get_sha_of_tag(repository, tag):
    """Get sha for tag."""
    sha = None
    tags_url = '{0}{1}/tags'.format(PROJECT_URL, repository)
    r = requests.get(tags_url)
    for item in r.json():
        if item['name'] == tag:
            sha = item['commit']['sha']
    return sha


def display_repo_lof(repository, tag):
    """Retrieving list of files from repository."""
    project_url = PROJECT_URL
    tag_sha = None
    if repository not in REPOSITORIES:
        print("Unknown repository '{0}'".format(repository))
        print()
        list_of_repos()
        return
    tree_content = get_repository_lof(project_url, repository, tag)
    if tree_content:
        print("\nFollowing files were found for repository"
              " '{0}' and tag '{1}':".format(repository, tag))
        for item in tree_content:
            print(item)
    else:
        print('\nNo file was found for repository {0} and {1}!'.format(
            repository, tag_sha))


def get_lang_files(repository, tag, lang, output_dir):
    """Donwload language files from repository based on tag."""
    print('Start of getting information for download of files for '
          '{0}:'.format(lang))
    if tag == "the_latest":
        tree_url = '{0}{1}/contents'.format(PROJECT_URL, repository)
        print("Retrieving the latest file(s) from repository '{0}'"
              .format(repository))
    else:
        tag_sha = get_sha_of_tag(repository, tag)
        if not tag_sha:
            print("Unknown tag '{0}' for repository '{1}'".format(
                tag, repository))
            return None
        print("Retrieving file(s) from repository '{0}', tagged as '{1}'"
              .format(repository, tag))
        tree_url = '{0}{1}/git/trees/{2}'.format(PROJECT_URL, repository,
                                                 tag_sha)
    tree_content = requests.get(tree_url).json()
    if isinstance(tree_content, dict):
        tree = tree_content.get('tree')
    elif isinstance(tree_content, list):
        tree = tree_content
    else:
        print('Unexpected structure {0}'.format(type(tree)))
        return False
    for item in tree:
        code = None
        if '.' in item['path']:
            code = item['path'].split('.')[0]
        if lang == code:
            file_url = item.get('git_url')
            if not file_url:
                file_url = item.get('download_url')
            if not file_url:
                file_url = item.get('url')
            download_file(file_url, item['path'], item['size'], output_dir)


def main():
    """Main loop."""
    desc = "Tesseract traineddata downloader {}".format(__version__)
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-v", "--version", action='store_true', help="Print version info")
    parser.add_argument(
        "-o",
        "--output_dir",
        default=None,
        help="""Directory to store downloaded file.\n
                Default: TESSDATA_PREFIX environment variable if set,
                otherwise current directory""")
    parser.add_argument(
        "-r",
        "--repository",
        type=str,
        choices=REPOSITORIES,
        default="tessdata_best",
        help="Specify repository for download.\nDefault: 'tessdata_best'")
    parser.add_argument(
        "-lr",
        "--list_repos",
        action='store_true',
        help="Display list of repositories")
    parser.add_argument(
        "-t",
        "--tag",
        type=str,
        default="the_latest",
        help="Specify repository tag for download.\n"
        "Default: 'the_latest' (e.g. the latest commit)")
    parser.add_argument(
        "-lt",
        "--list_tags",
        action='store_true',
        help="Display list of tag for know repositories")
    parser.add_argument(
        "-lof",
        "--list_of_files",
        action='store_true',
        help="Display list of files for specified repository and tag "
        "(e.g. argument -r and -t must be used with this argument)")
    parser.add_argument(
        "-l", "--lang", help="Language or data code of traineddata.")
    args = parser.parse_args()

    if args.version:
        print(desc, __date__)
        print()
        print("Author:", __author__)
        print("Copyright:", __copyright__)
        print("License:", __license__)
        return
    if not args.output_dir and 'TESSDATA_PREFIX' in os.environ:
        args.output_dir = os.environ['TESSDATA_PREFIX']
    elif not args.output_dir:
        args.output_dir = "."
    if args.list_repos:
        list_of_repos()
    if args.list_tags:
        get_list_of_tags()
    if args.list_of_files:
        display_repo_lof(args.repository, args.tag)
    if args.lang:
        get_lang_files(args.repository, args.tag, args.lang, args.output_dir)
    # show help if no arguments provided
    if not len(sys.argv) > 1:
        parser.print_help()


if __name__ == '__main__':
    main()