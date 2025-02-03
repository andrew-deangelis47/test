from jobscope.exporter.exporter import JobscopeOrderExporter


class CustomOrderExporter(JobscopeOrderExporter):
    '''
    You will only need this if you're developing custom processors or customized behaviors that aren't
    already developed in the off the shelf integration.
    '''

    def _register_custom_processors(self):
        pass
