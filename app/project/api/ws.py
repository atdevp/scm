# --*-- coding: utf-8 --*--
from dwebsocket import require_websocket
import subprocess
import cfg
import os


def run_shell_command(command, project_name):

    path = os.path.join(cfg.CICD_CFG['SRC_CODE_PATH'], project_name)

    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True,
                         cwd=path)
    return iter(p.stdout.readline, b'')


@require_websocket
def output_compile_log(request):
    while True:
        data = request.websocket.wait()
        s = data.decode('utf-8')[1:-1]  # 去掉引号
        L = s.split(' ')
        if len(L) < 2:
            request.websocket.send(data)
            request.websocket.send(b'LogEnd')
        command, project_name = L[0], L[1]
        for line in run_shell_command(s, project_name):
            request.websocket.send(line)
