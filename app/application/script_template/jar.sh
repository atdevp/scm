#!/usr/bin/env bash





###########################################
###########set defalut java env############
###########################################
JAVA_HOME=/opt/jdk18
PATH=$JAVA_HOME/bin:$PATH
CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar
export JAVA_HOME PATH CLASSPATH

###########################################
########replaced parameters################
###########################################
root_home="/opt/INIT_USER"
pkg_name="PKG_NAME"
pool_name="POOL_NAME"
run_mode="RUN_MODE"
main_class="MAIN_CLASS"
main_args="MAIN_ARGS"
jvm_args="JVM_ARGS"


###########################################

app_home="${root_home}/${pool_name}"
app_log_home="${app_home}/logs"
app_temp_home="${app_home}/work/"
app_conf_home="${app_home}/conf/"
app_lib_home="${app_home}/lib"

if [ ! -d ${app_log_home} ]
then
    mkdir -p ${app_log_home}
fi

function get_service_pids() {
    pids=( `ps -eo pid,user,cmd | grep -v "grep" |grep "${app_lib_home}" | grep "${app_log_home}" | awk '{print $1}'` )
}


case "$1" in
    start)
        echo "starting server ${pool_name}"
        #all pids
        get_service_pids
        if [ ${#pids[*]} -gt 0 ]; then
            echo "${pool_name} is started,the pid is ${pids[@]}"
            exit 1
        fi
        
        if [ -n "${app_lib_home}" ]; then
            for i in `ls ${app_lib_home}`
            do
                app_class_path=${app_class_path}:${app_lib_home}/$i
            done
        fi
        export CLASSPATH=${CLASSPATH}:${app_class_path}
        
        #server start time
        start_time=`date "+%Y-%m-%d %H:%M:%S"`
        /opt/jdk18/bin/java ${jvm_args}  -Dserver_mode=${run_mode} -DlogPath=${app_log_home} -Dfile.encoding=UTF-8 -jar  ${app_lib_home}/${pkg_name} ${main_class} ${main_args}  >>${app_log_home}/${pool_name}.stdout 2>> ${app_log_home}/${pool_name}.stderr  &
        sleep 3
        
        get_service_pids
        if [ ${#pids[*]} -gt 1 ]; then
            echo "${pool_name} is start success,but find multiple instances pids: ${pids[@]}"
            exit 1
            elif [ ${#pids[*]} -eq 1 ]; then
            echo "${pool_name} is start success,the pid is ${pids[@]}"
        else
            echo "Fail,see log ${app_log_home}/${pool_name}.err"
            exit 1
        fi
    ;;
    stop)
        echo "stoping server ${pool_name}"
        #all pids
        get_service_pids
        if [ ${#pids[*]} -gt 1 ]; then
            echo "find multiple ${pool_name} proccess, infos:"
            ps -eo pid,user,cmd | grep "${service}" | grep "${main_class}"
            echo "stop server fail,please manual processing"
            exit 1
            elif [ ${#pids[*]} -eq 1 ]; then
            echo "kill -9 ${pids[@]}"
            kill -9 ${pids[@]}
            get_service_pids
            if [ ${#pids[*]} -gt 0 ]; then
                echo "stop server fail,please manual processing"
                exit 1
            else
                echo "stop server success"
            fi
        else
            echo "server ${pool_name} is not exist"
        fi
    ;;
    restart)
        $0 stop && sleep 2
        if [ ! $? -eq 0 ]; then
            $0 stop && sleep 1
        fi
        $0 start
    ;;
    *)
        echo "Usage ${0} <start|stop|restart>"
        exit 1
    ;;
esac
