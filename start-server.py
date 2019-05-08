import os
import sys
import subprocess

from threading import Thread
from hash_observer import HashObserver


def main(*args):
    ignored = {
        '*.md',
        '*.cfg',
        '*.pyc',
        os.path.basename(__file__),
    }

    with open('.gitignore') as gitignore:
        ignored |= set(line.strip() for line in gitignore.readlines() if line.strip())

    def start_server():
        sub = globals().get('sub')
        if sub is not None:
            sub.kill()
        globals()['sub'] = subprocess.Popen(['python', 'server/main.py'])

    def install_lib():
        sp = subprocess.Popen(['./install.sh'])
        sp.wait()
        start_server()

    install_lib()

    lib_observer = HashObserver(path='./lib', exclude=ignored)
    server_observer = HashObserver(path='./server', exclude=ignored)

    t1 = Thread(target=lib_observer.observe, args=(install_lib, ))
    t2 = Thread(target=server_observer.observe, args=(start_server, ))
    t1.start()
    t2.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        return -1
    finally:
        lib_observer.stop()
        server_observer.stop()

        t1.join()
        t2.join()

    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
