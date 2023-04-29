FROM ghcr.io/avinal/lark:latest

# Add files to docker
ADD main.py entrypoint.sh colors.json /

# run final script
CMD python3 /main.py && /entrypoint.sh