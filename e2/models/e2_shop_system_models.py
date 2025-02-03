# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = IS_TEST` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
# from e2.autonumber import AutoNumberMixin, AutoNumberColumn
from e2.settings import IS_TEST
from django.db import models
from baseintegration.utils.truncated_model import TruncatedModel


class Acctcode(TruncatedModel):
    acctcode = models.CharField(db_column='AcctCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    classification = models.CharField(db_column='Classification', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    acctcode_id = models.AutoField(db_column='AcctCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    accounttype = models.SmallIntegerField(db_column='AccountType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'AcctCode'


class Attend(TruncatedModel):
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    emplname = models.CharField(db_column='EmplName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    searchdate = models.SmallIntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    exported = models.CharField(db_column='Exported', max_length=1, blank=True, null=True)  # Field name made lowercase.
    attend_id = models.AutoField(db_column='Attend_ID', primary_key=True)  # Field name made lowercase.
    ticketdate = models.CharField(db_column='TicketDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Attend'
        unique_together = (('emplcode', 'searchdate'), ('emplcode', 'ticketdate'),)


class Attenddet(TruncatedModel):
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    emplname = models.CharField(db_column='EmplName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    attendcode = models.SmallIntegerField(db_column='AttendCode', blank=True, null=True)  # Field name made lowercase.
    searchdate = models.SmallIntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    actclockintime = models.CharField(db_column='ActClockInTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    actclockouttime = models.CharField(db_column='ActClockOutTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adjclockintime = models.CharField(db_column='AdjClockInTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adjclockouttime = models.CharField(db_column='AdjClockOutTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
    actclockindate = models.CharField(db_column='ActClockInDate', max_length=8, blank=True, null=True)  # Field name made lowercase.
    actclockoutdate = models.CharField(db_column='ActClockOutDate', max_length=8, blank=True, null=True)  # Field name made lowercase.
    adjclockindate = models.CharField(db_column='AdjClockInDate', max_length=8, blank=True, null=True)  # Field name made lowercase.
    adjclockoutdate = models.CharField(db_column='AdjClockOutDate', max_length=8, blank=True, null=True)  # Field name made lowercase.
    totacttime = models.FloatField(db_column='TotActTime', blank=True, null=True)  # Field name made lowercase.
    totadjtime = models.FloatField(db_column='TotAdjTime', blank=True, null=True)  # Field name made lowercase.
    payratecode = models.SmallIntegerField(db_column='PayRateCode', blank=True, null=True)  # Field name made lowercase.
    payrollrate = models.FloatField(db_column='PayrollRate', blank=True, null=True)  # Field name made lowercase.
    shift = models.SmallIntegerField(db_column='Shift', blank=True, null=True)  # Field name made lowercase.
    overtime = models.CharField(db_column='OverTime', max_length=1, blank=True, null=True)  # Field name made lowercase.
    holiday = models.CharField(db_column='Holiday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    otcalcflag = models.CharField(db_column='OTCalcFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    deviceno = models.SmallIntegerField(db_column='DeviceNo', blank=True, null=True)  # Field name made lowercase.
    attenddet_id = models.AutoField(db_column='AttendDet_ID', primary_key=True)  # Field name made lowercase.
    ticketdate = models.CharField(db_column='TicketDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'AttendDet'


class Attendancecodes(TruncatedModel):
    attendcode = models.SmallIntegerField(db_column='AttendCode', unique=True, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shortname = models.CharField(db_column='ShortName', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    clockable = models.CharField(db_column='Clockable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    attendancecodes_id = models.AutoField(db_column='AttendanceCodes_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'AttendanceCodes'


class AttendanceDetail(TruncatedModel):
    company_code = models.CharField(db_column='Company_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    attendance_header_id = models.IntegerField(db_column='Attendance_Header_ID', blank=True, null=True)  # Field name made lowercase.
    actual_clock_in = models.DateTimeField(db_column='Actual_Clock_In', blank=True, null=True)  # Field name made lowercase.
    actual_clock_out = models.DateTimeField(db_column='Actual_Clock_Out', blank=True, null=True)  # Field name made lowercase.
    adjusted_clock_in = models.DateTimeField(db_column='Adjusted_Clock_In', blank=True, null=True)  # Field name made lowercase.
    adjusted_clock_out = models.DateTimeField(db_column='Adjusted_Clock_Out', blank=True, null=True)  # Field name made lowercase.
    attendance_code = models.CharField(db_column='Attendance_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    payroll_code = models.CharField(db_column='Payroll_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    payroll_rate = models.FloatField(db_column='Payroll_Rate', blank=True, null=True)  # Field name made lowercase.
    gl_account = models.CharField(db_column='GL_Account', max_length=20, blank=True, null=True)  # Field name made lowercase.
    overtime = models.NullBooleanField(db_column='OverTime')  # Field name made lowercase.
    shift_code = models.CharField(db_column='Shift_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    holiday = models.NullBooleanField(db_column='Holiday')  # Field name made lowercase.
    created_by = models.CharField(db_column='Created_By', max_length=20, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    ot_calculation_flag = models.CharField(db_column='OT_Calculation_Flag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    collection_terminal_number = models.SmallIntegerField(db_column='Collection_Terminal_Number', blank=True, null=True)  # Field name made lowercase.
    payroll_amount = models.FloatField(db_column='Payroll_Amount', blank=True, null=True)  # Field name made lowercase.
    break_hours = models.FloatField(db_column='Break_Hours', blank=True, null=True)  # Field name made lowercase.
    break_code = models.CharField(db_column='Break_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paid_break = models.NullBooleanField(db_column='Paid_Break')  # Field name made lowercase.
    ot_factor = models.FloatField(db_column='OT_Factor', blank=True, null=True)  # Field name made lowercase.
    attendance_detail_id = models.AutoField(db_column='Attendance_Detail_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Attendance_Detail'


class AttendanceHeader(TruncatedModel):
    company_code = models.CharField(db_column='Company_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    employee_code = models.CharField(db_column='Employee_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    employee_name = models.CharField(db_column='Employee_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ticket_date = models.DateTimeField(db_column='Ticket_Date', blank=True, null=True)  # Field name made lowercase.
    pay_period_code = models.CharField(db_column='Pay_Period_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    exported = models.NullBooleanField(db_column='Exported')  # Field name made lowercase.
    attendance_header_code = models.CharField(db_column='Attendance_Header_Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_attendance_header_code = models.CharField(db_column='Source_Attendance_Header_Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    entered_date = models.DateTimeField(db_column='Entered_Date', blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='Entered_By', max_length=50, blank=True, null=True)  # Field name made lowercase.
    attendance_header_id = models.AutoField(db_column='Attendance_Header_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Attendance_Header'


class Bankcode(TruncatedModel):
    bankcode = models.CharField(db_column='BankCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nextcheck = models.IntegerField(db_column='NextCheck', blank=True, null=True)  # Field name made lowercase.
    bankacct = models.CharField(db_column='BankAcct', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bankcode_id = models.AutoField(db_column='BankCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'BankCode'


class Bankrecinprocess(TruncatedModel):
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typecode = models.CharField(db_column='TypeCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bankrecinprocess_id = models.AutoField(db_column='BankRecInProcess_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'BankRecInProcess'


class Benchmark(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    timestart = models.DateTimeField(db_column='TimeStart', blank=True, null=True)  # Field name made lowercase.
    timestop = models.DateTimeField(db_column='TimeStop', blank=True, null=True)  # Field name made lowercase.
    elapsedtime = models.FloatField(db_column='ElapsedTime', blank=True, null=True)  # Field name made lowercase.
    numusers = models.IntegerField(db_column='NumUsers', blank=True, null=True)  # Field name made lowercase.
    numjobs = models.IntegerField(db_column='NumJobs', blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=30, blank=True, null=True)  # Field name made lowercase.
    benchmark_id = models.AutoField(db_column='Benchmark_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Benchmark'


class Billing(TruncatedModel):
    invoiceno = models.CharField(db_column='InvoiceNo', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    periodno = models.CharField(db_column='PeriodNo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pymtstatus = models.CharField(db_column='PymtStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custdesc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invdate = models.DateTimeField(db_column='InvDate', blank=True, null=True)  # Field name made lowercase.
    pymtdate = models.DateTimeField(db_column='PymtDate', blank=True, null=True)  # Field name made lowercase.
    invoicetotal = models.FloatField(db_column='InvoiceTotal', blank=True, null=True)  # Field name made lowercase.
    amtpaidsofar = models.FloatField(db_column='AmtPaidSoFar', blank=True, null=True)  # Field name made lowercase.
    salestaxchgs = models.FloatField(db_column='SalesTaxChgs', blank=True, null=True)  # Field name made lowercase.
    custcheckno = models.CharField(db_column='CustCheckNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aracct = models.CharField(db_column='ARAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    discacct = models.CharField(db_column='DiscAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct = models.CharField(db_column='TaxAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    saddr1 = models.CharField(db_column='SAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    saddr2 = models.CharField(db_column='SAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scity = models.CharField(db_column='SCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sst = models.CharField(db_column='SSt', max_length=2, blank=True, null=True)  # Field name made lowercase.
    szip = models.CharField(db_column='SZip', max_length=10, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shippingchgs = models.FloatField(db_column='ShippingChgs', blank=True, null=True)  # Field name made lowercase.
    freightacct = models.CharField(db_column='FreightAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    invprinted = models.CharField(db_column='InvPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cashdiscamt = models.FloatField(db_column='CashDiscAmt', blank=True, null=True)  # Field name made lowercase.
    discdate = models.DateTimeField(db_column='DiscDate', blank=True, null=True)  # Field name made lowercase.
    netduedate = models.DateTimeField(db_column='NetDueDate', blank=True, null=True)  # Field name made lowercase.
    invposted = models.CharField(db_column='InvPosted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=30, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    gstchgs = models.FloatField(db_column='GSTChgs', blank=True, null=True)  # Field name made lowercase.
    gstacct = models.CharField(db_column='GSTAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    projpaydate = models.DateTimeField(db_column='ProjPayDate', blank=True, null=True)  # Field name made lowercase.
    ignoreminorder = models.CharField(db_column='IgnoreMinOrder', max_length=1, blank=True, null=True)  # Field name made lowercase.
    export = models.CharField(db_column='Export', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exported = models.CharField(db_column='Exported', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    exportedtoedi = models.CharField(db_column='ExportedToEDI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    billing_id = models.AutoField(db_column='Billing_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Billing'


class Billingdet(TruncatedModel):
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    qtyord = models.IntegerField(db_column='QtyOrd', blank=True, null=True)  # Field name made lowercase.
    qtyshipped = models.IntegerField(db_column='QtyShipped', blank=True, null=True)  # Field name made lowercase.
    qtycancel = models.IntegerField(db_column='QtyCancel', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    discpct = models.SmallIntegerField(db_column='DiscPct', blank=True, null=True)  # Field name made lowercase.
    taxstatus = models.CharField(db_column='TaxStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    salesacct = models.CharField(db_column='SalesAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    commpct = models.SmallIntegerField(db_column='CommPct', blank=True, null=True)  # Field name made lowercase.
    glacct1 = models.CharField(db_column='GLAcct1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesamt1 = models.FloatField(db_column='SalesAmt1', blank=True, null=True)  # Field name made lowercase.
    glacct2 = models.CharField(db_column='GLAcct2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesamt2 = models.FloatField(db_column='SalesAmt2', blank=True, null=True)  # Field name made lowercase.
    glacct3 = models.CharField(db_column='GLAcct3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesamt3 = models.FloatField(db_column='SalesAmt3', blank=True, null=True)  # Field name made lowercase.
    glacct4 = models.CharField(db_column='GLAcct4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesamt4 = models.FloatField(db_column='SalesAmt4', blank=True, null=True)  # Field name made lowercase.
    glacct5 = models.CharField(db_column='GLAcct5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesamt5 = models.FloatField(db_column='SalesAmt5', blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    delticketdate = models.DateTimeField(db_column='DelTicketDate', blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invitemno = models.SmallIntegerField(db_column='InvItemNo', blank=True, null=True)  # Field name made lowercase.
    linetotal = models.FloatField(db_column='LineTotal', blank=True, null=True)  # Field name made lowercase.
    newdiscpct = models.FloatField(db_column='NewDiscPct', blank=True, null=True)  # Field name made lowercase.
    newcommpct = models.FloatField(db_column='NewCommPct', blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    billingdet_id = models.AutoField(db_column='BillingDet_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    istaxable = models.BooleanField(db_column='IsTaxable')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'BillingDet'


class Binlocations(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    binlocation = models.CharField(db_column='BinLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotnumber = models.CharField(db_column='LotNumber', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qtyonhand = models.FloatField(db_column='QtyOnHand', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateposted = models.DateTimeField(db_column='DatePosted', blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binlocations_id = models.AutoField(db_column='BinLocations_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'BinLocations'


class Car(TruncatedModel):
    correctiveactionno = models.CharField(db_column='CorrectiveActionNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    correctiveactioncode = models.CharField(db_column='CorrectiveActionCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cardate = models.DateTimeField(db_column='CARDate', blank=True, null=True)  # Field name made lowercase.
    qcmanager = models.CharField(db_column='QCManager', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custrmano = models.CharField(db_column='CustRMANo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    rmaitemno = models.SmallIntegerField(db_column='RMAItemNo', blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    qtyreturned = models.IntegerField(db_column='QtyReturned', blank=True, null=True)  # Field name made lowercase.
    qtytorework = models.IntegerField(db_column='QtyToRework', blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reasonforreturn = models.TextField(db_column='ReasonForReturn', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    authorization = models.CharField(db_column='Authorization', max_length=15, blank=True, null=True)  # Field name made lowercase.
    responsedue = models.DateTimeField(db_column='ResponseDue', blank=True, null=True)  # Field name made lowercase.
    rootcause = models.TextField(db_column='RootCause', blank=True, null=True)  # Field name made lowercase.
    immediateaction = models.TextField(db_column='ImmediateAction', blank=True, null=True)  # Field name made lowercase.
    permanentaction = models.TextField(db_column='PermanentAction', blank=True, null=True)  # Field name made lowercase.
    signatureonfile = models.CharField(db_column='SignatureOnFile', max_length=1, blank=True, null=True)  # Field name made lowercase.
    implementationdate = models.DateTimeField(db_column='ImplementationDate', blank=True, null=True)  # Field name made lowercase.
    verificationofimplementation = models.TextField(db_column='VerificationOfImplementation', blank=True, null=True)  # Field name made lowercase.
    verificationby = models.CharField(db_column='VerificationBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    verificationdate = models.DateTimeField(db_column='VerificationDate', blank=True, null=True)  # Field name made lowercase.
    verificationofeffectiveness = models.TextField(db_column='VerificationOfEffectiveness', blank=True, null=True)  # Field name made lowercase.
    verificationofeffectivenessby = models.CharField(db_column='VerificationOfEffectivenessBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    closeoutdate = models.DateTimeField(db_column='CloseOutDate', blank=True, null=True)  # Field name made lowercase.
    enterby = models.CharField(db_column='EnterBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    enterdate = models.DateTimeField(db_column='EnterDate', blank=True, null=True)  # Field name made lowercase.
    feedbackno = models.CharField(db_column='FeedbackNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    returntype = models.CharField(db_column='ReturnType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    vendreturnno = models.CharField(db_column='VendReturnNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendrmano = models.CharField(db_column='VendRMANo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    carprinted = models.CharField(db_column='CARPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    carjobno = models.CharField(db_column='CARJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    car_id = models.AutoField(db_column='CAR_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CAR'


class CduSpecial(TruncatedModel):
    cdu_special_id = models.AutoField(db_column='CDU_Special_ID', primary_key=True)  # Field name made lowercase.
    reportname = models.TextField(db_column='ReportName')  # Field name made lowercase.
    active = models.BooleanField(db_column='Active')  # Field name made lowercase.
    company_id = models.TextField(db_column='Company_ID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    specialid = models.TextField(db_column='SpecialID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CDU_Special'


class Check(TruncatedModel):
    checkno = models.CharField(db_column='CheckNo', unique=True, max_length=16, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True)  # Field name made lowercase.
    grossamt = models.FloatField(db_column='GrossAmt', blank=True, null=True)  # Field name made lowercase.
    discountamt = models.FloatField(db_column='DiscountAmt', blank=True, null=True)  # Field name made lowercase.
    netamt = models.FloatField(db_column='NetAmt', blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='BankCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    clearedbank = models.CharField(db_column='ClearedBank', max_length=1, blank=True, null=True)  # Field name made lowercase.
    periodno = models.CharField(db_column='PeriodNo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    procflag = models.SmallIntegerField(db_column='ProcFlag', blank=True, null=True)  # Field name made lowercase.
    checkposted = models.CharField(db_column='CheckPosted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendoracctno = models.CharField(db_column='VendorAcctNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    paytoline1 = models.CharField(db_column='PayToLine1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paytoline2 = models.CharField(db_column='PayToLine2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paytoline3 = models.CharField(db_column='PayToLine3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paytoline4 = models.CharField(db_column='PayToLine4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    checkprinted = models.CharField(db_column='CheckPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    vendcurrencycode = models.CharField(db_column='VendCurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendexchrate = models.FloatField(db_column='VendExchRate', blank=True, null=True)  # Field name made lowercase.
    exchrategainlossamt = models.FloatField(db_column='ExchRateGainLossAmt', blank=True, null=True)  # Field name made lowercase.
    check_id = models.AutoField(db_column='Check_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Check'


class Checkdet(TruncatedModel):
    checkno = models.CharField(db_column='CheckNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invtotal = models.FloatField(db_column='InvTotal', blank=True, null=True)  # Field name made lowercase.
    grossamt = models.FloatField(db_column='GrossAmt', blank=True, null=True)  # Field name made lowercase.
    discamt = models.FloatField(db_column='DiscAmt', blank=True, null=True)  # Field name made lowercase.
    netamt = models.FloatField(db_column='NetAmt', blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invexchrate = models.FloatField(db_column='InvExchRate', blank=True, null=True)  # Field name made lowercase.
    exchrategainloss = models.FloatField(db_column='ExchRateGainLoss', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    checkdet_id = models.AutoField(db_column='CheckDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CheckDet'


class Collectiondef(TruncatedModel):
    commport = models.SmallIntegerField(db_column='CommPort', blank=True, null=True)  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refreshsec = models.SmallIntegerField(db_column='RefreshSec', blank=True, null=True)  # Field name made lowercase.
    companycode = models.CharField(db_column='CompanyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    mode = models.CharField(db_column='Mode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    splitprocessing = models.CharField(db_column='SplitProcessing', max_length=1, blank=True, null=True)  # Field name made lowercase.
    connectstring = models.CharField(db_column='ConnectString', max_length=255, blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=12, blank=True, null=True)  # Field name made lowercase.
    collectiondef_id = models.AutoField(db_column='CollectionDef_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CollectionDef'


class Company(TruncatedModel):
    companycode = models.CharField(db_column='CompanyCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    defaultsecurity = models.CharField(db_column='DefaultSecurity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=255, blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(db_column='Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr2 = models.CharField(db_column='Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nextordnum = models.IntegerField(db_column='NextOrdNum', blank=True, null=True)  # Field name made lowercase.
    nextinvnum = models.IntegerField(db_column='NextInvNum', blank=True, null=True)  # Field name made lowercase.
    nextseqjobnum = models.IntegerField(db_column='NextSeqJobNum', blank=True, null=True)  # Field name made lowercase.
    nextponum = models.IntegerField(db_column='NextPONum', blank=True, null=True)  # Field name made lowercase.
    nextquotenum = models.IntegerField(db_column='NextQuoteNum', blank=True, null=True)  # Field name made lowercase.
    nextdelnum = models.IntegerField(db_column='NextDelNum', blank=True, null=True)  # Field name made lowercase.
    nextrecnum = models.IntegerField(db_column='NextRecNum', blank=True, null=True)  # Field name made lowercase.
    nextjournum = models.IntegerField(db_column='NextJourNum', blank=True, null=True)  # Field name made lowercase.
    nextrfqnum = models.IntegerField(db_column='NextRFQNum', blank=True, null=True)  # Field name made lowercase.
    payroll1 = models.CharField(db_column='Payroll1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll2 = models.CharField(db_column='Payroll2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll3 = models.CharField(db_column='Payroll3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll4 = models.CharField(db_column='Payroll4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll5 = models.CharField(db_column='Payroll5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll6 = models.CharField(db_column='Payroll6', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll7 = models.CharField(db_column='Payroll7', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll8 = models.CharField(db_column='Payroll8', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll9 = models.CharField(db_column='Payroll9', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payroll10 = models.CharField(db_column='Payroll10', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing1 = models.CharField(db_column='Billing1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing2 = models.CharField(db_column='Billing2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing3 = models.CharField(db_column='Billing3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing4 = models.CharField(db_column='Billing4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing5 = models.CharField(db_column='Billing5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing6 = models.CharField(db_column='Billing6', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing7 = models.CharField(db_column='Billing7', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing8 = models.CharField(db_column='Billing8', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing9 = models.CharField(db_column='Billing9', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billing10 = models.CharField(db_column='Billing10', max_length=12, blank=True, null=True)  # Field name made lowercase.
    contact1title = models.CharField(db_column='Contact1Title', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contact2title = models.CharField(db_column='Contact2Title', max_length=15, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditlim = models.FloatField(db_column='CreditLim', blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    printcert = models.CharField(db_column='PrintCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ap = models.CharField(db_column='AP', max_length=12, blank=True, null=True)  # Field name made lowercase.
    retearn = models.CharField(db_column='RetEarn', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currearn = models.CharField(db_column='CurrEarn', max_length=12, blank=True, null=True)  # Field name made lowercase.
    purchdisc = models.CharField(db_column='PurchDisc', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ar = models.CharField(db_column='AR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    inv = models.CharField(db_column='Inv', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cashdisc = models.CharField(db_column='CashDisc', max_length=12, blank=True, null=True)  # Field name made lowercase.
    freight = models.CharField(db_column='Freight', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salestax = models.CharField(db_column='SalesTax', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cashar = models.CharField(db_column='CashAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cashap = models.CharField(db_column='CashAP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bankcodear = models.CharField(db_column='BankCodeAR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    bankcodeap = models.CharField(db_column='BankCodeAP', max_length=12, blank=True, null=True)  # Field name made lowercase.
    decimals = models.SmallIntegerField(db_column='Decimals', blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billingrt = models.SmallIntegerField(db_column='BillingRt', blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    unitstock = models.CharField(db_column='UnitStock', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.CharField(db_column='UnitPrice', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qtybreak1 = models.IntegerField(db_column='QtyBreak1', blank=True, null=True)  # Field name made lowercase.
    qtybreak2 = models.IntegerField(db_column='QtyBreak2', blank=True, null=True)  # Field name made lowercase.
    qtybreak3 = models.IntegerField(db_column='QtyBreak3', blank=True, null=True)  # Field name made lowercase.
    qtybreak4 = models.IntegerField(db_column='QtyBreak4', blank=True, null=True)  # Field name made lowercase.
    qtybreak5 = models.IntegerField(db_column='QtyBreak5', blank=True, null=True)  # Field name made lowercase.
    qtybreak6 = models.IntegerField(db_column='QtyBreak6', blank=True, null=True)  # Field name made lowercase.
    qtybreak7 = models.IntegerField(db_column='QtyBreak7', blank=True, null=True)  # Field name made lowercase.
    qtybreak8 = models.IntegerField(db_column='QtyBreak8', blank=True, null=True)  # Field name made lowercase.
    drawingfiledir = models.CharField(db_column='DrawingFileDir', max_length=255, blank=True, null=True)  # Field name made lowercase.
    markup = models.FloatField(db_column='Markup', blank=True, null=True)  # Field name made lowercase.
    miscdescrip = models.CharField(db_column='MiscDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    addparts = models.CharField(db_column='AddParts', max_length=1, blank=True, null=True)  # Field name made lowercase.
    postparts = models.CharField(db_column='PostParts', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spool = models.CharField(db_column='Spool', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedmethod = models.CharField(db_column='SchedMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    jobnocreation = models.CharField(db_column='JobNoCreation', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttcyclesetup = models.CharField(db_column='TTCycleSetup', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttmilitary = models.CharField(db_column='TTMilitary', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttpayroll = models.SmallIntegerField(db_column='TTPayroll', blank=True, null=True)  # Field name made lowercase.
    ttmachrun = models.SmallIntegerField(db_column='TTMachRun', blank=True, null=True)  # Field name made lowercase.
    ttbillingrate = models.SmallIntegerField(db_column='TTBillingRate', blank=True, null=True)  # Field name made lowercase.
    ttshift = models.SmallIntegerField(db_column='TTShift', blank=True, null=True)  # Field name made lowercase.
    ttunattend = models.SmallIntegerField(db_column='TTUnattend', blank=True, null=True)  # Field name made lowercase.
    chkstart = models.SmallIntegerField(db_column='chkStart', blank=True, null=True)  # Field name made lowercase.
    chkend = models.SmallIntegerField(db_column='chkEnd', blank=True, null=True)  # Field name made lowercase.
    chkstepnumber = models.SmallIntegerField(db_column='chkStepNumber', blank=True, null=True)  # Field name made lowercase.
    chkworkcenter = models.SmallIntegerField(db_column='chkWorkCenter', blank=True, null=True)  # Field name made lowercase.
    chkopernum = models.SmallIntegerField(db_column='chkOperNum', blank=True, null=True)  # Field name made lowercase.
    chksetup = models.SmallIntegerField(db_column='chkSetup', blank=True, null=True)  # Field name made lowercase.
    chkcycle = models.SmallIntegerField(db_column='chkCycle', blank=True, null=True)  # Field name made lowercase.
    chkpcsgood = models.SmallIntegerField(db_column='chkPcsGood', blank=True, null=True)  # Field name made lowercase.
    chkpcsscrap = models.SmallIntegerField(db_column='chkPcsScrap', blank=True, null=True)  # Field name made lowercase.
    chkpayroll = models.SmallIntegerField(db_column='chkPayroll', blank=True, null=True)  # Field name made lowercase.
    chkmachrun = models.SmallIntegerField(db_column='chkMachRun', blank=True, null=True)  # Field name made lowercase.
    chkbilling = models.SmallIntegerField(db_column='chkBilling', blank=True, null=True)  # Field name made lowercase.
    chkshift = models.SmallIntegerField(db_column='chkShift', blank=True, null=True)  # Field name made lowercase.
    chkunattend = models.SmallIntegerField(db_column='chkUnattend', blank=True, null=True)  # Field name made lowercase.
    chkcomments = models.SmallIntegerField(db_column='chkComments', blank=True, null=True)  # Field name made lowercase.
    expandbom = models.CharField(db_column='ExpandBOM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worksat = models.CharField(db_column='WorkSat', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worksun = models.CharField(db_column='WorkSun', max_length=1, blank=True, null=True)  # Field name made lowercase.
    containerdesc = models.CharField(db_column='ContainerDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    specialinst = models.CharField(db_column='SpecialInst', max_length=100, blank=True, null=True)  # Field name made lowercase.
    containerunit = models.CharField(db_column='ContainerUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    autoorderno = models.CharField(db_column='AutoOrderNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    patchlevel = models.SmallIntegerField(db_column='PatchLevel', blank=True, null=True)  # Field name made lowercase.
    autojobno = models.CharField(db_column='AutoJobNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autoinvno = models.CharField(db_column='AutoInvNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autopono = models.CharField(db_column='AutoPONo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autoquoteno = models.CharField(db_column='AutoQuoteNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autodelticketno = models.CharField(db_column='AutoDelTicketNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autoreceiverno = models.CharField(db_column='AutoReceiverNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autojournalno = models.CharField(db_column='AutoJournalNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autorfqno = models.CharField(db_column='AutoRFQNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    barlen = models.FloatField(db_column='BarLen', blank=True, null=True)  # Field name made lowercase.
    matchdelticketno = models.CharField(db_column='MatchDelTicketNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    barloss = models.FloatField(db_column='BarLoss', blank=True, null=True)  # Field name made lowercase.
    cutoff = models.FloatField(db_column='CutOff', blank=True, null=True)  # Field name made lowercase.
    stockallow = models.FloatField(db_column='StockAllow', blank=True, null=True)  # Field name made lowercase.
    sheetlen = models.FloatField(db_column='SheetLen', blank=True, null=True)  # Field name made lowercase.
    sheetwid = models.FloatField(db_column='SheetWid', blank=True, null=True)  # Field name made lowercase.
    faceallow = models.FloatField(db_column='FaceAllow', blank=True, null=True)  # Field name made lowercase.
    logdatacoll = models.CharField(db_column='LogDataColl', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ltrhdallowance = models.CharField(db_column='LtrHdAllowance', max_length=12, blank=True, null=True)  # Field name made lowercase.
    numlines = models.SmallIntegerField(db_column='NumLines', blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    acctgmethod = models.CharField(db_column='AcctgMethod', max_length=6, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    followup = models.SmallIntegerField(db_column='Followup', blank=True, null=True)  # Field name made lowercase.
    expires = models.SmallIntegerField(db_column='Expires', blank=True, null=True)  # Field name made lowercase.
    hrsleftbypcs = models.CharField(db_column='HrsLeftByPcs', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shownonworkdays = models.CharField(db_column='ShowNonWorkdays', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scheddisplayperiod = models.CharField(db_column='SchedDisplayPeriod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scheddisplaymode = models.CharField(db_column='SchedDisplayMode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedshowcurrent = models.CharField(db_column='SchedShowCurrent', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedshowpending = models.CharField(db_column='SchedShowPending', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedshowfuture = models.CharField(db_column='SchedShowFuture', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedshowwhatif = models.CharField(db_column='SchedShowWhatIf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    showpastdue = models.CharField(db_column='ShowPastDue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    showfuture = models.CharField(db_column='ShowFuture', max_length=1, blank=True, null=True)  # Field name made lowercase.
    realtimesched = models.CharField(db_column='RealTimeSched', max_length=1, blank=True, null=True)  # Field name made lowercase.
    overlapsteps = models.CharField(db_column='OverlapSteps', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workmon = models.CharField(db_column='WorkMon', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worktue = models.CharField(db_column='WorkTue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workwed = models.CharField(db_column='WorkWed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workthu = models.CharField(db_column='WorkThu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workfri = models.CharField(db_column='WorkFri', max_length=1, blank=True, null=True)  # Field name made lowercase.
    runonshift1 = models.CharField(db_column='RunOnShift1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    runonshift2 = models.CharField(db_column='RunOnShift2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    runonshift3 = models.CharField(db_column='RunOnShift3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    estimationtype = models.CharField(db_column='EstimationType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    estimationpath = models.CharField(db_column='EstimationPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimumorder = models.FloatField(db_column='MinimumOrder', blank=True, null=True)  # Field name made lowercase.
    fedidnum = models.CharField(db_column='FedIDNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    logoimage = models.CharField(db_column='LogoImage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    printlogoonquote = models.CharField(db_column='PrintLogoOnQuote', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonrfq = models.CharField(db_column='PrintLogoOnRFQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonpo = models.CharField(db_column='PrintLogoOnPO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonacknowledgment = models.CharField(db_column='PrintLogoOnAcknowledgment', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonworkorder = models.CharField(db_column='PrintLogoOnWorkOrder', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonpackingslip = models.CharField(db_column='PrintLogoOnPackingSlip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogooninvoice = models.CharField(db_column='PrintLogoOnInvoice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogooncert = models.CharField(db_column='PrintLogoOnCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    division1 = models.CharField(db_column='Division1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division2 = models.CharField(db_column='Division2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division3 = models.CharField(db_column='Division3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division4 = models.CharField(db_column='Division4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division5 = models.CharField(db_column='Division5', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division6 = models.CharField(db_column='Division6', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division7 = models.CharField(db_column='Division7', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division8 = models.CharField(db_column='Division8', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division9 = models.CharField(db_column='Division9', max_length=30, blank=True, null=True)  # Field name made lowercase.
    division10 = models.CharField(db_column='Division10', max_length=30, blank=True, null=True)  # Field name made lowercase.
    payrolltype = models.CharField(db_column='PayrollType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    payrollimportfile = models.CharField(db_column='PayrollImportFile', max_length=255, blank=True, null=True)  # Field name made lowercase.
    payrollexportfile = models.CharField(db_column='PayrollExportFile', max_length=255, blank=True, null=True)  # Field name made lowercase.
    shoplayoutfile = models.CharField(db_column='ShopLayoutFile', max_length=255, blank=True, null=True)  # Field name made lowercase.
    printlogoonstmt = models.CharField(db_column='PrintLogoOnStmt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    purchemplcode = models.SmallIntegerField(db_column='PurchEmplCode', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pricetier = models.CharField(db_column='PriceTier', max_length=1, blank=True, null=True)  # Field name made lowercase.
    overwritebins = models.CharField(db_column='OverwriteBins', max_length=1, blank=True, null=True)  # Field name made lowercase.
    touchscruserid = models.CharField(db_column='TouchscrUserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    kerfallow = models.FloatField(db_column='KerfAllow', blank=True, null=True)  # Field name made lowercase.
    vertclampallow = models.FloatField(db_column='VertClampAllow', blank=True, null=True)  # Field name made lowercase.
    horizclampallow = models.FloatField(db_column='HorizClampAllow', blank=True, null=True)  # Field name made lowercase.
    inventorymethod = models.CharField(db_column='InventoryMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inventorydecimals = models.SmallIntegerField(db_column='InventoryDecimals', blank=True, null=True)  # Field name made lowercase.
    allowrobfromstockjobs = models.CharField(db_column='AllowRobFromStockJobs', max_length=1, blank=True, null=True)  # Field name made lowercase.
    treatuserdeffieldsasone = models.CharField(db_column='TreatUserDefFieldsAsOne', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datacollmustcompletepreviousstep = models.CharField(db_column='DataCollMustCompletePreviousStep', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datacollcantgooverqty = models.CharField(db_column='DataCollCantGoOverQty', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flagclosedjobs = models.CharField(db_column='FlagClosedJobs', max_length=1, blank=True, null=True)  # Field name made lowercase.
    roundttshiftstart = models.CharField(db_column='RoundTTShiftStart', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prodcodeorworkcode = models.CharField(db_column='ProdCodeOrWorkCode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    time2roundshift = models.SmallIntegerField(db_column='Time2RoundShift', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=250, blank=True, null=True)  # Field name made lowercase.
    autoreturnno = models.CharField(db_column='AutoReturnNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autocorractno = models.CharField(db_column='AutoCorrActNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autofeedbackno = models.CharField(db_column='AutoFeedbackNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reworkworkcode = models.CharField(db_column='ReworkWorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    restockingpct = models.FloatField(db_column='RestockingPct', blank=True, null=True)  # Field name made lowercase.
    prioritysortcriteria1 = models.CharField(db_column='PrioritySortCriteria1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prioritysortcriteria2 = models.CharField(db_column='PrioritySortCriteria2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prioritysortcriteria3 = models.CharField(db_column='PrioritySortCriteria3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prioritysortcriteria4 = models.CharField(db_column='PrioritySortCriteria4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    autovendreturnno = models.CharField(db_column='AutoVendReturnNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qbusediif = models.CharField(db_column='QBUsedIIF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    financechargeworkcode = models.CharField(db_column='FinanceChargeWorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    autoncno = models.CharField(db_column='AutoNCNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogooncorr = models.CharField(db_column='PrintLogoOnCorr', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonnonconf = models.CharField(db_column='PrintLogoOnNonConf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogooncustdeb = models.CharField(db_column='PrintLogoOnCustDeb', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printlogoonvenddeb = models.CharField(db_column='PrintLogoOnVendDeb', max_length=1, blank=True, null=True)  # Field name made lowercase.
    toolingprodcode = models.CharField(db_column='ToolingProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    loadingmethod = models.CharField(db_column='LoadingMethod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    utilizationpct = models.FloatField(db_column='UtilizationPct', blank=True, null=True)  # Field name made lowercase.
    autodocno = models.CharField(db_column='AutoDocNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    requiredoccontrol = models.CharField(db_column='RequireDocControl', max_length=1, blank=True, null=True)  # Field name made lowercase.
    edisoftorderimportpath = models.CharField(db_column='EDISoftOrderImportPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edisoftshipmentexportpath = models.CharField(db_column='EDISoftShipmentExportPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edisoftinvoiceexportpath = models.CharField(db_column='EDISoftInvoiceExportPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    schedcycletime = models.CharField(db_column='SchedCycleTime', max_length=12, blank=True, null=True)  # Field name made lowercase.
    schedforwardactive = models.SmallIntegerField(db_column='SchedForwardActive', blank=True, null=True)  # Field name made lowercase.
    schedbackward = models.SmallIntegerField(db_column='SchedBackward', blank=True, null=True)  # Field name made lowercase.
    schedforwardpast = models.SmallIntegerField(db_column='SchedForwardPast', blank=True, null=True)  # Field name made lowercase.
    autovue_url = models.TextField(db_column='Autovue_URL', blank=True, null=True)  # Field name made lowercase.
    company_id = models.AutoField(db_column='Company_ID', primary_key=True)  # Field name made lowercase.
    logorepositoryid = models.IntegerField(db_column='LogoRepositoryID', blank=True, null=True)  # Field name made lowercase.
    timezone = models.CharField(db_column='TimeZone', max_length=50, blank=True, null=True)  # Field name made lowercase.
    istriggerservicerunning = models.BooleanField(db_column='IsTriggerServiceRunning')  # Field name made lowercase.
    isinsetupmode = models.BooleanField(db_column='IsInSetupMode')  # Field name made lowercase.
    qbosynccustomerbilling = models.BooleanField(db_column='QBOSyncCustomerBilling')  # Field name made lowercase.
    qbosyncvendorinvoice = models.BooleanField(db_column='QBOSyncVendorInvoice')  # Field name made lowercase.
    qbosyncmarkcustomerpaid = models.BooleanField(db_column='QBOSyncMarkCustomerPaid')  # Field name made lowercase.
    qbosyncmarkvendorpaid = models.BooleanField(db_column='QBOSyncMarkVendorPaid')  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qbosyncupdateonsave = models.BooleanField(db_column='QBOSyncUpdateOnSave')  # Field name made lowercase.
    warnduplicatecustomerpo = models.NullBooleanField(db_column='WarnDuplicateCustomerPO')  # Field name made lowercase.
    qbcurrencycode = models.CharField(db_column='QBCurrencyCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    isovernightscheduling = models.BooleanField(db_column='IsOvernightScheduling')  # Field name made lowercase.
    qbosyncastenabled = models.BooleanField(db_column='QBOSyncASTEnabled')  # Field name made lowercase.
    qbosyncitemtaxabledefault = models.BooleanField(db_column='QBOSyncItemTaxableDefault')  # Field name made lowercase.
    defaultqbitemtype = models.CharField(db_column='DefaultQBItemType', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Company'


class Companycalendar(TruncatedModel):
    object = models.CharField(db_column='Object', max_length=12, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    searchdate = models.SmallIntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    hrsavail = models.FloatField(db_column='HrsAvail', blank=True, null=True)  # Field name made lowercase.
    schedbegin = models.CharField(db_column='SchedBegin', max_length=5, blank=True, null=True)  # Field name made lowercase.
    schedend = models.CharField(db_column='SchedEnd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    hrsavailshift1 = models.FloatField(db_column='HrsAvailShift1', blank=True, null=True)  # Field name made lowercase.
    hrsavailshift2 = models.FloatField(db_column='HrsAvailShift2', blank=True, null=True)  # Field name made lowercase.
    hrsavailshift3 = models.FloatField(db_column='HrsAvailShift3', blank=True, null=True)  # Field name made lowercase.
    shift1begin = models.CharField(db_column='Shift1Begin', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shift1end = models.CharField(db_column='Shift1End', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shift2begin = models.CharField(db_column='Shift2Begin', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shift2end = models.CharField(db_column='Shift2End', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shift3begin = models.CharField(db_column='Shift3Begin', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shift3end = models.CharField(db_column='Shift3End', max_length=5, blank=True, null=True)  # Field name made lowercase.
    capacityfactor = models.SmallIntegerField(db_column='CapacityFactor', blank=True, null=True)  # Field name made lowercase.
    shift2capacityfactor = models.SmallIntegerField(db_column='Shift2CapacityFactor', blank=True, null=True)  # Field name made lowercase.
    shift3capacityfactor = models.SmallIntegerField(db_column='Shift3CapacityFactor', blank=True, null=True)  # Field name made lowercase.
    defemplcode = models.CharField(db_column='DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shift2defemplcode = models.CharField(db_column='Shift2DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shift3defemplcode = models.CharField(db_column='Shift3DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    companycalendar_id = models.AutoField(db_column='CompanyCalendar_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CompanyCalendar'
        unique_together = (('object', 'code', 'searchdate'),)


class Companyshipto(TruncatedModel):
    location = models.CharField(db_column='Location', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(db_column='Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr2 = models.CharField(db_column='Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    default = models.CharField(db_column='Default', max_length=1, blank=True, null=True)  # Field name made lowercase.
    companyshipto_id = models.AutoField(db_column='CompanyShipTo_ID', primary_key=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CompanyShipTo'


class Condition(TruncatedModel):
    conditioncode = models.CharField(db_column='ConditionCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=120, blank=True, null=True)  # Field name made lowercase.
    sql = models.TextField(db_column='SQL', blank=True, null=True)  # Field name made lowercase.
    showinquickview = models.CharField(db_column='ShowInQuickView', max_length=1, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    isanexe = models.CharField(db_column='IsAnEXE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    exepath = models.CharField(db_column='EXEPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    conditiontype = models.CharField(db_column='ConditionType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    formname = models.CharField(db_column='FormName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateused = models.DateTimeField(db_column='DateUsed', blank=True, null=True)  # Field name made lowercase.
    condition_id = models.AutoField(db_column='Condition_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Condition'
        unique_together = (('userid', 'conditiontype', 'conditioncode'),)


class Contactnotes(TruncatedModel):
    object = models.CharField(db_column='Object', max_length=12, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    followupdate = models.DateTimeField(db_column='FollowUpDate', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    private = models.CharField(db_column='Private', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contactnotes_id = models.AutoField(db_column='ContactNotes_ID', primary_key=True)  # Field name made lowercase.
    completed = models.CharField(db_column='Completed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    duration = models.FloatField(db_column='Duration', blank=True, null=True)  # Field name made lowercase.
    result = models.CharField(db_column='Result', max_length=30, blank=True, null=True)  # Field name made lowercase.
    email_guid = models.CharField(db_column='Email_Guid', max_length=200, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ContactNotes'


class Contacts(TruncatedModel):
    object = models.CharField(db_column='Object', max_length=12, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=12, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=30, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    extension = models.CharField(db_column='Extension', max_length=10, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    is_web_user = models.CharField(db_column='IsWebUser', max_length=1, blank=True, null=True)  # Field name made lowercase.
    web_password = models.CharField(db_column='WebPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    see_web_job_status = models.CharField(db_column='SeeWebJobStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    see_web_dollars = models.CharField(db_column='SeeWebDollars', max_length=1, blank=True, null=True)  # Field name made lowercase.
    conferencing_server = models.CharField(db_column='ConferencingServer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    conferencing_address = models.CharField(db_column='ConferencingAddress', max_length=255, blank=True, null=True)  # Field name made lowercase.
    counter = models.SmallIntegerField(db_column='Counter', blank=True, primary_key=True, editable=False)
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cell_phone = models.CharField(db_column='Cell_Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    see_web_executive_overview = models.CharField(db_column='SeeWebExecutiveOverview', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Contacts'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Hack to not save the maturity and months_open as they are computed columns
        if not IS_TEST:
            self._meta.local_fields = [f for f in self._meta.local_fields if f.name not in ('counter')]
        super(Contacts, self).save(force_insert, force_update, using, update_fields)


class Container(TruncatedModel):
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    containernumber = models.SmallIntegerField(db_column='ContainerNumber', blank=True, null=True)  # Field name made lowercase.
    trackingnumber = models.CharField(db_column='TrackingNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    containerunit = models.CharField(db_column='ContainerUnit', max_length=5, blank=True, null=True)  # Field name made lowercase.
    hazardousmatl = models.CharField(db_column='HazardousMatl', max_length=1, blank=True, null=True)  # Field name made lowercase.
    insurance = models.CharField(db_column='Insurance', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emptyweight = models.FloatField(db_column='EmptyWeight', blank=True, null=True)  # Field name made lowercase.
    fullweight = models.FloatField(db_column='FullWeight', blank=True, null=True)  # Field name made lowercase.
    declaredvalue = models.FloatField(db_column='DeclaredValue', blank=True, null=True)  # Field name made lowercase.
    descripofcontents = models.TextField(db_column='DescripOfContents', blank=True, null=True)  # Field name made lowercase.
    container_id = models.AutoField(db_column='Container_ID', primary_key=True)  # Field name made lowercase.
    length = models.IntegerField(db_column='Length', blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    shiplabelrepositoryid = models.IntegerField(db_column='ShipLabelRepositoryID', blank=True, null=True)  # Field name made lowercase.
    codlabelrepositoryid = models.IntegerField(db_column='CODLabelRepositoryID', blank=True, null=True)  # Field name made lowercase.
    returnlabelrepositoryid = models.IntegerField(db_column='ReturnLabelRepositoryID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Container'
        unique_together = (('delticketno', 'containernumber'),)


class Containerdet(TruncatedModel):
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    containernumber = models.SmallIntegerField(db_column='ContainerNumber', blank=True, null=True)  # Field name made lowercase.
    qtyinbox = models.FloatField(db_column='QtyInBox', blank=True, null=True)  # Field name made lowercase.
    containerdet_id = models.AutoField(db_column='ContainerDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ContainerDet'


class Correctiveactioncode(TruncatedModel):
    correctiveactioncode = models.CharField(db_column='CorrectiveActionCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    correctiveactioncode_id = models.AutoField(db_column='CorrectiveActionCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CorrectiveActionCode'


class Country(TruncatedModel):
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    country_id = models.AutoField(db_column='Country_ID', primary_key=True)  # Field name made lowercase.
    abrv = models.CharField(db_column='Abrv', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Country'


class Currencycode(TruncatedModel):
    currencycode = models.CharField(db_column='CurrencyCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    buyrate = models.FloatField(db_column='BuyRate', blank=True, null=True)  # Field name made lowercase.
    sellrate = models.FloatField(db_column='SellRate', blank=True, null=True)  # Field name made lowercase.
    currencysymbol = models.CharField(db_column='CurrencySymbol', max_length=10, blank=True, null=True)  # Field name made lowercase.
    decimalsymbol = models.CharField(db_column='DecimalSymbol', max_length=1, blank=True, null=True)  # Field name made lowercase.
    thousandsseparator = models.CharField(db_column='ThousandsSeparator', max_length=1, blank=True, null=True)  # Field name made lowercase.
    decimalplaces = models.SmallIntegerField(db_column='DecimalPlaces', blank=True, null=True)  # Field name made lowercase.
    currencyformat = models.CharField(db_column='CurrencyFormat', max_length=1, blank=True, null=True)  # Field name made lowercase.
    negcurrencyformat = models.CharField(db_column='NegCurrencyFormat', max_length=2, blank=True, null=True)  # Field name made lowercase.
    formatshow = models.CharField(db_column='FormatShow', max_length=20, blank=True, null=True)  # Field name made lowercase.
    negformatshow = models.CharField(db_column='NegFormatShow', max_length=20, blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode_id = models.AutoField(db_column='CurrencyCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qbcurrencycode = models.CharField(db_column='QBCurrencyCode', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CurrencyCode'


class Currencyhist(TruncatedModel):
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    modby = models.CharField(db_column='ModBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    datemod = models.DateTimeField(db_column='DateMod', blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=90, blank=True, null=True)  # Field name made lowercase.
    currencyhist_id = models.AutoField(db_column='CurrencyHist_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CurrencyHist'


class CustomerCode(TruncatedModel):
    customer_code = models.CharField(db_column='CustCode', unique=True, max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    customer_name = models.CharField(db_column='CustName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    discperc = models.FloatField(db_column='DiscPerc', blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditlim = models.FloatField(db_column='CreditLim', blank=True, null=True)  # Field name made lowercase.
    currrecbal = models.FloatField(db_column='CurrRecBal', blank=True, null=True)  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    b_addr1 = models.CharField(db_column='BAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    b_addr2 = models.CharField(db_column='BAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    b_city = models.CharField(db_column='BCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    b_state = models.CharField(db_column='BState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    b_zip_code = models.CharField(db_column='BZIPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    b_country = models.CharField(db_column='BCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact1 = models.CharField(db_column='Contact1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact1phone = models.CharField(db_column='Contact1Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact2 = models.CharField(db_column='Contact2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact2phone = models.CharField(db_column='Contact2Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    apcontact = models.CharField(db_column='APContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    apphone = models.CharField(db_column='APPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    comments1 = models.TextField(db_column='Comments1', blank=True, null=True)  # Field name made lowercase.
    dateopen = models.DateTimeField(db_column='DateOpen', blank=True, null=True)  # Field name made lowercase.
    datelast = models.DateTimeField(db_column='DateLast', blank=True, null=True)  # Field name made lowercase.
    comments2 = models.TextField(db_column='Comments2', blank=True, null=True)  # Field name made lowercase.
    defpriority = models.SmallIntegerField(db_column='DefPriority', blank=True, null=True)  # Field name made lowercase.
    avgdays2pay = models.SmallIntegerField(db_column='AvgDays2Pay', blank=True, null=True)  # Field name made lowercase.
    avgrecage = models.SmallIntegerField(db_column='AvgRecAge', blank=True, null=True)  # Field name made lowercase.
    crstatus = models.CharField(db_column='CRStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ytdsales = models.FloatField(db_column='YTDSales', blank=True, null=True)  # Field name made lowercase.
    enterby = models.CharField(db_column='EnterBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    enterdate = models.DateTimeField(db_column='EnterDate', blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    minimumorder = models.FloatField(db_column='MinimumOrder', blank=True, null=True)  # Field name made lowercase.
    fedidnum = models.CharField(db_column='FedIDNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    iswebuser = models.CharField(db_column='IsWebUser', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webpassword = models.CharField(db_column='WebPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    seewebjobstatus = models.CharField(db_column='SeeWebJobStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    seewebdollars = models.CharField(db_column='SeeWebDollars', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pricetier = models.SmallIntegerField(db_column='PriceTier', blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=250, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    restockingpct = models.FloatField(db_column='RestockingPct', blank=True, null=True)  # Field name made lowercase.
    seewebexecutiveoverview = models.CharField(db_column='SeeWebExecutiveOverview', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustCode'


class CustReturn(TruncatedModel):
    custrmano = models.CharField(db_column='CustRMANo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custdesc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    issuedate = models.DateTimeField(db_column='IssueDate', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reasonforreturn = models.TextField(db_column='ReasonForReturn', blank=True, null=True)  # Field name made lowercase.
    receivedate = models.DateTimeField(db_column='ReceiveDate', blank=True, null=True)  # Field name made lowercase.
    receivedby = models.CharField(db_column='ReceivedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receivingcomment = models.TextField(db_column='ReceivingComment', blank=True, null=True)  # Field name made lowercase.
    inspectiondate = models.DateTimeField(db_column='InspectionDate', blank=True, null=True)  # Field name made lowercase.
    inspectedby = models.CharField(db_column='InspectedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qccomment = models.TextField(db_column='QCComment', blank=True, null=True)  # Field name made lowercase.
    correctiveactioncode = models.CharField(db_column='CorrectiveActionCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate', blank=True, null=True)  # Field name made lowercase.
    orderedby = models.CharField(db_column='OrderedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    creditdate = models.DateTimeField(db_column='CreditDate', blank=True, null=True)  # Field name made lowercase.
    creditedby = models.CharField(db_column='CreditedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    createcreditmemo = models.CharField(db_column='CreateCreditMemo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    billcustforreturn = models.CharField(db_column='BillCustForReturn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    createdinvoiceno = models.CharField(db_column='CreatedInvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    correctiveactionno = models.CharField(db_column='CorrectiveActionNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    createcar = models.CharField(db_column='CreateCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    createnc = models.CharField(db_column='CreateNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    labelprinted = models.CharField(db_column='LabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    debitprinted = models.CharField(db_column='DebitPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.
    custreturn_id = models.AutoField(db_column='CustReturn_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustReturn'


class CustReturnDet(TruncatedModel):
    custrmano = models.CharField(db_column='CustRMANo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    origjobno = models.CharField(db_column='OrigJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    origqtyshipped = models.IntegerField(db_column='OrigQtyShipped', blank=True, null=True)  # Field name made lowercase.
    qtytorework = models.IntegerField(db_column='QtyToRework', blank=True, null=True)  # Field name made lowercase.
    qtytorestock = models.IntegerField(db_column='QtyToRestock', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reworkjobno = models.CharField(db_column='ReworkJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    rmaitemno = models.SmallIntegerField(db_column='RMAItemNo', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    binlocation = models.CharField(db_column='BinLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotnumber = models.TextField(db_column='LotNumber', blank=True, null=True)  # Field name made lowercase.
    origorderno = models.CharField(db_column='OrigOrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dtitemno = models.SmallIntegerField(db_column='DTItemNo', blank=True, null=True)  # Field name made lowercase.
    qtyreturned = models.IntegerField(db_column='QtyReturned', blank=True, null=True)  # Field name made lowercase.
    qtygood = models.IntegerField(db_column='QtyGood', blank=True, null=True)  # Field name made lowercase.
    createcar = models.CharField(db_column='CreateCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reasoncode = models.CharField(db_column='ReasonCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    createnc = models.CharField(db_column='CreateNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nonconfno = models.CharField(db_column='NonConfNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correctiveactionno = models.CharField(db_column='CorrectiveActionNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    restockingpct = models.FloatField(db_column='RestockingPct', blank=True, null=True)  # Field name made lowercase.
    custreturndet_id = models.AutoField(db_column='CustReturnDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustReturnDet'


class CustReturnReleases(TruncatedModel):
    custrmano = models.CharField(db_column='CustRMANo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    rmaitemno = models.SmallIntegerField(db_column='RMAItemNo', blank=True, null=True)  # Field name made lowercase.
    qtytorework = models.IntegerField(db_column='QtyToRework', blank=True, null=True)  # Field name made lowercase.
    qtytorestock = models.IntegerField(db_column='QtyToRestock', blank=True, null=True)  # Field name made lowercase.
    binlocation = models.CharField(db_column='BinLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotno = models.TextField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    custreturnreleases_id = models.AutoField(db_column='CustReturnReleases_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustReturnReleases'


class CustomReport(TruncatedModel):
    documentid = models.IntegerField(db_column='DocumentID')  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    packedreport = models.TextField(db_column='PackedReport')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DateCreated')  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy')  # Field name made lowercase.
    customreport_id = models.AutoField(db_column='CustomReport_ID', primary_key=True)  # Field name made lowercase.
    cdu_id = models.TextField(db_column='CDU_ID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustomReport'


class CustomSecuritySetting(TruncatedModel):
    customsecuritysetting_id = models.AutoField(db_column='CustomSecuritySetting_ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12)  # Field name made lowercase.
    module = models.CharField(db_column='Module', max_length=255)  # Field name made lowercase.
    access = models.BooleanField(db_column='Access')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustomSecuritySetting'


class CustomerShipAccounts(TruncatedModel):
    cust_code = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    account_type = models.CharField(db_column='AccountType', max_length=15, blank=True, null=True)  # Field name made lowercase.
    account_number = models.CharField(db_column='AccountNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=150, blank=True, null=True)  # Field name made lowercase.
    last_mod_date = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    last_mod_user = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    customer_ship_accounts_id = models.AutoField(db_column='CustomerShipAccounts_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CustomerShipAccounts'


class CutList(TruncatedModel):
    part_no = models.CharField(db_column='PartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sub_part_no = models.CharField(db_column='SubPartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    num_times = models.FloatField(db_column='NumTimes', blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    linear_qty = models.FloatField(db_column='LinearQty', blank=True, null=True)  # Field name made lowercase.
    stock_unit = models.CharField(db_column='StockUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    total_wt = models.FloatField(db_column='TotalWt', blank=True, null=True)  # Field name made lowercase.
    total_qty = models.FloatField(db_column='TotalQty', blank=True, null=True)  # Field name made lowercase.
    cut_list_id = models.AutoField(db_column='CutList_ID', primary_key=True)  # Field name made lowercase.
    last_mod_date = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    last_mod_user = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'CutList'


class Dcd(TruncatedModel):
    dcd = models.SmallIntegerField(db_column='DCD', unique=True, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    def_work_cntr = models.CharField(db_column='DefWorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    def_oper_code = models.CharField(db_column='DefOperCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    def_pay_rate = models.SmallIntegerField(db_column='DefPayRate', blank=True, null=True)  # Field name made lowercase.
    def_mach_run = models.SmallIntegerField(db_column='DefMachRun', blank=True, null=True)  # Field name made lowercase.
    def_setup_time = models.FloatField(db_column='DefSetupTime', blank=True, null=True)  # Field name made lowercase.
    def_pieces_finished = models.FloatField(db_column='DefPiecesFinished', blank=True, null=True)  # Field name made lowercase.
    def_pieces_scrapped = models.FloatField(db_column='DefPiecesScrapped', blank=True, null=True)  # Field name made lowercase.
    def_cycle_time = models.FloatField(db_column='DefCycleTime', blank=True, null=True)  # Field name made lowercase.
    def_empl_num = models.SmallIntegerField(db_column='DefEmplNum', blank=True, null=True)  # Field name made lowercase.
    def_job_num = models.CharField(db_column='DefJobNum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    def_seq_num = models.SmallIntegerField(db_column='DefSeqNum', blank=True, null=True)  # Field name made lowercase.
    allow_batch = models.CharField(db_column='AllowBatch', max_length=1, blank=True, null=True)  # Field name made lowercase.
    post_2_closed = models.CharField(db_column='Post2Closed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_multiple = models.CharField(db_column='AllowMultiple', max_length=1, blank=True, null=True)  # Field name made lowercase.
    attend_code = models.SmallIntegerField(db_column='AttendCode', blank=True, null=True)  # Field name made lowercase.
    prompt_4_next_wc = models.CharField(db_column='Prompt4NextWC', max_length=12, blank=True, null=True)  # Field name made lowercase.
    override_bar_code = models.CharField(db_column='OverrideBarCode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terminal_type = models.CharField(db_column='TerminalType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ip_address = models.CharField(db_column='IPAddress', max_length=30, blank=True, null=True)  # Field name made lowercase.
    port = models.SmallIntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=12, blank=True, null=True)  # Field name made lowercase.
    prompt_4_reason_code = models.CharField(db_column='Prompt4ReasonCode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dcd_id = models.AutoField(db_column='DCD_ID', primary_key=True)  # Field name made lowercase.
    last_mod_date = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    last_mod_user = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DCD'


class Dashboard(TruncatedModel):
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    date_ent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    ent_by = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    last_mod_date = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    last_mod_user = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dashboard_id = models.AutoField(db_column='Dashboard_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Dashboard'


class Dashboardpanel(TruncatedModel):
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dashboard_id = models.IntegerField(db_column='Dashboard_ID', blank=True, null=True)  # Field name made lowercase.
    rowindex = models.IntegerField(db_column='RowIndex', blank=True, null=True)  # Field name made lowercase.
    columnindex = models.IntegerField(db_column='ColumnIndex', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    displaytype = models.CharField(db_column='DisplayType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dashboardreport_id = models.IntegerField(db_column='DashboardReport_ID', blank=True, null=True)  # Field name made lowercase.
    xaxisfield = models.CharField(db_column='XAxisField', max_length=255, blank=True, null=True)  # Field name made lowercase.
    xaxislabel = models.CharField(db_column='XAxisLabel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yaxisfield = models.CharField(db_column='YAxisField', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yaxislabel = models.CharField(db_column='YAxisLabel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    piecategoryfield = models.CharField(db_column='PieCategoryField', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pievaluefield = models.CharField(db_column='PieValueField', max_length=255, blank=True, null=True)  # Field name made lowercase.
    headlinefield = models.CharField(db_column='HeadlineField', max_length=255, blank=True, null=True)  # Field name made lowercase.
    headlinefunction = models.CharField(db_column='HeadlineFunction', max_length=30, blank=True, null=True)  # Field name made lowercase.
    headlinedescription = models.TextField(db_column='HeadlineDescription', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dashboardpanel_id = models.AutoField(db_column='DashboardPanel_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DashboardPanel'


class Dashboardpaneltablefield(TruncatedModel):
    fieldname = models.CharField(db_column='FieldName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fieldindex = models.IntegerField(db_column='FieldIndex', blank=True, null=True)  # Field name made lowercase.
    dashboardpanel_id = models.IntegerField(db_column='DashboardPanel_ID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dashboardpaneltablefield_id = models.AutoField(db_column='DashboardPanelTableField_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DashboardPanelTableField'


class Dashboardreport(TruncatedModel):
    title = models.CharField(db_column='Title', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    dashboard_id = models.IntegerField(db_column='Dashboard_ID', blank=True, null=True)  # Field name made lowercase.
    reporttype = models.CharField(db_column='ReportType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reportcode = models.CharField(db_column='ReportCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    groupby = models.CharField(db_column='GroupBy', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateoption1 = models.CharField(db_column='DateOption1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datebegin1 = models.DateTimeField(db_column='DateBegin1', blank=True, null=True)  # Field name made lowercase.
    dateend1 = models.DateTimeField(db_column='DateEnd1', blank=True, null=True)  # Field name made lowercase.
    dateoption2 = models.CharField(db_column='DateOption2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datebegin2 = models.DateTimeField(db_column='DateBegin2', blank=True, null=True)  # Field name made lowercase.
    dateend2 = models.DateTimeField(db_column='DateEnd2', blank=True, null=True)  # Field name made lowercase.
    textoption1 = models.CharField(db_column='TextOption1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    booloption1 = models.NullBooleanField(db_column='BoolOption1')  # Field name made lowercase.
    reportdata = models.BinaryField(db_column='ReportData', blank=True, null=True)  # Field name made lowercase.
    lastreportdate = models.DateTimeField(db_column='LastReportDate', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dashboardreport_id = models.AutoField(db_column='DashboardReport_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DashboardReport'


class Dashboarduser(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dashboard_id = models.IntegerField(db_column='Dashboard_ID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dashboarduser_id = models.AutoField(db_column='DashboardUser_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DashboardUser'


class Datacollevents(TruncatedModel):
    deviceno = models.SmallIntegerField(db_column='DeviceNo', blank=True, null=True)  # Field name made lowercase.
    duration = models.SmallIntegerField(db_column='Duration', blank=True, null=True)  # Field name made lowercase.
    timestart = models.DateTimeField(db_column='TimeStart', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datacollevents_id = models.AutoField(db_column='DataCollEvents_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DataCollEvents'


class Datadictionary(TruncatedModel):
    fieldname = models.CharField(db_column='FieldName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datadictionary_id = models.AutoField(db_column='DataDictionary_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DataDictionary'


class Databaseversion(TruncatedModel):
    databaseversion = models.CharField(db_column='DatabaseVersion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isbeingupdated = models.NullBooleanField(db_column='IsBeingUpdated')  # Field name made lowercase.
    updatekey = models.CharField(db_column='UpdateKey', max_length=128, blank=True, null=True)  # Field name made lowercase.
    databaseversion_id = models.AutoField(db_column='DatabaseVersion_ID', primary_key=True)  # Field name made lowercase.
    isdblocked = models.BooleanField(db_column='IsDBLocked')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DatabaseVersion'


class Defaultfiles(TruncatedModel):
    companycode = models.CharField(db_column='CompanyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    printwithtrav = models.CharField(db_column='PrintWithTrav', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithwo = models.CharField(db_column='PrintWithWO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithack = models.CharField(db_column='PrintWithAck', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithquote = models.CharField(db_column='PrintWithQuote', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithdt = models.CharField(db_column='PrintWithDT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithpo = models.CharField(db_column='PrintWithPO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithcert = models.CharField(db_column='PrintWithCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    printwithrfq = models.CharField(db_column='PrintWithRFQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithinvoice = models.CharField(db_column='PrintWithInvoice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    defaultfiles_id = models.AutoField(db_column='DefaultFiles_ID', primary_key=True)  # Field name made lowercase.
    printwithcar = models.CharField(db_column='PrintWithCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithnc = models.CharField(db_column='PrintWithNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    docnumber = models.CharField(db_column='DocNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)  # Field name made lowercase.
    repositoryid = models.IntegerField(db_column='RepositoryID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DefaultFiles'


class Delticket(TruncatedModel):
    delticketno = models.CharField(db_column='DelTicketNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custdesc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipdate = models.DateTimeField(db_column='ShipDate', blank=True, null=True)  # Field name made lowercase.
    procflag = models.SmallIntegerField(db_column='ProcFlag', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shippingchgs = models.FloatField(db_column='ShippingChgs', blank=True, null=True)  # Field name made lowercase.
    dtprinted = models.CharField(db_column='DTPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certprinted = models.CharField(db_column='CertPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    labelprinted = models.CharField(db_column='LabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autobill = models.CharField(db_column='AutoBill', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipaddr1 = models.CharField(db_column='ShipAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipaddr2 = models.CharField(db_column='ShipAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipcity = models.CharField(db_column='ShipCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipst = models.CharField(db_column='ShipSt', max_length=2, blank=True, null=True)  # Field name made lowercase.
    shipzip = models.CharField(db_column='ShipZIP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    notes2cust = models.TextField(db_column='Notes2Cust', blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    numcontainers = models.SmallIntegerField(db_column='NumContainers', blank=True, null=True)  # Field name made lowercase.
    freightvendcode = models.CharField(db_column='FreightVendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    containerwt = models.FloatField(db_column='ContainerWt', blank=True, null=True)  # Field name made lowercase.
    descripofcontents = models.TextField(db_column='DescripOfContents', blank=True, null=True)  # Field name made lowercase.
    codamt = models.FloatField(db_column='CODAmt', blank=True, null=True)  # Field name made lowercase.
    freightterms = models.CharField(db_column='FreightTerms', max_length=1, blank=True, null=True)  # Field name made lowercase.
    specialinstructions = models.TextField(db_column='SpecialInstructions', blank=True, null=True)  # Field name made lowercase.
    containerunit = models.CharField(db_column='ContainerUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    weightofparts = models.FloatField(db_column='WeightOfParts', blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    remitname = models.CharField(db_column='RemitName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    remitaddr1 = models.CharField(db_column='RemitAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remitaddr2 = models.CharField(db_column='RemitAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remitcity = models.CharField(db_column='RemitCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remitst = models.CharField(db_column='RemitSt', max_length=2, blank=True, null=True)  # Field name made lowercase.
    remitzip = models.CharField(db_column='RemitZIP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    remitcountry = models.CharField(db_column='RemitCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    codfee = models.FloatField(db_column='CODFee', blank=True, null=True)  # Field name made lowercase.
    freightcharge = models.FloatField(db_column='FreightCharge', blank=True, null=True)  # Field name made lowercase.
    codfeeprepaid = models.CharField(db_column='CODFeePrepaid', max_length=1, blank=True, null=True)  # Field name made lowercase.
    freightchargeprepaid = models.CharField(db_column='FreightChargePrepaid', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codamountprepaid = models.CharField(db_column='CODAmountPrepaid', max_length=1, blank=True, null=True)  # Field name made lowercase.
    containeroption = models.SmallIntegerField(db_column='ContainerOption', blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    handlingchg = models.FloatField(db_column='HandlingChg', blank=True, null=True)  # Field name made lowercase.
    exported = models.CharField(db_column='Exported', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    exportedtoedi = models.CharField(db_column='ExportedToEDI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    canbolprinted = models.CharField(db_column='CanBOLPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cancooprinted = models.CharField(db_column='CanCOOPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    canciprinted = models.CharField(db_column='CanCIPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.
    delticket_id = models.AutoField(db_column='DelTicket_ID', primary_key=True)  # Field name made lowercase.
    isshipmentfromsystem = models.NullBooleanField(db_column='IsShipmentFromSystem')  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DelTicket'


class Delticketdet(TruncatedModel):
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    qtyopen = models.IntegerField(db_column='QtyOpen', blank=True, null=True)  # Field name made lowercase.
    qty2ship = models.IntegerField(db_column='Qty2Ship', blank=True, null=True)  # Field name made lowercase.
    qty2stock = models.IntegerField(db_column='Qty2Stock', blank=True, null=True)  # Field name made lowercase.
    qty2cancel = models.IntegerField(db_column='Qty2Cancel', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    masterjobno = models.CharField(db_column='MasterJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    dtitemno = models.SmallIntegerField(db_column='DTItemNo', blank=True, null=True)  # Field name made lowercase.
    partwt = models.FloatField(db_column='PartWt', blank=True, null=True)  # Field name made lowercase.
    qtyfromstock = models.IntegerField(db_column='QtyFromStock', blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    containernumber = models.CharField(db_column='ContainerNumber', max_length=12, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    delticketdet_id = models.AutoField(db_column='DelTicketDet_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    istaxable = models.BooleanField(db_column='IsTaxable')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DelTicketDet'


class Dept(TruncatedModel):
    deptnum = models.CharField(db_column='DeptNum', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dept_id = models.AutoField(db_column='Dept_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Dept'


class Dispatch(TruncatedModel):
    workcntr = models.SmallIntegerField(db_column='WorkCntr', blank=True, null=True)  # Field name made lowercase.
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    pcteff = models.SmallIntegerField(db_column='PctEff', blank=True, null=True)  # Field name made lowercase.
    altworkcntr = models.SmallIntegerField(db_column='AltWorkCntr', blank=True, null=True)  # Field name made lowercase.
    altemplcode = models.SmallIntegerField(db_column='AltEmplCode', blank=True, null=True)  # Field name made lowercase.
    dispatch_id = models.AutoField(db_column='Dispatch_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Dispatch'


class Divisions(TruncatedModel):
    divisionno = models.IntegerField(db_column='DivisionNo', unique=True, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=30, blank=True, null=True)  # Field name made lowercase.
    divisions_id = models.AutoField(db_column='Divisions_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Divisions'


class Document(TruncatedModel):
    reportname = models.CharField(db_column='ReportName', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    document_id = models.IntegerField(db_column='Document_ID', primary_key=True)  # Field name made lowercase.
    filename = models.TextField(db_column='FileName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Document'


class Documentcontrol(TruncatedModel):
    docnumber = models.CharField(db_column='DocNumber', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate', blank=True, null=True)  # Field name made lowercase.
    docstatus = models.CharField(db_column='DocStatus', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)  # Field name made lowercase.
    filelocation = models.CharField(db_column='FileLocation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    proposedby = models.CharField(db_column='ProposedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    proposaldate = models.DateTimeField(db_column='ProposalDate', blank=True, null=True)  # Field name made lowercase.
    proposalcomments = models.TextField(db_column='ProposalComments', blank=True, null=True)  # Field name made lowercase.
    approvedby = models.CharField(db_column='ApprovedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    approvaldate = models.DateTimeField(db_column='ApprovalDate', blank=True, null=True)  # Field name made lowercase.
    approvalcomments = models.TextField(db_column='ApprovalComments', blank=True, null=True)  # Field name made lowercase.
    releasedby = models.CharField(db_column='ReleasedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    releasedate = models.DateTimeField(db_column='ReleaseDate', blank=True, null=True)  # Field name made lowercase.
    releasecomments = models.TextField(db_column='ReleaseComments', blank=True, null=True)  # Field name made lowercase.
    retiredby = models.CharField(db_column='RetiredBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    retirementdate = models.DateTimeField(db_column='RetirementDate', blank=True, null=True)  # Field name made lowercase.
    retirementcomments = models.TextField(db_column='RetirementComments', blank=True, null=True)  # Field name made lowercase.
    printed = models.CharField(db_column='Printed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    documentcontrol_id = models.AutoField(db_column='DocumentControl_ID', primary_key=True)  # Field name made lowercase.
    repositoryid = models.IntegerField(db_column='RepositoryID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DocumentControl'


class Documentcontrolhistory(TruncatedModel):
    docnumber = models.CharField(db_column='DocNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    filelocation = models.CharField(db_column='FileLocation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    updatedparts = models.CharField(db_column='UpdatedParts', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updatedjobs = models.CharField(db_column='UpdatedJobs', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spunofffile = models.CharField(db_column='SpunOffFile', max_length=1, blank=True, null=True)  # Field name made lowercase.
    documentcontrolhistory_id = models.AutoField(db_column='DocumentControlHistory_ID', primary_key=True)  # Field name made lowercase.
    repositoryid = models.IntegerField(db_column='RepositoryID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DocumentControlHistory'


class Documentreview(TruncatedModel):
    docnumber = models.CharField(db_column='DocNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reviewcode = models.CharField(db_column='ReviewCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    completed = models.CharField(db_column='Completed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    documentreview_id = models.AutoField(db_column='DocumentReview_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DocumentReview'


class Documenttype(TruncatedModel):
    documenttype = models.CharField(db_column='DocumentType', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    documenttype_id = models.AutoField(db_column='DocumentType_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'DocumentType'


class Emplcode(TruncatedModel):
    emplcode = models.SmallIntegerField(db_column='EmplCode', unique=True, blank=True, null=True)  # Field name made lowercase.
    emplname = models.CharField(db_column='EmplName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shift = models.SmallIntegerField(db_column='Shift', blank=True, null=True)  # Field name made lowercase.
    rate1 = models.FloatField(db_column='Rate1', blank=True, null=True)  # Field name made lowercase.
    rate2 = models.FloatField(db_column='Rate2', blank=True, null=True)  # Field name made lowercase.
    rate3 = models.FloatField(db_column='Rate3', blank=True, null=True)  # Field name made lowercase.
    rate4 = models.FloatField(db_column='Rate4', blank=True, null=True)  # Field name made lowercase.
    rate5 = models.FloatField(db_column='Rate5', blank=True, null=True)  # Field name made lowercase.
    rate6 = models.FloatField(db_column='Rate6', blank=True, null=True)  # Field name made lowercase.
    rate7 = models.FloatField(db_column='Rate7', blank=True, null=True)  # Field name made lowercase.
    rate8 = models.FloatField(db_column='Rate8', blank=True, null=True)  # Field name made lowercase.
    rate9 = models.FloatField(db_column='Rate9', blank=True, null=True)  # Field name made lowercase.
    rate10 = models.FloatField(db_column='Rate10', blank=True, null=True)  # Field name made lowercase.
    hiredate = models.DateTimeField(db_column='HireDate', blank=True, null=True)  # Field name made lowercase.
    termdate = models.DateTimeField(db_column='TermDate', blank=True, null=True)  # Field name made lowercase.
    lastreview = models.DateTimeField(db_column='LastReview', blank=True, null=True)  # Field name made lowercase.
    nextreview = models.DateTimeField(db_column='NextReview', blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(db_column='Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr2 = models.CharField(db_column='Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='SSN', max_length=11, blank=True, null=True)  # Field name made lowercase.
    defpayrollrate = models.SmallIntegerField(db_column='DefPayrollRate', blank=True, null=True)  # Field name made lowercase.
    emplshortname = models.CharField(db_column='EmplShortName', max_length=5, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    break1time = models.CharField(db_column='Break1Time', max_length=4, blank=True, null=True)  # Field name made lowercase.
    break1duration = models.SmallIntegerField(db_column='Break1Duration', blank=True, null=True)  # Field name made lowercase.
    break2time = models.CharField(db_column='Break2Time', max_length=4, blank=True, null=True)  # Field name made lowercase.
    break2duration = models.SmallIntegerField(db_column='Break2Duration', blank=True, null=True)  # Field name made lowercase.
    break3time = models.CharField(db_column='Break3Time', max_length=4, blank=True, null=True)  # Field name made lowercase.
    break3duration = models.SmallIntegerField(db_column='Break3Duration', blank=True, null=True)  # Field name made lowercase.
    break4time = models.CharField(db_column='Break4Time', max_length=4, blank=True, null=True)  # Field name made lowercase.
    break4duration = models.SmallIntegerField(db_column='Break4Duration', blank=True, null=True)  # Field name made lowercase.
    deptnum = models.CharField(db_column='DeptNum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shiftbeg = models.CharField(db_column='ShiftBeg', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shiftend = models.CharField(db_column='ShiftEnd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    otmethod = models.CharField(db_column='OTMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otthreshold = models.SmallIntegerField(db_column='OTThreshold', blank=True, null=True)  # Field name made lowercase.
    otfactor = models.FloatField(db_column='OTFactor', blank=True, null=True)  # Field name made lowercase.
    worksaturday = models.CharField(db_column='WorkSaturday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worksunday = models.CharField(db_column='WorkSunday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workmonday = models.CharField(db_column='WorkMonday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worktuesday = models.CharField(db_column='WorkTuesday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workwednesday = models.CharField(db_column='WorkWednesday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workthursday = models.CharField(db_column='WorkThursday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workfriday = models.CharField(db_column='WorkFriday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    applyautobreak = models.CharField(db_column='ApplyAutoBreak', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emplcodeimagefile = models.CharField(db_column='EmplCodeImageFile', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    allowbatchatclock = models.CharField(db_column='AllowBatchAtClock', max_length=1, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    newemplshortname = models.CharField(db_column='NewEmplShortName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    emplcode_id = models.AutoField(db_column='EmplCode_ID', primary_key=True)  # Field name made lowercase.
    imagerepositoryid = models.IntegerField(db_column='ImageRepositoryID', blank=True, null=True)  # Field name made lowercase.
    isgeofenceenabled = models.NullBooleanField(db_column='IsGeoFenceEnabled')  # Field name made lowercase.
    geofenceradius = models.FloatField(db_column='GeoFenceRadius', blank=True, null=True)  # Field name made lowercase.
    isssidfenceenabled = models.NullBooleanField(db_column='IsSSIDFenceEnabled')  # Field name made lowercase.
    ssid = models.CharField(db_column='SSID', max_length=64, blank=True, null=True)  # Field name made lowercase.
    companyshiptolocation = models.CharField(db_column='CompanyShipToLocation', max_length=30, blank=True, null=True)  # Field name made lowercase.
    isdatacollectionuser = models.NullBooleanField(db_column='IsDataCollectionUser')  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    signaturerepositoryid = models.IntegerField(db_column='SignatureRepositoryID', blank=True, null=True)  # Field name made lowercase.
    signatureimagefile = models.CharField(db_column='SignatureImageFile', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'EmplCode'


class Empltraining(TruncatedModel):
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    emplname = models.CharField(db_column='EmplName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    trainingcode = models.CharField(db_column='TrainingCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    instructor = models.CharField(db_column='Instructor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    empltraining_id = models.AutoField(db_column='EmplTraining_ID', primary_key=True)  # Field name made lowercase.
    completed = models.CharField(db_column='Completed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'EmplTraining'


class Errors(TruncatedModel):
    errornum = models.IntegerField(db_column='ErrorNum', unique=True, blank=True, null=True)  # Field name made lowercase.
    errorexpl = models.CharField(db_column='ErrorExpl', max_length=100, blank=True, null=True)  # Field name made lowercase.
    errordetail = models.TextField(db_column='ErrorDetail', blank=True, null=True)  # Field name made lowercase.
    errorlevel = models.SmallIntegerField(db_column='ErrorLevel', blank=True, null=True)  # Field name made lowercase.
    errors_id = models.AutoField(db_column='Errors_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Errors'


class Estim(TruncatedModel):
    partno = models.CharField(db_column='PartNo', unique=True, max_length=30, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    altpartno = models.CharField(db_column='AltPartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    entdate = models.DateTimeField(db_column='EntDate', blank=True, null=True)  # Field name made lowercase.
    pricingunit = models.CharField(db_column='PricingUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty1 = models.IntegerField(db_column='Qty1', blank=True, null=True)  # Field name made lowercase.
    price1 = models.FloatField(db_column='Price1', blank=True, null=True)  # Field name made lowercase.
    qty2 = models.IntegerField(db_column='Qty2', blank=True, null=True)  # Field name made lowercase.
    price2 = models.FloatField(db_column='Price2', blank=True, null=True)  # Field name made lowercase.
    qty3 = models.IntegerField(db_column='Qty3', blank=True, null=True)  # Field name made lowercase.
    price3 = models.FloatField(db_column='Price3', blank=True, null=True)  # Field name made lowercase.
    qty4 = models.IntegerField(db_column='Qty4', blank=True, null=True)  # Field name made lowercase.
    price4 = models.FloatField(db_column='Price4', blank=True, null=True)  # Field name made lowercase.
    qty5 = models.IntegerField(db_column='Qty5', blank=True, null=True)  # Field name made lowercase.
    price5 = models.FloatField(db_column='Price5', blank=True, null=True)  # Field name made lowercase.
    qty6 = models.IntegerField(db_column='Qty6', blank=True, null=True)  # Field name made lowercase.
    price6 = models.FloatField(db_column='Price6', blank=True, null=True)  # Field name made lowercase.
    qty7 = models.IntegerField(db_column='Qty7', blank=True, null=True)  # Field name made lowercase.
    price7 = models.FloatField(db_column='Price7', blank=True, null=True)  # Field name made lowercase.
    qty8 = models.IntegerField(db_column='Qty8', blank=True, null=True)  # Field name made lowercase.
    price8 = models.FloatField(db_column='Price8', blank=True, null=True)  # Field name made lowercase.
    lastpricechg = models.DateTimeField(db_column='LastPriceChg', blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billingrate = models.SmallIntegerField(db_column='BillingRate', blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revdate = models.DateTimeField(db_column='RevDate', blank=True, null=True)  # Field name made lowercase.
    drawnum = models.CharField(db_column='DrawNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partwt = models.FloatField(db_column='PartWt', blank=True, null=True)  # Field name made lowercase.
    commpct = models.FloatField(db_column='CommPct', blank=True, null=True)  # Field name made lowercase.
    miscchg = models.FloatField(db_column='MiscChg', blank=True, null=True)  # Field name made lowercase.
    miscdescrip = models.CharField(db_column='MiscDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    routeempl = models.CharField(db_column='RouteEmpl', max_length=12, blank=True, null=True)  # Field name made lowercase.
    routedate = models.DateTimeField(db_column='RouteDate', blank=True, null=True)  # Field name made lowercase.
    drawingfilename = models.CharField(db_column='DrawingFileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    globalmarkuppct = models.FloatField(db_column='GlobalMarkupPct', blank=True, null=True)  # Field name made lowercase.
    ljno = models.CharField(db_column='LJNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ljqty = models.FloatField(db_column='LJQty', blank=True, null=True)  # Field name made lowercase.
    ljdatefin = models.DateTimeField(db_column='LJDateFin', blank=True, null=True)  # Field name made lowercase.
    ljprice = models.FloatField(db_column='LJPrice', blank=True, null=True)  # Field name made lowercase.
    ljquoteno = models.CharField(db_column='LJQuoteNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ljdate = models.DateTimeField(db_column='LJDate', blank=True, null=True)  # Field name made lowercase.
    qtyip = models.FloatField(db_column='QtyIP', blank=True, null=True)  # Field name made lowercase.
    lastdelticketno = models.CharField(db_column='LastDelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastdelticketdate = models.DateTimeField(db_column='LastDelTicketDate', blank=True, null=True)  # Field name made lowercase.
    lastdelticketqty = models.IntegerField(db_column='LastDelTicketQty', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    stockunit = models.CharField(db_column='StockUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qtyonhand = models.FloatField(db_column='QtyOnHand', blank=True, null=True)  # Field name made lowercase.
    reordlevel = models.IntegerField(db_column='ReOrdLevel', blank=True, null=True)  # Field name made lowercase.
    reordqty = models.IntegerField(db_column='ReOrdQty', blank=True, null=True)  # Field name made lowercase.
    qtyonres = models.FloatField(db_column='QtyOnRes', blank=True, null=True)  # Field name made lowercase.
    lrno = models.CharField(db_column='LRNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lrdate = models.DateTimeField(db_column='LRDate', blank=True, null=True)  # Field name made lowercase.
    lrqty = models.FloatField(db_column='LRQty', blank=True, null=True)  # Field name made lowercase.
    binloc1 = models.CharField(db_column='BinLoc1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty1 = models.FloatField(db_column='BinQty1', blank=True, null=True)  # Field name made lowercase.
    binloc2 = models.CharField(db_column='BinLoc2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty2 = models.FloatField(db_column='BinQty2', blank=True, null=True)  # Field name made lowercase.
    binloc3 = models.CharField(db_column='BinLoc3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty3 = models.FloatField(db_column='BinQty3', blank=True, null=True)  # Field name made lowercase.
    binloc4 = models.CharField(db_column='BinLoc4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty4 = models.FloatField(db_column='BinQty4', blank=True, null=True)  # Field name made lowercase.
    binloc5 = models.CharField(db_column='BinLoc5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty5 = models.FloatField(db_column='BinQty5', blank=True, null=True)  # Field name made lowercase.
    vendcode1 = models.CharField(db_column='VendCode1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode2 = models.CharField(db_column='VendCode2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode3 = models.CharField(db_column='VendCode3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    leadtime = models.SmallIntegerField(db_column='LeadTime', blank=True, null=True)  # Field name made lowercase.
    purchunit = models.CharField(db_column='PurchUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    purchfactor = models.FloatField(db_column='PurchFactor', blank=True, null=True)  # Field name made lowercase.
    markuppct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    pqty1 = models.IntegerField(db_column='PQty1', blank=True, null=True)  # Field name made lowercase.
    pcost1 = models.FloatField(db_column='PCost1', blank=True, null=True)  # Field name made lowercase.
    pqty2 = models.IntegerField(db_column='PQty2', blank=True, null=True)  # Field name made lowercase.
    pcost2 = models.FloatField(db_column='PCost2', blank=True, null=True)  # Field name made lowercase.
    pqty3 = models.IntegerField(db_column='PQty3', blank=True, null=True)  # Field name made lowercase.
    pcost3 = models.FloatField(db_column='PCost3', blank=True, null=True)  # Field name made lowercase.
    pqty4 = models.IntegerField(db_column='PQty4', blank=True, null=True)  # Field name made lowercase.
    pcost4 = models.FloatField(db_column='PCost4', blank=True, null=True)  # Field name made lowercase.
    pqty5 = models.IntegerField(db_column='PQty5', blank=True, null=True)  # Field name made lowercase.
    pcost5 = models.FloatField(db_column='PCost5', blank=True, null=True)  # Field name made lowercase.
    pqty6 = models.IntegerField(db_column='PQty6', blank=True, null=True)  # Field name made lowercase.
    pcost6 = models.FloatField(db_column='PCost6', blank=True, null=True)  # Field name made lowercase.
    pqty7 = models.IntegerField(db_column='PQty7', blank=True, null=True)  # Field name made lowercase.
    pcost7 = models.FloatField(db_column='PCost7', blank=True, null=True)  # Field name made lowercase.
    pqty8 = models.IntegerField(db_column='PQty8', blank=True, null=True)  # Field name made lowercase.
    pcost8 = models.FloatField(db_column='PCost8', blank=True, null=True)  # Field name made lowercase.
    stockingcost = models.FloatField(db_column='StockingCost', blank=True, null=True)  # Field name made lowercase.
    lpono = models.CharField(db_column='LPONo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lpodate = models.DateTimeField(db_column='LPODate', blank=True, null=True)  # Field name made lowercase.
    lpoqty = models.FloatField(db_column='LPOQty', blank=True, null=True)  # Field name made lowercase.
    lpocost = models.FloatField(db_column='LPOCost', blank=True, null=True)  # Field name made lowercase.
    qtyonorder = models.FloatField(db_column='QtyOnOrder', blank=True, null=True)  # Field name made lowercase.
    qtyoutside = models.FloatField(db_column='QtyOutside', blank=True, null=True)  # Field name made lowercase.
    markup1 = models.FloatField(db_column='Markup1', blank=True, null=True)  # Field name made lowercase.
    markup2 = models.FloatField(db_column='Markup2', blank=True, null=True)  # Field name made lowercase.
    markup3 = models.FloatField(db_column='Markup3', blank=True, null=True)  # Field name made lowercase.
    markup4 = models.FloatField(db_column='Markup4', blank=True, null=True)  # Field name made lowercase.
    markup5 = models.FloatField(db_column='Markup5', blank=True, null=True)  # Field name made lowercase.
    markup6 = models.FloatField(db_column='Markup6', blank=True, null=True)  # Field name made lowercase.
    markup7 = models.FloatField(db_column='Markup7', blank=True, null=True)  # Field name made lowercase.
    markup8 = models.FloatField(db_column='Markup8', blank=True, null=True)  # Field name made lowercase.
    lockprice = models.CharField(db_column='LockPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcmethod = models.CharField(db_column='CalcMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printed = models.CharField(db_column='Printed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    purchglcode = models.CharField(db_column='PurchGLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    bin1lot = models.TextField(db_column='Bin1Lot', blank=True, null=True)  # Field name made lowercase.
    bin2lot = models.TextField(db_column='Bin2Lot', blank=True, null=True)  # Field name made lowercase.
    bin3lot = models.TextField(db_column='Bin3Lot', blank=True, null=True)  # Field name made lowercase.
    bin4lot = models.TextField(db_column='Bin4Lot', blank=True, null=True)  # Field name made lowercase.
    bin5lot = models.TextField(db_column='Bin5Lot', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    defaultbinloc = models.CharField(db_column='DefaultBinLoc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    matchqtybreaks = models.CharField(db_column='MatchQtyBreaks', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_decimal_inventory = models.NullBooleanField(db_column='Allow_Decimal_Inventory')  # Field name made lowercase.
    allow_decimal_purchasing = models.NullBooleanField(db_column='Allow_Decimal_Purchasing')  # Field name made lowercase.
    automatically_fill_requirements = models.NullBooleanField(db_column='Automatically_Fill_Requirements')  # Field name made lowercase.
    automatically_use_partial_records = models.NullBooleanField(db_column='Automatically_Use_Partial_Records')  # Field name made lowercase.
    automatically_combine_partial_records = models.NullBooleanField(db_column='Automatically_Combine_Partial_Records')  # Field name made lowercase.
    inspect_orders = models.NullBooleanField(db_column='Inspect_Orders')  # Field name made lowercase.
    inspect_customer_returns = models.NullBooleanField(db_column='Inspect_Customer_Returns')  # Field name made lowercase.
    inspect_receivers = models.NullBooleanField(db_column='Inspect_Receivers')  # Field name made lowercase.
    inspect_internal_rejections = models.NullBooleanField(db_column='Inspect_Internal_Rejections')  # Field name made lowercase.
    using_time_tickets = models.NullBooleanField(db_column='Using_Time_Tickets')  # Field name made lowercase.
    stocking_unit_new = models.CharField(db_column='Stocking_Unit_New', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stocking_purchasing_factor_new = models.FloatField(db_column='Stocking_Purchasing_Factor_New', blank=True, null=True)  # Field name made lowercase.
    purchasing_unit_new = models.CharField(db_column='Purchasing_Unit_New', max_length=3, blank=True, null=True)  # Field name made lowercase.
    purchasing_purchasing_factor_new = models.FloatField(db_column='Purchasing_Purchasing_Factor_New', blank=True, null=True)  # Field name made lowercase.
    part_weight_new = models.FloatField(db_column='Part_Weight_New', blank=True, null=True)  # Field name made lowercase.
    saved_by_utility = models.NullBooleanField(db_column='Saved_By_Utility')  # Field name made lowercase.
    new_purchasing_factor = models.FloatField(db_column='New_Purchasing_Factor', blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Estim'


class Estimrpt(TruncatedModel):
    partno = models.CharField(db_column='PartNo', unique=True, max_length=30, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    startqty1 = models.IntegerField(db_column='StartQty1', blank=True, null=True)  # Field name made lowercase.
    quoteqty1 = models.IntegerField(db_column='QuoteQty1', blank=True, null=True)  # Field name made lowercase.
    psetup1 = models.FloatField(db_column='PSetup1', blank=True, null=True)  # Field name made lowercase.
    pcycle1 = models.FloatField(db_column='PCycle1', blank=True, null=True)  # Field name made lowercase.
    pmaterial1 = models.FloatField(db_column='PMaterial1', blank=True, null=True)  # Field name made lowercase.
    poutside1 = models.FloatField(db_column='POutside1', blank=True, null=True)  # Field name made lowercase.
    pcomm1 = models.FloatField(db_column='PComm1', blank=True, null=True)  # Field name made lowercase.
    price1 = models.FloatField(db_column='Price1', blank=True, null=True)  # Field name made lowercase.
    clabor1 = models.FloatField(db_column='CLabor1', blank=True, null=True)  # Field name made lowercase.
    cburden1 = models.FloatField(db_column='CBurden1', blank=True, null=True)  # Field name made lowercase.
    cmaterial1 = models.FloatField(db_column='CMaterial1', blank=True, null=True)  # Field name made lowercase.
    coutside1 = models.FloatField(db_column='COutside1', blank=True, null=True)  # Field name made lowercase.
    ccomm1 = models.FloatField(db_column='CComm1', blank=True, null=True)  # Field name made lowercase.
    cost1 = models.FloatField(db_column='Cost1', blank=True, null=True)  # Field name made lowercase.
    totjobtime1 = models.FloatField(db_column='TotJobTime1', blank=True, null=True)  # Field name made lowercase.
    avghourly1 = models.FloatField(db_column='AvgHourly1', blank=True, null=True)  # Field name made lowercase.
    startqty2 = models.IntegerField(db_column='StartQty2', blank=True, null=True)  # Field name made lowercase.
    quoteqty2 = models.IntegerField(db_column='QuoteQty2', blank=True, null=True)  # Field name made lowercase.
    psetup2 = models.FloatField(db_column='PSetup2', blank=True, null=True)  # Field name made lowercase.
    pcycle2 = models.FloatField(db_column='PCycle2', blank=True, null=True)  # Field name made lowercase.
    pmaterial2 = models.FloatField(db_column='PMaterial2', blank=True, null=True)  # Field name made lowercase.
    poutside2 = models.FloatField(db_column='POutside2', blank=True, null=True)  # Field name made lowercase.
    pcomm2 = models.FloatField(db_column='PComm2', blank=True, null=True)  # Field name made lowercase.
    price2 = models.FloatField(db_column='Price2', blank=True, null=True)  # Field name made lowercase.
    clabor2 = models.FloatField(db_column='CLabor2', blank=True, null=True)  # Field name made lowercase.
    cburden2 = models.FloatField(db_column='CBurden2', blank=True, null=True)  # Field name made lowercase.
    cmaterial2 = models.FloatField(db_column='CMaterial2', blank=True, null=True)  # Field name made lowercase.
    coutside2 = models.FloatField(db_column='COutside2', blank=True, null=True)  # Field name made lowercase.
    ccomm2 = models.FloatField(db_column='CComm2', blank=True, null=True)  # Field name made lowercase.
    cost2 = models.FloatField(db_column='Cost2', blank=True, null=True)  # Field name made lowercase.
    totjobtime2 = models.FloatField(db_column='TotJobTime2', blank=True, null=True)  # Field name made lowercase.
    avghourly2 = models.FloatField(db_column='AvgHourly2', blank=True, null=True)  # Field name made lowercase.
    startqty3 = models.IntegerField(db_column='StartQty3', blank=True, null=True)  # Field name made lowercase.
    quoteqty3 = models.IntegerField(db_column='QuoteQty3', blank=True, null=True)  # Field name made lowercase.
    psetup3 = models.FloatField(db_column='PSetup3', blank=True, null=True)  # Field name made lowercase.
    pcycle3 = models.FloatField(db_column='PCycle3', blank=True, null=True)  # Field name made lowercase.
    pmaterial3 = models.FloatField(db_column='PMaterial3', blank=True, null=True)  # Field name made lowercase.
    poutside3 = models.FloatField(db_column='POutside3', blank=True, null=True)  # Field name made lowercase.
    pcomm3 = models.FloatField(db_column='PComm3', blank=True, null=True)  # Field name made lowercase.
    price3 = models.FloatField(db_column='Price3', blank=True, null=True)  # Field name made lowercase.
    clabor3 = models.FloatField(db_column='CLabor3', blank=True, null=True)  # Field name made lowercase.
    cburden3 = models.FloatField(db_column='CBurden3', blank=True, null=True)  # Field name made lowercase.
    cmaterial3 = models.FloatField(db_column='CMaterial3', blank=True, null=True)  # Field name made lowercase.
    coutside3 = models.FloatField(db_column='COutside3', blank=True, null=True)  # Field name made lowercase.
    ccomm3 = models.FloatField(db_column='CComm3', blank=True, null=True)  # Field name made lowercase.
    cost3 = models.FloatField(db_column='Cost3', blank=True, null=True)  # Field name made lowercase.
    totjobtime3 = models.FloatField(db_column='TotJobTime3', blank=True, null=True)  # Field name made lowercase.
    avghourly3 = models.FloatField(db_column='AvgHourly3', blank=True, null=True)  # Field name made lowercase.
    startqty4 = models.IntegerField(db_column='StartQty4', blank=True, null=True)  # Field name made lowercase.
    quoteqty4 = models.IntegerField(db_column='QuoteQty4', blank=True, null=True)  # Field name made lowercase.
    psetup4 = models.FloatField(db_column='PSetup4', blank=True, null=True)  # Field name made lowercase.
    pcycle4 = models.FloatField(db_column='PCycle4', blank=True, null=True)  # Field name made lowercase.
    pmaterial4 = models.FloatField(db_column='PMaterial4', blank=True, null=True)  # Field name made lowercase.
    poutside4 = models.FloatField(db_column='POutside4', blank=True, null=True)  # Field name made lowercase.
    pcomm4 = models.FloatField(db_column='PComm4', blank=True, null=True)  # Field name made lowercase.
    price4 = models.FloatField(db_column='Price4', blank=True, null=True)  # Field name made lowercase.
    clabor4 = models.FloatField(db_column='CLabor4', blank=True, null=True)  # Field name made lowercase.
    cburden4 = models.FloatField(db_column='CBurden4', blank=True, null=True)  # Field name made lowercase.
    cmaterial4 = models.FloatField(db_column='CMaterial4', blank=True, null=True)  # Field name made lowercase.
    coutside4 = models.FloatField(db_column='COutside4', blank=True, null=True)  # Field name made lowercase.
    ccomm4 = models.FloatField(db_column='CComm4', blank=True, null=True)  # Field name made lowercase.
    cost4 = models.FloatField(db_column='Cost4', blank=True, null=True)  # Field name made lowercase.
    totjobtime4 = models.FloatField(db_column='TotJobTime4', blank=True, null=True)  # Field name made lowercase.
    avghourly4 = models.FloatField(db_column='AvgHourly4', blank=True, null=True)  # Field name made lowercase.
    startqty5 = models.IntegerField(db_column='StartQty5', blank=True, null=True)  # Field name made lowercase.
    quoteqty5 = models.IntegerField(db_column='QuoteQty5', blank=True, null=True)  # Field name made lowercase.
    psetup5 = models.FloatField(db_column='PSetup5', blank=True, null=True)  # Field name made lowercase.
    pcycle5 = models.FloatField(db_column='PCycle5', blank=True, null=True)  # Field name made lowercase.
    pmaterial5 = models.FloatField(db_column='PMaterial5', blank=True, null=True)  # Field name made lowercase.
    poutside5 = models.FloatField(db_column='POutside5', blank=True, null=True)  # Field name made lowercase.
    pcomm5 = models.FloatField(db_column='PComm5', blank=True, null=True)  # Field name made lowercase.
    price5 = models.FloatField(db_column='Price5', blank=True, null=True)  # Field name made lowercase.
    clabor5 = models.FloatField(db_column='CLabor5', blank=True, null=True)  # Field name made lowercase.
    cburden5 = models.FloatField(db_column='CBurden5', blank=True, null=True)  # Field name made lowercase.
    cmaterial5 = models.FloatField(db_column='CMaterial5', blank=True, null=True)  # Field name made lowercase.
    coutside5 = models.FloatField(db_column='COutside5', blank=True, null=True)  # Field name made lowercase.
    ccomm5 = models.FloatField(db_column='CComm5', blank=True, null=True)  # Field name made lowercase.
    cost5 = models.FloatField(db_column='Cost5', blank=True, null=True)  # Field name made lowercase.
    totjobtime5 = models.FloatField(db_column='TotJobTime5', blank=True, null=True)  # Field name made lowercase.
    avghourly5 = models.FloatField(db_column='AvgHourly5', blank=True, null=True)  # Field name made lowercase.
    startqty6 = models.IntegerField(db_column='StartQty6', blank=True, null=True)  # Field name made lowercase.
    quoteqty6 = models.IntegerField(db_column='QuoteQty6', blank=True, null=True)  # Field name made lowercase.
    psetup6 = models.FloatField(db_column='PSetup6', blank=True, null=True)  # Field name made lowercase.
    pcycle6 = models.FloatField(db_column='PCycle6', blank=True, null=True)  # Field name made lowercase.
    pmaterial6 = models.FloatField(db_column='PMaterial6', blank=True, null=True)  # Field name made lowercase.
    poutside6 = models.FloatField(db_column='POutside6', blank=True, null=True)  # Field name made lowercase.
    pcomm6 = models.FloatField(db_column='PComm6', blank=True, null=True)  # Field name made lowercase.
    price6 = models.FloatField(db_column='Price6', blank=True, null=True)  # Field name made lowercase.
    clabor6 = models.FloatField(db_column='CLabor6', blank=True, null=True)  # Field name made lowercase.
    cburden6 = models.FloatField(db_column='CBurden6', blank=True, null=True)  # Field name made lowercase.
    cmaterial6 = models.FloatField(db_column='CMaterial6', blank=True, null=True)  # Field name made lowercase.
    coutside6 = models.FloatField(db_column='COutside6', blank=True, null=True)  # Field name made lowercase.
    ccomm6 = models.FloatField(db_column='CComm6', blank=True, null=True)  # Field name made lowercase.
    cost6 = models.FloatField(db_column='Cost6', blank=True, null=True)  # Field name made lowercase.
    totjobtime6 = models.FloatField(db_column='TotJobTime6', blank=True, null=True)  # Field name made lowercase.
    avghourly6 = models.FloatField(db_column='AvgHourly6', blank=True, null=True)  # Field name made lowercase.
    startqty7 = models.IntegerField(db_column='StartQty7', blank=True, null=True)  # Field name made lowercase.
    quoteqty7 = models.IntegerField(db_column='QuoteQty7', blank=True, null=True)  # Field name made lowercase.
    psetup7 = models.FloatField(db_column='PSetup7', blank=True, null=True)  # Field name made lowercase.
    pcycle7 = models.FloatField(db_column='PCycle7', blank=True, null=True)  # Field name made lowercase.
    pmaterial7 = models.FloatField(db_column='PMaterial7', blank=True, null=True)  # Field name made lowercase.
    poutside7 = models.FloatField(db_column='POutside7', blank=True, null=True)  # Field name made lowercase.
    pcomm7 = models.FloatField(db_column='PComm7', blank=True, null=True)  # Field name made lowercase.
    price7 = models.FloatField(db_column='Price7', blank=True, null=True)  # Field name made lowercase.
    clabor7 = models.FloatField(db_column='CLabor7', blank=True, null=True)  # Field name made lowercase.
    cburden7 = models.FloatField(db_column='CBurden7', blank=True, null=True)  # Field name made lowercase.
    cmaterial7 = models.FloatField(db_column='CMaterial7', blank=True, null=True)  # Field name made lowercase.
    coutside7 = models.FloatField(db_column='COutside7', blank=True, null=True)  # Field name made lowercase.
    ccomm7 = models.FloatField(db_column='CComm7', blank=True, null=True)  # Field name made lowercase.
    cost7 = models.FloatField(db_column='Cost7', blank=True, null=True)  # Field name made lowercase.
    totjobtime7 = models.FloatField(db_column='TotJobTime7', blank=True, null=True)  # Field name made lowercase.
    avghourly7 = models.FloatField(db_column='AvgHourly7', blank=True, null=True)  # Field name made lowercase.
    startqty8 = models.IntegerField(db_column='StartQty8', blank=True, null=True)  # Field name made lowercase.
    quoteqty8 = models.IntegerField(db_column='QuoteQty8', blank=True, null=True)  # Field name made lowercase.
    psetup8 = models.FloatField(db_column='PSetup8', blank=True, null=True)  # Field name made lowercase.
    pcycle8 = models.FloatField(db_column='PCycle8', blank=True, null=True)  # Field name made lowercase.
    pmaterial8 = models.FloatField(db_column='PMaterial8', blank=True, null=True)  # Field name made lowercase.
    poutside8 = models.FloatField(db_column='POutside8', blank=True, null=True)  # Field name made lowercase.
    pcomm8 = models.FloatField(db_column='PComm8', blank=True, null=True)  # Field name made lowercase.
    price8 = models.FloatField(db_column='Price8', blank=True, null=True)  # Field name made lowercase.
    clabor8 = models.FloatField(db_column='CLabor8', blank=True, null=True)  # Field name made lowercase.
    cburden8 = models.FloatField(db_column='CBurden8', blank=True, null=True)  # Field name made lowercase.
    cmaterial8 = models.FloatField(db_column='CMaterial8', blank=True, null=True)  # Field name made lowercase.
    coutside8 = models.FloatField(db_column='COutside8', blank=True, null=True)  # Field name made lowercase.
    ccomm8 = models.FloatField(db_column='CComm8', blank=True, null=True)  # Field name made lowercase.
    cost8 = models.FloatField(db_column='Cost8', blank=True, null=True)  # Field name made lowercase.
    totjobtime8 = models.FloatField(db_column='TotJobTime8', blank=True, null=True)  # Field name made lowercase.
    avghourly8 = models.FloatField(db_column='AvgHourly8', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'EstimRpt'


class Feedback(TruncatedModel):
    feedbackno = models.CharField(db_column='FeedbackNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    feedbackdate = models.DateTimeField(db_column='FeedbackDate', blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custrmano = models.CharField(db_column='CustRMANo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    feedbacktype = models.CharField(db_column='FeedbackType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    feedbackcode = models.CharField(db_column='FeedbackCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    resolution = models.TextField(db_column='Resolution', blank=True, null=True)  # Field name made lowercase.
    closeout = models.TextField(db_column='CloseOut', blank=True, null=True)  # Field name made lowercase.
    mgrcloseout = models.CharField(db_column='MgrCloseOut', max_length=12, blank=True, null=True)  # Field name made lowercase.
    closeoutdate = models.DateTimeField(db_column='CloseOutDate', blank=True, null=True)  # Field name made lowercase.
    createcar = models.CharField(db_column='CreateCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    correctiveactioncode = models.CharField(db_column='CorrectiveActionCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    enterby = models.CharField(db_column='EnterBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    enterdate = models.DateTimeField(db_column='EnterDate', blank=True, null=True)  # Field name made lowercase.
    feedback_id = models.AutoField(db_column='Feedback_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Feedback'


class Feedbackcode(TruncatedModel):
    feedbackcode = models.CharField(db_column='FeedbackCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    feedbacktype = models.CharField(db_column='FeedbackType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    feedbackcode_id = models.AutoField(db_column='FeedbackCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'FeedbackCode'


class Fiscalyearstatus(TruncatedModel):
    fiscalyear = models.CharField(db_column='FiscalYear', unique=True, max_length=12)  # Field name made lowercase.
    begindate = models.CharField(db_column='BeginDate', unique=True, max_length=10)  # Field name made lowercase.
    isclosed = models.BooleanField(db_column='IsClosed')  # Field name made lowercase.
    ishistorical = models.BooleanField(db_column='IsHistorical')  # Field name made lowercase.
    ishistoricallocked = models.BooleanField(db_column='IsHistoricalLocked')  # Field name made lowercase.
    fiscalyearstatus_id = models.AutoField(db_column='FiscalYearStatus_ID', primary_key=True)  # Field name made lowercase.
    fiscalyeartypeint = models.SmallIntegerField(db_column='FiscalYearTypeInt')  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'FiscalYearStatus'


class Gl(TruncatedModel):
    journalno = models.CharField(db_column='JournalNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', max_length=2, blank=True, null=True)  # Field name made lowercase.
    clearedbank = models.CharField(db_column='ClearedBank', max_length=1, blank=True, null=True)  # Field name made lowercase.
    transdate = models.DateTimeField(db_column='TransDate', blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateposted = models.DateTimeField(db_column='DatePosted', blank=True, null=True)  # Field name made lowercase.
    datereversed = models.DateTimeField(db_column='DateReversed', blank=True, null=True)  # Field name made lowercase.
    explanation = models.TextField(db_column='Explanation', blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='BankCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    periodno = models.CharField(db_column='PeriodNo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    gl_id = models.AutoField(db_column='GL_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'GL'


class Glaccounts(TruncatedModel):
    glacctnum = models.CharField(db_column='GLAcctNum', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    acctcode = models.CharField(db_column='AcctCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    division = models.SmallIntegerField(db_column='Division', blank=True, null=True)  # Field name made lowercase.
    accumacct = models.CharField(db_column='AccumAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    glaccounts_id = models.AutoField(db_column='GLAccounts_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'GLAccounts'


class Glbalance(TruncatedModel):
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    periodno = models.CharField(db_column='PeriodNo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    budgetamount = models.FloatField(db_column='BudgetAmount', blank=True, null=True)  # Field name made lowercase.
    glbalance_id = models.AutoField(db_column='GLBalance_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'GLBalance'
        unique_together = (('glcode', 'periodno'),)


class Gldet(TruncatedModel):
    journalno = models.CharField(db_column='JournalNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glaccount = models.CharField(db_column='GLAccount', max_length=12, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    explanation = models.TextField(db_column='Explanation', blank=True, null=True)  # Field name made lowercase.
    gldet_id = models.AutoField(db_column='GLDet_ID', primary_key=True)  # Field name made lowercase.
    document_number = models.CharField(db_column='Document_Number', max_length=30, blank=True, null=True)  # Field name made lowercase.
    document_date = models.DateTimeField(db_column='Document_Date', blank=True, null=True)  # Field name made lowercase.
    custvendcode = models.CharField(db_column='CustVendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custvendname = models.CharField(db_column='CustVendName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'GLDet'


class Glfiscalyearbalance(TruncatedModel):
    glacctnum = models.CharField(db_column='GLAcctNum', max_length=12)  # Field name made lowercase.
    fiscalyear = models.CharField(db_column='FiscalYear', max_length=12)  # Field name made lowercase.
    begbalance = models.FloatField(db_column='BegBalance')  # Field name made lowercase.
    glfiscalyearbalance_id = models.AutoField(db_column='GLFiscalYearBalance_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'GLFiscalYearBalance'
        unique_together = (('glacctnum', 'fiscalyear'),)


class Gridsettings(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    form = models.CharField(db_column='Form', max_length=40, blank=True, null=True)  # Field name made lowercase.
    control = models.CharField(db_column='Control', max_length=30, blank=True, null=True)  # Field name made lowercase.
    split = models.SmallIntegerField(db_column='Split', blank=True, null=True)  # Field name made lowercase.
    column = models.SmallIntegerField(db_column='Column', blank=True, null=True)  # Field name made lowercase.
    alignment = models.SmallIntegerField(db_column='Alignment', blank=True, null=True)  # Field name made lowercase.
    allowfocus = models.CharField(db_column='AllowFocus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autodropdown = models.CharField(db_column='AutoDropDown', max_length=1, blank=True, null=True)  # Field name made lowercase.
    button = models.CharField(db_column='Button', max_length=1, blank=True, null=True)  # Field name made lowercase.
    caption = models.CharField(db_column='Caption', max_length=30, blank=True, null=True)  # Field name made lowercase.
    datawidth = models.SmallIntegerField(db_column='DataWidth', blank=True, null=True)  # Field name made lowercase.
    defaultvalue = models.CharField(db_column='DefaultValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dropdown = models.CharField(db_column='DropDown', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dropdownlist = models.CharField(db_column='DropDownList', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editmask = models.CharField(db_column='EditMask', max_length=30, blank=True, null=True)  # Field name made lowercase.
    headalignment = models.SmallIntegerField(db_column='HeadAlignment', blank=True, null=True)  # Field name made lowercase.
    locked = models.CharField(db_column='Locked', max_length=1, blank=True, null=True)  # Field name made lowercase.
    numberformat = models.CharField(db_column='NumberFormat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    order = models.SmallIntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    visible = models.CharField(db_column='Visible', max_length=1, blank=True, null=True)  # Field name made lowercase.
    width = models.FloatField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    wraptext = models.CharField(db_column='WrapText', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totalcolumn = models.CharField(db_column='TotalColumn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    jump = models.CharField(db_column='Jump', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sort = models.CharField(db_column='Sort', max_length=1, blank=True, null=True)  # Field name made lowercase.
    merge = models.CharField(db_column='Merge', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gridsettings_id = models.AutoField(db_column='GridSettings_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'GridSettings'


class Hotspotcolumnsummary(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    condition_id = models.IntegerField(db_column='Condition_ID')  # Field name made lowercase.
    fieldname = models.CharField(db_column='FieldName', max_length=255)  # Field name made lowercase.
    columnsummary = models.CharField(db_column='ColumnSummary', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'HotSpotColumnSummary'


class Importcustomer(TruncatedModel):
    custcode = models.CharField(db_column='CustCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    custname = models.CharField(db_column='CustName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    discperc = models.FloatField(db_column='DiscPerc', blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditlim = models.FloatField(db_column='CreditLim', blank=True, null=True)  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    baddr1 = models.CharField(db_column='BAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    baddr2 = models.CharField(db_column='BAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bcity = models.CharField(db_column='BCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bstate = models.CharField(db_column='BState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    bzipcode = models.CharField(db_column='BZIPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bcountry = models.CharField(db_column='BCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact1 = models.CharField(db_column='Contact1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact1phone = models.CharField(db_column='Contact1Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact2 = models.CharField(db_column='Contact2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact2phone = models.CharField(db_column='Contact2Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    apcontact = models.CharField(db_column='APContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    apphone = models.CharField(db_column='APPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    comments1 = models.TextField(db_column='Comments1', blank=True, null=True)  # Field name made lowercase.
    comments2 = models.TextField(db_column='Comments2', blank=True, null=True)  # Field name made lowercase.
    defpriority = models.SmallIntegerField(db_column='DefPriority', blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    minimumorder = models.FloatField(db_column='MinimumOrder', blank=True, null=True)  # Field name made lowercase.
    fedidnum = models.CharField(db_column='FedIDNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pricetier = models.SmallIntegerField(db_column='PriceTier', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=250, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    restockingpct = models.FloatField(db_column='RestockingPct', blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    importcustomer_id = models.AutoField(db_column='ImportCustomer_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ImportCustomer'


class Importestimateheader(TruncatedModel):
    partno = models.CharField(db_column='PartNo', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    altpartno = models.CharField(db_column='AltPartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    commissionpct = models.FloatField(db_column='CommissionPct', blank=True, null=True)  # Field name made lowercase.
    misctoolingchg = models.FloatField(db_column='MiscToolingChg', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    qty1 = models.IntegerField(db_column='Qty1', blank=True, null=True)  # Field name made lowercase.
    pricefactor1 = models.FloatField(db_column='PriceFactor1', blank=True, null=True)  # Field name made lowercase.
    price1 = models.FloatField(db_column='Price1', blank=True, null=True)  # Field name made lowercase.
    qty2 = models.IntegerField(db_column='Qty2', blank=True, null=True)  # Field name made lowercase.
    pricefactor2 = models.FloatField(db_column='PriceFactor2', blank=True, null=True)  # Field name made lowercase.
    price2 = models.FloatField(db_column='Price2', blank=True, null=True)  # Field name made lowercase.
    qty3 = models.IntegerField(db_column='Qty3', blank=True, null=True)  # Field name made lowercase.
    pricefactor3 = models.FloatField(db_column='PriceFactor3', blank=True, null=True)  # Field name made lowercase.
    price3 = models.FloatField(db_column='Price3', blank=True, null=True)  # Field name made lowercase.
    qty4 = models.IntegerField(db_column='Qty4', blank=True, null=True)  # Field name made lowercase.
    pricefactor4 = models.FloatField(db_column='PriceFactor4', blank=True, null=True)  # Field name made lowercase.
    price4 = models.FloatField(db_column='Price4', blank=True, null=True)  # Field name made lowercase.
    qty5 = models.IntegerField(db_column='Qty5', blank=True, null=True)  # Field name made lowercase.
    pricefactor5 = models.FloatField(db_column='PriceFactor5', blank=True, null=True)  # Field name made lowercase.
    price5 = models.FloatField(db_column='Price5', blank=True, null=True)  # Field name made lowercase.
    qty6 = models.IntegerField(db_column='Qty6', blank=True, null=True)  # Field name made lowercase.
    pricefactor6 = models.FloatField(db_column='PriceFactor6', blank=True, null=True)  # Field name made lowercase.
    price6 = models.FloatField(db_column='Price6', blank=True, null=True)  # Field name made lowercase.
    qty7 = models.IntegerField(db_column='Qty7', blank=True, null=True)  # Field name made lowercase.
    pricefactor7 = models.FloatField(db_column='PriceFactor7', blank=True, null=True)  # Field name made lowercase.
    price7 = models.FloatField(db_column='Price7', blank=True, null=True)  # Field name made lowercase.
    drawnum = models.CharField(db_column='DrawNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    importestimateheader_id = models.AutoField(db_column='ImportEstimateHeader_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ImportEstimateHeader'


class Importestimatematerial(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    subpartno = models.CharField(db_column='SubPartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    moredescription = models.TextField(db_column='MoreDescription', blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    markuppct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    materialpounds = models.FloatField(db_column='MaterialPounds', blank=True, null=True)  # Field name made lowercase.
    weightperfoot = models.FloatField(db_column='WeightPerFoot', blank=True, null=True)  # Field name made lowercase.
    materialpriceunit = models.CharField(db_column='MaterialPriceUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    importestimatematerial_id = models.AutoField(db_column='ImportEstimateMaterial_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ImportEstimateMaterial'
        unique_together = (('partno', 'subpartno'),)


class Importestimaterouting(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stepno = models.IntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    steptype = models.CharField(db_column='StepType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workcntr = models.CharField(db_column='WorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opercode = models.CharField(db_column='OperCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    stepdescription = models.CharField(db_column='StepDescription', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stepnotes = models.CharField(db_column='StepNotes', max_length=50, blank=True, null=True)  # Field name made lowercase.
    setuphrs = models.FloatField(db_column='SetupHrs', blank=True, null=True)  # Field name made lowercase.
    setupunit = models.CharField(db_column='SetupUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cycletime = models.FloatField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    cycleunit = models.CharField(db_column='CycleUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    machinesrun = models.IntegerField(db_column='MachinesRun', blank=True, null=True)  # Field name made lowercase.
    teamsize = models.IntegerField(db_column='TeamSize', blank=True, null=True)  # Field name made lowercase.
    scrappct = models.FloatField(db_column='ScrapPct', blank=True, null=True)  # Field name made lowercase.
    pctefficiency = models.FloatField(db_column='PctEfficiency', blank=True, null=True)  # Field name made lowercase.
    billinghourlyrate = models.FloatField(db_column='BillingHourlyRate', blank=True, null=True)  # Field name made lowercase.
    burdenhourlyrate2 = models.FloatField(db_column='BurdenHourlyRate2', blank=True, null=True)  # Field name made lowercase.
    laborhourlyrate = models.FloatField(db_column='LaborHourlyRate', blank=True, null=True)  # Field name made lowercase.
    unattendedop = models.CharField(db_column='UnattendedOp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    leadtimedays = models.IntegerField(db_column='LeadTimeDays', blank=True, null=True)  # Field name made lowercase.
    markuppct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    certsrequired = models.CharField(db_column='CertsRequired', max_length=1, blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    outsidecost1 = models.FloatField(db_column='OutsideCost1', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost1 = models.FloatField(db_column='PerishableToolCost1', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost1 = models.FloatField(db_column='OneTimeToolCost1', blank=True, null=True)  # Field name made lowercase.
    onetimecost1 = models.FloatField(db_column='OneTimeCost1', blank=True, null=True)  # Field name made lowercase.
    outsidecost2 = models.FloatField(db_column='OutsideCost2', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost2 = models.FloatField(db_column='PerishableToolCost2', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost2 = models.FloatField(db_column='OneTimeToolCost2', blank=True, null=True)  # Field name made lowercase.
    onetimecost2 = models.FloatField(db_column='OneTimeCost2', blank=True, null=True)  # Field name made lowercase.
    outsidecost3 = models.FloatField(db_column='OutsideCost3', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost3 = models.FloatField(db_column='PerishableToolCost3', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost3 = models.FloatField(db_column='OneTimeToolCost3', blank=True, null=True)  # Field name made lowercase.
    onetimecost3 = models.FloatField(db_column='OneTimeCost3', blank=True, null=True)  # Field name made lowercase.
    outsidecost4 = models.FloatField(db_column='OutsideCost4', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost4 = models.FloatField(db_column='PerishableToolCost4', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost4 = models.FloatField(db_column='OneTimeToolCost4', blank=True, null=True)  # Field name made lowercase.
    onetimecost4 = models.FloatField(db_column='OneTimeCost4', blank=True, null=True)  # Field name made lowercase.
    outsidecost5 = models.FloatField(db_column='OutsideCost5', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost5 = models.FloatField(db_column='PerishableToolCost5', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost5 = models.FloatField(db_column='OneTimeToolCost5', blank=True, null=True)  # Field name made lowercase.
    onetimecost5 = models.FloatField(db_column='OneTimeCost5', blank=True, null=True)  # Field name made lowercase.
    outsidecost6 = models.FloatField(db_column='OutsideCost6', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost6 = models.FloatField(db_column='PerishableToolCost6', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost6 = models.FloatField(db_column='OneTimeToolCost6', blank=True, null=True)  # Field name made lowercase.
    onetimecost6 = models.FloatField(db_column='OneTimeCost6', blank=True, null=True)  # Field name made lowercase.
    outsidecost7 = models.FloatField(db_column='OutsideCost7', blank=True, null=True)  # Field name made lowercase.
    perishabletoolcost7 = models.FloatField(db_column='PerishableToolCost7', blank=True, null=True)  # Field name made lowercase.
    onetimetoolcost7 = models.FloatField(db_column='OneTimeToolCost7', blank=True, null=True)  # Field name made lowercase.
    onetimecost7 = models.FloatField(db_column='OneTimeCost7', blank=True, null=True)  # Field name made lowercase.
    burdenhourlyrate1 = models.FloatField(db_column='BurdenHourlyRate1', blank=True, null=True)  # Field name made lowercase.
    importestimaterouting_id = models.AutoField(db_column='ImportEstimateRouting_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ImportEstimateRouting'
        unique_together = (('partno', 'stepno'),)


class Importshipto(TruncatedModel):
    custcode = models.CharField(db_column='CustCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    saddr1 = models.CharField(db_column='SAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    saddr2 = models.CharField(db_column='SAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scity = models.CharField(db_column='SCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sstate = models.CharField(db_column='SState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    szipcode = models.CharField(db_column='SZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    scountry = models.CharField(db_column='SCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipcontact = models.CharField(db_column='ShipContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipphone = models.CharField(db_column='ShipPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipfax = models.CharField(db_column='ShipFAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=12, blank=True, null=True)  # Field name made lowercase.
    printcert = models.CharField(db_column='PrintCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    importshipto_id = models.AutoField(db_column='ImportShipTo_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ImportShipTo'


class Indexlookup(TruncatedModel):
    tablename = models.CharField(db_column='TableName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    indexname = models.CharField(db_column='IndexName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fieldname = models.CharField(db_column='FieldName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    storedprocedure = models.CharField(db_column='StoredProcedure', max_length=255, blank=True, null=True)  # Field name made lowercase.
    selectstatement = models.CharField(db_column='SelectStatement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datatype1 = models.SmallIntegerField(db_column='DataType1', blank=True, null=True)  # Field name made lowercase.
    datalength1 = models.SmallIntegerField(db_column='DataLength1', blank=True, null=True)  # Field name made lowercase.
    datatype2 = models.SmallIntegerField(db_column='DataType2', blank=True, null=True)  # Field name made lowercase.
    datalength2 = models.SmallIntegerField(db_column='DataLength2', blank=True, null=True)  # Field name made lowercase.
    datatype3 = models.SmallIntegerField(db_column='DataType3', blank=True, null=True)  # Field name made lowercase.
    datalength3 = models.SmallIntegerField(db_column='DataLength3', blank=True, null=True)  # Field name made lowercase.
    datatype4 = models.SmallIntegerField(db_column='DataType4', blank=True, null=True)  # Field name made lowercase.
    datalength4 = models.SmallIntegerField(db_column='DataLength4', blank=True, null=True)  # Field name made lowercase.
    indexlookup_id = models.AutoField(db_column='IndexLookup_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'IndexLookup'


class Inventoryadjustments(TruncatedModel):
    tagno = models.IntegerField(db_column='TagNo', blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    binlocation = models.CharField(db_column='BinLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotnumber = models.TextField(db_column='LotNumber', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oldqty = models.FloatField(db_column='OldQty', blank=True, null=True)  # Field name made lowercase.
    newqty = models.FloatField(db_column='NewQty', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateposted = models.DateTimeField(db_column='DatePosted', blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reason = models.TextField(db_column='Reason', blank=True, null=True)  # Field name made lowercase.
    inventoryadjustments_id = models.AutoField(db_column='InventoryAdjustments_ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    object = models.CharField(db_column='Object', max_length=30, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'InventoryAdjustments'


class Jobbill(TruncatedModel):
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invoicedate = models.DateTimeField(db_column='InvoiceDate', blank=True, null=True)  # Field name made lowercase.
    qtyshipped = models.FloatField(db_column='QtyShipped', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discpct = models.FloatField(db_column='DiscPct', blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    jobbill_id = models.AutoField(db_column='JobBill_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'JobBill'


class Jobmaterials(TruncatedModel):
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    mainpart = models.CharField(db_column='MainPart', max_length=1, blank=True, null=True)  # Field name made lowercase.
    binloc1 = models.CharField(db_column='BinLoc1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qtyposted1 = models.FloatField(db_column='QtyPosted1', blank=True, null=True)  # Field name made lowercase.
    binloc2 = models.CharField(db_column='BinLoc2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qtyposted2 = models.FloatField(db_column='QtyPosted2', blank=True, null=True)  # Field name made lowercase.
    binloc3 = models.CharField(db_column='BinLoc3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qtyposted3 = models.FloatField(db_column='QtyPosted3', blank=True, null=True)  # Field name made lowercase.
    binloc4 = models.CharField(db_column='BinLoc4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qtyposted4 = models.FloatField(db_column='QtyPosted4', blank=True, null=True)  # Field name made lowercase.
    binloc5 = models.CharField(db_column='BinLoc5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qtyposted5 = models.FloatField(db_column='QtyPosted5', blank=True, null=True)  # Field name made lowercase.
    postedfromstock = models.CharField(db_column='PostedFromStock', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dateposted = models.DateTimeField(db_column='DatePosted', blank=True, null=True)  # Field name made lowercase.
    stockingcost = models.FloatField(db_column='StockingCost', blank=True, null=True)  # Field name made lowercase.
    stockunit = models.CharField(db_column='StockUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    postedby = models.CharField(db_column='PostedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    resaleprice = models.FloatField(db_column='ResalePrice', blank=True, null=True)  # Field name made lowercase.
    pricingunit = models.CharField(db_column='PricingUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendinvno = models.CharField(db_column='VendInvNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    podate = models.DateTimeField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    outsideservice = models.CharField(db_column='OutsideService', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    delticketno = models.CharField(db_column='DelTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receiverdate = models.DateTimeField(db_column='ReceiverDate', blank=True, null=True)  # Field name made lowercase.
    delticketdate = models.DateTimeField(db_column='DelTicketDate', blank=True, null=True)  # Field name made lowercase.
    bin1lot = models.TextField(db_column='Bin1Lot', blank=True, null=True)  # Field name made lowercase.
    bin2lot = models.TextField(db_column='Bin2Lot', blank=True, null=True)  # Field name made lowercase.
    bin3lot = models.TextField(db_column='Bin3Lot', blank=True, null=True)  # Field name made lowercase.
    bin4lot = models.TextField(db_column='Bin4Lot', blank=True, null=True)  # Field name made lowercase.
    bin5lot = models.TextField(db_column='Bin5Lot', blank=True, null=True)  # Field name made lowercase.
    jobmaterials_id = models.AutoField(db_column='JobMaterials_ID', primary_key=True)  # Field name made lowercase.
    binlocautono = models.IntegerField(db_column='BinLocAutoNo', blank=True, null=True)  # Field name made lowercase.
    originalbincost = models.FloatField(db_column='OriginalBinCost', blank=True, null=True)  # Field name made lowercase.
    subassyjobno = models.CharField(db_column='SubAssyJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    mfgjobno = models.CharField(db_column='MfgJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'JobMaterials'


class JobReq(TruncatedModel):
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qty2buy = models.FloatField(db_column='Qty2Buy', blank=True, null=True)  # Field name made lowercase.
    jobdue = models.DateTimeField(db_column='JobDue', blank=True, null=True)  # Field name made lowercase.
    dateprocessed = models.DateTimeField(db_column='DateProcessed', blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    outsideservice = models.CharField(db_column='OutsideService', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    leadtime = models.SmallIntegerField(db_column='LeadTime', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    stockunit = models.CharField(db_column='StockUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    pricingunit = models.CharField(db_column='PricingUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    purchqty = models.FloatField(db_column='PurchQty', blank=True, null=True)  # Field name made lowercase.
    purchunit = models.CharField(db_column='PurchUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    certreq = models.CharField(db_column='CertReq', max_length=1, blank=True, null=True)  # Field name made lowercase.
    setupchg = models.DecimalField(db_column='SetupChg', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    podate = models.DateTimeField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    tempjobdue = models.DateTimeField(db_column='TempJobDue', blank=True, null=True)  # Field name made lowercase.
    jobreq_id = models.AutoField(db_column='JobReq_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'JobReq'


class Lastsettings(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12)  # Field name made lowercase.
    modelname = models.CharField(db_column='ModelName', max_length=255)  # Field name made lowercase.
    fieldname = models.CharField(db_column='FieldName', max_length=255)  # Field name made lowercase.
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    lastsettings_id = models.AutoField(db_column='LastSettings_ID', primary_key=True)  # Field name made lowercase.
    isqueued = models.BooleanField(db_column='IsQueued')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'LastSettings'
        unique_together = (('userid', 'modelname', 'fieldname', 'isqueued'),)


class Listviewsettings(TruncatedModel):
    frmname = models.CharField(db_column='frmName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lvwname = models.CharField(db_column='lvwName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    colno = models.SmallIntegerField(db_column='ColNo', blank=True, null=True)  # Field name made lowercase.
    position = models.SmallIntegerField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
    heading = models.CharField(db_column='Heading', max_length=50, blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    alignment = models.IntegerField(db_column='Alignment', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ListViewSettings'


class Maintschedule(TruncatedModel):
    object = models.CharField(db_column='Object', max_length=30, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=50, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    completed = models.CharField(db_column='Completed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    addtocalendar = models.CharField(db_column='AddToCalendar', max_length=1, blank=True, null=True)  # Field name made lowercase.
    thresholdtype = models.CharField(db_column='ThresholdType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    thresholdvalue = models.FloatField(db_column='ThresholdValue', blank=True, null=True)  # Field name made lowercase.
    thresholdunit = models.CharField(db_column='ThresholdUnit', max_length=12, blank=True, null=True)  # Field name made lowercase.
    maintcode = models.CharField(db_column='MaintCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    dayssincelastmaint = models.FloatField(db_column='DaysSinceLastMaint', blank=True, null=True)  # Field name made lowercase.
    hrssincelastmaint = models.FloatField(db_column='HrsSinceLastMaint', blank=True, null=True)  # Field name made lowercase.
    pcssincelastmaint = models.FloatField(db_column='PcsSinceLastMaint', blank=True, null=True)  # Field name made lowercase.
    emplcode = models.IntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    lastrun = models.DateTimeField(db_column='LastRun', blank=True, null=True)  # Field name made lowercase.
    maintschedule_id = models.AutoField(db_column='MaintSchedule_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'MaintSchedule'


class Materials(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    subpartno = models.CharField(db_column='SubPartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    purchased = models.SmallIntegerField(db_column='Purchased', blank=True, null=True)  # Field name made lowercase.
    vendor = models.CharField(db_column='Vendor', max_length=12, blank=True, null=True)  # Field name made lowercase.
    totalqty = models.FloatField(db_column='TotalQty', blank=True, null=True)  # Field name made lowercase.
    unitcost = models.FloatField(db_column='UnitCost', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  # Field name made lowercase.
    totalprice = models.FloatField(db_column='TotalPrice', blank=True, null=True)  # Field name made lowercase.
    totalwt = models.FloatField(db_column='TotalWt', blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    partwt = models.FloatField(db_column='PartWt', blank=True, null=True)  # Field name made lowercase.
    counter = models.SmallIntegerField(db_column='Counter', blank=True, primary_key=True, editable=False, null=True)
    itemno = models.IntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Materials'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Hack to not save the maturity and months_open as they are computed columns
        if not IS_TEST:
            self._meta.local_fields = [f for f in self._meta.local_fields if f.name not in ('counter')]
        super(Materials, self).save(force_insert, force_update, using, update_fields)


class Message(TruncatedModel):
    senderid = models.CharField(db_column='SenderID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receiverid = models.CharField(db_column='ReceiverID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    datesent = models.DateTimeField(db_column='DateSent', blank=True, null=True)  # Field name made lowercase.
    dateread = models.DateTimeField(db_column='DateRead', blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=50, blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    reply = models.TextField(db_column='Reply', blank=True, null=True)  # Field name made lowercase.
    counter = models.IntegerField(db_column='Counter')  # Field name made lowercase.
    cc = models.TextField(db_column='CC', blank=True, null=True)  # Field name made lowercase.
    bcc = models.TextField(db_column='BCC', blank=True, null=True)  # Field name made lowercase.
    message_id = models.AutoField(db_column='Message_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Message'


class Messagedocs(TruncatedModel):
    messageid = models.IntegerField(db_column='MessageID', blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    docpath = models.CharField(db_column='DocPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    messagedocs_id = models.AutoField(db_column='MessageDocs_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'MessageDocs'


class Misccosts(TruncatedModel):
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    unitcost = models.FloatField(db_column='UnitCost', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    postedby = models.CharField(db_column='PostedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    resaleprice = models.FloatField(db_column='ResalePrice', blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendinvno = models.CharField(db_column='VendInvNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    outsideservice = models.CharField(db_column='OutsideService', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    markuppct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    misccosts_id = models.AutoField(db_column='MiscCosts_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'MiscCosts'


class Miscfiles(TruncatedModel):
    object = models.CharField(db_column='Object', max_length=12, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    companycode = models.CharField(db_column='CompanyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    printwithtrav = models.CharField(db_column='PrintWithTrav', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithwo = models.CharField(db_column='PrintWithWO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithack = models.CharField(db_column='PrintWithAck', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithquote = models.CharField(db_column='PrintWithQuote', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithdt = models.CharField(db_column='PrintWithDT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithpo = models.CharField(db_column='PrintWithPO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithcert = models.CharField(db_column='PrintWithCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    printwithrfq = models.CharField(db_column='PrintWithRFQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithinvoice = models.CharField(db_column='PrintWithInvoice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    printwithcar = models.CharField(db_column='PrintWithCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithnc = models.CharField(db_column='PrintWithNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    docnumber = models.CharField(db_column='DocNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)  # Field name made lowercase.
    miscfiles_id = models.AutoField(db_column='MiscFiles_ID', primary_key=True)  # Field name made lowercase.
    printwithreturnauth = models.CharField(db_column='PrintWithReturnAuth', max_length=1, blank=True, null=True)  # Field name made lowercase.
    email_guid = models.CharField(db_column='Email_Guid', max_length=200, blank=True, null=True)  # Field name made lowercase.
    email_file_name = models.CharField(db_column='Email_File_Name', max_length=200, blank=True, null=True)  # Field name made lowercase.
    repositoryid = models.IntegerField(db_column='RepositoryID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'MiscFiles'


class Mobilesession(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    companycode = models.CharField(db_column='CompanyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    sessionkey = models.CharField(db_column='SessionKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastaccessdate = models.DateTimeField(db_column='LastAccessDate', blank=True, null=True)  # Field name made lowercase.
    mobilesession_id = models.AutoField(db_column='MobileSession_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'MobileSession'


class Nextnumber(TruncatedModel):
    object = models.CharField(db_column='Object', unique=True, max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    nextnumber = models.IntegerField(db_column='NextNumber', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'NextNumber'


class Nonconformance(TruncatedModel):
    nonconfno = models.CharField(db_column='NonConfNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    nonconfcode = models.CharField(db_column='NonConfCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nonconfdate = models.DateTimeField(db_column='NonConfDate', blank=True, null=True)  # Field name made lowercase.
    returntype = models.CharField(db_column='ReturnType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    returnno = models.CharField(db_column='ReturnNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    returnitemno = models.SmallIntegerField(db_column='ReturnItemNo', blank=True, null=True)  # Field name made lowercase.
    correctiveactionno = models.CharField(db_column='CorrectiveActionNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    qtyreturned = models.IntegerField(db_column='QtyReturned', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custponum = models.CharField(db_column='CustPONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendrmano = models.CharField(db_column='VendRMANo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enterby = models.CharField(db_column='EnterBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    enterdate = models.DateTimeField(db_column='EnterDate', blank=True, null=True)  # Field name made lowercase.
    ncdescrip = models.TextField(db_column='NCDescrip', blank=True, null=True)  # Field name made lowercase.
    inspectedby = models.CharField(db_column='InspectedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reasoncode = models.CharField(db_column='ReasonCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    disposition = models.CharField(db_column='Disposition', max_length=50, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotno = models.TextField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    responsiblemgr = models.CharField(db_column='ResponsibleMgr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=12, blank=True, null=True)  # Field name made lowercase.
    processdate = models.DateTimeField(db_column='ProcessDate', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    ncprinted = models.CharField(db_column='NCPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nonconformance_id = models.AutoField(db_column='NonConformance_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'NonConformance'


class Nonconformancecode(TruncatedModel):
    nonconfcode = models.CharField(db_column='NonConfCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nonconformancecode_id = models.AutoField(db_column='NonConformanceCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'NonConformanceCode'


class Notify(TruncatedModel):
    sql = models.TextField(db_column='SQL', blank=True, null=True)  # Field name made lowercase.
    begindate = models.DateTimeField(db_column='BeginDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    nextdate = models.DateTimeField(db_column='NextDate', blank=True, null=True)  # Field name made lowercase.
    interval = models.FloatField(db_column='Interval', blank=True, null=True)  # Field name made lowercase.
    numberoftimesleft = models.IntegerField(db_column='NumberOfTimesLeft', blank=True, null=True)  # Field name made lowercase.
    quitafterhit = models.CharField(db_column='QuitAfterHit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recipient = models.TextField(db_column='Recipient', blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=255, blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=30, blank=True, null=True)  # Field name made lowercase.
    keyvalue = models.CharField(db_column='KeyValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    keyvalue2 = models.CharField(db_column='KeyValue2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    conditioncode = models.CharField(db_column='ConditionCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notify_id = models.AutoField(db_column='Notify_ID', primary_key=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=60, blank=True, null=True)  # Field name made lowercase.
    lastrun = models.DateTimeField(db_column='LastRun', blank=True, null=True)  # Field name made lowercase.
    attachments = models.TextField(db_column='Attachments', blank=True, null=True)  # Field name made lowercase.
    messagetype = models.SmallIntegerField(db_column='MessageType', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=30, blank=True, null=True)  # Field name made lowercase.
    areacode = models.CharField(db_column='AreaCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    faxnumber = models.CharField(db_column='FAXNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    documents = models.TextField(db_column='Documents', blank=True, null=True)  # Field name made lowercase.
    object = models.CharField(db_column='Object', max_length=12, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    private = models.CharField(db_column='Private', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dialingprefix = models.CharField(db_column='DialingPrefix', max_length=30, blank=True, null=True)  # Field name made lowercase.
    interval_unit = models.CharField(db_column='Interval_Unit', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reportcriteria = models.TextField(db_column='ReportCriteria', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    isqueued = models.NullBooleanField(db_column='IsQueued')  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    altprovidersql = models.TextField(db_column='AltProviderSQL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Notify'


class Notifyoptions(TruncatedModel):
    area = models.CharField(db_column='Area', max_length=30, blank=True, null=True)  # Field name made lowercase.
    conditioncode = models.CharField(db_column='ConditionCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sql = models.TextField(db_column='SQL', blank=True, null=True)  # Field name made lowercase.
    notifyoptions_id = models.AutoField(db_column='NotifyOptions_ID', primary_key=True)  # Field name made lowercase.
    recipient = models.TextField(db_column='Recipient', blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=255, blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    attachments = models.TextField(db_column='Attachments', blank=True, null=True)  # Field name made lowercase.
    messagetype = models.SmallIntegerField(db_column='MessageType', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=30, blank=True, null=True)  # Field name made lowercase.
    areacode = models.CharField(db_column='AreaCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    faxnumber = models.CharField(db_column='FAXNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    documents = models.TextField(db_column='Documents', blank=True, null=True)  # Field name made lowercase.
    object = models.CharField(db_column='Object', max_length=12, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    private = models.CharField(db_column='Private', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dialingprefix = models.CharField(db_column='DialingPrefix', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    altprovidersql = models.TextField(db_column='AltProviderSQL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'NotifyOptions'


class Online(TruncatedModel):
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    workcntr = models.SmallIntegerField(db_column='WorkCntr', blank=True, null=True)  # Field name made lowercase.
    opercode = models.CharField(db_column='OperCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    payrollrate = models.SmallIntegerField(db_column='PayrollRate', blank=True, null=True)  # Field name made lowercase.
    machrun = models.SmallIntegerField(db_column='MachRun', blank=True, null=True)  # Field name made lowercase.
    cyclehrs = models.FloatField(db_column='CycleHrs', blank=True, null=True)  # Field name made lowercase.
    logontime = models.DateTimeField(db_column='LogonTime', blank=True, null=True)  # Field name made lowercase.
    deviceno = models.SmallIntegerField(db_column='DeviceNo', blank=True, null=True)  # Field name made lowercase.
    estimhrs = models.FloatField(db_column='EstimHrs', blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    logontimerval = models.FloatField(db_column='LogonTimerVal', blank=True, null=True)  # Field name made lowercase.
    breakstart = models.CharField(db_column='BreakStart', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pcsrun = models.FloatField(db_column='PcsRun', blank=True, null=True)  # Field name made lowercase.
    totalbreaktime = models.FloatField(db_column='TotalBreakTime', blank=True, null=True)  # Field name made lowercase.
    displaylogontime = models.DateTimeField(db_column='DisplayLogonTime', blank=True, null=True)  # Field name made lowercase.
    online_id = models.AutoField(db_column='Online_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Online'


class Opercode(TruncatedModel):
    opercode = models.CharField(db_column='OperCode', max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    opernum = models.SmallIntegerField(db_column='OperNum', unique=True, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    defsetuptime = models.FloatField(db_column='DefSetupTime', blank=True, null=True)  # Field name made lowercase.
    deftimeunit = models.CharField(db_column='DefTimeUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    defcycletime = models.FloatField(db_column='DefCycleTime', blank=True, null=True)  # Field name made lowercase.
    defcycleunit = models.CharField(db_column='DefCycleUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pcteff = models.SmallIntegerField(db_column='PctEff', blank=True, null=True)  # Field name made lowercase.
    nummach = models.SmallIntegerField(db_column='NumMach', blank=True, null=True)  # Field name made lowercase.
    scrappct = models.FloatField(db_column='ScrapPct', blank=True, null=True)  # Field name made lowercase.
    teamsize = models.SmallIntegerField(db_column='TeamSize', blank=True, null=True)  # Field name made lowercase.
    newdescrip = models.TextField(db_column='NewDescrip', blank=True, null=True)  # Field name made lowercase.
    unattendop = models.CharField(db_column='UnattendOp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nummachforjob = models.FloatField(db_column='NumMachForJob', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OperCode'


class OrderDet(TruncatedModel):
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    job_no = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    part_desc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=6, blank=True, null=True)  # Field name made lowercase.
    billing_rate = models.SmallIntegerField(db_column='BillingRate', blank=True, null=True)  # Field name made lowercase.
    work_code = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    prod_code = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    unit_price = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    pricing_unit = models.CharField(db_column='PricingUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    master_job_no = models.CharField(db_column='MasterJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    misc_chg = models.FloatField(db_column='MiscChg', blank=True, null=True)  # Field name made lowercase.
    misc_descrip = models.CharField(db_column='MiscDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    estim_start_date = models.DateTimeField(db_column='EstimStartDate', blank=True, null=True)  # Field name made lowercase.
    estim_end_date = models.DateTimeField(db_column='EstimEndDate', blank=True, null=True)  # Field name made lowercase.
    actual_start_date = models.DateTimeField(db_column='ActualStartDate', blank=True, null=True)  # Field name made lowercase.
    actual_end_date = models.DateTimeField(db_column='ActualEndDate', blank=True, null=True)  # Field name made lowercase.
    misc_chg_billed = models.CharField(db_column='MiscChgBilled', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trav_printed = models.CharField(db_column='TravPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc_pct = models.FloatField(db_column='DiscPct', blank=True, null=True)  # Field name made lowercase.
    cumulative_billing = models.FloatField(db_column='CumulativeBilling', blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    comm_pct = models.FloatField(db_column='CommPct', blank=True, null=True)  # Field name made lowercase.
    job_notes = models.TextField(db_column='JobNotes', blank=True, null=True)  # Field name made lowercase.
    qty_ordered = models.IntegerField(db_column='QtyOrdered', blank=True, null=True)  # Field name made lowercase.
    qty_to_make = models.IntegerField(db_column='QtyToMake', blank=True, null=True)  # Field name made lowercase.
    qty_to_stock = models.IntegerField(db_column='QtyToStock', blank=True, null=True)  # Field name made lowercase.
    qty_canceled = models.IntegerField(db_column='QtyCanceled', blank=True, null=True)  # Field name made lowercase.
    qty_shipped_2_cust = models.IntegerField(db_column='QtyShipped2Cust', blank=True, null=True)  # Field name made lowercase.
    qty_shipped_2_stock = models.IntegerField(db_column='QtyShipped2Stock', blank=True, null=True)  # Field name made lowercase.
    total_est_hrs = models.FloatField(db_column='TotalEstHrs', blank=True, null=True)  # Field name made lowercase.
    total_actual_hrs = models.FloatField(db_column='TotalActualHrs', blank=True, null=True)  # Field name made lowercase.
    due_date = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    prev_saved = models.CharField(db_column='PrevSaved', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rel_set = models.SmallIntegerField(db_column='RelSet', blank=True, null=True)  # Field name made lowercase.
    date_finished = models.DateTimeField(db_column='DateFinished', blank=True, null=True)  # Field name made lowercase.
    current_work_cntr = models.CharField(db_column='CurrentWorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    job_label_printed = models.CharField(db_column='JobLabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedule_locked = models.CharField(db_column='ScheduleLocked', max_length=1, blank=True, null=True)  # Field name made lowercase.
    over_lap = models.CharField(db_column='Overlap', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scheduled = models.CharField(db_column='Scheduled', max_length=1, blank=True, null=True)  # Field name made lowercase.
    master_step_no = models.SmallIntegerField(db_column='MasterStepNo', blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    temp_priority = models.SmallIntegerField(db_column='TempPriority', blank=True, null=True)  # Field name made lowercase.
    quote_no = models.CharField(db_column='QuoteNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    quote_item_no = models.SmallIntegerField(db_column='QuoteItemNo', blank=True, null=True)  # Field name made lowercase.
    job_on_hold = models.CharField(db_column='JobOnHold', max_length=1, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OrderDet'
        unique_together = (('orderno', 'itemno'),)


class Orderfiles(TruncatedModel):
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    printwithtrav = models.CharField(db_column='PrintWithTrav', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithwo = models.CharField(db_column='PrintWithWO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithack = models.CharField(db_column='PrintWithAck', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithquote = models.CharField(db_column='PrintWithQuote', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithdt = models.CharField(db_column='PrintWithDT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithpo = models.CharField(db_column='PrintWithPO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithcert = models.CharField(db_column='PrintWithCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    printwithrfq = models.CharField(db_column='PrintWithRFQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithinvoice = models.CharField(db_column='PrintWithInvoice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    counter = models.AutoField(db_column='Counter', primary_key=True)  # Field name made lowercase.
    printwithcar = models.CharField(db_column='PrintWithCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithnc = models.CharField(db_column='PrintWithNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    docnumber = models.CharField(db_column='DocNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)  # Field name made lowercase.
    printwithreturnauth = models.CharField(db_column='PrintWithReturnAuth', max_length=1, blank=True, null=True)  # Field name made lowercase.
    email_guid = models.CharField(db_column='Email_Guid', max_length=200, blank=True, null=True)  # Field name made lowercase.
    email_file_name = models.CharField(db_column='Email_File_Name', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OrderFiles'


class Orderhistoryimported(TruncatedModel):
    orderhistoryimported_id = models.AutoField(db_column='OrderHistoryImported_ID', primary_key=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custdesc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    mainduedate = models.DateTimeField(db_column='MainDueDate', blank=True, null=True)  # Field name made lowercase.
    notestocust = models.TextField(db_column='NotesToCust', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    pricingunit = models.CharField(db_column='PricingUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qtyordered = models.IntegerField(db_column='QtyOrdered', blank=True, null=True)  # Field name made lowercase.
    qtytostock = models.IntegerField(db_column='QtyToStock', blank=True, null=True)  # Field name made lowercase.
    totalesthrs = models.FloatField(db_column='TotalEstHrs', blank=True, null=True)  # Field name made lowercase.
    totalactualhrs = models.FloatField(db_column='TotalActualHrs', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    datefinished = models.DateTimeField(db_column='DateFinished', blank=True, null=True)  # Field name made lowercase.
    commpct = models.FloatField(db_column='CommPct', blank=True, null=True)  # Field name made lowercase.
    jobnotes = models.TextField(db_column='JobNotes', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'OrderHistoryImported'


class Orderimport(TruncatedModel):
    dateprocessed = models.DateTimeField(db_column='DateProcessed', blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notestocust = models.TextField(db_column='NotesToCust', blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=30, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    purchcontact = models.CharField(db_column='PurchContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipaddr1 = models.CharField(db_column='ShipAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipaddr2 = models.CharField(db_column='ShipAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipcity = models.CharField(db_column='ShipCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipst = models.CharField(db_column='ShipSt', max_length=2, blank=True, null=True)  # Field name made lowercase.
    shipzip = models.CharField(db_column='ShipZIP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    header_user_date1 = models.DateTimeField(db_column='Header_User_Date1', blank=True, null=True)  # Field name made lowercase.
    header_user_date2 = models.DateTimeField(db_column='Header_User_Date2', blank=True, null=True)  # Field name made lowercase.
    header_user_text1 = models.CharField(db_column='Header_User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    header_user_text2 = models.CharField(db_column='Header_User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    header_user_text3 = models.CharField(db_column='Header_User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    header_user_text4 = models.CharField(db_column='Header_User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    header_user_currency1 = models.FloatField(db_column='Header_User_Currency1', blank=True, null=True)  # Field name made lowercase.
    header_user_currency2 = models.FloatField(db_column='Header_User_Currency2', blank=True, null=True)  # Field name made lowercase.
    header_user_number1 = models.FloatField(db_column='Header_User_Number1', blank=True, null=True)  # Field name made lowercase.
    header_user_number2 = models.FloatField(db_column='Header_User_Number2', blank=True, null=True)  # Field name made lowercase.
    header_user_number3 = models.FloatField(db_column='Header_User_Number3', blank=True, null=True)  # Field name made lowercase.
    header_user_number4 = models.FloatField(db_column='Header_User_Number4', blank=True, null=True)  # Field name made lowercase.
    header_user_memo1 = models.TextField(db_column='Header_User_Memo1', blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    pricingunit = models.CharField(db_column='PricingUnit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discpct = models.FloatField(db_column='DiscPct', blank=True, null=True)  # Field name made lowercase.
    miscchg = models.FloatField(db_column='MiscChg', blank=True, null=True)  # Field name made lowercase.
    miscdescrip = models.CharField(db_column='MiscDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    billingrate = models.SmallIntegerField(db_column='BillingRate', blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commpct = models.FloatField(db_column='CommPct', blank=True, null=True)  # Field name made lowercase.
    jobnotes = models.TextField(db_column='JobNotes', blank=True, null=True)  # Field name made lowercase.
    detail_user_date1 = models.DateTimeField(db_column='Detail_User_Date1', blank=True, null=True)  # Field name made lowercase.
    detail_user_date2 = models.DateTimeField(db_column='Detail_User_Date2', blank=True, null=True)  # Field name made lowercase.
    detail_user_text1 = models.CharField(db_column='Detail_User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    detail_user_text2 = models.CharField(db_column='Detail_User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    detail_user_text3 = models.CharField(db_column='Detail_User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    detail_user_text4 = models.CharField(db_column='Detail_User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    detail_user_currency1 = models.FloatField(db_column='Detail_User_Currency1', blank=True, null=True)  # Field name made lowercase.
    detail_user_currency2 = models.FloatField(db_column='Detail_User_Currency2', blank=True, null=True)  # Field name made lowercase.
    detail_user_number1 = models.FloatField(db_column='Detail_User_Number1', blank=True, null=True)  # Field name made lowercase.
    detail_user_number2 = models.FloatField(db_column='Detail_User_Number2', blank=True, null=True)  # Field name made lowercase.
    detail_user_number3 = models.FloatField(db_column='Detail_User_Number3', blank=True, null=True)  # Field name made lowercase.
    detail_user_number4 = models.FloatField(db_column='Detail_User_Number4', blank=True, null=True)  # Field name made lowercase.
    detail_user_memo1 = models.TextField(db_column='Detail_User_Memo1', blank=True, null=True)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    orderimport_id = models.AutoField(db_column='OrderImport_ID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    edisoftorderno = models.CharField(db_column='EDISoftOrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    edisoftitemno = models.SmallIntegerField(db_column='EDISoftItemNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OrderImport'


class OrderRouting(TruncatedModel):
    order_no = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    step_no = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    work_or_vend = models.SmallIntegerField(db_column='WorkOrVend', blank=True, null=True)  # Field name made lowercase.
    work_cntr = models.CharField(db_column='WorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vend_code = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    oper_code = models.CharField(db_column='OperCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    setup_time = models.FloatField(db_column='SetupTime', blank=True, null=True)  # Field name made lowercase.
    time_unit = models.CharField(db_column='TimeUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cycle_time = models.FloatField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    cycle_unit = models.CharField(db_column='CycleUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mach_run = models.SmallIntegerField(db_column='MachRun', blank=True, null=True)  # Field name made lowercase.
    team_size = models.SmallIntegerField(db_column='TeamSize', blank=True, null=True)  # Field name made lowercase.
    scrap_pct = models.FloatField(db_column='ScrapPct', blank=True, null=True)  # Field name made lowercase.
    pct_eff = models.FloatField(db_column='PctEff', blank=True, null=True)  # Field name made lowercase.
    labor_acct = models.CharField(db_column='LaborAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    setup_rate = models.FloatField(db_column='SetupRate', blank=True, null=True)  # Field name made lowercase.
    cycle_rate = models.FloatField(db_column='CycleRate', blank=True, null=True)  # Field name made lowercase.
    burden_rate = models.FloatField(db_column='BurdenRate', blank=True, null=True)  # Field name made lowercase.
    labor_rate = models.FloatField(db_column='LaborRate', blank=True, null=True)  # Field name made lowercase.
    unattend_op = models.CharField(db_column='UnattendOp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lead_time = models.SmallIntegerField(db_column='LeadTime', blank=True, null=True)  # Field name made lowercase.
    markup_pct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    cert_req = models.CharField(db_column='CertReq', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gl_code = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cost1 = models.FloatField(db_column='Cost1', blank=True, null=True)  # Field name made lowercase.
    unit1 = models.CharField(db_column='Unit1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup1 = models.FloatField(db_column='Setup1', blank=True, null=True)  # Field name made lowercase.
    cost2 = models.FloatField(db_column='Cost2', blank=True, null=True)  # Field name made lowercase.
    unit2 = models.CharField(db_column='Unit2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup2 = models.FloatField(db_column='Setup2', blank=True, null=True)  # Field name made lowercase.
    cost3 = models.FloatField(db_column='Cost3', blank=True, null=True)  # Field name made lowercase.
    unit3 = models.CharField(db_column='Unit3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup3 = models.FloatField(db_column='Setup3', blank=True, null=True)  # Field name made lowercase.
    cost4 = models.FloatField(db_column='Cost4', blank=True, null=True)  # Field name made lowercase.
    unit4 = models.CharField(db_column='Unit4', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup4 = models.FloatField(db_column='Setup4', blank=True, null=True)  # Field name made lowercase.
    cost5 = models.FloatField(db_column='Cost5', blank=True, null=True)  # Field name made lowercase.
    unit5 = models.CharField(db_column='Unit5', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup5 = models.FloatField(db_column='Setup5', blank=True, null=True)  # Field name made lowercase.
    cost6 = models.FloatField(db_column='Cost6', blank=True, null=True)  # Field name made lowercase.
    unit6 = models.CharField(db_column='Unit6', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup6 = models.FloatField(db_column='Setup6', blank=True, null=True)  # Field name made lowercase.
    cost7 = models.FloatField(db_column='Cost7', blank=True, null=True)  # Field name made lowercase.
    unit7 = models.CharField(db_column='Unit7', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup7 = models.FloatField(db_column='Setup7', blank=True, null=True)  # Field name made lowercase.
    cost8 = models.FloatField(db_column='Cost8', blank=True, null=True)  # Field name made lowercase.
    unit8 = models.CharField(db_column='Unit8', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup8 = models.FloatField(db_column='Setup8', blank=True, null=True)  # Field name made lowercase.
    setup_price = models.FloatField(db_column='SetupPrice', blank=True, null=True)  # Field name made lowercase.
    cycle_price = models.FloatField(db_column='CyclePrice', blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    estim_start_date = models.DateTimeField(db_column='EstimStartDate', blank=True, null=True)  # Field name made lowercase.
    estim_end_date = models.DateTimeField(db_column='EstimEndDate', blank=True, null=True)  # Field name made lowercase.
    actual_start_date = models.DateTimeField(db_column='ActualStartDate', blank=True, null=True)  # Field name made lowercase.
    actual_end_date = models.DateTimeField(db_column='ActualEndDate', blank=True, null=True)  # Field name made lowercase.
    estim_qty = models.IntegerField(db_column='EstimQty', blank=True, null=True)  # Field name made lowercase.
    actual_pcs_good = models.IntegerField(db_column='ActualPcsGood', blank=True, null=True)  # Field name made lowercase.
    actual_pcs_scrap = models.IntegerField(db_column='ActualPcsScrap', blank=True, null=True)  # Field name made lowercase.
    ignore_vend_min = models.CharField(db_column='IgnoreVendMin', max_length=1, blank=True, null=True)  # Field name made lowercase.
    item_no = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=12, blank=True, null=True)  # Field name made lowercase.
    empl_code = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tot_est_hrs = models.FloatField(db_column='TotEstHrs', blank=True, null=True)  # Field name made lowercase.
    tot_act_hrs = models.FloatField(db_column='TotActHrs', blank=True, null=True)  # Field name made lowercase.
    tot_hrs_left = models.FloatField(db_column='TotHrsLeft', blank=True, null=True)  # Field name made lowercase.
    dept_num = models.CharField(db_column='DeptNum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    overlap = models.CharField(db_column='Overlap', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shift_2_def_empl_code = models.CharField(db_column='Shift2DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shift_3_def_empl_code = models.CharField(db_column='Shift3DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    num_mach_for_job = models.FloatField(db_column='NumMachForJob', blank=True, null=True)  # Field name made lowercase.
    job_no = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    temp_estim_start_date = models.DateTimeField(db_column='TempEstimStartDate', blank=True, null=True)  # Field name made lowercase.
    temp_estim_end_date = models.DateTimeField(db_column='TempEstimEndDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OrderRouting'


class Ordersubrouting(TruncatedModel):
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    numoftimes = models.SmallIntegerField(db_column='NumOfTimes', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cycletime = models.FloatField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    cycleunit = models.CharField(db_column='CycleUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totalcycletime = models.FloatField(db_column='TotalCycleTime', blank=True, null=True)  # Field name made lowercase.
    setuptime = models.FloatField(db_column='SetupTime', blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    setupunit = models.CharField(db_column='SetupUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ordersubrouting_id = models.AutoField(db_column='OrderSubRouting_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'OrderSubRouting'


class Order(TruncatedModel):
    order_no = models.CharField(db_column='OrderNo', unique=True, max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    quote_no = models.CharField(db_column='QuoteNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    customer_code = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    customer_desc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    po_num = models.CharField(db_column='PONum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    date_ent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    ent_by = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    sales_id = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    terms_code = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tax_code = models.CharField(db_column='TaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    purch_contact = models.CharField(db_column='PurchContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ship_addr1 = models.CharField(db_column='ShipAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ship_addr2 = models.CharField(db_column='ShipAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ship_city = models.CharField(db_column='ShipCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ship_state = models.CharField(db_column='ShipSt', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ship_zip = models.CharField(db_column='ShipZIP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ship_via = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notes_to_cust = models.TextField(db_column='NotesToCust', blank=True, null=True)  # Field name made lowercase.
    wo_printed = models.CharField(db_column='WOPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ack_printed = models.CharField(db_column='AckPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    jt_printed = models.CharField(db_column='JTPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    order_total = models.FloatField(db_column='OrderTotal', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=30, blank=True, null=True)  # Field name made lowercase.
    main_due_date = models.DateTimeField(db_column='MainDueDate', blank=True, null=True)  # Field name made lowercase.
    main_priority = models.SmallIntegerField(db_column='MainPriority', blank=True, null=True)  # Field name made lowercase.
    ship_to_name = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    gst_code = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currency_code = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exch_rate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    date_ent_label = models.DateTimeField(db_column='DateEntLabel', blank=True, null=True)  # Field name made lowercase.
    ship_code = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Orders'


class Po(TruncatedModel):
    ponum = models.CharField(db_column='PONum', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    rfqno = models.CharField(db_column='RFQNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    datereq = models.DateTimeField(db_column='DateReq', blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendquoteno = models.CharField(db_column='VendQuoteNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    purchasedby = models.CharField(db_column='PurchasedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    datecomplete = models.DateTimeField(db_column='DateComplete', blank=True, null=True)  # Field name made lowercase.
    s_addr1 = models.CharField(db_column='S_Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_addr2 = models.CharField(db_column='S_Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_city = models.CharField(db_column='S_City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_st = models.CharField(db_column='S_St', max_length=2, blank=True, null=True)  # Field name made lowercase.
    s_zip = models.CharField(db_column='S_Zip', max_length=10, blank=True, null=True)  # Field name made lowercase.
    s_country = models.CharField(db_column='S_Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pototal = models.FloatField(db_column='POTotal', blank=True, null=True)  # Field name made lowercase.
    procflag = models.SmallIntegerField(db_column='ProcFlag', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    notes2vend = models.TextField(db_column='Notes2Vend', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    poprinted = models.CharField(db_column='POPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delticketprinted = models.CharField(db_column='DelTicketPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mainduedate = models.DateTimeField(db_column='MainDueDate', blank=True, null=True)  # Field name made lowercase.
    labelprinted = models.CharField(db_column='LabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dateentlabel = models.DateTimeField(db_column='DateEntLabel', blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    gsttaxcode = models.CharField(db_column='GSTTaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    gsttaxchgs = models.FloatField(db_column='GSTTaxChgs', blank=True, null=True)  # Field name made lowercase.
    salestaxcode = models.CharField(db_column='SalesTaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salestaxchgs = models.FloatField(db_column='SalesTaxChgs', blank=True, null=True)  # Field name made lowercase.
    ignoreminorder = models.CharField(db_column='IgnoreMinOrder', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shippingaddresstype = models.CharField(db_column='ShippingAddressType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.
    po_id = models.AutoField(db_column='PO_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PO'


class Podet(TruncatedModel):
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    qtyord = models.FloatField(db_column='QtyOrd', blank=True, null=True)  # Field name made lowercase.
    qtyrec = models.FloatField(db_column='QtyRec', blank=True, null=True)  # Field name made lowercase.
    qtycancel = models.FloatField(db_column='QtyCancel', blank=True, null=True)  # Field name made lowercase.
    qtyreject = models.FloatField(db_column='QtyReject', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    unitcost = models.FloatField(db_column='UnitCost', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    markuppct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    outsideservice = models.CharField(db_column='OutsideService', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=6, blank=True, null=True)  # Field name made lowercase.
    relset = models.SmallIntegerField(db_column='RelSet', blank=True, null=True)  # Field name made lowercase.
    miscchg = models.FloatField(db_column='MiscChg', blank=True, null=True)  # Field name made lowercase.
    miscdesc = models.CharField(db_column='MiscDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rev = models.CharField(db_column='Rev', max_length=30, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    jobno1 = models.CharField(db_column='JobNo1', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno2 = models.CharField(db_column='JobNo2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno3 = models.CharField(db_column='JobNo3', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno4 = models.CharField(db_column='JobNo4', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno5 = models.CharField(db_column='JobNo5', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno6 = models.CharField(db_column='JobNo6', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno7 = models.CharField(db_column='JobNo7', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno8 = models.CharField(db_column='JobNo8', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno9 = models.CharField(db_column='JobNo9', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno10 = models.CharField(db_column='JobNo10', max_length=16, blank=True, null=True)  # Field name made lowercase.
    qtyreq1 = models.FloatField(db_column='QtyReq1', blank=True, null=True)  # Field name made lowercase.
    qtyreq2 = models.FloatField(db_column='QtyReq2', blank=True, null=True)  # Field name made lowercase.
    qtyreq3 = models.FloatField(db_column='QtyReq3', blank=True, null=True)  # Field name made lowercase.
    qtyreq4 = models.FloatField(db_column='QtyReq4', blank=True, null=True)  # Field name made lowercase.
    qtyreq5 = models.FloatField(db_column='QtyReq5', blank=True, null=True)  # Field name made lowercase.
    qtyreq6 = models.FloatField(db_column='QtyReq6', blank=True, null=True)  # Field name made lowercase.
    qtyreq7 = models.FloatField(db_column='QtyReq7', blank=True, null=True)  # Field name made lowercase.
    qtyreq8 = models.FloatField(db_column='QtyReq8', blank=True, null=True)  # Field name made lowercase.
    qtyreq9 = models.FloatField(db_column='QtyReq9', blank=True, null=True)  # Field name made lowercase.
    qtyreq10 = models.FloatField(db_column='QtyReq10', blank=True, null=True)  # Field name made lowercase.
    certreq = models.CharField(db_column='CertReq', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datefinished = models.DateTimeField(db_column='DateFinished', blank=True, null=True)  # Field name made lowercase.
    taxstatus = models.CharField(db_column='TaxStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    podet_id = models.AutoField(db_column='PODet_ID', primary_key=True)  # Field name made lowercase.
    gridduedate = models.CharField(db_column='GridDueDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    item_number = models.IntegerField(db_column='Item_Number', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PODet'
        unique_together = (('ponum', 'partno'),)


class Pohistoryimported(TruncatedModel):
    pohistoryimported_id = models.AutoField(db_column='POHistoryImported_ID', primary_key=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    podate = models.DateTimeField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    datereq = models.DateTimeField(db_column='DateReq', blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    vendquoteno = models.CharField(db_column='VendQuoteNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notes2vend = models.TextField(db_column='Notes2Vend', blank=True, null=True)  # Field name made lowercase.
    itemno = models.IntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qtyord = models.FloatField(db_column='QtyOrd', blank=True, null=True)  # Field name made lowercase.
    qtyrec = models.FloatField(db_column='QtyRec', blank=True, null=True)  # Field name made lowercase.
    qtycancel = models.FloatField(db_column='QtyCancel', blank=True, null=True)  # Field name made lowercase.
    qtyreject = models.FloatField(db_column='QtyReject', blank=True, null=True)  # Field name made lowercase.
    unitcost = models.FloatField(db_column='UnitCost', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receivedate = models.DateTimeField(db_column='ReceiveDate', blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'POHistoryImported'


class Poreleases(TruncatedModel):
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    qtyrejected = models.FloatField(db_column='QtyRejected', blank=True, null=True)  # Field name made lowercase.
    qtycanceled = models.FloatField(db_column='QtyCanceled', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    datereceived = models.DateTimeField(db_column='DateReceived', blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    poreleases_id = models.AutoField(db_column='POReleases_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'POReleases'


class Partcalc(TruncatedModel):
    userid = models.CharField(db_column='UserID', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    running = models.CharField(db_column='Running', max_length=1, blank=True, null=True)  # Field name made lowercase.
    exename = models.CharField(db_column='EXEName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    subpartno = models.CharField(db_column='SubPartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    reloadfields = models.CharField(db_column='ReloadFields', max_length=1, blank=True, null=True)  # Field name made lowercase.
    partcalc_id = models.AutoField(db_column='PartCalc_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PartCalc'


class Partfiles(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    printwithtrav = models.CharField(db_column='PrintWithTrav', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithwo = models.CharField(db_column='PrintWithWO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithack = models.CharField(db_column='PrintWithAck', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithquote = models.CharField(db_column='PrintWithQuote', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithdt = models.CharField(db_column='PrintWithDT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithpo = models.CharField(db_column='PrintWithPO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithcert = models.CharField(db_column='PrintWithCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    printwithrfq = models.CharField(db_column='PrintWithRFQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithinvoice = models.CharField(db_column='PrintWithInvoice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    counter = models.AutoField(db_column='Counter', primary_key=True)  # Field name made lowercase.
    printwithcar = models.CharField(db_column='PrintWithCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printwithnc = models.CharField(db_column='PrintWithNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    docnumber = models.CharField(db_column='DocNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revision = models.CharField(db_column='Revision', max_length=30, blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)  # Field name made lowercase.
    printwithreturnauth = models.CharField(db_column='PrintWithReturnAuth', max_length=1, blank=True, null=True)  # Field name made lowercase.
    email_guid = models.CharField(db_column='Email_Guid', max_length=200, blank=True, null=True)  # Field name made lowercase.
    email_file_name = models.CharField(db_column='Email_File_Name', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PartFiles'


class Periodstatus(TruncatedModel):
    period = models.CharField(db_column='Period', unique=True, max_length=14)  # Field name made lowercase.
    posted = models.CharField(db_column='Posted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    periodstatus_id = models.AutoField(db_column='PeriodStatus_ID', primary_key=True)  # Field name made lowercase.
    fiscalyear = models.CharField(db_column='FiscalYear', max_length=12)  # Field name made lowercase.
    begindate = models.CharField(db_column='BeginDate', unique=True, max_length=10)  # Field name made lowercase.
    enddate = models.CharField(db_column='EndDate', max_length=10)  # Field name made lowercase.
    isadjustmentperiod = models.BooleanField(db_column='IsAdjustmentPeriod')  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'PeriodStatus'


class Prodcode(TruncatedModel):
    prodcode = models.CharField(db_column='ProdCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aracct = models.CharField(db_column='ARAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cashdisc = models.CharField(db_column='CashDisc', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesacct = models.CharField(db_column='SalesAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    freightacct = models.CharField(db_column='FreightAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prodcode_id = models.AutoField(db_column='ProdCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ProdCode'


class Prompt(TruncatedModel):
    field = models.CharField(db_column='Field', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    caption = models.CharField(db_column='Caption', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fillcombostring = models.CharField(db_column='FillComboString', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prompt_id = models.AutoField(db_column='Prompt_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Prompt'


class Quote(TruncatedModel):
    quoteno = models.CharField(db_column='QuoteNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    definedcust = models.CharField(db_column='DefinedCust', max_length=1, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custdesc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(db_column='Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr2 = models.CharField(db_column='Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    st = models.CharField(db_column='St', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=10, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    inqnum = models.CharField(db_column='InqNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    quotedby = models.CharField(db_column='QuotedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=30, blank=True, null=True)  # Field name made lowercase.
    followupdate = models.DateTimeField(db_column='FollowUpDate', blank=True, null=True)  # Field name made lowercase.
    expiredate = models.DateTimeField(db_column='ExpireDate', blank=True, null=True)  # Field name made lowercase.
    printed = models.CharField(db_column='Printed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    dateentlabel = models.DateTimeField(db_column='DateEntLabel', blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    quote_id = models.AutoField(db_column='Quote_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Quote'


class Quotedet(TruncatedModel):
    quoteno = models.CharField(db_column='QuoteNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    qty1 = models.IntegerField(db_column='Qty1', blank=True, null=True)  # Field name made lowercase.
    price1 = models.FloatField(db_column='Price1', blank=True, null=True)  # Field name made lowercase.
    unit1 = models.CharField(db_column='Unit1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty2 = models.IntegerField(db_column='Qty2', blank=True, null=True)  # Field name made lowercase.
    price2 = models.FloatField(db_column='Price2', blank=True, null=True)  # Field name made lowercase.
    unit2 = models.CharField(db_column='Unit2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty3 = models.IntegerField(db_column='Qty3', blank=True, null=True)  # Field name made lowercase.
    price3 = models.FloatField(db_column='Price3', blank=True, null=True)  # Field name made lowercase.
    unit3 = models.CharField(db_column='Unit3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty4 = models.IntegerField(db_column='Qty4', blank=True, null=True)  # Field name made lowercase.
    price4 = models.FloatField(db_column='Price4', blank=True, null=True)  # Field name made lowercase.
    unit4 = models.CharField(db_column='Unit4', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty5 = models.IntegerField(db_column='Qty5', blank=True, null=True)  # Field name made lowercase.
    price5 = models.FloatField(db_column='Price5', blank=True, null=True)  # Field name made lowercase.
    unit5 = models.CharField(db_column='Unit5', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty6 = models.IntegerField(db_column='Qty6', blank=True, null=True)  # Field name made lowercase.
    price6 = models.FloatField(db_column='Price6', blank=True, null=True)  # Field name made lowercase.
    unit6 = models.CharField(db_column='Unit6', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty7 = models.IntegerField(db_column='Qty7', blank=True, null=True)  # Field name made lowercase.
    price7 = models.FloatField(db_column='Price7', blank=True, null=True)  # Field name made lowercase.
    unit7 = models.CharField(db_column='Unit7', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty8 = models.IntegerField(db_column='Qty8', blank=True, null=True)  # Field name made lowercase.
    price8 = models.FloatField(db_column='Price8', blank=True, null=True)  # Field name made lowercase.
    unit8 = models.CharField(db_column='Unit8', max_length=3, blank=True, null=True)  # Field name made lowercase.
    miscchg = models.FloatField(db_column='MiscChg', blank=True, null=True)  # Field name made lowercase.
    miscdescrip = models.CharField(db_column='MiscDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', max_length=40, blank=True, null=True)  # Field name made lowercase.
    commpct = models.FloatField(db_column='CommPct', blank=True, null=True)  # Field name made lowercase.
    discpct = models.FloatField(db_column='DiscPct', blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobnotes = models.TextField(db_column='JobNotes', blank=True, null=True)  # Field name made lowercase.
    rev = models.CharField(db_column='Rev', max_length=10, blank=True, null=True)  # Field name made lowercase.
    quotepart = models.CharField(db_column='QuotePart', max_length=1, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=4, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    quotedet_id = models.AutoField(db_column='QuoteDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    istaxable = models.BooleanField(db_column='IsTaxable')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'QuoteDet'
        unique_together = (('quoteno', 'itemno'),)


class Rfq(TruncatedModel):
    rfqno = models.CharField(db_column='RFQNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    v_addr1 = models.CharField(db_column='V_Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    v_addr2 = models.CharField(db_column='V_Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    v_city = models.CharField(db_column='V_City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    v_st = models.CharField(db_column='V_St', max_length=2, blank=True, null=True)  # Field name made lowercase.
    v_zip = models.CharField(db_column='V_Zip', max_length=10, blank=True, null=True)  # Field name made lowercase.
    v_country = models.CharField(db_column='V_Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    s_addr1 = models.CharField(db_column='S_Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_addr2 = models.CharField(db_column='S_Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_city = models.CharField(db_column='S_City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    s_st = models.CharField(db_column='S_St', max_length=2, blank=True, null=True)  # Field name made lowercase.
    s_zip = models.CharField(db_column='S_Zip', max_length=10, blank=True, null=True)  # Field name made lowercase.
    s_country = models.CharField(db_column='S_Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendorquote = models.CharField(db_column='VendorQuote', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reqby = models.CharField(db_column='ReqBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    datereq = models.DateTimeField(db_column='DateReq', blank=True, null=True)  # Field name made lowercase.
    expiredate = models.DateTimeField(db_column='ExpireDate', blank=True, null=True)  # Field name made lowercase.
    printed = models.CharField(db_column='Printed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rfqtype = models.CharField(db_column='RFQType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rfqouttype = models.CharField(db_column='RFQOutType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salestaxcode = models.CharField(db_column='SalesTaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.
    rfq_id = models.AutoField(db_column='RFQ_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'RFQ'


class Rfqdet(TruncatedModel):
    rfqno = models.CharField(db_column='RFQNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    qty1 = models.IntegerField(db_column='Qty1', blank=True, null=True)  # Field name made lowercase.
    price1 = models.FloatField(db_column='Price1', blank=True, null=True)  # Field name made lowercase.
    unit1 = models.CharField(db_column='Unit1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qty2 = models.IntegerField(db_column='Qty2', blank=True, null=True)  # Field name made lowercase.
    price2 = models.FloatField(db_column='Price2', blank=True, null=True)  # Field name made lowercase.
    qty3 = models.IntegerField(db_column='Qty3', blank=True, null=True)  # Field name made lowercase.
    price3 = models.FloatField(db_column='Price3', blank=True, null=True)  # Field name made lowercase.
    qty4 = models.IntegerField(db_column='Qty4', blank=True, null=True)  # Field name made lowercase.
    price4 = models.FloatField(db_column='Price4', blank=True, null=True)  # Field name made lowercase.
    qty5 = models.IntegerField(db_column='Qty5', blank=True, null=True)  # Field name made lowercase.
    price5 = models.FloatField(db_column='Price5', blank=True, null=True)  # Field name made lowercase.
    qty6 = models.IntegerField(db_column='Qty6', blank=True, null=True)  # Field name made lowercase.
    price6 = models.FloatField(db_column='Price6', blank=True, null=True)  # Field name made lowercase.
    qty7 = models.IntegerField(db_column='Qty7', blank=True, null=True)  # Field name made lowercase.
    price7 = models.FloatField(db_column='Price7', blank=True, null=True)  # Field name made lowercase.
    qty8 = models.IntegerField(db_column='Qty8', blank=True, null=True)  # Field name made lowercase.
    price8 = models.FloatField(db_column='Price8', blank=True, null=True)  # Field name made lowercase.
    miscchg = models.FloatField(db_column='MiscChg', blank=True, null=True)  # Field name made lowercase.
    miscdescrip = models.CharField(db_column='MiscDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prodcode = models.CharField(db_column='ProdCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobnotes = models.TextField(db_column='JobNotes', blank=True, null=True)  # Field name made lowercase.
    rev = models.CharField(db_column='Rev', max_length=10, blank=True, null=True)  # Field name made lowercase.
    quotepart = models.CharField(db_column='QuotePart', max_length=1, blank=True, null=True)  # Field name made lowercase.
    jobno1 = models.CharField(db_column='JobNo1', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno2 = models.CharField(db_column='JobNo2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno3 = models.CharField(db_column='JobNo3', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno4 = models.CharField(db_column='JobNo4', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno5 = models.CharField(db_column='JobNo5', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno6 = models.CharField(db_column='JobNo6', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno7 = models.CharField(db_column='JobNo7', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno8 = models.CharField(db_column='JobNo8', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno9 = models.CharField(db_column='JobNo9', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno10 = models.CharField(db_column='JobNo10', max_length=16, blank=True, null=True)  # Field name made lowercase.
    qtyreq1 = models.FloatField(db_column='QtyReq1', blank=True, null=True)  # Field name made lowercase.
    qtyreq2 = models.FloatField(db_column='QtyReq2', blank=True, null=True)  # Field name made lowercase.
    qtyreq3 = models.FloatField(db_column='QtyReq3', blank=True, null=True)  # Field name made lowercase.
    qtyreq4 = models.FloatField(db_column='QtyReq4', blank=True, null=True)  # Field name made lowercase.
    qtyreq5 = models.FloatField(db_column='QtyReq5', blank=True, null=True)  # Field name made lowercase.
    qtyreq6 = models.FloatField(db_column='QtyReq6', blank=True, null=True)  # Field name made lowercase.
    qtyreq7 = models.FloatField(db_column='QtyReq7', blank=True, null=True)  # Field name made lowercase.
    qtyreq8 = models.FloatField(db_column='QtyReq8', blank=True, null=True)  # Field name made lowercase.
    qtyreq9 = models.FloatField(db_column='QtyReq9', blank=True, null=True)  # Field name made lowercase.
    qtyreq10 = models.FloatField(db_column='QtyReq10', blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=4, blank=True, null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    taxstatus = models.CharField(db_column='TaxStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rfqdet_id = models.AutoField(db_column='RFQDet_ID', primary_key=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'RFQDet'


class Reasoncode(TruncatedModel):
    reasoncode = models.CharField(db_column='ReasonCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    reasonnum = models.SmallIntegerField(db_column='ReasonNum', unique=True, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    createrma = models.CharField(db_column='CreateRMA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reasoncode_id = models.AutoField(db_column='ReasonCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ReasonCode'


class Receipt(TruncatedModel):
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custdesc = models.CharField(db_column='CustDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    checkno = models.CharField(db_column='CheckNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    recdate = models.DateTimeField(db_column='RecDate', blank=True, null=True)  # Field name made lowercase.
    grossamt = models.FloatField(db_column='GrossAmt', blank=True, null=True)  # Field name made lowercase.
    discountamt = models.FloatField(db_column='DiscountAmt', blank=True, null=True)  # Field name made lowercase.
    netamt = models.FloatField(db_column='NetAmt', blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='BankCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    clearedbank = models.CharField(db_column='ClearedBank', max_length=1, blank=True, null=True)  # Field name made lowercase.
    periodno = models.CharField(db_column='PeriodNo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    procflag = models.SmallIntegerField(db_column='ProcFlag', blank=True, null=True)  # Field name made lowercase.
    recposted = models.CharField(db_column='RecPosted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    salesid = models.CharField(db_column='SalesID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=30, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    custcurrencycode = models.CharField(db_column='CustCurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custexchrate = models.FloatField(db_column='CustExchRate', blank=True, null=True)  # Field name made lowercase.
    exchrategainlossamt = models.FloatField(db_column='ExchRateGainLossAmt', blank=True, null=True)  # Field name made lowercase.
    receipt_id = models.AutoField(db_column='Receipt_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Receipt'
        unique_together = (('custcode', 'checkno'),)


class Receiptdet(TruncatedModel):
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    checkno = models.CharField(db_column='CheckNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    recdate = models.DateTimeField(db_column='RecDate', blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invtotal = models.FloatField(db_column='InvTotal', blank=True, null=True)  # Field name made lowercase.
    grossamt = models.FloatField(db_column='GrossAmt', blank=True, null=True)  # Field name made lowercase.
    discamt = models.FloatField(db_column='DiscAmt', blank=True, null=True)  # Field name made lowercase.
    netamt = models.FloatField(db_column='NetAmt', blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invexchrate = models.FloatField(db_column='InvExchRate', blank=True, null=True)  # Field name made lowercase.
    exchrategainloss = models.FloatField(db_column='ExchRateGainLoss', blank=True, null=True)  # Field name made lowercase.
    receiptdet_id = models.AutoField(db_column='ReceiptDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ReceiptDet'


class Receiver(TruncatedModel):
    receiverno = models.CharField(db_column='ReceiverNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    packingslipno = models.CharField(db_column='PackingSlipNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receivedate = models.DateTimeField(db_column='ReceiveDate', blank=True, null=True)  # Field name made lowercase.
    procflag = models.SmallIntegerField(db_column='ProcFlag', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shippingchgs = models.FloatField(db_column='ShippingChgs', blank=True, null=True)  # Field name made lowercase.
    recvrprinted = models.CharField(db_column='RecvrPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certprinted = models.CharField(db_column='CertPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    billed = models.CharField(db_column='Billed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    labelprinted = models.CharField(db_column='LabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    debitprinted = models.CharField(db_column='DebitPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recvlabelprinted = models.CharField(db_column='RecvLabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.
    receiver_id = models.AutoField(db_column='Receiver_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Receiver'


class Receiverbins(TruncatedModel):
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    binlabel = models.CharField(db_column='BinLabel', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty1 = models.FloatField(db_column='BinQty1', blank=True, null=True)  # Field name made lowercase.
    binloc1 = models.CharField(db_column='BinLoc1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty2 = models.FloatField(db_column='BinQty2', blank=True, null=True)  # Field name made lowercase.
    binloc2 = models.CharField(db_column='BinLoc2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty3 = models.FloatField(db_column='BinQty3', blank=True, null=True)  # Field name made lowercase.
    binloc3 = models.CharField(db_column='BinLoc3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty4 = models.FloatField(db_column='BinQty4', blank=True, null=True)  # Field name made lowercase.
    binloc4 = models.CharField(db_column='BinLoc4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    binqty5 = models.FloatField(db_column='BinQty5', blank=True, null=True)  # Field name made lowercase.
    binloc5 = models.CharField(db_column='BinLoc5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receiverbins_id = models.AutoField(db_column='ReceiverBins_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ReceiverBins'


class Receiverdet(TruncatedModel):
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    qtyopen = models.FloatField(db_column='QtyOpen', blank=True, null=True)  # Field name made lowercase.
    qty2receive = models.FloatField(db_column='Qty2Receive', blank=True, null=True)  # Field name made lowercase.
    qty2stock = models.FloatField(db_column='Qty2Stock', blank=True, null=True)  # Field name made lowercase.
    qty2cancel = models.FloatField(db_column='Qty2Cancel', blank=True, null=True)  # Field name made lowercase.
    qty2reject = models.FloatField(db_column='Qty2Reject', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    procflag = models.SmallIntegerField(db_column='ProcFlag', blank=True, null=True)  # Field name made lowercase.
    jobno1 = models.CharField(db_column='JobNo1', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno2 = models.CharField(db_column='JobNo2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno3 = models.CharField(db_column='JobNo3', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno4 = models.CharField(db_column='JobNo4', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno5 = models.CharField(db_column='JobNo5', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno6 = models.CharField(db_column='JobNo6', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno7 = models.CharField(db_column='JobNo7', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno8 = models.CharField(db_column='JobNo8', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno9 = models.CharField(db_column='JobNo9', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jobno10 = models.CharField(db_column='JobNo10', max_length=16, blank=True, null=True)  # Field name made lowercase.
    qtyreceived1 = models.FloatField(db_column='QtyReceived1', blank=True, null=True)  # Field name made lowercase.
    qtyreceived2 = models.FloatField(db_column='QtyReceived2', blank=True, null=True)  # Field name made lowercase.
    qtyreceived3 = models.FloatField(db_column='QtyReceived3', blank=True, null=True)  # Field name made lowercase.
    qtyreceived4 = models.FloatField(db_column='QtyReceived4', blank=True, null=True)  # Field name made lowercase.
    qtyreceived5 = models.FloatField(db_column='QtyReceived5', blank=True, null=True)  # Field name made lowercase.
    qtyreceived6 = models.FloatField(db_column='QtyReceived6', blank=True, null=True)  # Field name made lowercase.
    qtyreceived7 = models.FloatField(db_column='QtyReceived7', blank=True, null=True)  # Field name made lowercase.
    qtyreceived8 = models.FloatField(db_column='QtyReceived8', blank=True, null=True)  # Field name made lowercase.
    qtyreceived9 = models.FloatField(db_column='QtyReceived9', blank=True, null=True)  # Field name made lowercase.
    qtyreceived10 = models.FloatField(db_column='QtyReceived10', blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qtyopen1 = models.FloatField(db_column='QtyOpen1', blank=True, null=True)  # Field name made lowercase.
    qtyopen2 = models.FloatField(db_column='QtyOpen2', blank=True, null=True)  # Field name made lowercase.
    qtyopen3 = models.FloatField(db_column='QtyOpen3', blank=True, null=True)  # Field name made lowercase.
    qtyopen4 = models.FloatField(db_column='QtyOpen4', blank=True, null=True)  # Field name made lowercase.
    qtyopen5 = models.FloatField(db_column='QtyOpen5', blank=True, null=True)  # Field name made lowercase.
    qtyopen6 = models.FloatField(db_column='QtyOpen6', blank=True, null=True)  # Field name made lowercase.
    qtyopen7 = models.FloatField(db_column='QtyOpen7', blank=True, null=True)  # Field name made lowercase.
    qtyopen8 = models.FloatField(db_column='QtyOpen8', blank=True, null=True)  # Field name made lowercase.
    qtyopen9 = models.FloatField(db_column='QtyOpen9', blank=True, null=True)  # Field name made lowercase.
    qtyopen10 = models.FloatField(db_column='QtyOpen10', blank=True, null=True)  # Field name made lowercase.
    qtycancel1 = models.FloatField(db_column='QtyCancel1', blank=True, null=True)  # Field name made lowercase.
    qtycancel2 = models.FloatField(db_column='QtyCancel2', blank=True, null=True)  # Field name made lowercase.
    qtycancel3 = models.FloatField(db_column='QtyCancel3', blank=True, null=True)  # Field name made lowercase.
    qtycancel4 = models.FloatField(db_column='QtyCancel4', blank=True, null=True)  # Field name made lowercase.
    qtycancel5 = models.FloatField(db_column='QtyCancel5', blank=True, null=True)  # Field name made lowercase.
    qtycancel6 = models.FloatField(db_column='QtyCancel6', blank=True, null=True)  # Field name made lowercase.
    qtycancel7 = models.FloatField(db_column='QtyCancel7', blank=True, null=True)  # Field name made lowercase.
    qtycancel8 = models.FloatField(db_column='QtyCancel8', blank=True, null=True)  # Field name made lowercase.
    qtycancel9 = models.FloatField(db_column='QtyCancel9', blank=True, null=True)  # Field name made lowercase.
    qtycancel10 = models.FloatField(db_column='QtyCancel10', blank=True, null=True)  # Field name made lowercase.
    qtyreject1 = models.FloatField(db_column='QtyReject1', blank=True, null=True)  # Field name made lowercase.
    qtyreject2 = models.FloatField(db_column='QtyReject2', blank=True, null=True)  # Field name made lowercase.
    qtyreject3 = models.FloatField(db_column='QtyReject3', blank=True, null=True)  # Field name made lowercase.
    qtyreject4 = models.FloatField(db_column='QtyReject4', blank=True, null=True)  # Field name made lowercase.
    qtyreject5 = models.FloatField(db_column='QtyReject5', blank=True, null=True)  # Field name made lowercase.
    qtyreject6 = models.FloatField(db_column='QtyReject6', blank=True, null=True)  # Field name made lowercase.
    qtyreject7 = models.FloatField(db_column='QtyReject7', blank=True, null=True)  # Field name made lowercase.
    qtyreject8 = models.FloatField(db_column='QtyReject8', blank=True, null=True)  # Field name made lowercase.
    qtyreject9 = models.FloatField(db_column='QtyReject9', blank=True, null=True)  # Field name made lowercase.
    qtyreject10 = models.FloatField(db_column='QtyReject10', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    lotno = models.TextField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    binlabel = models.CharField(db_column='BinLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    receiverdet_id = models.AutoField(db_column='ReceiverDet_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ReceiverDet'


class Relation(TruncatedModel):
    parenttable = models.CharField(db_column='ParentTable', max_length=255, blank=True, null=True)  # Field name made lowercase.
    childtable = models.CharField(db_column='ChildTable', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parentkey = models.CharField(db_column='ParentKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    childkey = models.CharField(db_column='ChildKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    childindex = models.CharField(db_column='ChildIndex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    relation_id = models.AutoField(db_column='Relation_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Relation'


class Releases(TruncatedModel):
    orderno = models.CharField(db_column='OrderNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    deltype = models.SmallIntegerField(db_column='DelType', blank=True, null=True)  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    datecomplete = models.DateTimeField(db_column='DateComplete', blank=True, null=True)  # Field name made lowercase.
    deliveryticketno = models.CharField(db_column='DeliveryTicketNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    itemno = models.SmallIntegerField(db_column='ItemNo', blank=True, null=True)  # Field name made lowercase.
    destjobno = models.CharField(db_column='DestJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    mfgjobno = models.CharField(db_column='MfgJobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    binlocation = models.CharField(db_column='BinLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lotno = models.TextField(db_column='LotNo', blank=True, null=True)  # Field name made lowercase.
    edisoftitemno = models.SmallIntegerField(db_column='EDISoftItemNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Releases'


class Repository(TruncatedModel):
    repositoryid = models.AutoField(db_column='RepositoryID', primary_key=True)  # Field name made lowercase.
    filename = models.CharField(db_column='Filename', max_length=1024)  # Field name made lowercase.
    contenttype = models.CharField(db_column='ContentType', max_length=1024)  # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FileSize')  # Field name made lowercase.
    folderid = models.IntegerField(db_column='FolderID')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    updateduserid = models.CharField(db_column='UpdatedUserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    progress = models.FloatField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
    filesecret = models.CharField(db_column='FileSecret', max_length=36, blank=True, null=True)  # Field name made lowercase.
    incloud = models.NullBooleanField(db_column='InCloud')  # Field name made lowercase.
    accesscount = models.IntegerField(db_column='AccessCount', blank=True, null=True)  # Field name made lowercase.
    lastaccessed = models.DateTimeField(db_column='LastAccessed', blank=True, null=True)  # Field name made lowercase.
    lastserver = models.CharField(db_column='LastServer', max_length=128, blank=True, null=True)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Repository'


class Repositoryfolder(TruncatedModel):
    folderid = models.AutoField(db_column='FolderID', primary_key=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=256)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'RepositoryFolder'


class Repositorysecurity(TruncatedModel):
    folderid = models.IntegerField(db_column='FolderID')  # Field name made lowercase.
    usergroupid = models.IntegerField(db_column='UserGroupID')  # Field name made lowercase.
    securityflags = models.IntegerField(db_column='SecurityFlags')  # Field name made lowercase.
    repositorysecurity_id = models.AutoField(db_column='RepositorySecurity_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'RepositorySecurity'
        unique_together = (('folderid', 'usergroupid'),)


class Reviewcode(TruncatedModel):
    reviewcode = models.CharField(db_column='ReviewCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reviewcode_id = models.AutoField(db_column='ReviewCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ReviewCode'


class Routing(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True, primary_key=True)  # Field name made lowercase.
    workorvend = models.SmallIntegerField(db_column='WorkOrVend', blank=True, null=True)  # Field name made lowercase.
    workcntr = models.CharField(db_column='WorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opercode = models.CharField(db_column='OperCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    setuptime = models.FloatField(db_column='SetupTime', blank=True, null=True)  # Field name made lowercase.
    timeunit = models.CharField(db_column='TimeUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cycletime = models.FloatField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    cycleunit = models.CharField(db_column='CycleUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    machrun = models.SmallIntegerField(db_column='MachRun', blank=True, null=True)  # Field name made lowercase.
    teamsize = models.SmallIntegerField(db_column='TeamSize', blank=True, null=True)  # Field name made lowercase.
    scrappct = models.FloatField(db_column='ScrapPct', blank=True, null=True)  # Field name made lowercase.
    pcteff = models.FloatField(db_column='PctEff', blank=True, null=True)  # Field name made lowercase.
    laboracct = models.CharField(db_column='LaborAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    setuprate = models.FloatField(db_column='SetupRate', blank=True, null=True)  # Field name made lowercase.
    cyclerate = models.FloatField(db_column='CycleRate', blank=True, null=True)  # Field name made lowercase.
    burdenrate = models.FloatField(db_column='BurdenRate', blank=True, null=True)  # Field name made lowercase.
    laborrate = models.FloatField(db_column='LaborRate', blank=True, null=True)  # Field name made lowercase.
    unattendop = models.CharField(db_column='UnattendOp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    leadtime = models.SmallIntegerField(db_column='LeadTime', blank=True, null=True)  # Field name made lowercase.
    markuppct = models.FloatField(db_column='MarkupPct', blank=True, null=True)  # Field name made lowercase.
    certreq = models.CharField(db_column='CertReq', max_length=1, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cost1 = models.FloatField(db_column='Cost1', blank=True, null=True)  # Field name made lowercase.
    unit1 = models.CharField(db_column='Unit1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup1 = models.FloatField(db_column='Setup1', blank=True, null=True)  # Field name made lowercase.
    cost2 = models.FloatField(db_column='Cost2', blank=True, null=True)  # Field name made lowercase.
    unit2 = models.CharField(db_column='Unit2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup2 = models.FloatField(db_column='Setup2', blank=True, null=True)  # Field name made lowercase.
    cost3 = models.FloatField(db_column='Cost3', blank=True, null=True)  # Field name made lowercase.
    unit3 = models.CharField(db_column='Unit3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup3 = models.FloatField(db_column='Setup3', blank=True, null=True)  # Field name made lowercase.
    cost4 = models.FloatField(db_column='Cost4', blank=True, null=True)  # Field name made lowercase.
    unit4 = models.CharField(db_column='Unit4', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup4 = models.FloatField(db_column='Setup4', blank=True, null=True)  # Field name made lowercase.
    cost5 = models.FloatField(db_column='Cost5', blank=True, null=True)  # Field name made lowercase.
    unit5 = models.CharField(db_column='Unit5', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup5 = models.FloatField(db_column='Setup5', blank=True, null=True)  # Field name made lowercase.
    cost6 = models.FloatField(db_column='Cost6', blank=True, null=True)  # Field name made lowercase.
    unit6 = models.CharField(db_column='Unit6', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup6 = models.FloatField(db_column='Setup6', blank=True, null=True)  # Field name made lowercase.
    cost7 = models.FloatField(db_column='Cost7', blank=True, null=True)  # Field name made lowercase.
    unit7 = models.CharField(db_column='Unit7', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup7 = models.FloatField(db_column='Setup7', blank=True, null=True)  # Field name made lowercase.
    cost8 = models.FloatField(db_column='Cost8', blank=True, null=True)  # Field name made lowercase.
    unit8 = models.CharField(db_column='Unit8', max_length=3, blank=True, null=True)  # Field name made lowercase.
    setup8 = models.FloatField(db_column='Setup8', blank=True, null=True)  # Field name made lowercase.
    setupprice = models.FloatField(db_column='SetupPrice', blank=True, null=True)  # Field name made lowercase.
    cycleprice = models.FloatField(db_column='CyclePrice', blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    estimqty = models.IntegerField(db_column='EstimQty', blank=True, null=True)  # Field name made lowercase.
    actualpiecesgood = models.IntegerField(db_column='ActualPiecesGood', blank=True, null=True)  # Field name made lowercase.
    actualpiecesscrapped = models.IntegerField(db_column='ActualPiecesScrapped', blank=True, null=True)  # Field name made lowercase.
    ignorevendmin = models.CharField(db_column='IgnoreVendMin', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nummachforjob = models.FloatField(db_column='NumMachForJob', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Routing'
        unique_together = (('partno', 'stepno'),)


class Salesid(TruncatedModel):
    salesid = models.CharField(db_column='SalesID', unique=True, max_length=12, primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commperc = models.FloatField(db_column='CommPerc', blank=True, null=True)  # Field name made lowercase.
    commacct = models.CharField(db_column='CommAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ytdsales = models.FloatField(db_column='YTDSales', blank=True, null=True)  # Field name made lowercase.
    ytdcomm = models.FloatField(db_column='YTDComm', blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(db_column='Addr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr2 = models.CharField(db_column='Addr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'SalesID'


class Scheduling(TruncatedModel):
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    workcntr = models.CharField(db_column='WorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    searchdate = models.IntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    hours = models.FloatField(db_column='Hours', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=12, blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    manhrs = models.FloatField(db_column='ManHrs', blank=True, null=True)  # Field name made lowercase.
    shift = models.SmallIntegerField(db_column='Shift', blank=True, null=True)  # Field name made lowercase.
    qtime = models.FloatField(db_column='QTime', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    scheduling_id = models.AutoField(db_column='Scheduling_ID', primary_key=True)  # Field name made lowercase.
    breakhrs = models.FloatField(db_column='BreakHrs', blank=True, null=True)  # Field name made lowercase.
    machine = models.IntegerField(db_column='Machine', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Scheduling'


class Security(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    companycode = models.CharField(db_column='CompanyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    area = models.IntegerField(db_column='Area', blank=True, null=True)  # Field name made lowercase.
    has_access = models.IntegerField(db_column='Has_Access', blank=True, null=True)  # Field name made lowercase.
    security_id = models.AutoField(db_column='Security_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Security'
        unique_together = (('userid', 'companycode', 'area'),)


class Servicelogs(TruncatedModel):
    servicetype = models.CharField(db_column='ServiceType', max_length=20)  # Field name made lowercase.
    areatype = models.CharField(db_column='AreaType', max_length=60, blank=True, null=True)  # Field name made lowercase.
    wasfailure = models.NullBooleanField(db_column='WasFailure')  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    rundate = models.DateTimeField(db_column='RunDate')  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12)  # Field name made lowercase.
    servicelogs_id = models.AutoField(db_column='ServiceLogs_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ServiceLogs'


class Shipmethod(TruncatedModel):
    shippingcode = models.CharField(db_column='ShippingCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendorcode = models.CharField(db_column='VendorCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shippingdescription = models.CharField(db_column='ShippingDescription', max_length=30, blank=True, null=True)  # Field name made lowercase.
    insurance = models.CharField(db_column='Insurance', max_length=1, blank=True, null=True)  # Field name made lowercase.
    containerunit = models.CharField(db_column='ContainerUnit', max_length=5, blank=True, null=True)  # Field name made lowercase.
    handlingcharge = models.FloatField(db_column='HandlingCharge', blank=True, null=True)  # Field name made lowercase.
    codfee = models.FloatField(db_column='CODFee', blank=True, null=True)  # Field name made lowercase.
    accountnumber = models.CharField(db_column='AccountNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    emptycontainerweight = models.FloatField(db_column='EmptyContainerWeight', blank=True, null=True)  # Field name made lowercase.
    maximumcontainerweight = models.FloatField(db_column='MaximumContainerWeight', blank=True, null=True)  # Field name made lowercase.
    declaredvalue = models.FloatField(db_column='DeclaredValue', blank=True, null=True)  # Field name made lowercase.
    descripofcontents = models.TextField(db_column='DescripOfContents', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=150, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    shipmethod_id = models.AutoField(db_column='ShipMethod_ID', primary_key=True)  # Field name made lowercase.
    apikey = models.CharField(db_column='APIKey', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meternumber = models.CharField(db_column='MeterNumber', max_length=9, blank=True, null=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='AccountType', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salt = models.CharField(db_column='Salt', max_length=512, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    iszebralabels = models.NullBooleanField(db_column='IsZebraLabels')  # Field name made lowercase.
    labelformat = models.CharField(db_column='LabelFormat', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ShipMethod'


class Shipto(TruncatedModel):
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    saddr1 = models.CharField(db_column='SAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    saddr2 = models.CharField(db_column='SAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scity = models.CharField(db_column='SCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sstate = models.CharField(db_column='SState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    szipcode = models.CharField(db_column='SZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    scountry = models.CharField(db_column='SCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipcontact = models.CharField(db_column='ShipContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipphone = models.CharField(db_column='ShipPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shipfax = models.CharField(db_column='ShipFAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    printcert = models.CharField(db_column='PrintCert', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fob = models.CharField(db_column='FOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    counter = models.SmallIntegerField(db_column='Counter', blank=True, null=True, primary_key=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shiptoname = models.CharField(db_column='ShipToName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ShipTo'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Hack to not save the maturity and months_open as they are computed columns
        if not IS_TEST:
            self._meta.local_fields = [f for f in self._meta.local_fields if f.name not in ('counter')]
        super(Shipto, self).save(force_insert, force_update, using, update_fields)


class Shortcut(TruncatedModel):
    object = models.CharField(db_column='Object', max_length=30, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=30, blank=True, null=True)  # Field name made lowercase.
    code2 = models.CharField(db_column='Code2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    top = models.FloatField(db_column='Top', blank=True, null=True)  # Field name made lowercase.
    left = models.FloatField(db_column='Left', blank=True, null=True)  # Field name made lowercase.
    shortcut_id = models.AutoField(db_column='Shortcut_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Shortcut'


class Stateabrv(TruncatedModel):
    abrv = models.CharField(db_column='Abrv', max_length=2, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stateabrv_id = models.AutoField(db_column='StateAbrv_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'StateAbrv'


class Subrouting(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    numoftimes = models.SmallIntegerField(db_column='NumOfTimes', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cycletime = models.FloatField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    cycleunit = models.CharField(db_column='CycleUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totalcycletime = models.FloatField(db_column='TotalCycleTime', blank=True, null=True)  # Field name made lowercase.
    setuptime = models.FloatField(db_column='SetupTime', blank=True, null=True)  # Field name made lowercase.
    setupunit = models.CharField(db_column='SetupUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subrouting_id = models.AutoField(db_column='SubRouting_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'SubRouting'


class Tadefaults(TruncatedModel):
    companycode = models.CharField(db_column='CompanyCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    shiftbeg1 = models.CharField(db_column='ShiftBeg1', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shiftend1 = models.CharField(db_column='ShiftEnd1', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shiftbeg2 = models.CharField(db_column='ShiftBeg2', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shiftend2 = models.CharField(db_column='ShiftEnd2', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shiftbeg3 = models.CharField(db_column='ShiftBeg3', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shiftend3 = models.CharField(db_column='ShiftEnd3', max_length=5, blank=True, null=True)  # Field name made lowercase.
    otcalc = models.CharField(db_column='OTCalc', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otmethod = models.CharField(db_column='OTMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otthreshold = models.SmallIntegerField(db_column='OTThreshold', blank=True, null=True)  # Field name made lowercase.
    otfactor = models.FloatField(db_column='OTFactor', blank=True, null=True)  # Field name made lowercase.
    innearest = models.SmallIntegerField(db_column='InNearest', blank=True, null=True)  # Field name made lowercase.
    inroundupat = models.SmallIntegerField(db_column='InRoundupAt', blank=True, null=True)  # Field name made lowercase.
    outnearest = models.SmallIntegerField(db_column='OutNearest', blank=True, null=True)  # Field name made lowercase.
    outroundupat = models.SmallIntegerField(db_column='OutRoundupAt', blank=True, null=True)  # Field name made lowercase.
    autoround = models.CharField(db_column='AutoRound', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schedround = models.CharField(db_column='SchedRound', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inearly = models.SmallIntegerField(db_column='InEarly', blank=True, null=True)  # Field name made lowercase.
    inlate = models.SmallIntegerField(db_column='InLate', blank=True, null=True)  # Field name made lowercase.
    outearly = models.SmallIntegerField(db_column='OutEarly', blank=True, null=True)  # Field name made lowercase.
    outlate = models.SmallIntegerField(db_column='OutLate', blank=True, null=True)  # Field name made lowercase.
    periodbeg = models.CharField(db_column='PeriodBeg', max_length=10, blank=True, null=True)  # Field name made lowercase.
    runningglobal = models.CharField(db_column='RunningGlobal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    starting_date = models.DateTimeField(db_column='Starting_Date', blank=True, null=True)  # Field name made lowercase.
    convert_orders = models.NullBooleanField(db_column='Convert_Orders')  # Field name made lowercase.
    convert_open_orders_only = models.NullBooleanField(db_column='Convert_Open_Orders_Only')  # Field name made lowercase.
    convert_job_reqs_filled_from_bins = models.NullBooleanField(db_column='Convert_Job_Reqs_Filled_From_Bins')  # Field name made lowercase.
    convert_purchasing = models.NullBooleanField(db_column='Convert_Purchasing')  # Field name made lowercase.
    convert_time_tickets = models.NullBooleanField(db_column='Convert_Time_Tickets')  # Field name made lowercase.
    convert_quality = models.NullBooleanField(db_column='Convert_Quality')  # Field name made lowercase.
    convert_accounting = models.NullBooleanField(db_column='Convert_Accounting')  # Field name made lowercase.
    conversion_check_pass_date = models.DateTimeField(db_column='Conversion_Check_Pass_Date', blank=True, null=True)  # Field name made lowercase.
    tadefaults_id = models.AutoField(db_column='TADefaults_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TADefaults'


class Taxcode(TruncatedModel):
    taxcode = models.CharField(db_column='TaxCode', unique=True, max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    taxfactor = models.FloatField(db_column='TaxFactor', blank=True, null=True)  # Field name made lowercase.
    taxacct = models.CharField(db_column='TaxAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct1 = models.CharField(db_column='TaxAcct1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct2 = models.CharField(db_column='TaxAcct2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct3 = models.CharField(db_column='TaxAcct3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct4 = models.CharField(db_column='TaxAcct4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct5 = models.CharField(db_column='TaxAcct5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct6 = models.CharField(db_column='TaxAcct6', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct7 = models.CharField(db_column='TaxAcct7', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct8 = models.CharField(db_column='TaxAcct8', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct9 = models.CharField(db_column='TaxAcct9', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxacct10 = models.CharField(db_column='TaxAcct10', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    applytoall = models.CharField(db_column='ApplyToAll', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TaxCode'


class Tempschedule(TruncatedModel):
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    workcntr = models.CharField(db_column='WorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    searchdate = models.IntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    hours = models.FloatField(db_column='Hours', blank=True, null=True)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    manhrs = models.FloatField(db_column='ManHrs', blank=True, null=True)  # Field name made lowercase.
    shift = models.SmallIntegerField(db_column='Shift', blank=True, null=True)  # Field name made lowercase.
    qtime = models.FloatField(db_column='QTime', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    tempschedule_id = models.AutoField(db_column='TempSchedule_ID', primary_key=True)  # Field name made lowercase.
    breakhrs = models.FloatField(db_column='BreakHrs', blank=True, null=True)  # Field name made lowercase.
    machine = models.IntegerField(db_column='Machine', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TempSchedule'


class Terms(TruncatedModel):
    termscode = models.CharField(db_column='TermsCode', unique=True, max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    discperc = models.FloatField(db_column='DiscPerc', blank=True, null=True)  # Field name made lowercase.
    lateperc = models.FloatField(db_column='LatePerc', blank=True, null=True)  # Field name made lowercase.
    discdays = models.SmallIntegerField(db_column='DiscDays', blank=True, null=True)  # Field name made lowercase.
    netduedays = models.SmallIntegerField(db_column='NetDueDays', blank=True, null=True)  # Field name made lowercase.
    method = models.SmallIntegerField(db_column='Method', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Terms'


class Timeticket(TruncatedModel):
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    emplname = models.CharField(db_column='EmplName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    searchdate = models.IntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    timeticket_id = models.AutoField(db_column='TimeTicket_ID', primary_key=True)  # Field name made lowercase.
    ticketdate = models.CharField(db_column='TicketDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TimeTicket'
        unique_together = (('emplcode', 'ticketdate'),)


class Timeticketdet(TruncatedModel):
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    emplname = models.CharField(db_column='EmplName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    workcntr = models.SmallIntegerField(db_column='WorkCntr', blank=True, null=True)  # Field name made lowercase.
    opernum = models.SmallIntegerField(db_column='OperNum', blank=True, null=True)  # Field name made lowercase.
    payrollrate = models.SmallIntegerField(db_column='PayrollRate', blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    machrun = models.SmallIntegerField(db_column='MachRun', blank=True, null=True)  # Field name made lowercase.
    piecesfinished = models.FloatField(db_column='PiecesFinished', blank=True, null=True)  # Field name made lowercase.
    piecesscrapped = models.FloatField(db_column='PiecesScrapped', blank=True, null=True)  # Field name made lowercase.
    cycletime = models.FloatField(db_column='CycleTime', blank=True, null=True)  # Field name made lowercase.
    setuptime = models.FloatField(db_column='SetupTime', blank=True, null=True)  # Field name made lowercase.
    shift = models.SmallIntegerField(db_column='Shift', blank=True, null=True)  # Field name made lowercase.
    billingrate = models.SmallIntegerField(db_column='BillingRate', blank=True, null=True)  # Field name made lowercase.
    adjustedpayrate = models.FloatField(db_column='AdjustedPayRate', blank=True, null=True)  # Field name made lowercase.
    actualpayrate = models.FloatField(db_column='ActualPayRate', blank=True, null=True)  # Field name made lowercase.
    burdenrate = models.FloatField(db_column='BurdenRate', blank=True, null=True)  # Field name made lowercase.
    timestart = models.CharField(db_column='TimeStart', max_length=5, blank=True, null=True)  # Field name made lowercase.
    timeend = models.CharField(db_column='TimeEnd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    setuprate = models.FloatField(db_column='SetupRate', blank=True, null=True)  # Field name made lowercase.
    cyclerate = models.FloatField(db_column='CycleRate', blank=True, null=True)  # Field name made lowercase.
    unattendop = models.CharField(db_column='UnattendOp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    manhrs = models.FloatField(db_column='ManHrs', blank=True, null=True)  # Field name made lowercase.
    machhrs = models.FloatField(db_column='MachHrs', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    overtime = models.CharField(db_column='OverTime', max_length=1, blank=True, null=True)  # Field name made lowercase.
    searchdate = models.IntegerField(db_column='SearchDate', blank=True, null=True)  # Field name made lowercase.
    timeticketdet_id = models.AutoField(db_column='TimeTicketDet_ID', primary_key=True)  # Field name made lowercase.
    posted = models.CharField(db_column='Posted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nextworkcntr = models.CharField(db_column='NextWorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    deviceno = models.SmallIntegerField(db_column='DeviceNo', blank=True, null=True)  # Field name made lowercase.
    nummachforjob = models.FloatField(db_column='NumMachForJob', blank=True, null=True)  # Field name made lowercase.
    online_id = models.IntegerField(db_column='Online_ID', blank=True, null=True)  # Field name made lowercase.
    logofftime = models.DateTimeField(db_column='LogoffTime', blank=True, null=True)  # Field name made lowercase.
    reasonnum = models.FloatField(db_column='ReasonNum', blank=True, null=True)  # Field name made lowercase.
    custrmano = models.CharField(db_column='CustRMANo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    convert_me = models.NullBooleanField(db_column='Convert_Me')  # Field name made lowercase.
    attendance_header_id = models.IntegerField(db_column='Attendance_Header_ID', blank=True, null=True)  # Field name made lowercase.
    attendance_detail_id = models.IntegerField(db_column='Attendance_Detail_ID', blank=True, null=True)  # Field name made lowercase.
    ticketdate = models.CharField(db_column='TicketDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ismaterialallocated = models.BooleanField(db_column='IsMaterialAllocated')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TimeTicketDet'


class Toolingcode(TruncatedModel):
    toolingcode = models.CharField(db_column='ToolingCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    toolingcode_id = models.AutoField(db_column='ToolingCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ToolingCode'


class Toolingmaintenance(TruncatedModel):
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    toolingcode = models.CharField(db_column='ToolingCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    toolingmaintenance_id = models.AutoField(db_column='ToolingMaintenance_ID', primary_key=True)  # Field name made lowercase.
    completed = models.CharField(db_column='Completed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ToolingMaintenance'


class Trainingcode(TruncatedModel):
    trainingcode = models.CharField(db_column='TrainingCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    instructor = models.CharField(db_column='Instructor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    trainingcode_id = models.AutoField(db_column='TrainingCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'TrainingCode'


class Translation(TruncatedModel):
    english = models.CharField(db_column='English', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    spanish = models.CharField(db_column='Spanish', max_length=255, blank=True, null=True)  # Field name made lowercase.
    french = models.CharField(db_column='French', max_length=255, blank=True, null=True)  # Field name made lowercase.
    translation_id = models.AutoField(db_column='Translation_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'Translation'


class Ultragridlayouts(TruncatedModel):
    layoutname = models.CharField(db_column='LayoutName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    layoutsize = models.IntegerField(db_column='LayoutSize', blank=True, null=True)  # Field name made lowercase.
    layoutcontent = models.BinaryField(db_column='LayoutContent', blank=True, null=True)  # Field name made lowercase.
    ultragridlayouts_id = models.AutoField(db_column='UltraGridLayouts_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UltraGridLayouts'


class Useractivity(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12)  # Field name made lowercase.
    token = models.CharField(db_column='Token', max_length=36)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated')  # Field name made lowercase.
    useractivity_id = models.AutoField(db_column='UserActivity_ID', primary_key=True)  # Field name made lowercase.
    devicetoken = models.CharField(db_column='DeviceToken', max_length=72, blank=True, null=True)  # Field name made lowercase.
    devicedata = models.CharField(db_column='DeviceData', max_length=512, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserActivity'
        unique_together = (('userid', 'token'), ('userid', 'token', 'devicetoken'),)


class Userdefrptvals(TruncatedModel):
    report = models.CharField(db_column='Report', max_length=30, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    filternumber = models.SmallIntegerField(db_column='FilterNumber', blank=True, null=True)  # Field name made lowercase.
    not1 = models.SmallIntegerField(db_column='Not1', blank=True, null=True)  # Field name made lowercase.
    chk1 = models.SmallIntegerField(db_column='Chk1', blank=True, null=True)  # Field name made lowercase.
    not2 = models.SmallIntegerField(db_column='Not2', blank=True, null=True)  # Field name made lowercase.
    chk2 = models.SmallIntegerField(db_column='Chk2', blank=True, null=True)  # Field name made lowercase.
    not3 = models.SmallIntegerField(db_column='Not3', blank=True, null=True)  # Field name made lowercase.
    chk3 = models.SmallIntegerField(db_column='Chk3', blank=True, null=True)  # Field name made lowercase.
    not4 = models.SmallIntegerField(db_column='Not4', blank=True, null=True)  # Field name made lowercase.
    chk4 = models.SmallIntegerField(db_column='Chk4', blank=True, null=True)  # Field name made lowercase.
    not5 = models.SmallIntegerField(db_column='Not5', blank=True, null=True)  # Field name made lowercase.
    chk5 = models.SmallIntegerField(db_column='Chk5', blank=True, null=True)  # Field name made lowercase.
    not6 = models.SmallIntegerField(db_column='Not6', blank=True, null=True)  # Field name made lowercase.
    chk6 = models.SmallIntegerField(db_column='Chk6', blank=True, null=True)  # Field name made lowercase.
    not7 = models.SmallIntegerField(db_column='Not7', blank=True, null=True)  # Field name made lowercase.
    chk7 = models.SmallIntegerField(db_column='Chk7', blank=True, null=True)  # Field name made lowercase.
    not8 = models.SmallIntegerField(db_column='Not8', blank=True, null=True)  # Field name made lowercase.
    chk8 = models.SmallIntegerField(db_column='Chk8', blank=True, null=True)  # Field name made lowercase.
    not9 = models.SmallIntegerField(db_column='Not9', blank=True, null=True)  # Field name made lowercase.
    chk9 = models.SmallIntegerField(db_column='Chk9', blank=True, null=True)  # Field name made lowercase.
    not10 = models.SmallIntegerField(db_column='Not10', blank=True, null=True)  # Field name made lowercase.
    chk10 = models.SmallIntegerField(db_column='Chk10', blank=True, null=True)  # Field name made lowercase.
    not11 = models.SmallIntegerField(db_column='Not11', blank=True, null=True)  # Field name made lowercase.
    chk11 = models.SmallIntegerField(db_column='Chk11', blank=True, null=True)  # Field name made lowercase.
    not12 = models.SmallIntegerField(db_column='Not12', blank=True, null=True)  # Field name made lowercase.
    chk12 = models.SmallIntegerField(db_column='Chk12', blank=True, null=True)  # Field name made lowercase.
    not13 = models.SmallIntegerField(db_column='Not13', blank=True, null=True)  # Field name made lowercase.
    chk13 = models.SmallIntegerField(db_column='Chk13', blank=True, null=True)  # Field name made lowercase.
    date1lo = models.DateTimeField(db_column='Date1Lo', blank=True, null=True)  # Field name made lowercase.
    date1hi = models.DateTimeField(db_column='Date1Hi', blank=True, null=True)  # Field name made lowercase.
    date2lo = models.DateTimeField(db_column='Date2Lo', blank=True, null=True)  # Field name made lowercase.
    date2hi = models.DateTimeField(db_column='Date2Hi', blank=True, null=True)  # Field name made lowercase.
    text1 = models.CharField(db_column='Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text2 = models.CharField(db_column='Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text3 = models.CharField(db_column='Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text4 = models.CharField(db_column='Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currency1lo = models.CharField(db_column='Currency1Lo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currency1hi = models.CharField(db_column='Currency1Hi', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currency2lo = models.CharField(db_column='Currency2Lo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    currency2hi = models.CharField(db_column='Currency2Hi', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number1lo = models.CharField(db_column='Number1Lo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number1hi = models.CharField(db_column='Number1Hi', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number2lo = models.CharField(db_column='Number2Lo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number2hi = models.CharField(db_column='Number2Hi', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number3lo = models.CharField(db_column='Number3Lo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number3hi = models.CharField(db_column='Number3Hi', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number4lo = models.CharField(db_column='Number4Lo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    number4hi = models.CharField(db_column='Number4Hi', max_length=12, blank=True, null=True)  # Field name made lowercase.
    memo1 = models.CharField(db_column='Memo1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    userdefrptvals_id = models.AutoField(db_column='UserDefRptVals_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserDefRptVals'
        unique_together = (('report', 'userid', 'filternumber'),)


class Usergridcolumnsettings(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=14)  # Field name made lowercase.
    screengridid = models.IntegerField(db_column='ScreenGridID')  # Field name made lowercase.
    columnkey = models.CharField(db_column='ColumnKey', max_length=50)  # Field name made lowercase.
    headertext = models.CharField(db_column='HeaderText', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ishidden = models.NullBooleanField(db_column='IsHidden')  # Field name made lowercase.
    width = models.SmallIntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    columnorder = models.SmallIntegerField(db_column='ColumnOrder', blank=True, null=True)  # Field name made lowercase.
    usergridcolumnsettings_id = models.AutoField(db_column='UserGridColumnSettings_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserGridColumnSettings'
        unique_together = (('userid', 'screengridid', 'columnkey'),)


class Usergroup(TruncatedModel):
    usergroupid = models.AutoField(db_column='UserGroupID', primary_key=True)  # Field name made lowercase.
    usergroupname = models.CharField(db_column='UserGroupName', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserGroup'


class Usergrouplink(TruncatedModel):
    usergroupid = models.IntegerField(db_column='UserGroupID')  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12)  # Field name made lowercase.
    usergrouplink_id = models.AutoField(db_column='UserGroupLink_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserGroupLink'
        unique_together = (('userid', 'usergroupid'),)


class Userlabels(TruncatedModel):
    area = models.CharField(db_column='Area', unique=True, max_length=30, blank=True, null=True)  # Field name made lowercase.
    date1 = models.CharField(db_column='Date1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    date2 = models.CharField(db_column='Date2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text1 = models.CharField(db_column='Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text2 = models.CharField(db_column='Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text3 = models.CharField(db_column='Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text4 = models.CharField(db_column='Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currency1 = models.CharField(db_column='Currency1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    currency2 = models.CharField(db_column='Currency2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    number1 = models.CharField(db_column='Number1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    number2 = models.CharField(db_column='Number2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    number3 = models.CharField(db_column='Number3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    number4 = models.CharField(db_column='Number4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    memo1 = models.CharField(db_column='Memo1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    text1default = models.TextField(db_column='Text1Default', blank=True, null=True)  # Field name made lowercase.
    text2default = models.TextField(db_column='Text2Default', blank=True, null=True)  # Field name made lowercase.
    text3default = models.TextField(db_column='Text3Default', blank=True, null=True)  # Field name made lowercase.
    text4default = models.TextField(db_column='Text4Default', blank=True, null=True)  # Field name made lowercase.
    userlabels_id = models.AutoField(db_column='UserLabels_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserLabels'


class Usermessage(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserMessage'
        unique_together = (('id', 'groupid'),)


class Usermessagegroup(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=12)  # Field name made lowercase.
    pincode = models.IntegerField(db_column='PINCode')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    dateopened = models.DateTimeField(db_column='DateOpened', blank=True, null=True)  # Field name made lowercase.
    dateclosed = models.DateTimeField(db_column='DateClosed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserMessageGroup'
        unique_together = (('id', 'groupid'),)


class Usermessageinbox(TruncatedModel):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    usermessageid = models.IntegerField(db_column='UserMessageID')  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=12)  # Field name made lowercase.
    recipient = models.CharField(db_column='Recipient', max_length=12)  # Field name made lowercase.
    isread = models.BooleanField(db_column='IsRead')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserMessageInbox'
        unique_together = (('id', 'usermessageid'),)


class Userreport(TruncatedModel):
    userid = models.CharField(db_column='UserID', unique=True, max_length=10, blank=True, null=True)  # Field name made lowercase.
    companydescrip = models.CharField(db_column='CompanyDescrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    asofdate = models.DateTimeField(db_column='AsOfDate', blank=True, null=True)  # Field name made lowercase.
    userreport_id = models.AutoField(db_column='UserReport_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserReport'


class Usertransactions(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    object = models.CharField(db_column='Object', max_length=30, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=50, blank=True, null=True)  # Field name made lowercase.
    value2 = models.CharField(db_column='Value2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=30, blank=True, null=True)  # Field name made lowercase.
    transdate = models.DateTimeField(db_column='TransDate', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    usertransactions_id = models.AutoField(db_column='UserTransactions_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'UserTransactions'


class Vendcode(TruncatedModel):
    vendcode = models.CharField(db_column='VendCode', unique=True, max_length=12, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    vendname = models.CharField(db_column='VendName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glacct1 = models.CharField(db_column='GLAcct1', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc1 = models.FloatField(db_column='GLPerc1', blank=True, null=True)  # Field name made lowercase.
    glacct2 = models.CharField(db_column='GLAcct2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc2 = models.FloatField(db_column='GLPerc2', blank=True, null=True)  # Field name made lowercase.
    glacct3 = models.CharField(db_column='GLAcct3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc3 = models.FloatField(db_column='GLPerc3', blank=True, null=True)  # Field name made lowercase.
    glacct4 = models.CharField(db_column='GLAcct4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc4 = models.FloatField(db_column='GLPerc4', blank=True, null=True)  # Field name made lowercase.
    glacct5 = models.CharField(db_column='GLAcct5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc5 = models.FloatField(db_column='GLPerc5', blank=True, null=True)  # Field name made lowercase.
    glacct6 = models.CharField(db_column='GLAcct6', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc6 = models.FloatField(db_column='GLPerc6', blank=True, null=True)  # Field name made lowercase.
    glacct7 = models.CharField(db_column='GLAcct7', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc7 = models.FloatField(db_column='GLPerc7', blank=True, null=True)  # Field name made lowercase.
    glacct8 = models.CharField(db_column='GLAcct8', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc8 = models.FloatField(db_column='GLPerc8', blank=True, null=True)  # Field name made lowercase.
    glacct9 = models.CharField(db_column='GLAcct9', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc9 = models.FloatField(db_column='GLPerc9', blank=True, null=True)  # Field name made lowercase.
    glacct10 = models.CharField(db_column='GLAcct10', max_length=12, blank=True, null=True)  # Field name made lowercase.
    glperc10 = models.FloatField(db_column='GLPerc10', blank=True, null=True)  # Field name made lowercase.
    printticket = models.CharField(db_column='PrintTicket', max_length=1, blank=True, null=True)  # Field name made lowercase.
    outserv = models.CharField(db_column='OutServ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    paddr1 = models.CharField(db_column='PAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paddr2 = models.CharField(db_column='PAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pcity = models.CharField(db_column='PCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pstate = models.CharField(db_column='PState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pzipcode = models.CharField(db_column='PZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pcountry = models.CharField(db_column='PCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    saddr1 = models.CharField(db_column='SAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    saddr2 = models.CharField(db_column='SAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scity = models.CharField(db_column='SCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sstate = models.CharField(db_column='SState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    szipcode = models.CharField(db_column='SZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    scountry = models.CharField(db_column='SCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    raddr1 = models.CharField(db_column='RAddr1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    raddr2 = models.CharField(db_column='RAddr2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rcity = models.CharField(db_column='RCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rstate = models.CharField(db_column='RState', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rzipcode = models.CharField(db_column='RZipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rcountry = models.CharField(db_column='RCountry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pcontact = models.CharField(db_column='PContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pphone = models.CharField(db_column='PPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    arcontact = models.CharField(db_column='ARContact', max_length=30, blank=True, null=True)  # Field name made lowercase.
    arphone = models.CharField(db_column='ARPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dateopen = models.DateTimeField(db_column='DateOpen', blank=True, null=True)  # Field name made lowercase.
    datelast = models.DateTimeField(db_column='DateLast', blank=True, null=True)  # Field name made lowercase.
    deffob = models.CharField(db_column='DefFOB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendacctnum = models.CharField(db_column='VendAcctNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ytdpurchases = models.FloatField(db_column='YTDPurchases', blank=True, null=True)  # Field name made lowercase.
    minorder = models.FloatField(db_column='MinOrder', blank=True, null=True)  # Field name made lowercase.
    comments1 = models.TextField(db_column='Comments1', blank=True, null=True)  # Field name made lowercase.
    comments2 = models.TextField(db_column='Comments2', blank=True, null=True)  # Field name made lowercase.
    enterby = models.CharField(db_column='EnterBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    enterdate = models.DateTimeField(db_column='EnterDate', blank=True, null=True)  # Field name made lowercase.
    leadtime = models.SmallIntegerField(db_column='LeadTime', blank=True, null=True)  # Field name made lowercase.
    markup = models.FloatField(db_column='Markup', blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    setupchg = models.FloatField(db_column='SetupChg', blank=True, null=True)  # Field name made lowercase.
    salestaxcode = models.CharField(db_column='SalesTaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    gsttaxcode = models.CharField(db_column='GSTTaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    schedbegin = models.CharField(db_column='SchedBegin', max_length=5, blank=True, null=True)  # Field name made lowercase.
    schedend = models.CharField(db_column='SchedEnd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    worksaturday = models.CharField(db_column='WorkSaturday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worksunday = models.CharField(db_column='WorkSunday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    defemplcode = models.CharField(db_column='DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    avgdays2pay = models.SmallIntegerField(db_column='AvgDays2Pay', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ten99 = models.CharField(db_column='Ten99', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fedidnum = models.CharField(db_column='FedIDNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shipcode = models.CharField(db_column='ShipCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    iswebuser = models.CharField(db_column='IsWebUser', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webpassword = models.CharField(db_column='WebPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    seewebjobstatus = models.CharField(db_column='SeeWebJobStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    seewebdollars = models.CharField(db_column='SeeWebDollars', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webviewpassword = models.CharField(db_column='WebViewPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=250, blank=True, null=True)  # Field name made lowercase.
    restockingpct = models.FloatField(db_column='RestockingPct', blank=True, null=True)  # Field name made lowercase.
    seewebexecutiveoverview = models.CharField(db_column='SeeWebExecutiveOverview', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qbvendcode = models.CharField(db_column='QBVendCode', max_length=41, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendCode'


class Vendreturn(TruncatedModel):
    vendreturnno = models.CharField(db_column='VendReturnNo', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendrmano = models.CharField(db_column='VendRMANo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    issuedate = models.DateTimeField(db_column='IssueDate', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    reasonforreturn = models.TextField(db_column='ReasonForReturn', blank=True, null=True)  # Field name made lowercase.
    receivedate = models.DateTimeField(db_column='ReceiveDate', blank=True, null=True)  # Field name made lowercase.
    receivedby = models.CharField(db_column='ReceivedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receivingcomment = models.TextField(db_column='ReceivingComment', blank=True, null=True)  # Field name made lowercase.
    inspectiondate = models.DateTimeField(db_column='InspectionDate', blank=True, null=True)  # Field name made lowercase.
    inspectedby = models.CharField(db_column='InspectedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    qccomment = models.TextField(db_column='QCComment', blank=True, null=True)  # Field name made lowercase.
    correctiveactioncode = models.CharField(db_column='CorrectiveActionCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    podate = models.DateTimeField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    purchby = models.CharField(db_column='PurchBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    creditdate = models.DateTimeField(db_column='CreditDate', blank=True, null=True)  # Field name made lowercase.
    creditedby = models.CharField(db_column='CreditedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    createcreditmemo = models.CharField(db_column='CreateCreditMemo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    billusforreturn = models.CharField(db_column='BillUsForReturn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    createdvendinvoiceno = models.CharField(db_column='CreatedVendInvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    correctiveactionno = models.CharField(db_column='CorrectiveActionNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    createcar = models.CharField(db_column='CreateCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    createnc = models.CharField(db_column='CreateNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    labelprinted = models.CharField(db_column='LabelPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    debitprinted = models.CharField(db_column='DebitPrinted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendreturn_id = models.AutoField(db_column='VendReturn_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendReturn'


class Vendreturndet(TruncatedModel):
    vendreturnno = models.CharField(db_column='VendReturnNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    partdesc = models.TextField(db_column='PartDesc', blank=True, null=True)  # Field name made lowercase.
    stepno = models.SmallIntegerField(db_column='StepNo', blank=True, null=True)  # Field name made lowercase.
    origqtyreceived = models.IntegerField(db_column='OrigQtyReceived', blank=True, null=True)  # Field name made lowercase.
    qtytoreject = models.IntegerField(db_column='QtyToReject', blank=True, null=True)  # Field name made lowercase.
    qtytocancel = models.IntegerField(db_column='QtyToCancel', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=3, blank=True, null=True)  # Field name made lowercase.
    vendreturnitemno = models.SmallIntegerField(db_column='VendReturnItemNo', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    recvitemno = models.SmallIntegerField(db_column='RecvItemNo', blank=True, null=True)  # Field name made lowercase.
    qtyreturned = models.IntegerField(db_column='QtyReturned', blank=True, null=True)  # Field name made lowercase.
    qtygood = models.IntegerField(db_column='QtyGood', blank=True, null=True)  # Field name made lowercase.
    createcar = models.CharField(db_column='CreateCAR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reasoncode = models.CharField(db_column='ReasonCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    createnc = models.CharField(db_column='CreateNC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nonconfno = models.CharField(db_column='NonConfNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correctiveactionno = models.CharField(db_column='CorrectiveActionNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    restockingpct = models.FloatField(db_column='RestockingPct', blank=True, null=True)  # Field name made lowercase.
    vendreturndet_id = models.AutoField(db_column='VendReturnDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendReturnDet'


class Vendreturnreleases(TruncatedModel):
    vendreturnno = models.CharField(db_column='VendReturnNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendreturnitemno = models.SmallIntegerField(db_column='VendReturnItemNo', blank=True, null=True)  # Field name made lowercase.
    releaseqty = models.IntegerField(db_column='ReleaseQty', blank=True, null=True)  # Field name made lowercase.
    qtytoreject = models.IntegerField(db_column='QtyToReject', blank=True, null=True)  # Field name made lowercase.
    qtytocancel = models.IntegerField(db_column='QtyToCancel', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    vendreturnreleases_id = models.AutoField(db_column='VendReturnReleases_ID', primary_key=True)  # Field name made lowercase.
    poreleases_id = models.IntegerField(db_column='POReleases_ID', blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendReturnReleases'


class Vendtype(TruncatedModel):
    vendtype = models.CharField(db_column='VendType', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendtype_id = models.AutoField(db_column='VendType_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendType'


class Vendorinv(TruncatedModel):
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    periodno = models.CharField(db_column='PeriodNo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    receiverno = models.CharField(db_column='ReceiverNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pymtstatus = models.CharField(db_column='PymtStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    venddesc = models.CharField(db_column='VendDesc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invdate = models.DateTimeField(db_column='InvDate', blank=True, null=True)  # Field name made lowercase.
    pymtdate = models.DateTimeField(db_column='PymtDate', blank=True, null=True)  # Field name made lowercase.
    invoicetotal = models.FloatField(db_column='InvoiceTotal', blank=True, null=True)  # Field name made lowercase.
    amtpaidsofar = models.FloatField(db_column='AmtPaidSoFar', blank=True, null=True)  # Field name made lowercase.
    checkno = models.CharField(db_column='CheckNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    apacct = models.CharField(db_column='APAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    discacct = models.CharField(db_column='DiscAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendtype = models.CharField(db_column='VendType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    termscode = models.CharField(db_column='TermsCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shippingchgs = models.FloatField(db_column='ShippingChgs', blank=True, null=True)  # Field name made lowercase.
    freightacct = models.CharField(db_column='FreightAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    entby = models.CharField(db_column='EntBy', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateent = models.DateTimeField(db_column='DateEnt', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    cashdiscamt = models.FloatField(db_column='CashDiscAmt', blank=True, null=True)  # Field name made lowercase.
    discdate = models.DateTimeField(db_column='DiscDate', blank=True, null=True)  # Field name made lowercase.
    netduedate = models.DateTimeField(db_column='NetDueDate', blank=True, null=True)  # Field name made lowercase.
    invposted = models.CharField(db_column='InvPosted', max_length=1, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    holdpymt = models.CharField(db_column='HoldPymt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    exchrate = models.FloatField(db_column='ExchRate', blank=True, null=True)  # Field name made lowercase.
    gstcode = models.CharField(db_column='GSTCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    gstchgs = models.FloatField(db_column='GSTChgs', blank=True, null=True)  # Field name made lowercase.
    gstacct = models.CharField(db_column='GSTAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salestaxcode = models.CharField(db_column='SalesTaxCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salestaxchgs = models.FloatField(db_column='SalesTaxChgs', blank=True, null=True)  # Field name made lowercase.
    salestaxacct = models.CharField(db_column='SalesTaxAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    projpaydate = models.DateTimeField(db_column='ProjPayDate', blank=True, null=True)  # Field name made lowercase.
    exported = models.CharField(db_column='Exported', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendorinv_id = models.AutoField(db_column='VendorInv_ID', primary_key=True)  # Field name made lowercase.
    accountingid = models.CharField(db_column='AccountingID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendorInv'
        unique_together = (('vendcode', 'invoiceno'),)


class Vendorinvdet(TruncatedModel):
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    glacct = models.CharField(db_column='GLAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    taxstatus = models.CharField(db_column='TaxStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendorinvdet_id = models.AutoField(db_column='VendorInvDet_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendorInvDet'


class Vendorinvpos(TruncatedModel):
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ponum = models.CharField(db_column='PONum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    podate = models.DateTimeField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    poamt = models.FloatField(db_column='POAmt', blank=True, null=True)  # Field name made lowercase.
    vendorinvpos_id = models.AutoField(db_column='VendorInvPOs_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'VendorInvPOs'


class Wcmaintcode(TruncatedModel):
    wcmaintcode = models.CharField(db_column='WCMaintCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emplcode = models.SmallIntegerField(db_column='EmplCode', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    wcmaintcode_id = models.AutoField(db_column='WCMaintCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WCMaintCode'


class Wcmaintenance(TruncatedModel):
    workcntr = models.CharField(db_column='WorkCntr', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workcntrname = models.CharField(db_column='WorkCntrName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wcmaintcode = models.CharField(db_column='WCMaintCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.TextField(db_column='Descrip', blank=True, null=True)  # Field name made lowercase.
    emplcode = models.CharField(db_column='EmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    jobno = models.CharField(db_column='JobNo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wcmaintenance_id = models.AutoField(db_column='WCMaintenance_ID', primary_key=True)  # Field name made lowercase.
    completed = models.CharField(db_column='Completed', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WCMaintenance'


class Webrequest(TruncatedModel):
    ipaddress = models.CharField(db_column='IPAddress', max_length=30, blank=True, null=True)  # Field name made lowercase.
    request = models.CharField(db_column='Request', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parameter1 = models.TextField(db_column='Parameter1', blank=True, null=True)  # Field name made lowercase.
    parameter2 = models.TextField(db_column='Parameter2', blank=True, null=True)  # Field name made lowercase.
    reply = models.TextField(db_column='Reply', blank=True, null=True)  # Field name made lowercase.
    winsockindex = models.IntegerField(db_column='WinsockIndex', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    webrequest_id = models.AutoField(db_column='WebRequest_ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WebRequest'


class Webviewsettings(TruncatedModel):
    pagingrecs = models.IntegerField(db_column='PagingRecs', blank=True, null=True)  # Field name made lowercase.
    webmasteremail = models.CharField(db_column='WebmasterEmail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    welcomemessage = models.TextField(db_column='WelcomeMessage', blank=True, null=True)  # Field name made lowercase.
    heading_backcolor = models.CharField(db_column='Heading_BackColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    heading_forecolor = models.CharField(db_column='Heading_ForeColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    form_backcolor = models.CharField(db_column='Form_BackColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    form_forecolor = models.CharField(db_column='Form_ForeColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    page_bgcolor = models.CharField(db_column='Page_BGColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    background = models.TextField(db_column='Background', blank=True, null=True)  # Field name made lowercase.
    pgheading_color = models.CharField(db_column='PgHeading_Color', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sidebar_color = models.CharField(db_column='Sidebar_Color', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WebViewSettings'


class Webviewusers(TruncatedModel):
    userid = models.CharField(db_column='UserID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=12, blank=True, null=True)  # Field name made lowercase.
    seewebdollars = models.CharField(db_column='SeeWebDollars', max_length=1, blank=True, null=True)  # Field name made lowercase.
    seewebjobstatus = models.CharField(db_column='SeeWebJobStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    level = models.CharField(db_column='Level', max_length=12, blank=True, null=True)  # Field name made lowercase.
    custcode = models.CharField(db_column='CustCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    vendcode = models.CharField(db_column='VendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    seewebexecutiveoverview = models.CharField(db_column='SeeWebExecutiveOverview', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webviewusers_id = models.AutoField(db_column='WebViewUsers_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WebViewUsers'


class Workcntr(TruncatedModel):
    workcntr = models.SmallIntegerField(db_column='WorkCntr', unique=True, blank=True, null=True, primary_key=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    deptnum = models.CharField(db_column='DeptNum', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cycle1 = models.FloatField(db_column='Cycle1', blank=True, null=True)  # Field name made lowercase.
    setup1 = models.FloatField(db_column='Setup1', blank=True, null=True)  # Field name made lowercase.
    cycle2 = models.FloatField(db_column='Cycle2', blank=True, null=True)  # Field name made lowercase.
    setup2 = models.FloatField(db_column='Setup2', blank=True, null=True)  # Field name made lowercase.
    cycle3 = models.FloatField(db_column='Cycle3', blank=True, null=True)  # Field name made lowercase.
    setup3 = models.FloatField(db_column='Setup3', blank=True, null=True)  # Field name made lowercase.
    cycle4 = models.FloatField(db_column='Cycle4', blank=True, null=True)  # Field name made lowercase.
    setup4 = models.FloatField(db_column='Setup4', blank=True, null=True)  # Field name made lowercase.
    cycle5 = models.FloatField(db_column='Cycle5', blank=True, null=True)  # Field name made lowercase.
    setup5 = models.FloatField(db_column='Setup5', blank=True, null=True)  # Field name made lowercase.
    cycle6 = models.FloatField(db_column='Cycle6', blank=True, null=True)  # Field name made lowercase.
    setup6 = models.FloatField(db_column='Setup6', blank=True, null=True)  # Field name made lowercase.
    cycle7 = models.FloatField(db_column='Cycle7', blank=True, null=True)  # Field name made lowercase.
    setup7 = models.FloatField(db_column='Setup7', blank=True, null=True)  # Field name made lowercase.
    cycle8 = models.FloatField(db_column='Cycle8', blank=True, null=True)  # Field name made lowercase.
    setup8 = models.FloatField(db_column='Setup8', blank=True, null=True)  # Field name made lowercase.
    cycle9 = models.FloatField(db_column='Cycle9', blank=True, null=True)  # Field name made lowercase.
    setup9 = models.FloatField(db_column='Setup9', blank=True, null=True)  # Field name made lowercase.
    cycle10 = models.FloatField(db_column='Cycle10', blank=True, null=True)  # Field name made lowercase.
    setup10 = models.FloatField(db_column='Setup10', blank=True, null=True)  # Field name made lowercase.
    hrsavail = models.FloatField(db_column='HrsAvail', blank=True, null=True)  # Field name made lowercase.
    defaulttimeunit = models.CharField(db_column='DefaultTimeUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    burdenrate = models.FloatField(db_column='BurdenRate', blank=True, null=True)  # Field name made lowercase.
    queuetime = models.FloatField(db_column='QueueTime', blank=True, null=True)  # Field name made lowercase.
    queueunit = models.CharField(db_column='QueueUnit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    laboracct = models.CharField(db_column='LaborAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    laborrate = models.FloatField(db_column='LaborRate', blank=True, null=True)  # Field name made lowercase.
    defsetuptime = models.FloatField(db_column='DefSetupTime', blank=True, null=True)  # Field name made lowercase.
    shortname = models.CharField(db_column='ShortName', max_length=10, blank=True, null=True)  # Field name made lowercase.
    altopcode = models.SmallIntegerField(db_column='AltOpCode', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    oldworkcntr = models.CharField(db_column='OldWorkCntr', max_length=3, blank=True, null=True)  # Field name made lowercase.
    attendcode = models.CharField(db_column='AttendCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    opercode = models.CharField(db_column='OperCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    schedbegin = models.CharField(db_column='SchedBegin', max_length=5, blank=True, null=True)  # Field name made lowercase.
    schedend = models.CharField(db_column='SchedEnd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    capacityfactor = models.FloatField(db_column='CapacityFactor', blank=True, null=True)  # Field name made lowercase.
    worksaturday = models.CharField(db_column='WorkSaturday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worksunday = models.CharField(db_column='WorkSunday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    defemplcode = models.CharField(db_column='DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    workmonday = models.CharField(db_column='WorkMonday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    worktuesday = models.CharField(db_column='WorkTuesday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workwednesday = models.CharField(db_column='WorkWednesday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workthursday = models.CharField(db_column='WorkThursday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workfriday = models.CharField(db_column='WorkFriday', max_length=1, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shift2defemplcode = models.CharField(db_column='Shift2DefEmplCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    shift3defemplcode = models.CharField(db_column='Shift3DefEmplCode', max_length=21, blank=True, null=True)  # Field name made lowercase.
    runonshift1 = models.CharField(db_column='RunOnShift1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    runonshift2 = models.CharField(db_column='RunOnShift2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    runonshift3 = models.CharField(db_column='RunOnShift3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hrsavailshift1 = models.FloatField(db_column='HrsAvailShift1', blank=True, null=True)  # Field name made lowercase.
    hrsavailshift2 = models.FloatField(db_column='HrsAvailShift2', blank=True, null=True)  # Field name made lowercase.
    hrsavailshift3 = models.FloatField(db_column='HrsAvailShift3', blank=True, null=True)  # Field name made lowercase.
    locationtop = models.IntegerField(db_column='LocationTop', blank=True, null=True)  # Field name made lowercase.
    locationleft = models.IntegerField(db_column='LocationLeft', blank=True, null=True)  # Field name made lowercase.
    workcntrimagefile = models.CharField(db_column='WorkCntrImageFile', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user_date1 = models.DateTimeField(db_column='User_Date1', blank=True, null=True)  # Field name made lowercase.
    user_date2 = models.DateTimeField(db_column='User_Date2', blank=True, null=True)  # Field name made lowercase.
    user_text1 = models.CharField(db_column='User_Text1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text2 = models.CharField(db_column='User_Text2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text3 = models.CharField(db_column='User_Text3', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_text4 = models.CharField(db_column='User_Text4', max_length=30, blank=True, null=True)  # Field name made lowercase.
    user_currency1 = models.FloatField(db_column='User_Currency1', blank=True, null=True)  # Field name made lowercase.
    user_currency2 = models.FloatField(db_column='User_Currency2', blank=True, null=True)  # Field name made lowercase.
    user_number1 = models.FloatField(db_column='User_Number1', blank=True, null=True)  # Field name made lowercase.
    user_number2 = models.FloatField(db_column='User_Number2', blank=True, null=True)  # Field name made lowercase.
    user_number3 = models.FloatField(db_column='User_Number3', blank=True, null=True)  # Field name made lowercase.
    user_number4 = models.FloatField(db_column='User_Number4', blank=True, null=True)  # Field name made lowercase.
    user_memo1 = models.TextField(db_column='User_Memo1', blank=True, null=True)  # Field name made lowercase.
    loadingmethod = models.CharField(db_column='LoadingMethod', max_length=12, blank=True, null=True)  # Field name made lowercase.
    utilizationpct = models.FloatField(db_column='UtilizationPct', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WorkCntr'


class Workcode(TruncatedModel):
    workcode = models.CharField(db_column='WorkCode', unique=True, max_length=12, blank=True, null=True)  # Field name made lowercase.
    descrip = models.CharField(db_column='Descrip', max_length=30, blank=True, null=True)  # Field name made lowercase.
    aracct = models.CharField(db_column='ARAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cashdisc = models.CharField(db_column='CashDisc', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesacct = models.CharField(db_column='SalesAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    freightacct = models.CharField(db_column='FreightAcct', max_length=12, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='Active', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workcode_id = models.AutoField(db_column='WorkCode_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'WorkCode'


class Zipcodes(TruncatedModel):
    city = models.CharField(db_column='City', max_length=30, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=3, blank=True, null=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zipcodes_id = models.AutoField(db_column='ZipCodes_ID', primary_key=True)  # Field name made lowercase.
    lastmoddate = models.DateTimeField(db_column='LastModDate', blank=True, null=True)  # Field name made lowercase.
    lastmoduser = models.CharField(db_column='LastModUser', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'ZipCodes'
