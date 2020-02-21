

import os
import subprocess



def shell(*args, **kw):
    kw['stdout'] = subprocess.PIPE
    kw['stderr'] = subprocess.PIPE

    p = subprocess.Popen(*args, *kw)
    sout, serr = p.communicate()

    return p.returncode, sout, serr


class CloneError(Exception):
    pass


class PullError(Exception):
    pass


class CheckoutError(Exception):
    pass


class CommitError(Exception):
    pass


class Git:
    def __init__(self, url, path):
        self.url = url
        self.base_dir = path

    def __metaname(self):
        return self.url.split('/')[-1].split['.'][0]

    def clone(self, path=None):
        if not path:
            raise CloneError('invalid clone path')
        
        cmd = 'git clone --recursive '+ self.url
        code, _, err = shell(cmd, shell=True, cwd=os.getcwd())
        if code != 0:
            raise CloneError()

    def pull(self, br='master'):
        md = os.path.join(self.base_dir, self.__metaname())
        step1 = 'git fetch origin'
        step2 = 'git reset --hard origin/' + br
        step3 = 'git submodule update --init --recursive'
        
        cmds = (step1, step2, step3)
        for cmd in cmds:
            code, _, err = shell(cmd, shell=True, cwd=os.chdir(md))
            if code != 0:
                raise PullError(err)

    def checkout(self, br):
        md = os.path.join(self.base_dir, self.__metaname())
        code, stdout, err = shell('git branch', shell=True, cwd=os.chdir(md))
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
        md = os.path.join(self.base_dir, self.__metaname())
        cmd = "git log  --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit -n 10"
        code, _, err = shell(cmd, shell=True, cwd=os.chdir(md))
        if code != 0:
            raise CommitError(err)



