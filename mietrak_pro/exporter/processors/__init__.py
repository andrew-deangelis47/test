from baseintegration.exporter.processor import BaseProcessor


class MietrakProProcessor(BaseProcessor):
    """
    This is the default processor for all MIE Trak Pro processor classes
    """

    # set this flag to T/F on whether a rollback should happen.
    do_rollback = False
