# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from baseintegration.utils.truncated_model import TruncatedModel


class Materialtype(TruncatedModel):
    materialcode = models.CharField(db_column='MaterialCode', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'MaterialType'


class Quoteheader(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=50)  # Field name made lowercase.
    requestforquoteid = models.ForeignKey('Requestforquote', models.DO_NOTHING, db_column='RequestForQuoteID')  # Field name made lowercase.
    parentquoteid = models.CharField(db_column='ParentQuoteID', max_length=50)  # Field name made lowercase.
    subquotenum = models.IntegerField(db_column='SubQuoteNum')  # Field name made lowercase.
    vetquoteid = models.CharField(db_column='VETQuoteId', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vetparentquoteid = models.CharField(db_column='VETParentQuoteID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    quotedate = models.DateField(db_column='QuoteDate', blank=True, null=True)  # Field name made lowercase.
    partnumber = models.CharField(db_column='PartNumber', max_length=30)  # Field name made lowercase.
    revisionnumber = models.CharField(db_column='RevisionNumber', max_length=6, blank=True, null=True)  # Field name made lowercase.
    partdescription = models.CharField(db_column='PartDescription', max_length=50, blank=True, null=True)  # Field name made lowercase.
    extendedpartdescription = models.TextField(db_column='ExtendedPartDescription', blank=True, null=True)  # Field name made lowercase.
    fginventoryno = models.CharField(db_column='FGInventoryNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    internalnotes = models.TextField(db_column='InternalNotes', blank=True, null=True)  # Field name made lowercase.
    customernotes = models.TextField(db_column='CustomerNotes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'QuoteHeader'


class Quotematerials(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    quoteheaderid = models.CharField(db_column='QuoteHeaderID', max_length=50)  # Field name made lowercase.
    partnumber = models.CharField(db_column='PartNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stockuom = models.CharField(db_column='StockUOM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rawmaterialinventoryno = models.CharField(db_column='RawMaterialInventoryNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    quantityperpiece = models.DecimalField(db_column='QuantityPerPiece', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    extendedpartdescription = models.TextField(db_column='ExtendedPartDescription', blank=True, null=True)  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'QuoteMaterials'


class Quoteoperations(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    quoteheaderid = models.CharField(db_column='QuoteHeaderID', max_length=50)  # Field name made lowercase.
    operationnumber = models.IntegerField(db_column='OperationNumber')  # Field name made lowercase.
    workcentercode = models.CharField(db_column='WorkCenterCode', max_length=5)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    operationtype = models.CharField(db_column='OperationType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    setuphours = models.DecimalField(db_column='SetupHours', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    runtimetype = models.CharField(db_column='RunTimeType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    runtime = models.DecimalField(db_column='RunTime', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    setuphourlyrate = models.DecimalField(db_column='SetupHourlyRate', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    laborrate = models.DecimalField(db_column='LaborRate', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    burdenrate = models.DecimalField(db_column='BurdenRate', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'QuoteOperations'


class Quotequantities(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    quoteheaderid = models.CharField(db_column='QuoteHeaderID', max_length=50)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=12, decimal_places=3)  # Field name made lowercase.
    priceperpiece = models.DecimalField(db_column='PricePerPiece', max_digits=12, decimal_places=6)  # Field name made lowercase.
    numberofsetups = models.IntegerField(db_column='NumberOfSetups')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'QuoteQuantities'


class Quoteonetimecharges(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=10, decimal_places=4)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extendedprice = models.DecimalField(db_column='ExtendedPrice', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    quoteheaderid = models.CharField(db_column='QuoteHeaderID', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'QuoteOneTimeCharges'


class Requestforquote(TruncatedModel):
    id = models.CharField(db_column='ID', primary_key=True, max_length=50)  # Field name made lowercase.
    vetrequestforquoteid = models.CharField(db_column='VETRequestForQuoteID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rfqdate = models.DateField(db_column='RFQDate', blank=True, null=True)  # Field name made lowercase.
    customercode = models.CharField(db_column='CustomerCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    customername = models.CharField(db_column='CustomerName', max_length=35, blank=True, null=True)  # Field name made lowercase.
    customeraddressline1 = models.CharField(db_column='CustomerAddressLine1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customeraddressline2 = models.CharField(db_column='CustomerAddressLine2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customeraddressline3 = models.CharField(db_column='CustomerAddressLine3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customeraddressline4 = models.CharField(db_column='CustomerAddressLine4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    salespersonname = models.CharField(db_column='SalesPersonName', max_length=35, blank=True, null=True)  # Field name made lowercase.
    salespersonemail = models.CharField(db_column='SalesPersonEmail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    processed = models.BooleanField(db_column='Processed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'RequestForQuote'


class Accounts(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    credit_line = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    estitrack_account_id = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    phone_ext = models.CharField(max_length=10, blank=True, null=True)
    tax_exempt = models.BooleanField(blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'accounts'


class BillingAddress(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    estitrack_account_id = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'billing_address'


class Contacts(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    phone_ext = models.CharField(max_length=10, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    customercode = models.CharField(db_column='CustomerCode', max_length=7, blank=True, null=True)  # Field name made lowercase.
    vendorcode = models.CharField(db_column='VendorCode', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'contacts'


class Facilities(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    attention = models.CharField(max_length=100, blank=True, null=True)
    estitrack_account_id = models.CharField(max_length=50, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'facilities'


class HistoricalEstimatedActualHours(TruncatedModel):
    shop_order_number = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    revision = models.CharField(max_length=100)
    work_center_name = models.CharField(max_length=100)
    hours_quoted = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    hours_actual = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    quantityproduced = models.IntegerField(db_column='QuantityProduced', blank=True, null=True)  # Field name made lowercase.
    operationnumber = models.IntegerField(db_column='OperationNumber', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='Id', primary_key=True, max_length=18)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'historical_estimated_actual_hours'


class HistoricalOrders(TruncatedModel):
    id = models.CharField(primary_key=True, max_length=15)
    shop_order_number = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    revision = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    quantity_ordered = models.IntegerField(blank=True, null=True)
    gain_loss = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    profit_margin = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'historical_orders'


class Inventory(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    inventory_number = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    extendedpartdescription = models.TextField(db_column='ExtendedPartDescription', blank=True, null=True)  # Field name made lowercase.
    piece_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    thickness = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    width = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    length = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    shape_code = models.CharField(max_length=100, blank=True, null=True)
    inventory = models.IntegerField(blank=True, null=True)
    materialcode = models.CharField(db_column='MaterialCode', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'inventory'


class Vendors(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    phone_ext = models.CharField(max_length=10, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vendors'


class WorkCenters(TruncatedModel):
    id = models.IntegerField(primary_key=True)
    work_center_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    labor_rate = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    burden_rate = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'work_centers'
