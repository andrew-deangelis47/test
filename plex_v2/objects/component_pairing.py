from paperless.objects.orders import OrderComponent
from plex_v2.objects.part import Part
from typing import List


class Pairing:
    """
    represents a pp component and its corresponding plex component
    """

    pp_component: OrderComponent
    plex_component: Part

    def __init__(self, pp_component: OrderComponent, plex_component: Part):
        self.pp_component = pp_component
        self.plex_component = plex_component


class PPComponentPlexComponentPairings:
    """
    represents a list of component pairings
    each paperless component, and its matching plex component
    """

    pairings: List[Pairing]

    def __init__(self):
        self.pairings: List[Pairing] = []

    def add_pairing(self, pp_component: OrderComponent, plex_component: Part) -> None:
        pairing = Pairing(pp_component, plex_component)
        self.pairings.append(pairing)
