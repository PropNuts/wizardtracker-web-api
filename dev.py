import eventlet
eventlet.monkey_patch()

from app import run_app


if __name__ == '__main__':
    run_app()
