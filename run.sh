#!/usr/bin/env bash
#
# run.sh
# Copyright (C) 2019 LeonTao
#
# Distributed under terms of the MIT license.
#


mkdir -p data/
mkdir -p data_raw/

scrapy list
scrapy crawl guahao
