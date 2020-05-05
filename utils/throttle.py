from utils.init import RedisPool
import time

visit = {}


class IPRateThrottle(object):
    def __init__(self):
        if not RedisPool:
            self.cache = {'name': RedisPool, 'type': 'redis'}
        else:
            self.cache = {'name': None, 'type': 'local'}

        self.rate = 3  # 3/s

    def allow_request(self, request, view):
        ip = request.META.get('REMOTE_ADDR')
        self.ip = ip
        ctime = time.time()
        if self.cache['type'] == 'local':

            if ip not in visit:
                visit[ip] = [ctime]
                return True

            history = visit.get(ip)

            length = len(history)
            while length > 0 and ctime - history[-1] > 1:
                history.pop(0)
                length -= 1

            if len(history) < self.rate:
                history.append(ctime)
                return True

            return False

        cli = self.cache['name']
        if not cli.exists(ip):
            cli.lpush(ip, ctime)
            return True

        length = cli.llen(ip)
        while length > 0 and ctime - float(
                cli.lindex(ip, length - 1).decode('UTF-8')) > 1:
            cli.lpop(ip)
            length = length - 1

        if length < self.rate:
            cli.rpush(ip, ctime)
            return True

        return False

    def wait(self):
        ctime = time.time()

        if self.cache['type'] == 'local':
            history = visit.get(self.ip)
            return 60 - (ctime - history[-1])

        cli = self.cache['name']
        length = cli.llen(self.ip)
        last = float(cli.lindex(self.ip, length - 1).decode('UTF-8'))

        return 60 - (ctime - last)
