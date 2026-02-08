import sims4.log

class OmutsuLogger:

    def __init__(self, group_name):
        self.logger = sims4.log.Logger(group_name)

    def debug(self, message, *args, owner=None):
        self.logger.debug(message, *args, **{"owner": owner})

    def info(self, message, *args, owner=None):
        self.logger.info(message, *args, **{"owner": owner})

    def warn(self, message, *args, owner=None):
        self.logger.warn(message, *args, **{"owner": owner})

    def error(self, message, *args, owner=None):
        self.logger.error(message, *args, **{"owner": owner})

    def exception(self, message, *args, exc=None, owner=None):
        self.logger.exception(message, *args, **{'exc':exc, 'owner':owner})
