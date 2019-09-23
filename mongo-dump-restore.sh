#!/usr/bin/env bash
# Create By Jenner.luo

get-docker-id(){
    local docker_name=$1
    echo $(docker ps --filter name=$docker_name -q)
}
docker-exec-cmd(){
    local container_id=$1
    local cmd=$2
    docker exec $container_id bash -c "$cmd"
}
mongo-dump-cmd(){
    local table_name=$1
    local gzip_name=$2
    local query=${3:-}
    local db_name=dbName    
    local host=192.168.1.1
    local port=27017    
    local cmd_prifix="mongodump --host $host --port $port --db $db_name --collection $table_name --gzip --archive=$gzip_name"
    if [ ! $query == "" ];then
        echo "$cmd_prifix --query='$query' "
    else
        echo "$cmd_prifix"
    fi
}
mongo-restore-cmd(){
    local table_name=$1
    local gzip_name=$2
    local db_name=dbName  
    local port=27017    
    local user=dbUser
    local password=dbpaswrd
    echo "mongorestore --port 27017 -u $user -p $password --db $db_name --numInsertionWorkersPerCollection=3  --gzip --archive=$gzip_name"
}
mongo-dump-restore(){
    local table_name=$1
    local gzip_name=/data/mongodb/$table_name-$(date +%F%Z%T).gzip
    local query=${2:-}
    docker-exec-cmd "$(get-docker-id 'mongodb_mongos*')" "$(mongo-dump-cmd $table_name $gzip_name $query)"
    if [ $? == 0 ];then
        docker-exec-cmd "$(get-docker-id 'mongodb_mongos*')" "$(mongo-restore-cmd $table_name $gzip_name)"
    else
        echo "mongodump $table_name error."
    fi    
}
main(){
    # mongo-dump-restore voices "{time:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}"
    # mongo-dump-restore voices 
    # mongo-dump-restore watches "{lastlog:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}"
    # mongo-dump-restore files "{uploadDate:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}"
    # mongo-dump-restore lbs "{time:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}" 
    # mongo-dump-restore status "{time:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}" 
    # mongo-dump-restore steps "{time:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}"     
    # mongo-dump-restore informs "{time:{\$gte:ISODate(\"2019-09-22T06:00:00Z\")}}" 
    echo "Finish main."
}
main
