

import os
import subprocess
from utils.exceptions import CloneError, PullError, CheckoutError, CommitError, GitWorkSpacePathNotFind
import cfg

def shell(*args, **kwargs):
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE

    p = subprocess.Popen(*args, **kwargs)
    stdout, stderr = p.communicate()

    return p.returncode, stdout, stderr



class Git:
    def __init__(self, url=None):
        self.url = url
        self.ws_path = cfg.CICD_CFG['SRC_CODE_PATH']

        if not os.path.exists(self.ws_path):
            raise GitWorkSpacePathNotFind("%s not find", self.ws_path)

        if os.getcwd() != self.ws_path:
            os.chdir(self.ws_path)

    def __metaname(self):
        return self.url.split('/')[-1].split('.')[0]

    def clone(self):

        if os.path.exists(os.path.join(self.ws_path, self.__metaname())):
            return
        
        cmd = 'git clone --recursive '+ self.url
        code, _, err = shell(cmd, shell=True, cwd=os.chdir(self.ws_path))
        if code != 0:
            raise CloneError(err)

    def pull(self, br='master'):
        pro_path = os.path.join(self.ws_path, self.__metaname())
        step1 = 'git fetch origin'
        step2 = 'git reset --hard origin/' + br
        step3 = 'git submodule update --init --recursive'
        
        cmds = (step1, step2, step3)
        for cmd in cmds:
            code, _, err = shell(cmd, shell=True, cwd=os.chdir(pro_path))
            if code != 0:
                raise PullError(err)

    def checkout(self, br):
        pro_path = os.path.join(self.ws_path, self.__metaname())
        code, stdout, err = shell('git branch', shell=True, cwd=os.chdir(pro_path))
        if code != 0 :
            raise CheckoutError(err)

        result = stdout.split('\n')[0:-1]
        brs = []
        for item in result:
            if item.startswith('* '):
                brs.append(item.split('* ')[1])
            else:
                brs.append(item.strip())

        if br in brs:
            cmd = 'git checkout ' + br
        else:
            cmd = 'git checkout -b ' + br

        code, _, err = shell(cmd, shell=True, cwd=os.chdir(md))
        if code != 0:
            raise CheckoutError(err)

    def get_commit(self):
        md = os.path.join(self.ws_path, self.__metaname())
        cmd = "git log  --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit -n 10"
        code, _, err = shell(cmd, shell=True, cwd=os.chdir(md))
        if code != 0:
            raise CommitError(err)



