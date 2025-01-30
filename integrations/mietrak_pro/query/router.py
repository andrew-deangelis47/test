from mietrak_pro.models import Division, Router, Routerstatus, Routerworkcenter, Workcenter, Operation, ActivityLog, \
    Activitylogtype, Party
from datetime import datetime
from mietrak_pro.utils import get_version_number, VERSION_2020, VERSION_2019


def create_router(customer, item, router_status, is_default_router, division_pk: int = 1, estimator=None):
    division = Division.objects.get(divisionpk=division_pk)
    router_status = Routerstatus.objects.get(description=router_status)
    # Note that the itemdescription field on the Router record can only be 200 characters, but the description field on
    # the Item record can be 500 characters
    item_description = item.description
    now = datetime.now()

    router = Router.objects.create(
        customerfk=customer,
        divisionfk=division,
        itemfk=item,
        routerstatusfk=router_status,
        routertype=0,
        defaultrouter=is_default_router,
        engineeringchange=0,
        specification=0,
        datestamp=now,
        lastchangeddatestamp=now,
        itemdescription=item_description,
        partnumber=item.partnumber,
        revision=item.revision,
    )
    router.routernumber = str(router.routerpk)
    router.save()

    log_type = Activitylogtype.objects.get(activitylogtypepk=46)

    activitylog = ActivityLog(
        routerfk=router,
        datestamp=now,
        comment=f'Paperless created router - {estimator.email if estimator else ""}',
        activitylogtypefk=log_type
    )
    activitylog.save()

    return router


def delete_existing_bom_and_routing(router, estimator):
    log_type = Activitylogtype.objects.get(activitylogtypepk=74)

    activitylog = ActivityLog(
        routerfk=router,
        datestamp=datetime.now(),
        comment=f'Paperless deleted router - {estimator.email if estimator else ""}',
        activitylogtypefk=log_type
    )
    activitylog.save()
    router_work_center_records = Routerworkcenter.objects.filter(routerfk=router)
    router_work_center_records.delete()


def create_subrouter_bom_link(router, subrouter, sequence_number, bom_quantity=1., overagepercentage=0):
    position_index = Routerworkcenter.objects.filter(routerfk=router).count() + 1

    subrouter_bom_link = Routerworkcenter(
        routerfk=router,
        itemrouterfk=subrouter,
        sequencenumber=sequence_number,
        orderby=position_index,
        againstgrain=0,
        certificationsrequired=0,
        doublesided=0,
        nestable=0,
        nonamortizeditem=0,
        setstatustopullfrominventory=0,
        singlepartnestable=0,
        stopsequence=0,
        unattendedoperation=0,
        useexactmaterialcalculation=0,
        graindirection=0,
        partsrequired=1.,
        quantityrequired=bom_quantity,
        minutesperpart=0,
        setuptime=0.,
        overagepercentage=overagepercentage
    )
    if get_version_number() != VERSION_2019:
        subrouter_bom_link.shiploose = 0
        subrouter_bom_link.aqlrequired = 0
        subrouter_bom_link.bulkship = 0

    subrouter_bom_link.save()
    return subrouter_bom_link


def create_bom_item_link(router, part, sequence_number, bom_quantity=1., blank_width: float = None,
                         blank_length: float = None, parts_per_blank=None, part_length=None, part_width=None,
                         stock_length=None, stock_width=None, mat_notes=None, part_thickness=None, density=0,
                         overagepercentage=0, leadtime=0, daysout=0, supplier_name=None, setup_charge=0,
                         quantityperinverse=1., useexactmaterialcalculation=1, minimum=0):
    # Figure out what position to assign, but don't count routing lines
    supplier = Party.objects.filter(name=supplier_name).first()
    position_index = Routerworkcenter.objects.filter(routerfk=router, workcenterfk__isnull=True).count() + 1
    bom_item_link = Routerworkcenter(
        routerfk=router,
        itemfk=part,
        supplierfk=part.partyfk if not supplier else supplier,
        unitofmeasuresetfk=part.unitofmeasuresetfk,
        sequencenumber=sequence_number,
        orderby=position_index,
        againstgrain=0,
        certificationsrequired=0,
        setstatustopullfrominventory=0,
        graindirection=0,
        donotprintbom=0,
        partsperblank=parts_per_blank,  # TODO - should this be set depending on the material?
        stocklength=stock_length,
        stockwidth=stock_width,
        partlength=part_length,
        partwidth=part_width,
        partsrequired=1.,
        quantityrequired=bom_quantity,
        quantityperinverse=quantityperinverse,  # TODO - what to do here?
        minutesperpart=0,
        setuptime=0.,
        vendorunit=part.vendorunit,
        blankwidth=blank_width,
        blanklength=blank_length,
        comment=mat_notes,
        thickness=part_thickness,
        singlepartnestable=0,
        nestable=0,
        useexactmaterialcalculation=useexactmaterialcalculation,
        weightfactor=part.weightfactor,
        overagepercentage=overagepercentage,
        leadtime=leadtime,
        daysout=daysout,
        setupcharge=setup_charge,
        minimum=minimum,
    )
    if get_version_number() != VERSION_2019:
        bom_item_link.shiploose = 0
        bom_item_link.bulkship = 0
    bom_item_link.save()
    return bom_item_link


def create_routing_line(router, work_center, runtime_minutes, setup_time_minutes, pieces_per_hour, operation_notes,
                        operation=None):
    # Only count routing lines
    position_index = Routerworkcenter.objects.filter(routerfk=router, workcenterfk__isnull=False).count() + 1

    if operation is None:
        operation = work_center.defaultoperationfk

    routing_line = Routerworkcenter(
        routerfk=router,
        operationfk=operation,
        workcenterfk=work_center,
        runemployees=1,
        sequencenumber=position_index,
        setupemployees=1,
        stopsequence=0,
        unattendedoperation=0,
        unattendedpercentage=0.,
        lagtime=work_center.lagtime,
        minutesperpart=runtime_minutes,
        setuptime=setup_time_minutes,
        piecesperhour=pieces_per_hour,
        comment=operation_notes,
        requiredcomment=0,
    )
    if get_version_number() != VERSION_2019:
        routing_line.aqlrequired = 0
    routing_line.save()
    return routing_line


def get_work_center_from_description(work_center_description):
    work_center = Workcenter.objects.filter(description=work_center_description).first()
    return work_center


def get_work_center_from_pk(work_center_pk: int):
    work_center = Workcenter.objects.get(workcenterpk=work_center_pk)
    return work_center


def get_operation_from_pk(operation_pk: int):
    operation = Operation.objects.get(operationpk=operation_pk)
    return operation


def create_default_work_center(work_center_code, work_center_description, division_pk: int = 1):
    division = Division.objects.get(divisionpk=division_pk)

    work_center = Workcenter(
        divisionfk=division,
        code=work_center_code,
        description=work_center_description,
        active=1,
        donotshowonwhiteboard=0,
        nonproductionasset=0,
        defaultloadingworkcenter=0,
        monday=1,
        tuesday=1,
        wednesday=1,
        thursday=1,
        friday=1,
        saturday=0,
        sunday=0,
        nonrouter=0,
        workordernestflag=0,
        meterreading=0,
    )
    if get_version_number() not in [VERSION_2020, VERSION_2019]:
        work_center.allowindirect = 0

    if get_version_number() != VERSION_2019:
        work_center.aqlrequired = 0

    work_center.save(force_insert=True)

    return work_center
