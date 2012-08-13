from syslog import syslog as log
import syslog
import uuid
from .. import transaction

FACILITY = {
    "user": syslog.LOG_USER,
    "daemon": syslog.LOG_DAEMON,
    "local0": syslog.LOG_LOCAL0,
    "local1": syslog.LOG_LOCAL1,
    "local2": syslog.LOG_LOCAL2,
    "local3": syslog.LOG_LOCAL3,
    "local4": syslog.LOG_LOCAL4,
    "local5": syslog.LOG_LOCAL5,
    "local6": syslog.LOG_LOCAL6,
    "local7": syslog.LOG_LOCAL7,
}

class Syslogger:
    """
    Log all messages to syslog, keep no history.
    """
    def __init__(self, config, global_config):
        tag = config.get("tag", "vagoth")
        facility = config.get("facility", "user")
        if facility not in FACILITY:
            facility = "user"
        syslog.openlog(tag, syslog.LOG_NOWAIT, FACILITY[facility])

    def log_vm_action(self, vm_name, action, msg=None):
        """
        :param source: who/what instigated this action
        :param vm_name: name of VM this action is being done on
        :param action: name of action
        :param msg: an optional message string
        """
        line = "txid={0} source={1} vm_name={2} action={3}".format(
            transaction.get_txid(),
            transaction.get_source(),
            vm_name,
            action
        )
        if msg:
            log(syslog.LOG_INFO, line + ": " + msg)
        else:
            log(syslog.LOG_INFO, line)

    def log_vm(self, vm_name, msg):
        """
        :param vm_name: name of VM this action is being done on
        :param msg: message to log
        """
        line = "txid={0} source={1} vm_name={2}: {3}".format(
            transaction.get_txid(),
            transaction.get_source(),
            vm_name,
            msg
        )
        log(syslog.LOG_INFO, line)

    def log_driver_call(self, node_name, vm_name, action, response):
        """
        :param node_name: name of node in driver call
        :param vm_name: name of VM this action is being done on
        :param action: name of action
        :param response: response from driver
        """
        log(syslog.LOG_DEBUG, "txid={0} source={1} node_name={2}, vm_name={3} action={4} response={5}".format(
            transaction.get_txid(),
            transaction.get_source(),
            node_name,
            vm_name,
            action,
            str(response)
        ))

    def get_vm_log(self, vm_name, limit=10, txid=None):
        """
        :param vm_name: name of VM
        :param limit: max number of log entries to return
        :param txid: transaction id (limit if supplied)
        """
        return []

    def txlog(self, priority, msg):
        """
        :param msg: a generic info message
        :param priority: syslog priority enum
        """
        log(priority, "txid={0} source={1}: {2}".format(
            transaction.get_txid(),
            transaction.get_source(),
            msg
        ))

    def info(self, msg):
        """
        :param msg: a generic info message
        """
        self.txlog(syslog.LOG_INFO, "info: "+msg)

    def debug(self, msg):
        """
        :param msg: a debugging message
        """
        self.txlog(syslog.LOG_DEBUG, "debug: "+msg)

    def warn(self, msg):
        """
        :param msg: a generic warning
        """
        self.txlog(syslog.LOG_WARNING, "WARN: "+msg)

    def error(self, msg, exception=None, traceback=None):
        """
        :param msg: error message
        :param exception: an optional exception
        """
        # create a random txid if needed, for multiline exception log
        self.txlog(syslog.LOG_ERR, "ERR: "+msg)
        if exception and traceback:
            exc = traceback.format_exception(exc.__class__, exc, traceback)
            for line in exc.strip().split("\n"):
                self.txlog(syslog.LOG_ERR, line)
        elif exception:
            self.txlog(syslog.LOG_ERR, str(exception))

