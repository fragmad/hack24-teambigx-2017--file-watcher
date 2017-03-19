#!/bin/bash

mkdir -p ~/tmp/storage/
mkdir -p ~/tmp/storage/user1/foo
mkdir -p ~/tmp/storage/user2/
mkdir -p ~/tmp/storage/files_external

touch ~/tmp/storage/user1/user1_file1
touch ~/tmp/storage/user1/foo/user1_file2
touch ~/tmp/storage/user2/user2_file1
touch ~/tmp/storage/files_external/evil_file
