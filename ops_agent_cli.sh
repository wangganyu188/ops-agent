#!/usr/bin/env bash
#author:moore moorewqk@163.com


###################
#filebeat 启动关闭
#
###################

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
NAME="ops-agent"
APPBASE=/usr/local/${NAME}
BIN=${APPBASE}/run.py
PIDFILE=/usr/local/${NAME}/$NAME.pid

start ()
{
    echo -n "Starting $NAME... "
    if ps aux | grep $NAME | grep -v grep| grep -v start| grep -v restart;then
        echo "$NAME (pid `pidof $NAME`) already running."
        exit 1
    fi
    cd ${APPBASE}; source venv/bin/activate; nohup python run.py start  >/dev/null 2>&1 & echo $! > $PIDFILE

    if [ "$?" != 0 ] ; then
        echo " failed"
        exit 1
    else
        echo "$NAME start done"
    fi
}

stop()
{
    echo -n "Stoping $NAME... "
    if ! ps aux | grep $NAME | grep -v grep|grep -v stop; then
        echo "$NAME is not running."
        exit 1
    fi
    pid=`ps aux | grep $NAME | grep -v grep|awk '{print $2}'`
    kill -9 `cat $PIDFILE`
    kill -9 $pid
    if [ "$?" != 0 ] ; then
        echo " failed. Use force-quit kill -9 it "
        exit 1
    else
        echo "$NAME stop done"
    fi

}

status ()
{
    if ps aux | grep $NAME | grep -v grep|grep -v status; then
        PID=`pidof $NAME`
        echo "$NAME (pid $PID) is running..."
    else
        echo "$NAME is stopped"
        exit 0
    fi

}


case "$1" in
    start)
        start
        ;;

    stop)
        stop
        ;;

    status)
        status
        ;;
    restart)
        stop

        start
        ;;
    force-quit)
        echo -n "Terminating $NAME... "

        if ! netstat -tnpl | grep -q $NAME; then
            echo "$NAME is not running."
            exit 1
        fi

        kill `pidof $NAME`

        if [ "$?" != 0 ] ; then
            echo " failed"
            exit 1
        else
            echo "$NAME done"
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;

esac