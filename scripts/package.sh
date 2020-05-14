#!/bin/bash


project=""
module=""
scheme=""
version=""
target=""
save=""
dependence=""


function Usage(){
    echo "Usage:"
    echo "package.sh [-p <project>] [-m <module>] [-e <scheme>] [-v <version>] [-t <target>] [-s <save_path>] [-c <dependence>]"
    exit -1
}


if [ $# -eq 0 ]; then
    Usage
fi


while getopts p:m:e:v:t:s:c: opt
do
  case "$opt" in
  p)
    if [ -z $OPTARG ];then
        Usage
    fi
    project=$OPTARG
    ;;
  m)
    if [ -z $OPTARG ];then
        Usage
    fi
    module=$OPTARG
    ;;
  e)
    if [ -z $OPTARG ];then
        Usage
    fi
    scheme=$OPTARG
    ;;
  v)
    if [ -z $OPTARG ];then
        Usage
    fi
    version=$OPTARG
    ;;
  t)
    if [ -z $OPTARG ];then
        Usage
    fi
    target=$OPTARG
    ;;
  s)
    if [ -z $OPTARG ];then
        Usage
    fi
    save=$OPTARG
    ;;
  c)
    if [ -z $OPTARG ];then
        Usage
    fi
    dependence=$OPTARG
    ;;
  *) 
    echo "Unknown option: $opt"
    ;;
  esac
done


function commit()
{
    
    local commit_msg=`git log --oneline | head -n 1`
    echo "Git最新一条提交记录: $commit_msg"
}

function compile()
{
    
    local update=""

    if [ "$dependence" == "yes" ];then
        update="-U"
    fi
    
    if [ "$module" != "no-module" ];then
        cmd="mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true -pl $module -am -P $scheme -Dprofile=$scheme"
        echo "编译命令: $cmd"
        mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true -pl $module -am -P $scheme -Dprofile=$scheme
    else
        cmd="mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true  -P $scheme -Dprofile=$scheme"
        echo "编译命令: $cmd"
        mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true  -P $scheme -Dprofile=$scheme
    fi

}


function main()
{
    start_time=`date +%s`
    commit
    compile
    end_time=`date +%s`
    echo "执行时间花费: $((end_time-start_time)) s"
    echo "LogEnd"
    exit 0
}

main

