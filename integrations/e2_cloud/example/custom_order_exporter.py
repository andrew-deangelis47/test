from e2_cloud.exporter.exporter import E2CloudOrderExporter


class CustomOrderExporter(E2CloudOrderExporter):
    '''
    You will only need this if you're developing custom processors or customized behaviors that aren't
    already developed in the off the shelf integration.
    '''

    def _register_custom_processors(self):
        pass
