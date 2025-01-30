from mietrak_pro.query.router import create_router, delete_existing_bom_and_routing
from mietrak_pro.exporter.utils import RouterData
import mietrak_pro.models

from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger


class RouterProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, part, customer):
        router, is_router_new = self.get_or_create_router(part, customer)
        if self.should_rebuild_existing_router(is_router_new, part, customer):
            self.clear_existing_bom_and_routing(part, router)
        router_data = RouterData(router=router, is_router_new=is_router_new)
        return router_data

    def get_or_create_router(self, part, customer):
        existing_routers = mietrak_pro.models.Router.objects.filter(itemfk=part.itempk)
        is_router_new = False
        division_pk = self._exporter.division_pk
        if existing_routers:
            logger.info(
                f'Found existing router(s) for part number {part.partnumber} and revision {part.revision} - selecting default router')
            router = existing_routers.filter(defaultrouter=True).first()
        else:
            logger.info(
                f'Did not find router for part number {part.partnumber} and revision {part.revision} - creating one')
            router_status = self.get_router_status(part, customer)
            is_default_router = self.get_is_default_router(part, customer)
            router = create_router(customer, part, router_status, is_default_router,
                                   division_pk)
            is_router_new = True
        return router, is_router_new

    def get_router_status(self, part, customer):
        return 'Pending Approval'

    def get_is_default_router(self, part, customer):
        ''' It looks like MIE Trak Pro's internal logic is to always set defaultrouter to True for the first Router,
            and to set it to False for any subsequent Routers if another default Router exists. '''
        return True

    def should_rebuild_existing_router(self, is_router_new, part, customer):
        return (not is_router_new) and self._exporter.erp_config.should_rebuild_existing_mietrak_pro_routers

    def clear_existing_bom_and_routing(self, part, router):
        logger.info(f'Clearing router for part number {part.partnumber} and revision {part.revision}')
        delete_existing_bom_and_routing(router, self._exporter.estimator)
