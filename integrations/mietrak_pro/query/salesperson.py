from typing import Optional
from mietrak_pro.models import Party, Partysalesperson, Salesorder, Salesordersalesperson


def get_salesperson_by_id(salesperson_id: int) -> Optional[Party]:
    return Party.objects.filter(partypk=salesperson_id).first()


def get_party_salesperson_for_customer_by_salesperson(customer: Party, salesperson: Party) \
        -> Optional[Partysalesperson]:
    return Partysalesperson.objects.filter(partyfk=customer, salespersonfk_id=salesperson).first()


def create_party_salesperson(customer: Party, salesperson: Party) -> Partysalesperson:
    party_salesperson = Partysalesperson.objects.create(
        partyfk=customer,
        salespersonfk=salesperson,
        commissionpercentage=0.,
        # TODO - can I pull this from somewhere? Or must this be set per customer? We don't have this in Paperless.
        defaultsalesperson=0,
    )
    return party_salesperson


def get_order_salesperson_for_order_by_salesperson(sales_order: Salesorder, salesperson: Party) \
        -> Optional[Salesordersalesperson]:
    return Salesordersalesperson.objects.filter(salesorderfk=sales_order, salespersonfk_id=salesperson).first()


def create_order_salesperson(sales_order: Salesorder, salesperson: Party,
                             partysalesperson: Partysalesperson = None) -> Salesordersalesperson:
    commissionpercentage = 0.
    if partysalesperson:
        commissionpercentage = partysalesperson.commissionpercentage
    order_salesperson = Salesordersalesperson.objects.create(
        salesorderfk=sales_order,
        salespersonfk=salesperson,
        commisionpercentage=commissionpercentage,
        # TODO - can I pull this from somewhere? Or must this be set per order? We don't have this in Paperless
        # The commissions were imported for herold, through a custom processor
        # They want it pulled directly from the existing salesperson for that customer, so maybe it can be a lookup
        # of an argument getting passed, and they wanted multiple salespeople to show up, so not doing P3L overrides now
    )
    return order_salesperson
