from visualestitrack.exporter.exporter import VisualEstiTrackOrderExporter


class CustomOrderExporter(VisualEstiTrackOrderExporter):
    '''
    You will only need this if you're developing custom processors or customized behaviors that aren't
    already developed in the off the shelf exporter. If the custom behavior you're adding is something
    that future customers might want/need, build it as a config option in example-e2
    '''

    def _register_custom_processors(self):
        pass
