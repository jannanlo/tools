#!/bin/bash
#Create By lzn

docker-image-grep(){
   local grep_str=${1:=""}
  docker images|grep $grep_str|awk '{print $1":"$2}'
}

docker-rmi-grep(){
   local grep_str=${1:=""}
  docker rmi $(docker images|grep $grep_str|awk '{print $1":"$2}')
}
