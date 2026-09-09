import logging
import os
import subprocess
import sys
import time

from prometheus_client import Gauge, start_http_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

BEAT_HEALTH = Gauge(
    "intelliview_celery_beat_health",
    "Celery Beat process health",
)

BEAT_PORT = int(os.getenv("BEAT_METRICS_PORT", "9102"))

beat_process = None


def main() -> int:
    global beat_process

    start_http_server(BEAT_PORT)
    BEAT_HEALTH.set(1)

    logger.info("Celery Beat metrics server started on port %s", BEAT_PORT)

    beat_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "celery",
            "-A",
            "workers.celery_app",
            "beat",
            "--loglevel=info",
        ]
    )

    logger.info("Celery Beat started with PID %s", beat_process.pid)

    try:
        while True:
            return_code = beat_process.poll()

            if return_code is not None:
                logger.error(
                    "Celery Beat stopped with exit code %s",
                    return_code,
                )
                BEAT_HEALTH.set(0)
                return return_code

            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Stopping Celery Beat")

    finally:
        BEAT_HEALTH.set(0)

        if beat_process is not None and beat_process.poll() is None:
            beat_process.terminate()
            try:
                beat_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                beat_process.kill()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
