import os.path
import subprocess
import time


class Monitor:
    def __init__(self):
        self.status = {
            "mysql": True,
            "nginx": True,
            "memcached": True,
            "php-fpm-74": True,
        }
        self.check = {
            "last_check": 0.0,
            "failed_time": 0.0,
            "failed_send_time": 0.0,
            "success_send_time": 0.0
        }

    def mysql(self):
        process = subprocess.run(["pgrep", "-x", "mysqld"], capture_output=True)
        if process.returncode != 0:
            self.status.update({"mysql": False})
            process = subprocess.run(['/etc/init.d/mysqld', 'start'])
            print(process.stdout)
        else:
            self.status.update({"mysql": True})

    def nginx(self):
        nginx_shell = '/etc/init.d/nginx'
        process = subprocess.run([nginx_shell, "status"], capture_output=True)
        if process.stdout.decode("utf8").find("running") == -1:
            self.status.update({"nginx": False})
            process = subprocess.run([nginx_shell, 'start'])
            print(process.stdout)
        else:
            self.status.update({"nginx": True})

    def memcached(self):
        process = subprocess.run(["pgrep", "-x", "memcached"], capture_output=True)
        if process.returncode != 0:
            self.status.update({"memcached": False})
            process = subprocess.run(['/etc/init.d/memcached', 'start'])
            print(process.stdout)
        else:
            self.status.update({"memcached": True})

    def php_fpm_74(self):
        php_74 = "/etc/init.d/php-fpm-74"
        if os.path.exists(php_74):
            process = subprocess.run([php_74, "status"], capture_output=True)
            if process.stdout.decode("utf8").find("running") == -1:
                self.status.update({"php-fpm-74": False})
                process = subprocess.run([php_74, 'start'])
                print(process.stdout)
            else:
                self.status.update({"php-fpm-74": True})

    def is_failed(self):
        failed = dict((k, v) for (k, v) in self.status.items() if not v)
        return len(failed.items()) > 0

    def run(self):
        self.mysql()
        self.memcached()
        self.php_fpm_74()
        self.nginx()
        cache = os.path.join(os.getcwd(), "cache")
        if not os.path.exists(cache):
            os.makedirs(cache)

        self.check.update({"last_check": time.time()})

        if self.is_failed() and not self.check.get("failed_time"):
            self.check.update({"failed_time": time.time()})


if __name__ == "__main__":
    monitor = Monitor()
    monitor.run()
