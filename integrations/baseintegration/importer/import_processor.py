from ...baseintegration.importer import BaseImporter


class BaseImportProcessor:
    """
    The base processor class for all other resource processors in integrations. Will be overridden for each resource in
    the ERP that needs to be created/retrieved/edited
    """
    # set this flag to T/F on whether a rollback should happen if an error is encounted in the integration.
    do_rollback = False
    repeat_part_batch = list()

    def __init__(self, importer: BaseImporter):
        """
        We want to ensure that each time a Processor is created, it has a reference to the Integration that created it
        to access context and configuration data.
        """
        self._importer = importer

    def run(self, *args, **kwargs):
        """
        This is only run by the Integration instance to obtain a resource.
        :return: the resources this processor ensured were present
        """
        args, kwargs = self._pre_process(*args, **kwargs)
        ret_vals = self._process(*args, **kwargs)
        resources = self._post_process(ret_vals, *args, **kwargs)
        return resources

    def _process(self, *args, **kwargs):
        """
        This is the main driver that will need to be implemented by every subclass. There are a variable number of
        kwargs defined here, but there will be explicitly required parameters on the subclasses. See:
        https://stackoverflow.com/questions/14626279/inheritance-best-practice-args-kwargs-or-explicitly-specifying-parameters
        This is the main method that drives the integration logic.
        This will return an instance(s) of the resource(s) it is supposed to process.
        :param args:
        :param kwargs:
        :return:
        """
        raise ValueError(f"_process() method not implemented on {self.__class__.__name__}")

    def _pre_process(self, *args, **kwargs):
        """
        Called before _process() in case any additional actions need to be taken before the resource is created. The
        values returned here are going to be passed in as the parameters for _process
        :param args:
        :param kwargs:
        :return:
        """
        return args, kwargs

    def _post_process(self, resources, *args, **kwargs):
        """
        After the resource has been created, this method is used to do any additional operations on that resource, or
        create new resources.
        :param resource: The resource object produced by ._process()
        :param args: The args passed to ._process() to create the resource
        :param kwargs: The kwargs passed to ._process() to create the resource
        :return:
        """
        return resources

    def rollback(self, resources, *args, **kwargs):
        """
        The default here should be to delete the resource that was created. If it is a django object we could call
        obj.delete(), etc. Should be overridden by a good default ERP interface and then on a per-instance as to whether
        the particular processor should remove the resource it created/found. Ex: We probably DO want to rollback order
        data, but MAY not want to roll back customer data.
        """
        pass
