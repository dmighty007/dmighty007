# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Avinal Kumar <avinal.xlvii@gmail.com>
#
# Distributed under the terms of MIT License
# The full license is in the file LICENSE, distributed with this software.

FROM python:3.11-alpine

# Add files to docker
ADD main.py entrypoint.sh colors.json /

# run final script
CMD python3 /main.py && /entrypoint.sh
