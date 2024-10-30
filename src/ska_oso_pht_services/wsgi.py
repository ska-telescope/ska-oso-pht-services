"""
Entry point for application
"""

import logging

from ska_ser_logging import configure_logging, get_default_formatter

from ska_oso_pht_services import create_app

app = create_app()

if __name__ == "__main__":
    # TEMP: hacking pydevd plugin path. Otherwise it won't handle space(s)
    import sys
    argv = []
    for a in sys.orig_argv:
        if "pydevd" in a:
            argv.append(f'"{a}"')
        else:
            argv.append(a)

    sys.orig_argv = argv

    app.run(host="0.0.0.0")
else:
    from gunicorn import glogging

    class UniformLogger(glogging.Logger):
        def setup(self, cfg):
            # override the configuration but inherit gunicorn logging level
            super().setup(cfg)
            configure_logging(level=self.loglevel)

            # Override gunicorn format with SKA.
            self._set_handler(self.error_log, cfg.errorlog,
                              get_default_formatter())

    # presume being run from gunicorn
    # use gunicorn logging level for app and module loggers
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.app.logger.setLevel(gunicorn_logger.level)
    logger = logging.getLogger("ska_db_oda")
    logger.setLevel(gunicorn_logger.level)
