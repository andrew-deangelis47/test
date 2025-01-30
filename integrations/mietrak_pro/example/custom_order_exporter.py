from mietrak_pro.exporter.exporter import MieTrakProOrderExporter


class CustomOrderExporter(MieTrakProOrderExporter):
    '''
    You will only need this if you're developing custom processors or customized behaviors that aren't
    already developed in the off the shelf integration. If the custom behavior you're adding is something
    that future customers might want/need, build it as a config option
    '''

    def _register_custom_processors(self):
        pass
