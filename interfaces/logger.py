class ILogger:
    """
    ILogger is used to log actions.
    """
    def log_vm_action(txid, source, vm_name, action, msg=None):
        """
        :param txid: transaction id
        :param source: who/what instigated this action
        :param vm_name: name of VM this action is being done on
        :param action: name of action
        :param msg: an optional message string
        """

    def log_vm(txid, source, vm_name, msg):
        """
        :param txid: transaction id
        :param source: who/what instigated this message
        :param vm_name: name of VM this action is being done on
        :param msg: message to log
        """

    def log_driver_call(txid, source, node_name, vm_name, action, response):
        """
        :param txid: transaction id
        :param source: who/what instigated this message
        :param node_name: name of node in driver call
        :param vm_name: name of VM this action is being done on
        :param action: name of action
        :param response: response from driver
        """

    def get_vm_log(vm_name, limit=10, txid=None):
        """
        :param vm_name: name of VM
        :param limit: max number of log entries to return
        :param txid: transaction id (limit if supplied)
        """

    def info(msg):
        """
        :param msg: a generic info message
        """

    def warn(msg):
        """
        :param msg: a generic warning
        """

    def error(msg, exception=None, txid=None):
        """
        :param msg: error message
        :param exception: an optional exception
        :param txid: an optional transaction id
        """

    def debug(msg):
        """
        :param msg: a debugging message
        """
