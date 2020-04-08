#!/bin/bash
# Create By lzn

function  goCmd()
{
  local gopath_src=$GOPATH/src
  local current_dir=$(pwd)
  docker run -it --rm --network host -e "CGO_ENABLED=0" -e "GOOS=linux" -v $gopath_src:/go/src  -v $(pwd):$(pwd) --workdir /go/src${current_dir#*src}  golang:alpine sh -c "go  $* "
}

if [ ! -n "$GOPATH" ];then
  echo "GOPATH does not exist!"
  exit 1
else
  goCmd $*
fi
