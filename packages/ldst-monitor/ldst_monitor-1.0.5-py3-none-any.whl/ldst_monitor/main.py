from .monitor import Monitor
from .ding import Ding
import time
from dotenv import load_dotenv

load_dotenv()

monitor = Monitor()


def run():
    while True:
        monitor.run()
        print(monitor.is_failed(), monitor.check.get("failed_time"))
        if monitor.is_failed() and monitor.check.get("failed_time") \
                and ((time.time() - monitor.check.get("failed_send_time")) > 20 or
                     not monitor.check.get("failed_send_time")):
            ding = Ding()
            monitor.check.update({"failed_send_time": time.time()})
            print(monitor.status)
            msg = [k + " 服务停止了." for (k, v) in monitor.status.items() if not v]
            if ding.send_text(" > ".join(msg)):
                monitor.failed_send_time = time.time()
        elif not monitor.is_failed() and monitor.check.get("failed_time"):
            monitor.check.update({"failed_time": 0.0})
            print("success")

        # send
        time.sleep(3)
