#!/bin/bash


source /etc/profile

if [ $# != 2 ];then
    echo "Args is not enough. Now args is $#"
    echo "LogEnd"
    exit -1
fi

PROJECT_NAME=$1
PKG_MODULE=$2
PKG_ENV=$3
PKG_TAG=$4
TARGET_NAME=$5
SAVE_PATH=$6
IS_OR_DEPENDENT=$7


function echo_commit_msg()
{
    
    local commit_msg=`git log --oneline | head -n 1`
    echo "Git最新一条提交记录: $commit_msg"
}

function compile_project()
{
    
    local update=""
    
    if [ "$IS_OR_DEPENDENT" == "yes" ];then
        update="-U"
    fi
    
    if [ "$PKG_MODULE" != "None" ];then
        cmd="mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true -pl $PKG_MODULE -am -P $PKG_ENV -Dprofile=$PKG_ENV"
        echo "编译命令: $cmd"
        mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true -pl $PKG_MODULE -am -P $PKG_ENV -Dprofile=$PKG_ENV
    else
        cmd="mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true  -P $PKG_ENV -Dprofile=$PKG_ENV"
        echo "编译命令: $cmd"
        mvn clean package $update -Dmaven.test.skip=true -Dmaven.compile.fork=true  -P $PKG_ENV -Dprofile=$PKG_ENV
    fi
    
    if [ $? -ne 0 ];then
        echo "编译结束,编译命令执行失败!"
        echo "LogEnd"
        exit -1
    fi
    echo "编译结束,编译命令执行成功!"
    
}


function copy_to_save_path()
{
    # copy_to_save_path $src_filename $PROJECT_NAME $ptype

    if [ "$PKG_ENV" == "online" ]; then
        if [ "$3" == "zip" ]; then
            scp $1 ${SAVE_PATH}/${2}_${PKG_MODULE}.zip-${PKG_TAG}
        else
            scp $1 ${SAVE_PATH}/${TARGET_NAME}-${PKG_TAG}
        fi
    else
        if [ "$3" == "zip" ];then
            scp $1 ${SAVE_PATH}/${2}_${PKG_MODULE}.zip
        else
            scp $1 ${SAVE_PATH}
        fi

    fi

    
    if [ $? -eq 0 ];then
        echo "已拷贝到下载路径,可以发布"
    else
        echo "未拷贝到下载路径,不可以发布"
        echo "LogEnd"
        exit -1
    fi
}



function scp_pkg_name_for_deploy()
{
    local src_pkg_name=$TARGET_NAME
    ptype=`echo "$TARGET_NAME"|awk -F "." '{print $NF}'`
    d=`pwd`
    echo "当前路径:" $d
    
    if [ $ptype == "zip" ];then
        if [ "$PKG_MODULE" == "None" ];then
            src_pkg_name=`ls target | grep 'zip$'`
        else
            src_pkg_name=`ls ${PKG_MODULE}/target | grep 'zip$'`
        fi
    fi
    
    if [ "$PKG_MODULE" == "None" ];then
        src_filename="target/$src_pkg_name"
    else
        src_filename="$PKG_MODULE/target/$src_pkg_name"
    fi
    
    echo "拷贝的FileName：" $src_filename
    fileSize=`ls -lh "$src_filename"  | awk '{print $5}'`
    echo "文件大小: "  $fileSize
   
    copy_to_save_path $src_filename $PROJECT_NAME $ptype
    
    
}

function main()
{
    start_time=`date +%s`
    echo_commit_msg
    compile_project
    scp_pkg_name_for_deploy
    echo_commit_msg
    end_time=`date +%s`
    echo "执行时间花费: $((end_time-start_time)) s"
    echo "LogEnd"
    exit 0
}

main

