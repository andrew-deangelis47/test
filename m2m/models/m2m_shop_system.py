from __future__ import unicode_literals
from django.db import models
from baseintegration.utils.truncated_model import TruncatedModel
from m2m.autonumber import AutoNumberMixin, AutoColumn, AddressNumberMixin
from m2m.settings import IS_TEST


class Apvendx(TruncatedModel):
    fvendno = models.CharField(max_length=6)
    fcompany = models.CharField(max_length=35)
    fbuyer = models.CharField(max_length=3)
    fcacctnum = models.CharField(max_length=25)
    fccusno = models.CharField(max_length=20)
    fcdefshpto = models.CharField(max_length=6)
    fcity = models.CharField(max_length=20)
    fcountry = models.CharField(max_length=25)
    fcfname = models.CharField(max_length=15)
    fcontact = models.CharField(max_length=20)
    fcshipvia = models.CharField(max_length=20)
    fcterms = models.CharField(max_length=4)
    fccurid = models.CharField(max_length=3)
    fcuser1 = models.CharField(max_length=40)
    fcuser2 = models.CharField(max_length=40)
    fcuser3 = models.CharField(max_length=40)
    fduser1 = models.DateTimeField()
    fdsince = models.DateTimeField()
    ffax = models.CharField(max_length=20)
    fiso9000 = models.BooleanField()
    flimit = models.DecimalField(max_digits=19, decimal_places=4)
    fllongdist = models.BooleanField()
    fnminamt = models.DecimalField(max_digits=19, decimal_places=4)
    fnuser1 = models.DecimalField(max_digits=17, decimal_places=5)
    fnuser2 = models.DecimalField(max_digits=17, decimal_places=5)
    fphone = models.CharField(max_length=20)
    fprepaid = models.DecimalField(max_digits=19, decimal_places=4)
    fsalestax = models.DecimalField(max_digits=7, decimal_places=3)
    fstate = models.CharField(max_length=20)
    fstatus = models.CharField(max_length=1)
    furgency = models.IntegerField()
    fdramt = models.DecimalField(max_digits=19, decimal_places=4)
    fvtype = models.CharField(max_length=2)
    fzip = models.CharField(max_length=10)
    f1099 = models.BooleanField()
    fcstatus = models.CharField(max_length=1)
    flistaxabl = models.BooleanField()
    fcemail = models.CharField(max_length=100)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fmstreet = models.TextField()
    fmuser1 = models.TextField()
    fdisttype = models.CharField(max_length=10)
    fchangeby = models.CharField(max_length=25)
    fcngdate = models.DateTimeField()
    fcsubstatus = models.CharField(max_length=1)
    freasoncng = models.TextField()
    fnremdelivery = models.IntegerField()
    fvremadvmail = models.CharField(max_length=100)
    fvremadvfax = models.CharField(max_length=20)
    fleftvend = models.BooleanField()
    ftaxid = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'apvendx'


class Qtmast(AutoNumberMixin, TruncatedModel):
    auto_number_attrs = [AutoColumn('fquoteno', 'QTMAST.FQUOTENO')]

    fcompany = models.CharField(max_length=35)  # 'Company'
    fquoteno = models.CharField(max_length=10)  # 'Quote'
    fackdate = models.DateTimeField()  # 'Entry Date'
    fccurid = models.CharField(max_length=3)
    fcfactor = models.DecimalField(max_digits=22, decimal_places=10)
    fcfname = models.CharField(max_length=15)
    fcfromno = models.CharField(max_length=25)
    fcfromtype = models.CharField(max_length=5)
    fcity = models.CharField(max_length=20)
    fcountry = models.CharField(max_length=25)
    fdatedue = models.DateTimeField()
    fdaterecvd = models.DateTimeField()  # 'Due Date'
    fdcurdate = models.DateTimeField()
    fdexpired = models.DateTimeField()
    fdistno = models.CharField(max_length=6)
    fdsalespn = models.CharField(max_length=25)
    fduplicate = models.BooleanField()
    festimator = models.CharField(max_length=3)
    ffax = models.CharField(max_length=20)
    fjobname = models.CharField(max_length=65)  # 'Reference Name'
    fcsoldto = models.CharField(max_length=6)
    fcustno = models.CharField(max_length=6)  # 'Customer Number'
    fnextenum = models.CharField(max_length=3)
    fnextinum = models.CharField(max_length=3)
    fordpotent = models.CharField(max_length=1)
    fordtime = models.CharField(max_length=1)
    fphone = models.CharField(max_length=20)
    fprint_dt = models.DateTimeField()
    fprinted = models.BooleanField()
    fquotecopy = models.CharField(max_length=1)
    fquotedate = models.DateTimeField()
    fquoteto = models.CharField(max_length=20)
    frequestno = models.CharField(max_length=15)  # 'Their Request No'
    frevno = models.CharField(max_length=2)
    fsalespn = models.CharField(max_length=3)
    fstate = models.CharField(max_length=20)
    fstatus = models.CharField(max_length=20)  # 'Status'
    ftype = models.CharField(max_length=1)
    fzip = models.CharField(max_length=10)
    fcusrchr1 = models.CharField(max_length=20)
    fcusrchr2 = models.CharField(max_length=40)
    fcusrchr3 = models.CharField(max_length=40)
    fnusrqty1 = models.DecimalField(max_digits=15, decimal_places=5)
    fnusrcur1 = models.DecimalField(max_digits=17, decimal_places=5)
    fdusrdate1 = models.DateTimeField()
    fdisrate = models.DecimalField(max_digits=15, decimal_places=5)
    fterm = models.CharField(max_length=4)
    fpaytype = models.CharField(max_length=1)
    fdeurodate = models.DateTimeField()
    feurofctr = models.DecimalField(max_digits=17, decimal_places=5)
    fusercode = models.CharField(max_length=7)
    fcshipto = models.CharField(max_length=6)
    fltotal = models.BooleanField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fclosmemo = models.TextField()  # This field type is a guess. 'Closing Memo'
    fmstreet = models.TextField()  # This field type is a guess.
    fmusermemo = models.TextField()  # This field type is a guess.
    fsalumemo = models.TextField()  # This field type is a guess. 'Salutation'
    fccontkey = models.CharField(max_length=10)
    flcontract = models.BooleanField()
    fndbrmod = models.IntegerField()
    contractnu = models.CharField(db_column='ContractNu', max_length=10)  # Field name made lowercase.
    opportunnum = models.CharField(db_column='OpportunNum', max_length=10)  # Field name made lowercase.
    # modifieddate = models.DateTimeField(db_column='ModifiedDate')  # No longer exists withing M2M
    oppcrtype = models.CharField(db_column='OppCrType', max_length=3)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate')  # No longer exists withing M2M
    fbilladdr = models.CharField(max_length=6)
    contactnum = models.CharField(max_length=6)

    class Meta:
        managed = IS_TEST
        db_table = 'qtmast'


class Qtitem(TruncatedModel):
    fenumber = models.CharField(max_length=3)
    finumber = models.CharField(max_length=3)
    fpartno = models.CharField(max_length=25)
    fpartrev = models.CharField(max_length=3)
    fquoteno = models.CharField(max_length=10)
    fbomqty = models.DecimalField(max_digits=15, decimal_places=5)
    fcfromitem = models.CharField(max_length=3)
    fcfromno = models.CharField(max_length=25)
    fcfromtype = models.CharField(max_length=5)
    fcustpart = models.CharField(max_length=25)
    fcustptrev = models.CharField(max_length=3)
    fcas_bom = models.BooleanField()
    fcas_rtg = models.BooleanField()
    fdet_bom = models.BooleanField()
    fdet_rtg = models.BooleanField()
    festqty = models.DecimalField(max_digits=15, decimal_places=5)
    ffixact = models.DecimalField(max_digits=21, decimal_places=8)
    fgroup = models.CharField(max_length=6)
    flabact = models.DecimalField(max_digits=17, decimal_places=5)
    flordered = models.BooleanField()
    fmatlact = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdact = models.DecimalField(max_digits=17, decimal_places=5)
    fmeasure = models.CharField(max_length=3)
    fnextinum = models.IntegerField()
    fothract = models.DecimalField(max_digits=17, decimal_places=5)
    fprintmemo = models.BooleanField()
    fprodcl = models.CharField(max_length=4)
    frtgsetupa = models.DecimalField(max_digits=17, decimal_places=5)
    fschecode = models.CharField(max_length=6)
    fsetupact = models.DecimalField(max_digits=17, decimal_places=5)
    fsono = models.CharField(max_length=10)
    fsource = models.CharField(max_length=1)
    fstandpart = models.BooleanField()
    fsubact = models.DecimalField(max_digits=17, decimal_places=5)
    ftoolact = models.DecimalField(max_digits=17, decimal_places=5)
    ftotptime = models.DecimalField(max_digits=17, decimal_places=5)
    ftotstime = models.DecimalField(max_digits=17, decimal_places=5)
    fulabcost = models.DecimalField(max_digits=17, decimal_places=5)
    funetprice = models.DecimalField(max_digits=17, decimal_places=5)
    fllotreqd = models.BooleanField()
    fclotext = models.CharField(max_length=1)
    fcprodid = models.CharField(max_length=6)
    funettxnpric = models.DecimalField(max_digits=17, decimal_places=5)
    funeteuropr = models.DecimalField(max_digits=17, decimal_places=5)
    fschedtype = models.CharField(max_length=1)
    flistaxabl = models.BooleanField()
    fljrdif = models.BooleanField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fdelivery = models.TextField()  # This field type is a guess.
    fdesc = models.TextField()  # This field type is a guess.
    fdescmemo = models.TextField()  # This field type is a guess.
    fac = models.CharField(max_length=20)
    sfac = models.CharField(max_length=20)
    fcpbtype = models.CharField(max_length=1)
    itccost = models.DecimalField(db_column='ITCCOST', max_digits=17, decimal_places=5)  # Field name made lowercase.
    fcudrev = models.CharField(max_length=3)
    fndbrmod = models.IntegerField()
    fctpdate = models.DateTimeField()
    fctptrans = models.DateTimeField()
    contractnu = models.CharField(db_column='ContractNu', max_length=10)  # Field name made lowercase.
    flrfqreqd = models.BooleanField(db_column='Flrfqreqd')  # Field name made lowercase.
    fcostfrom = models.CharField(db_column='Fcostfrom', max_length=10)  # Field name made lowercase.
    # isordered = models.NullBooleanField(db_column='Isordered')  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate')  # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate')  # No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'qtitem'


class Qtdbom(TruncatedModel):
    fbompart = models.CharField(max_length=25)
    fbomrev = models.CharField(max_length=3)
    fbominum = models.CharField(max_length=4)
    fbomlcost = models.DecimalField(max_digits=21, decimal_places=8)
    fbommeas = models.CharField(max_length=3)
    fbomocost = models.DecimalField(max_digits=21, decimal_places=8)
    fbomsource = models.CharField(max_length=1)
    fcostfrom = models.CharField(max_length=10)
    fextqty = models.DecimalField(max_digits=19, decimal_places=8)
    ffixcost = models.DecimalField(max_digits=21, decimal_places=8)
    finumber = models.CharField(max_length=3)
    fitem = models.CharField(max_length=6)
    flabcost = models.DecimalField(max_digits=21, decimal_places=8)
    flastoper = models.IntegerField()
    flevel = models.CharField(max_length=2)
    flextend = models.BooleanField()
    fltooling = models.BooleanField()
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fnonpro = models.IntegerField()
    fnumopers = models.IntegerField()
    forgbomqty = models.DecimalField(max_digits=15, decimal_places=5)
    fothrcost = models.DecimalField(max_digits=21, decimal_places=8)
    fovhdcost = models.DecimalField(max_digits=21, decimal_places=8)
    fparinum = models.CharField(max_length=4)
    fquoteno = models.CharField(max_length=10)
    fsetupcost = models.DecimalField(max_digits=21, decimal_places=8)
    fsubcost = models.DecimalField(max_digits=21, decimal_places=8)
    ftotptime = models.DecimalField(max_digits=14, decimal_places=7)
    ftotqty = models.DecimalField(max_digits=15, decimal_places=5)
    ftotstime = models.DecimalField(max_digits=14, decimal_places=7)
    fuprice = models.DecimalField(max_digits=21, decimal_places=8)
    fvendno = models.CharField(max_length=6)
    fllotreqd = models.BooleanField()
    fclotext = models.CharField(max_length=1)
    fnoperno = models.IntegerField(db_column='FNOPERNO')
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fbomdesc = models.TextField()  # This field type is a guess.
    fstdmemo = models.TextField()  # This field type is a guess.
    fac = models.CharField(max_length=20)
    fcbomudrev = models.CharField(max_length=3)
    fndbrmod = models.IntegerField()
    flrfqreqd = models.BooleanField(db_column='Flrfqreqd')  # Field name made lowercase.
    fcsource = models.CharField(db_column='fcSource', max_length=10)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate')  # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate') # No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'qtdbom'


class Qtdrtg(TruncatedModel):
    fbominum = models.CharField(max_length=4)
    fchngrates = models.CharField(max_length=1)
    felpstime = models.DecimalField(max_digits=8, decimal_places=2)
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    finumber = models.CharField(max_length=3)
    flschedule = models.BooleanField()
    fmovetime = models.DecimalField(max_digits=8, decimal_places=2)
    foperno = models.IntegerField()
    foperqty = models.DecimalField(max_digits=19, decimal_places=6)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fpro_id = models.CharField(max_length=7)
    fquoteno = models.CharField(max_length=10)
    fsetuptime = models.DecimalField(max_digits=7, decimal_places=2)
    fstddesc = models.CharField(max_length=4)
    fulabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fuovrhdcos = models.DecimalField(max_digits=7, decimal_places=2)
    fuprodtime = models.DecimalField(max_digits=16, decimal_places=10)
    fusubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fllotreqd = models.BooleanField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fdescript = models.TextField()  # This field type is a guess.
    fopermemo = models.TextField()  # This field type is a guess.
    fndbrmod = models.IntegerField()
    fnsimulops = models.IntegerField()
    cycleunits = models.DecimalField(db_column='CycleUnits', max_digits=13,
                                     decimal_places=3)  # Field name made lowercase.
    unitsize = models.DecimalField(db_column='UnitSize', max_digits=13, decimal_places=3)  # Field name made lowercase.
    fccharcode = models.CharField(max_length=10)
    # createddate = models.DateTimeField(db_column='CreatedDate')  # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate') # No longer exists withing M2M

    class Meta:
        managed = False
        db_table = 'qtdrtg'


class Qtpest(TruncatedModel):
    fenumber = models.CharField(max_length=3)
    finumber = models.CharField(max_length=3)
    fquantity = models.DecimalField(max_digits=15, decimal_places=5)
    fquoteno = models.CharField(max_length=10)
    fdiscount = models.DecimalField(max_digits=17, decimal_places=5)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fpartno = models.CharField(max_length=25)
    fcpartrev = models.CharField(max_length=3)
    funetprice = models.DecimalField(max_digits=17, decimal_places=5)
    fnetprice = models.DecimalField(max_digits=17, decimal_places=5)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    fsetupcost = models.DecimalField(max_digits=17, decimal_places=5)
    fsubcost = models.DecimalField(max_digits=17, decimal_places=5)
    ftoolcost = models.DecimalField(max_digits=17, decimal_places=5)
    fnettxnprice = models.DecimalField(max_digits=17, decimal_places=5)
    funettxnpric = models.DecimalField(max_digits=17, decimal_places=5)
    fneteuropr = models.DecimalField(max_digits=17, decimal_places=5)
    funeteuropr = models.DecimalField(max_digits=17, decimal_places=5)
    fdiscpct = models.DecimalField(max_digits=17, decimal_places=5)
    identity_column = models.AutoField(unique=True, primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fcudrev = models.CharField(max_length=3)
    fmatlpadj = models.DecimalField(max_digits=16, decimal_places=5)
    ftoolpadj = models.DecimalField(max_digits=16, decimal_places=5)
    flabpadj = models.DecimalField(max_digits=16, decimal_places=5)
    fovhdpadj = models.DecimalField(max_digits=16, decimal_places=5)
    fsubpadj = models.DecimalField(max_digits=16, decimal_places=5)
    fothrpadj = models.DecimalField(max_digits=16, decimal_places=5)
    fsetuppadj = models.DecimalField(max_digits=16, decimal_places=5)
    # createddate = models.DateTimeField(db_column='CreatedDate')  # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate') # No longer exists withing M2M

    class Meta:
        managed = False
        db_table = 'qtpest'


class SlcdpmExt(TruncatedModel):
    identity_column = models.AutoField(db_column='Identity_Column', primary_key=True)  # Field name made lowercase.
    # timestamp_column = models.TextField(db_column='Timestamp_Column', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fkey_id = models.IntegerField(db_column='FKey_ID', unique=True)  # Field name made lowercase.
    insiderep = models.CharField(db_column='INSIDEREP', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    mktsector = models.CharField(db_column='MKTSECTOR', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    certrev = models.CharField(db_column='CERTREV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    finalinsp = models.CharField(db_column='FINALINSP', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    millcert = models.CharField(db_column='MILLCERT', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    custpartreqd = models.CharField(db_column='CUSTPARTREQD', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    shipearly = models.CharField(db_column='SHIPEARLY', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    shipexact = models.CharField(db_column='SHIPEXACT', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    invoicenotes = models.CharField(db_column='INVOICENOTES', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    shipnotes = models.CharField(db_column='SHIPNOTES', max_length=250, blank=True,
                                 null=True)  # Field name made lowercase.
    cofa = models.CharField(db_column='COFA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cofc = models.CharField(db_column='COFC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    slsyr = models.CharField(db_column='SLSYR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ytdsls = models.DecimalField(db_column='YTDSLS', max_digits=10, decimal_places=2, blank=True,
                                 null=True)  # Field name made lowercase.
    lysls = models.DecimalField(db_column='LYSLS', max_digits=10, decimal_places=2, blank=True,
                                null=True)  # Field name made lowercase.
    twolysls = models.DecimalField(db_column='TWOLYSLS', max_digits=10, decimal_places=2, blank=True,
                                   null=True)  # Field name made lowercase.
    custreq = models.TextField(db_column='CUSTREQ', blank=True,
                               null=True)  # Field name made lowercase. This field type is a guess.
    frozenpro = models.NullBooleanField(db_column='FROZENPRO')  # Field name made lowercase.
    fregion = models.CharField(db_column='FREGION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    freptype = models.CharField(db_column='FREPTYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fslspn = models.CharField(db_column='FSLSPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fidealnumber = models.IntegerField(db_column='FIDEALNUMBER', blank=True, null=True)  # Field name made lowercase.
    currforecast = models.DecimalField(db_column='CURRFORECAST', max_digits=19, decimal_places=4, blank=True,
                                       null=True)  # Field name made lowercase.
    jan1potcodea = models.CharField(db_column='JAN1POTCODEA', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    jan1potcode = models.CharField(db_column='JAN1POTCODE', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    touchplancd = models.CharField(db_column='TOUCHPLANCD', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    quoteapprovalrequired = models.CharField(max_length=1)

    class Meta:
        managed = IS_TEST
        db_table = 'SLCDPM_EXT'


class Slcdpmx(AutoNumberMixin, TruncatedModel):
    auto_number_attrs = [AutoColumn('fcustno', 'CUSTNO')]

    fcustno = models.CharField(max_length=6)
    fcompany = models.CharField(max_length=35)
    fcity = models.CharField(max_length=20)
    fphone = models.CharField(max_length=20)
    fann_sales = models.IntegerField()
    fbacklog = models.DecimalField(max_digits=16, decimal_places=4)
    fbalnxt = models.DecimalField(max_digits=17, decimal_places=5)
    fcfname = models.CharField(max_length=15)
    fcontact = models.CharField(max_length=20)
    fcountry = models.CharField(max_length=25)
    fcreated = models.DateTimeField()
    fcrlimit = models.IntegerField()
    fcshipto = models.CharField(max_length=6)
    fcsoldto = models.CharField(max_length=6)
    fcurrency = models.CharField(max_length=3)
    fcusrchr1 = models.CharField(max_length=20)
    fcusrchr2 = models.CharField(max_length=40)
    fcusrchr3 = models.CharField(max_length=40)
    fdbdate = models.DateTimeField()
    fdbrate = models.CharField(max_length=4)
    fdisrate = models.DecimalField(max_digits=8, decimal_places=3)
    fdistno = models.CharField(max_length=6)
    fdusrdate1 = models.DateTimeField()
    fllongdist = models.BooleanField()
    ffax = models.CharField(max_length=20)
    ffincharge = models.BooleanField()
    ffob = models.CharField(max_length=20)
    fmtdamtnxt = models.DecimalField(max_digits=17, decimal_places=5)
    fmtdsamt = models.DecimalField(max_digits=17, decimal_places=5)
    fnardayslt = models.DecimalField(max_digits=17, decimal_places=5)
    fno_employ = models.IntegerField()
    fcpaydex = models.CharField(max_length=3)
    fnusrcur1 = models.DecimalField(max_digits=17, decimal_places=5)
    fnusrqty1 = models.DecimalField(max_digits=15, decimal_places=5)
    fpaytype = models.CharField(max_length=1)
    fpriority = models.CharField(max_length=2)
    fsalcompct = models.DecimalField(max_digits=8, decimal_places=3)
    fsalespn = models.CharField(max_length=3)
    fsicno1 = models.CharField(max_length=4)
    fsicno2 = models.CharField(max_length=4)
    fshipvia = models.CharField(max_length=20)
    fsince = models.DateTimeField()
    fstate = models.CharField(max_length=20)
    ftaxcode = models.CharField(max_length=10)
    ftaxexempt = models.CharField(max_length=15)
    ftaxrate = models.DecimalField(max_digits=7, decimal_places=3)
    fterm = models.CharField(max_length=4)
    fterr = models.CharField(max_length=10)
    ftype = models.CharField(max_length=1)
    fusercode = models.CharField(max_length=7)
    fytdsamt = models.DecimalField(max_digits=16, decimal_places=4)
    fyr_estab = models.CharField(max_length=4)
    fzip = models.CharField(max_length=10)
    fcstatus = models.CharField(max_length=1)
    flistaxabl = models.BooleanField()
    fcemail = models.CharField(max_length=100)
    flisfcast = models.BooleanField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fbus_type = models.TextField()  # This field type is a guess.
    fmnotes = models.TextField()  # This field type is a guess.
    fmstreet = models.TextField()  # This field type is a guess.
    fmusrmemo1 = models.TextField()  # This field type is a guess.
    fncrmmod = models.IntegerField()
    fccrmacct = models.CharField(max_length=12)
    fscmprty = models.IntegerField()
    fdisttype = models.CharField(max_length=10)
    subtype = models.CharField(db_column='SubType', max_length=15)  # Field name made lowercase.
    fledited = models.BooleanField(db_column='flEdited')  # Field name made lowercase.
    furl = models.CharField(db_column='fURL', max_length=255)  # Field name made lowercase.
    contactnum = models.CharField(db_column='ContactNum', max_length=6)  # Field name made lowercase.
    homephone = models.CharField(db_column='HomePhone', max_length=20)  # Field name made lowercase.
    mobilephone = models.CharField(db_column='MobilePhone', max_length=20)  # Field name made lowercase.
    naicscode = models.CharField(db_column='NAICsCode', max_length=6)  # Field name made lowercase.
    fchangeby = models.CharField(max_length=25)
    fcngdate = models.DateTimeField()
    fcsubstatus = models.CharField(max_length=1)
    freasoncng = models.TextField()  # This field type is a guess.
    flpaybycc = models.BooleanField()

    class Meta:
        managed = IS_TEST
        db_table = 'slcdpmx'


class Syphon(AutoNumberMixin, TruncatedModel):
    auto_number_attrs = [AutoColumn('number', 'SYPHON.NUMBER')]

    fllongdist = models.BooleanField()
    fcfax = models.CharField(max_length=25)
    fcclass = models.CharField(max_length=3)
    fcemail = models.CharField(max_length=100)
    fcextensio = models.CharField(max_length=6)
    fcnumber = models.CharField(max_length=25)
    fcsourceid = models.CharField(max_length=6)
    fcs_alias = models.CharField(max_length=10)
    fcbesttime = models.CharField(max_length=10)
    fccurid = models.CharField(max_length=3)
    fcfname = models.CharField(max_length=15)
    fcontact = models.CharField(max_length=20)
    fcrange = models.CharField(max_length=10)
    fsalute = models.CharField(max_length=5)
    fctitle = models.CharField(max_length=25)
    fccountry = models.CharField(max_length=25)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fmnotes = models.TextField()  # This field type is a guess.
    fncrmmod = models.IntegerField()
    fccrmcntct = models.CharField(max_length=12)
    number = models.CharField(db_column='Number', max_length=6)  # Field name made lowercase.
    phonework = models.CharField(db_column='PhoneWork', max_length=20)  # Field name made lowercase.
    phonehome = models.CharField(db_column='PhoneHome', max_length=20)  # Field name made lowercase.
    phonemobile = models.CharField(db_column='PhoneMobile', max_length=20)  # Field name made lowercase.
    address = models.TextField(db_column='Address')  # Field name made lowercase. This field type is a guess.
    city = models.CharField(db_column='City', max_length=20)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=20)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=10)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=100)  # Field name made lowercase.
    isprimary = models.BooleanField(db_column='IsPrimary')  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate') # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate')  # No longer exists withing M2M
    fledited = models.BooleanField(db_column='flEdited')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'syphon'


class Sysequ(TruncatedModel):
    fcclass = models.CharField(max_length=25)
    fcprompt = models.CharField(max_length=25)
    fcprefix = models.CharField(max_length=5)
    fcseqtype = models.CharField(max_length=1)
    fcsuffix = models.CharField(max_length=5)
    fcnumber = models.CharField(max_length=25)
    fnwidth = models.IntegerField()
    fnincremen = models.IntegerField()
    fnbase36di = models.IntegerField()
    fcbase36sk = models.CharField(max_length=10)
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fnmaxwidth = models.IntegerField()
    flallowwidthchng = models.BooleanField()

    class Meta:
        managed = IS_TEST
        db_table = 'sysequ'


class Syaddr(AddressNumberMixin, TruncatedModel):
    fllongdist = models.BooleanField()
    fcaddrkey = models.CharField(max_length=6)
    fcaddrtype = models.CharField(max_length=1)
    fcaliaskey = models.CharField(max_length=6)
    fcalias = models.CharField(max_length=10)
    fcfname = models.CharField(max_length=15)
    fclname = models.CharField(max_length=20)
    fccounty = models.CharField(max_length=20)
    fccompany = models.CharField(max_length=35)
    fccity = models.CharField(max_length=20)
    fccountry = models.CharField(max_length=25)
    fcfax = models.CharField(max_length=20)
    fcphone = models.CharField(max_length=20)
    fcstate = models.CharField(max_length=20)
    fczip = models.CharField(max_length=10)
    fcjrdict = models.CharField(max_length=10)
    fcemail = models.CharField(max_length=100)
    fcloc = models.CharField(max_length=14)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fmnotes = models.TextField()  # This field type is a guess.
    fmstreet = models.TextField()  # This field type is a guess.
    fncrmmod = models.IntegerField()
    fccrmaddrs = models.CharField(max_length=12)
    fac = models.CharField(max_length=20)
    phonehome = models.CharField(db_column='PhoneHome', max_length=20)  # Field name made lowercase.
    phonemoblie = models.CharField(db_column='PhoneMoblie', max_length=20)  # Field name made lowercase.
    contactnum = models.CharField(db_column='ContactNum', max_length=6)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate')  # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate')  # No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'syaddr'


class Somast(AutoNumberMixin, TruncatedModel):
    auto_number_attrs = [AutoColumn('fsono', 'SOMAST.FSONO')]

    fsono = models.CharField(max_length=10)
    fcustno = models.CharField(max_length=6)
    fcompany = models.CharField(max_length=35)
    fcity = models.CharField(max_length=20)
    fcustpono = models.CharField(max_length=20)
    fackdate = models.DateTimeField()
    fcanc_dt = models.DateTimeField()
    fccurid = models.CharField(max_length=3)
    fcfactor = models.DecimalField(max_digits=22, decimal_places=10)
    fcfname = models.CharField(max_length=15)
    fcfromno = models.CharField(max_length=25, blank=True, null=True)
    fcfromtype = models.CharField(max_length=5)
    fcontact = models.CharField(max_length=30)
    fclos_dt = models.DateTimeField()
    fcountry = models.CharField(max_length=25)
    fcusrchr1 = models.CharField(max_length=20)
    fcusrchr2 = models.CharField(max_length=40)
    fcusrchr3 = models.CharField(max_length=40)
    fdcurdate = models.DateTimeField()
    fdisrate = models.DecimalField(max_digits=8, decimal_places=3)
    fdistno = models.CharField(max_length=6)
    fduedate = models.DateTimeField()
    fduplicate = models.BooleanField()
    fdusrdate1 = models.DateTimeField()
    festimator = models.CharField(max_length=3)
    ffax = models.CharField(max_length=20)
    ffob = models.CharField(max_length=20)
    fnextenum = models.CharField(max_length=3)
    fnextinum = models.CharField(max_length=3)
    fnusrqty1 = models.DecimalField(max_digits=15, decimal_places=5)
    fnusrcur1 = models.DecimalField(max_digits=17, decimal_places=5)
    forderdate = models.DateTimeField()
    fordername = models.CharField(max_length=65)
    fordrevdt = models.DateTimeField()
    fpaytype = models.CharField(max_length=1)
    fphone = models.CharField(max_length=20)
    fprint_dt = models.DateTimeField()
    fprinted = models.BooleanField()
    fsalcompct = models.DecimalField(max_digits=8, decimal_places=3)
    fsalecom = models.BooleanField()
    fshipvia = models.CharField(max_length=20)
    fshptoaddr = models.CharField(max_length=6)
    fsocoord = models.CharField(max_length=3)
    fsoldaddr = models.CharField(max_length=6)
    fsoldby = models.CharField(max_length=3)
    fsorev = models.CharField(max_length=2)
    fstate = models.CharField(max_length=20)
    fstatus = models.CharField(max_length=20)
    ftaxcode = models.CharField(max_length=3)
    ftaxrate = models.DecimalField(max_digits=7, decimal_places=3)
    fterm = models.CharField(max_length=4)
    fterr = models.CharField(max_length=10)
    fzip = models.CharField(max_length=10)
    flprofprtd = models.BooleanField()
    flprofrqd = models.BooleanField()
    fndpstrcvd = models.DecimalField(max_digits=17, decimal_places=5)
    fndpstrqd = models.DecimalField(max_digits=17, decimal_places=5)
    fdeurodate = models.DateTimeField()
    feurofctr = models.DecimalField(max_digits=17, decimal_places=5)
    fsalescode = models.CharField(max_length=7)
    fusercode = models.CharField(max_length=7)
    fncancchrge = models.DecimalField(max_digits=17, decimal_places=5)
    flchgpnd = models.BooleanField()
    fllasteco = models.CharField(max_length=25)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fackmemo = models.TextField()  # This field type is a guess.
    fmstreet = models.TextField()  # This field type is a guess.
    fmusrmemo1 = models.TextField()  # This field type is a guess.
    fccontkey = models.CharField(max_length=10)
    flcontract = models.BooleanField()
    fndbrmod = models.IntegerField()
    fccommcode = models.CharField(max_length=10)
    fpriority = models.IntegerField()
    contractnu = models.CharField(db_column='ContractNu', max_length=10)  # Field name made lowercase.
    fbilladdr = models.CharField(max_length=6)
    opportunnum = models.CharField(db_column='OpportunNum', max_length=10)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate', auto_now=True)  # No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', auto_now=True)  # No longer exists withing M2M
    oppcrtype = models.CharField(db_column='OppCrType', max_length=3)  # Field name made lowercase.
    quotenumber = models.CharField(db_column='QuoteNumber', max_length=10)  # Field name made lowercase.
    contactnum = models.CharField(max_length=6)
    flpaybycc = models.BooleanField()

    class Meta:
        managed = IS_TEST
        db_table = 'somast'


class Soitem(TruncatedModel):
    finumber = models.CharField(max_length=3)
    fpartno = models.CharField(max_length=25)
    fpartrev = models.CharField(max_length=3)
    fsono = models.CharField(max_length=10)
    fclotext = models.CharField(max_length=1)
    fllotreqd = models.BooleanField()
    fautocreat = models.BooleanField()
    fcas_bom = models.BooleanField()
    fcas_rtg = models.BooleanField()
    fcommpct = models.DecimalField(max_digits=8, decimal_places=2)
    fcustpart = models.CharField(max_length=25)
    fcustptrev = models.CharField(max_length=3)
    fdet_bom = models.BooleanField()
    fdet_rtg = models.BooleanField()
    fduedate = models.DateTimeField()
    fenumber = models.CharField(max_length=3)
    ffixact = models.DecimalField(max_digits=17, decimal_places=5)
    fgroup = models.CharField(max_length=6)
    flabact = models.DecimalField(max_digits=17, decimal_places=5)
    fmatlact = models.DecimalField(max_digits=17, decimal_places=5)
    fmeasure = models.CharField(max_length=3)
    fmultiple = models.BooleanField()
    fnextinum = models.IntegerField()
    fnextrel = models.CharField(max_length=3, blank=True, null=True)
    fnunder = models.DecimalField(max_digits=12, decimal_places=5)
    fnover = models.DecimalField(max_digits=12, decimal_places=5)
    fordertype = models.CharField(max_length=3)
    fothract = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdact = models.DecimalField(max_digits=17, decimal_places=5)
    fprice = models.BooleanField()
    fprintmemo = models.BooleanField()
    fprodcl = models.CharField(max_length=4)
    fquantity = models.DecimalField(max_digits=17, decimal_places=5)
    fcfromtype = models.CharField(max_length=6)
    fcfromno = models.CharField(max_length=25, blank=True, null=True)
    fcfromitem = models.CharField(max_length=3)
    fquoteqty = models.DecimalField(max_digits=15, decimal_places=5)
    frtgsetupa = models.DecimalField(max_digits=17, decimal_places=5)
    fschecode = models.CharField(max_length=6)
    fshipitem = models.BooleanField()
    fsoldby = models.CharField(max_length=3)
    fsource = models.CharField(max_length=1)
    fstandpart = models.BooleanField()
    fsubact = models.DecimalField(max_digits=17, decimal_places=5)
    fsummary = models.BooleanField()
    ftaxcode = models.CharField(max_length=3)
    ftaxrate = models.DecimalField(max_digits=7, decimal_places=3)
    ftoolact = models.DecimalField(max_digits=17, decimal_places=5)
    ftnumoper = models.IntegerField()
    ftotnonpr = models.IntegerField()
    ftotptime = models.DecimalField(max_digits=15, decimal_places=5)
    ftotstime = models.DecimalField(max_digits=15, decimal_places=5)
    fulabcost1 = models.DecimalField(max_digits=17, decimal_places=5)
    fviewprice = models.BooleanField()
    fcprodid = models.CharField(max_length=6)
    fschedtype = models.CharField(max_length=1)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fdesc = models.TextField()
    fdescmemo = models.TextField()
    fndbrmod = models.IntegerField()
    fac = models.CharField(max_length=20)
    sfac = models.CharField(max_length=20)
    itccost = models.DecimalField(db_column='ITCCOST', max_digits=17, decimal_places=5)  # Field name made lowercase.
    fcaltum = models.CharField(db_column='FcAltUM', max_length=3)  # Field name made lowercase.
    fnaltqty = models.DecimalField(db_column='FnAltQty', max_digits=17, decimal_places=5)  # Field name made lowercase.
    fcudrev = models.CharField(max_length=3)
    fnlatefact = models.DecimalField(max_digits=4, decimal_places=2)
    fnsobuf = models.IntegerField()
    manualplan = models.BooleanField(db_column='ManualPlan')  # Field name made lowercase.
    contractnu = models.CharField(db_column='ContractNu', max_length=10)  # Field name made lowercase.
    flrfqreqd = models.BooleanField(db_column='Flrfqreqd')  # Field name made lowercase.
    fcostfrom = models.CharField(db_column='Fcostfrom', max_length=10)  # Field name made lowercase.
    fcitemstatus = models.CharField(db_column='fcItemStatus', max_length=20)  # Field name made lowercase.
    fdrequestdate = models.DateTimeField()
    fdcreateddate = models.DateTimeField()
    fdmodifieddate = models.DateTimeField(auto_now=True)
    forigreqdt = models.DateTimeField(db_column='FOrigReqDt')  # Field name made lowercase.
    ffinalschd = models.BooleanField(db_column='FFinalSchd')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'soitem'


class Sorels(TruncatedModel):
    fenumber = models.CharField(max_length=3)
    finumber = models.CharField(max_length=3)
    fpartno = models.CharField(max_length=25)
    fpartrev = models.CharField(max_length=3)
    frelease = models.CharField(max_length=3)
    fshptoaddr = models.CharField(max_length=6)
    fsono = models.CharField(max_length=10)
    favailship = models.BooleanField()
    fbook = models.DecimalField(max_digits=15, decimal_places=5)
    fbqty = models.DecimalField(max_digits=15, decimal_places=5)
    fdiscount = models.DecimalField(max_digits=17, decimal_places=5)
    fduedate = models.DateTimeField()
    finvamount = models.DecimalField(max_digits=17, decimal_places=5)
    finvqty = models.DecimalField(max_digits=15, decimal_places=5)
    fjob = models.BooleanField()
    fjoqty = models.DecimalField(max_digits=15, decimal_places=5)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    flngth = models.DecimalField(max_digits=15, decimal_places=5)
    flshipdate = models.DateTimeField()
    fmasterrel = models.BooleanField()
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fmaxqty = models.DecimalField(max_digits=15, decimal_places=5)
    fmqty = models.DecimalField(max_digits=15, decimal_places=5)
    fmsi = models.DecimalField(max_digits=15, decimal_places=5)
    fnetprice = models.DecimalField(max_digits=17, decimal_places=5)
    fninvship = models.DecimalField(max_digits=15, decimal_places=5)
    fnpurvar = models.DecimalField(max_digits=19, decimal_places=4)
    forderqty = models.DecimalField(max_digits=15, decimal_places=5)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    fpoqty = models.DecimalField(max_digits=15, decimal_places=5)
    fpostatus = models.CharField(max_length=10)
    fquant = models.DecimalField(max_digits=15, decimal_places=5)
    fsetupcost = models.DecimalField(max_digits=17, decimal_places=5)
    fshipbook = models.DecimalField(max_digits=15, decimal_places=5)
    fshipbuy = models.DecimalField(max_digits=15, decimal_places=5)
    fshipmake = models.DecimalField(max_digits=15, decimal_places=5)
    fshpbefdue = models.BooleanField()
    fsplitshp = models.BooleanField()
    fstatus = models.CharField(max_length=20)
    fstkqty = models.DecimalField(max_digits=15, decimal_places=5)
    fsubcost = models.DecimalField(max_digits=17, decimal_places=5)
    ftoolcost = models.DecimalField(max_digits=17, decimal_places=5)
    ftoshpbook = models.DecimalField(max_digits=15, decimal_places=5)
    ftoshpbuy = models.DecimalField(max_digits=15, decimal_places=5)
    ftoshpmake = models.DecimalField(max_digits=15, decimal_places=5)
    funetprice = models.DecimalField(max_digits=17, decimal_places=5)
    fvendno = models.CharField(max_length=6)
    fwidth = models.DecimalField(max_digits=15, decimal_places=5)
    fnretpoqty = models.DecimalField(max_digits=17, decimal_places=5)
    fnettxnprice = models.DecimalField(max_digits=17, decimal_places=5)
    funettxnpric = models.DecimalField(max_digits=17, decimal_places=5)
    fneteuropr = models.DecimalField(max_digits=17, decimal_places=5)
    funeteuropr = models.DecimalField(max_digits=17, decimal_places=5)
    fdiscpct = models.DecimalField(max_digits=17, decimal_places=5)
    fljrdif = models.BooleanField()
    flistaxabl = models.BooleanField()
    flatp = models.BooleanField()
    fcbin = models.CharField(max_length=14)
    fcloc = models.CharField(max_length=14)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fdelivery = models.TextField()  # This field type is a guess.
    fcpbtype = models.CharField(max_length=1)
    fcudrev = models.CharField(max_length=3)
    fndbrmod = models.IntegerField()
    fpriority = models.IntegerField()
    scheddate = models.DateTimeField(db_column='SchedDate')  # Field name made lowercase.
    flinvcposs = models.BooleanField(db_column='flInvcPoss')  # Field name made lowercase.
    fmatlpadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    ftoolpadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    flabpadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    fovhdpadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    fsubpadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    fothrpadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    fsetuppadj = models.DecimalField(max_digits=16, decimal_places=5, blank=True, null=True)
    fnisoqty = models.DecimalField(db_column='fnISOQty', max_digits=15, decimal_places=5)  # Field name made lowercase.
    earlydays = models.IntegerField(db_column='EARLYDAYS')  # Field name made lowercase.
    fcrelsstatus = models.CharField(db_column='fcRelsStatus', max_length=20)  # Field name made lowercase.
    fdrequestdate = models.DateTimeField()
    fdcreateddate = models.DateTimeField()
    fdmodifieddate = models.DateTimeField(auto_now=True)
    forigreqdt = models.DateTimeField(db_column='FOrigReqDt')  # Field name made lowercase.
    ffinalschd = models.BooleanField(db_column='FFinalSchd')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'sorels'


class Sodrtg(TruncatedModel):
    fbominum = models.CharField(max_length=4)
    fchngrates = models.CharField(max_length=1)
    fcstddesc = models.CharField(max_length=4)
    felpstime = models.DecimalField(max_digits=12, decimal_places=5)
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    finumber = models.CharField(max_length=3)
    flaborutil = models.DecimalField(max_digits=7, decimal_places=2)
    flschedule = models.BooleanField()
    fmovetime = models.DecimalField(max_digits=8, decimal_places=2)
    foperno = models.IntegerField()
    foperqty = models.DecimalField(max_digits=19, decimal_places=6)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fpro_id = models.CharField(max_length=7)
    fsetuptime = models.DecimalField(max_digits=7, decimal_places=2)
    fsono = models.CharField(max_length=10)
    fulabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fuovrhdcos = models.DecimalField(max_digits=7, decimal_places=2)
    fuprodtime = models.DecimalField(max_digits=16, decimal_places=10)
    fusubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fllotreqd = models.BooleanField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fdescript = models.TextField()  # This field type is a guess.
    fopermemo = models.TextField()  # This field type is a guess.
    fndbrmod = models.IntegerField()
    fnsimulops = models.IntegerField()
    fyield = models.DecimalField(max_digits=12, decimal_places=5)
    fsetyield = models.DecimalField(max_digits=8, decimal_places=2)
    cycleunits = models.DecimalField(db_column='CycleUnits', max_digits=13,
                                     decimal_places=3)  # Field name made lowercase.
    unitsize = models.DecimalField(db_column='UnitSize', max_digits=13, decimal_places=3)  # Field name made lowercase.
    fccharcode = models.CharField(max_length=10)

    class Meta:
        managed = IS_TEST
        db_table = 'sodrtg'


class SodrtgExt(TruncatedModel):
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField()  # This field type is a guess.
    fkey_id = models.IntegerField()
    fnmins = models.DecimalField(max_digits=18, decimal_places=0)
    fnseconds = models.DecimalField(max_digits=18, decimal_places=0)
    fnpasses = models.DecimalField(max_digits=18, decimal_places=0)
    fnopermu = models.DecimalField(max_digits=18, decimal_places=2)
    fnoperuprice = models.DecimalField(max_digits=18, decimal_places=3)
    fnopereprice = models.DecimalField(max_digits=18, decimal_places=3)

    class Meta:
        managed = IS_TEST
        db_table = 'sodrtg_ext'


class Sodbom(TruncatedModel):
    fbominum = models.CharField(max_length=4)
    fbompart = models.CharField(max_length=25)
    fbomrev = models.CharField(max_length=3)
    finumber = models.CharField(max_length=3)
    fitem = models.CharField(max_length=6)
    fparinum = models.CharField(max_length=4)
    fsono = models.CharField(max_length=10)
    fbomlcost = models.DecimalField(max_digits=21, decimal_places=8)
    fbommeas = models.CharField(max_length=3)
    fbomocost = models.DecimalField(max_digits=21, decimal_places=8)
    fbomsource = models.CharField(max_length=1)
    fcostfrom = models.CharField(max_length=10)
    fextqty = models.DecimalField(max_digits=15, decimal_places=5)
    ffixcost = models.DecimalField(max_digits=21, decimal_places=8)
    flabcost = models.DecimalField(max_digits=21, decimal_places=8)
    flabsetcos = models.DecimalField(max_digits=21, decimal_places=8)
    flastoper = models.IntegerField()
    flevel = models.CharField(max_length=2)
    flextend = models.BooleanField()
    fltooling = models.BooleanField()
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fnonpro = models.IntegerField()
    fnumopers = models.IntegerField()
    fothrcost = models.DecimalField(max_digits=21, decimal_places=8)
    fovhdcost = models.DecimalField(max_digits=21, decimal_places=8)
    fovrhdsetc = models.DecimalField(max_digits=21, decimal_places=8)
    fsubcost = models.DecimalField(max_digits=21, decimal_places=8)
    ftotptime = models.DecimalField(max_digits=14, decimal_places=7)
    ftotqty = models.DecimalField(max_digits=15, decimal_places=5)
    ftotstime = models.DecimalField(max_digits=14, decimal_places=7)
    fvendno = models.CharField(max_length=6)
    fllotreqd = models.BooleanField()
    fclotext = models.CharField(max_length=1)
    fnoperno = models.IntegerField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fbomdesc = models.TextField()  # This field type is a guess.
    fstdmemo = models.TextField()  # This field type is a guess.
    fac = models.CharField(max_length=20)
    fcbomudrev = models.CharField(max_length=3)
    fndbrmod = models.IntegerField()
    flrfqreqd = models.BooleanField(db_column='Flrfqreqd')  # Field name made lowercase.
    fcsource = models.CharField(db_column='fcSource', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'sodbom'


class SoitemExt(TruncatedModel):
    identity_column = models.AutoField(db_column='Identity_Column', primary_key=True)  # Field name made lowercase.
    # timestamp_column = models.TextField(db_column='Timestamp_Column', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    fkey_id = models.IntegerField(db_column='FKey_ID', unique=True)  # Field name made lowercase.
    size = models.IntegerField(db_column='SIZE', blank=True, null=True)  # Field name made lowercase.
    fisurcharge = models.CharField(max_length=3)
    fcpartdesc = models.CharField(max_length=240)
    fccustptno = models.CharField(max_length=45)
    fcprodgrp = models.CharField(max_length=10)
    fmmatltemp = models.TextField()  # This field type is a guess.
    fcod = models.CharField(max_length=32)
    fcround = models.CharField(max_length=32)
    fcstraight = models.CharField(max_length=32)
    fcfinish = models.CharField(max_length=32)
    fchardness = models.CharField(max_length=32)
    fcshape = models.CharField(max_length=32)
    fcodtol = models.CharField(max_length=32)
    fcbetobe = models.CharField(max_length=32)
    fcheatreat = models.CharField(max_length=32)
    fcthick = models.CharField(max_length=32)
    fcthicktol = models.CharField(max_length=32)
    fcid = models.CharField(max_length=32)
    fcidtol = models.CharField(max_length=32)
    fcsize = models.CharField(max_length=32)
    fcuom = models.CharField(max_length=32)
    fmnotes = models.TextField()  # This field type is a guess.
    fcastm = models.CharField(max_length=32)
    fccda = models.CharField(max_length=32)
    fcbechamf = models.CharField(max_length=32)
    fcwidth = models.CharField(max_length=32)
    fcwidthtol = models.CharField(max_length=32)
    fcshipmth = models.CharField(max_length=32)
    fclen = models.CharField(max_length=32)
    fclentol = models.CharField(max_length=32)
    fcams = models.CharField(max_length=32)
    fmponotes = models.TextField()  # This field type is a guess.
    fcsubcut = models.CharField(max_length=1)
    fcsubtest = models.CharField(max_length=1)
    fcbc_cut = models.CharField(max_length=1)
    fcautomatic = models.CharField(max_length=1)
    fchtcat = models.CharField(max_length=50)
    ftplpartno = models.CharField(max_length=25)
    fclenuom = models.CharField(max_length=3)
    fkey_id_bctplrtg = models.IntegerField()
    fqq = models.CharField(max_length=32)
    fqtfinumber = models.CharField(max_length=3)
    unitsurcharge = models.DecimalField(max_digits=18, decimal_places=3)

    class Meta:
        managed = IS_TEST
        db_table = 'SOITEM_EXT'


class Bcsocost(TruncatedModel):
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField()  # This field type is a guess.
    fsono = models.CharField(max_length=6)
    finumber = models.CharField(max_length=3)
    fnnorelease = models.DecimalField(max_digits=18, decimal_places=0)
    fnbomutcost = models.DecimalField(max_digits=18, decimal_places=3)
    fnmatlcost = models.DecimalField(max_digits=18, decimal_places=3)
    fnutpricadj = models.DecimalField(max_digits=18, decimal_places=3)
    fnmisccost = models.DecimalField(max_digits=18, decimal_places=5)
    fnmatlutcost = models.DecimalField(max_digits=18, decimal_places=3)
    fnqty = models.DecimalField(max_digits=18, decimal_places=5)
    fnmatlmin = models.DecimalField(max_digits=18, decimal_places=5)
    fcprodcl = models.CharField(max_length=2)
    fnsurcharge = models.DecimalField(max_digits=18, decimal_places=5)
    fnsurchargemu = models.DecimalField(max_digits=18, decimal_places=3)
    fnobomutcost = models.DecimalField(max_digits=18, decimal_places=5)
    frpso = models.BooleanField()
    frpinv = models.BooleanField()

    class Meta:
        managed = IS_TEST
        db_table = 'bcsocost'


class Bcsortgcost(TruncatedModel):
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField()  # This field type is a guess.
    fcoperno = models.DecimalField(max_digits=18, decimal_places=0)
    fcwcname = models.CharField(max_length=16)
    fnsuhours = models.DecimalField(max_digits=18, decimal_places=2)
    fnnosu = models.DecimalField(max_digits=18, decimal_places=5)
    fnunithours = models.DecimalField(max_digits=18, decimal_places=5)
    fnlabrate = models.DecimalField(max_digits=18, decimal_places=5)
    fnovhdrate = models.DecimalField(max_digits=18, decimal_places=5)
    fnmatlcost = models.DecimalField(max_digits=18, decimal_places=5)
    fnutpricadj = models.DecimalField(max_digits=18, decimal_places=5)
    fnefffactor = models.DecimalField(max_digits=18, decimal_places=5)
    fnsubcost = models.DecimalField(max_digits=18, decimal_places=5)
    fnminlab = models.DecimalField(max_digits=18, decimal_places=5)
    fcpro_id = models.CharField(max_length=7)
    fkey_id = models.IntegerField()

    class Meta:
        managed = IS_TEST
        db_table = 'bcsortgcost'


class Inwork(TruncatedModel):
    fnavgwkhrs = models.DecimalField(max_digits=6, decimal_places=2)
    fcpro_id = models.CharField(max_length=7)
    fcpro_name = models.CharField(max_length=17)
    fccomments = models.CharField(max_length=54)
    fdept = models.CharField(max_length=4)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fnavgque = models.DecimalField(max_digits=7, decimal_places=1)
    flschedule = models.BooleanField()
    fnmax1 = models.IntegerField()
    fnmax2 = models.IntegerField()
    fnmax3 = models.IntegerField()
    fnmaxque = models.DecimalField(max_digits=7, decimal_places=1)
    fnpctutil = models.DecimalField(max_digits=6, decimal_places=1)
    fnqueallow = models.DecimalField(max_digits=8, decimal_places=2)
    fnstd1 = models.IntegerField()
    fnstd2 = models.IntegerField()
    fnstd3 = models.IntegerField()
    fnstd_prod = models.DecimalField(max_digits=11, decimal_places=6)
    fnstd_set = models.DecimalField(max_digits=7, decimal_places=2)
    fnsumdur = models.DecimalField(max_digits=9, decimal_places=1)
    fovrhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    fscheduled = models.CharField(max_length=1)
    fspandays = models.IntegerField()
    fnpque = models.DecimalField(max_digits=7, decimal_places=1)
    flconstrnt = models.BooleanField()
    identity_column = models.AutoField(unique=True, primary_key=True)
    fac = models.CharField(max_length=20)
    fcstdormax = models.CharField(max_length=8)
    fndbrmod = models.IntegerField()
    fnloadcapc = models.DecimalField(max_digits=6, decimal_places=2)
    fnmaxcapload = models.DecimalField(max_digits=4, decimal_places=1)
    flaltset = models.BooleanField()
    fcsyncmisc = models.CharField(max_length=20)
    queuehrs = models.DecimalField(db_column='QueueHrs', max_digits=9, decimal_places=2)  # Field name made lowercase.
    constbuff = models.DecimalField(db_column='ConstBuff', max_digits=5, decimal_places=1)  # Field name made lowercase.
    resgroup = models.CharField(db_column='ResGroup', max_length=15)  # Field name made lowercase.
    flbflabor = models.BooleanField(db_column='flBFLabor')  # Field name made lowercase.
    cycleunits = models.DecimalField(db_column='CycleUnits', max_digits=13,
                                     decimal_places=3)  # Field name made lowercase.
    simopstype = models.CharField(db_column='SimOpsType', max_length=10)  # Field name made lowercase.
    size = models.DecimalField(db_column='Size', max_digits=13, decimal_places=3)  # Field name made lowercase.
    canbreak = models.BooleanField(db_column='CanBreak')  # Field name made lowercase.
    sizeum = models.CharField(db_column='SizeUM', max_length=3)  # Field name made lowercase.
    timefence = models.IntegerField(db_column='TimeFence')  # Field name made lowercase.
    fcgroup = models.CharField(db_column='fcGroup', max_length=10)  # Field name made lowercase.
    fracsimops = models.BooleanField(db_column='FracSimOps')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'inwork'


class InmastExt(TruncatedModel):
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField()  # This field type is a guess.
    fkey_id = models.IntegerField()
    sigmanestbom = models.BooleanField(blank=True, null=True)
    materialtype = models.CharField(max_length=100, blank=True, null=True)
    grossweight = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    modifieddate = models.DateTimeField(blank=True, null=True)
    surcharge = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    mtlcategory = models.CharField(max_length=100)
    dimlength = models.DecimalField(max_digits=18, decimal_places=1, blank=True, null=True)
    dimwidth = models.DecimalField(max_digits=18, decimal_places=1, blank=True, null=True)
    baseammindex = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    chklta = models.BooleanField(blank=True, null=True)
    txtltaquote = models.CharField(max_length=20, blank=True, null=True)
    duedateadj = models.CharField(max_length=2, blank=True, null=True)
    chkreplace = models.BooleanField(blank=True, null=True)
    txtreplace = models.CharField(max_length=25, blank=True, null=True)
    specgravity = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    shape = models.CharField(max_length=20, blank=True, null=True)
    density = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    mtlthickness = models.CharField(max_length=50, blank=True, null=True)
    margindollarplan = models.DecimalField(max_digits=18, decimal_places=5)

    class Meta:
        managed = IS_TEST
        db_table = 'inmast_ext'


class Inmastx(TruncatedModel):
    fpartno = models.CharField(max_length=25)
    frev = models.CharField(max_length=3)
    fcstscode = models.CharField(max_length=1)
    fdescript = models.CharField(max_length=35)
    flchgpnd = models.BooleanField()
    fmeasure = models.CharField(max_length=3)
    fsource = models.CharField(max_length=1)
    fleadtime = models.DecimalField(max_digits=7, decimal_places=1)
    fprice = models.DecimalField(max_digits=17, decimal_places=5)
    fstdcost = models.DecimalField(max_digits=17, decimal_places=5)
    f2totcost = models.DecimalField(max_digits=17, decimal_places=5)
    flastcost = models.DecimalField(max_digits=17, decimal_places=5)
    flocate1 = models.CharField(max_length=14)
    fbin1 = models.CharField(max_length=14)
    f2costcode = models.CharField(max_length=1)
    f2displcst = models.DecimalField(max_digits=17, decimal_places=5)
    f2dispmcst = models.DecimalField(max_digits=17, decimal_places=5)
    f2dispocst = models.DecimalField(max_digits=17, decimal_places=5)
    f2disptcst = models.DecimalField(max_digits=17, decimal_places=5)
    f2labcost = models.DecimalField(max_digits=17, decimal_places=5)
    f2matlcost = models.DecimalField(max_digits=17, decimal_places=5)
    f2ovhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    favgcost = models.DecimalField(max_digits=17, decimal_places=5)
    fbulkissue = models.CharField(max_length=1)
    fbuyer = models.CharField(max_length=3)
    fcalc_lead = models.CharField(max_length=1)
    fcbackflsh = models.CharField(max_length=1)
    fcnts = models.IntegerField()
    fcopymemo = models.CharField(max_length=1)
    fcostcode = models.CharField(max_length=1)
    fcpurchase = models.CharField(max_length=1)
    fcstperinv = models.DecimalField(max_digits=13, decimal_places=9)
    fdisplcost = models.DecimalField(max_digits=17, decimal_places=5)
    fdispmcost = models.DecimalField(max_digits=17, decimal_places=5)
    fdispocost = models.DecimalField(max_digits=17, decimal_places=5)
    fdispprice = models.DecimalField(max_digits=17, decimal_places=5)
    fdisptcost = models.DecimalField(max_digits=17, decimal_places=5)
    fdrawno = models.CharField(max_length=25)
    fdrawsize = models.CharField(max_length=2)
    fendqty1 = models.DecimalField(max_digits=15, decimal_places=5)
    fendqty10 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty11 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty12 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty2 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty3 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty4 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty5 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty6 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty7 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty8 = models.DecimalField(max_digits=17, decimal_places=5)
    fendqty9 = models.DecimalField(max_digits=17, decimal_places=5)
    fgroup = models.CharField(max_length=6)
    finspect = models.CharField(max_length=1)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    flasteoc = models.CharField(max_length=25)
    flct = models.DateTimeField()
    fllotreqd = models.BooleanField()
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fmeasure2 = models.CharField(max_length=3)
    fnweight = models.DecimalField(max_digits=10, decimal_places=3)
    fovhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    fprodcl = models.CharField(max_length=4)
    freordqty = models.DecimalField(max_digits=15, decimal_places=5)
    frevdt = models.DateTimeField(auto_now=True)
    frolledup = models.CharField(max_length=1)
    fsafety = models.DecimalField(max_digits=15, decimal_places=5)
    fschecode = models.CharField(max_length=6)
    fuprodtime = models.DecimalField(max_digits=9, decimal_places=3)
    fyield = models.DecimalField(max_digits=8, decimal_places=3)
    fabccode = models.CharField(max_length=1)
    ftaxable = models.BooleanField()
    fcusrchr1 = models.CharField(max_length=20)
    fcusrchr2 = models.CharField(max_length=40)
    fcusrchr3 = models.CharField(max_length=40)
    fnusrqty1 = models.DecimalField(max_digits=15, decimal_places=5)
    fnusrcur1 = models.DecimalField(max_digits=17, decimal_places=5)
    fdusrdate1 = models.DateTimeField()
    fcdncfile = models.CharField(max_length=80)
    fccadfile1 = models.CharField(max_length=250)
    fccadfile2 = models.CharField(max_length=250)
    fccadfile3 = models.CharField(max_length=250)
    fclotext = models.CharField(max_length=1)
    flexpreqd = models.BooleanField()
    fdlastpc = models.DateTimeField()
    fschedtype = models.CharField(max_length=1)
    fldctracke = models.BooleanField()
    fddcrefdat = models.DateTimeField()
    fndctax = models.DecimalField(max_digits=17, decimal_places=5)
    fndcduty = models.DecimalField(max_digits=17, decimal_places=5)
    fndcfreigh = models.DecimalField(max_digits=17, decimal_places=5)
    fndcmisc = models.DecimalField(max_digits=17, decimal_places=5)
    fcratedisc = models.CharField(max_length=1)
    flconstrnt = models.BooleanField()
    flistaxabl = models.BooleanField()
    fcjrdict = models.CharField(max_length=10)
    flaplpart = models.BooleanField()
    flfanpart = models.BooleanField()
    fnfanaglvl = models.IntegerField()
    fcplnclass = models.CharField(max_length=1)
    fcclass = models.CharField(max_length=12)
    fidims = models.IntegerField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fcomment = models.TextField()
    fmusrmemo1 = models.TextField()
    fstdmemo = models.TextField()
    fndbrmod = models.IntegerField()
    fac = models.CharField(max_length=20, blank=True, null=True)
    sfac = models.CharField(max_length=20, blank=True, null=True)
    itcfixed = models.DecimalField(max_digits=17, decimal_places=5, blank=True, null=True)
    itcunit = models.DecimalField(max_digits=17, decimal_places=5, blank=True, null=True)
    fnponhand = models.DecimalField(db_column='fnPOnHand', max_digits=16,
                                    decimal_places=5)  # Field name made lowercase.
    fnlndtomfg = models.DecimalField(db_column='fnLndToMfg', max_digits=16,
                                     decimal_places=5)  # Field name made lowercase.
    fipcsonhd = models.IntegerField(db_column='fiPcsOnHd')  # Field name made lowercase.
    fcudrev = models.CharField(max_length=3)
    fluseudrev = models.BooleanField()
    flsendslx = models.BooleanField(db_column='flSendSLX')  # Field name made lowercase.
    fcslxprod = models.CharField(db_column='fcSLXProd', max_length=12)  # Field name made lowercase.
    flfsrtn = models.BooleanField(db_column='flFSRtn')  # Field name made lowercase.
    fnlatefact = models.DecimalField(max_digits=4, decimal_places=2)
    fnsobuf = models.IntegerField()
    fnpurbuf = models.IntegerField()
    flcnstrpur = models.BooleanField()
    fdvenfence = models.DateTimeField()
    fllatefact = models.BooleanField(db_column='flLatefact')  # Field name made lowercase.
    flsobuf = models.BooleanField(db_column='flSOBuf')  # Field name made lowercase.
    flpurbuf = models.BooleanField(db_column='flPurBuf')  # Field name made lowercase.
    flholdstoc = models.BooleanField(db_column='flHoldStoc')  # Field name made lowercase.
    fnholdstoc = models.DecimalField(db_column='fnHoldStoc', max_digits=4,
                                     decimal_places=2)  # Field name made lowercase.
    manualplan = models.BooleanField(db_column='ManualPlan')  # Field name made lowercase.
    scheddate = models.DateTimeField(db_column='SchedDate')  # Field name made lowercase.
    flocbfdef = models.CharField(max_length=14)
    fbinbfdef = models.CharField(max_length=14)
    docktime = models.IntegerField(db_column='DockTime')  # Field name made lowercase.
    fnifttime = models.DecimalField(max_digits=7, decimal_places=1)
    flsynchon = models.BooleanField(db_column='flSynchOn')  # Field name made lowercase.
    # fshipvia = models.CharField(max_length=20)
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True) No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'inmastx'


class Invcur(TruncatedModel):
    fcpartno = models.CharField(max_length=25)
    fcpartrev = models.CharField(max_length=3)
    flanycur = models.BooleanField()
    identity_column = models.AutoField(unique=True, primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fac = models.CharField(max_length=20)
    fcudrev = models.CharField(max_length=3)
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True) No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'invcur'


class Inrtgc(TruncatedModel):
    fpartno = models.CharField(max_length=25)
    fcpartrev = models.CharField(max_length=3)
    fbatch01 = models.IntegerField()
    fbatch02 = models.IntegerField()
    fbatch03 = models.IntegerField()
    fbatch04 = models.IntegerField()
    fbatch05 = models.IntegerField()
    fbatch06 = models.IntegerField()
    fbatch07 = models.IntegerField()
    fbatch08 = models.IntegerField()
    fbatch09 = models.IntegerField()
    fbatch10 = models.IntegerField()
    fbatch11 = models.IntegerField()
    fbatch12 = models.IntegerField()
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fmax01 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax02 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax03 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax04 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax05 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax06 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax07 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax08 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax09 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax10 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax11 = models.DecimalField(max_digits=15, decimal_places=5)
    fmax12 = models.DecimalField(max_digits=15, decimal_places=5)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovrhdcos = models.DecimalField(max_digits=17, decimal_places=5)
    fqty01 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty02 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty03 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty04 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty05 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty06 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty07 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty08 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty09 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty10 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty11 = models.DecimalField(max_digits=15, decimal_places=5)
    fqty12 = models.DecimalField(max_digits=15, decimal_places=5)
    frev_date = models.DateTimeField()
    fsetuplabc = models.DecimalField(max_digits=17, decimal_places=5)
    fsetupovrc = models.DecimalField(max_digits=17, decimal_places=5)
    fsetuptime = models.DecimalField(max_digits=14, decimal_places=5)
    fspq = models.DecimalField(max_digits=15, decimal_places=5)
    fstdrtg = models.CharField(max_length=1)
    fsubcost = models.DecimalField(max_digits=17, decimal_places=5)
    ftottime = models.DecimalField(max_digits=14, decimal_places=5)
    identity_column = models.AutoField(unique=True, primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fndbrmod = models.IntegerField()
    fac = models.CharField(max_length=20)
    fcudrev = models.CharField(max_length=3)
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True) No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'inrtgc'


class Inrtgs(TruncatedModel):
    fpartno = models.CharField(max_length=25)
    fcpartrev = models.CharField(max_length=3)
    foperno = models.IntegerField()
    fchngrates = models.CharField(max_length=1)
    fcstddesc = models.CharField(max_length=4)
    felpstime = models.DecimalField(max_digits=12, decimal_places=5)
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    flschedule = models.BooleanField()
    fmovetime = models.DecimalField(max_digits=8, decimal_places=2)
    foperqty = models.DecimalField(max_digits=15, decimal_places=5)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fpro_id = models.CharField(max_length=7)
    fsetuptime = models.DecimalField(max_digits=7, decimal_places=2)
    fsubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fulabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fuovrhdcos = models.DecimalField(max_digits=17, decimal_places=5)
    fuprodtime = models.DecimalField(max_digits=16, decimal_places=10)
    fusubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fllotreqd = models.BooleanField()
    fccharcode = models.CharField(max_length=10)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fopermemo = models.TextField()
    fndbrmod = models.IntegerField()
    fac = models.CharField(max_length=20)
    fcudrev = models.CharField(max_length=3)
    fnsimulops = models.IntegerField()
    fyield = models.DecimalField(max_digits=12, decimal_places=5)
    fsetyield = models.DecimalField(max_digits=8, decimal_places=2)
    flbflabor = models.BooleanField(db_column='flBFLabor')  # Field name made lowercase.
    cycleunits = models.DecimalField(db_column='CycleUnits', max_digits=13,
                                     decimal_places=3)  # Field name made lowercase.
    unitsize = models.DecimalField(db_column='UnitSize', max_digits=13, decimal_places=3)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True) No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'inrtgs'


class Inbomm(TruncatedModel):
    fpartno = models.CharField(max_length=25)
    fcpartrev = models.CharField(max_length=3)
    fnbommax = models.IntegerField()
    fnbommin = models.IntegerField()
    fdlastrev = models.DateTimeField()
    identity_column = models.AutoField(unique=True, primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    facilityid = models.CharField(max_length=20)
    fcudrev = models.CharField(max_length=3)
    # fcdesc = models.CharField(db_column='fcDesc', max_length=35, blank=True, null=True)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True) No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'inbomm'


class Inboms(TruncatedModel):
    fcomponent = models.CharField(max_length=25)
    fcomprev = models.CharField(max_length=3)
    fitem = models.CharField(max_length=6)
    fparent = models.CharField(max_length=25)
    fparentrev = models.CharField(max_length=3)
    fend_ef_dt = models.DateTimeField()
    fmemoexist = models.CharField(max_length=1)
    fqty = models.DecimalField(max_digits=15, decimal_places=5)
    freqd = models.CharField(max_length=1)
    fst_ef_dt = models.DateTimeField()
    flextend = models.BooleanField()
    fltooling = models.BooleanField()
    fnoperno = models.IntegerField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fbommemo = models.TextField()
    fndbrmod = models.IntegerField()
    cfacilityid = models.CharField(max_length=20)
    pfacilityid = models.CharField(max_length=20)
    fcompudrev = models.CharField(max_length=3)
    fcparudrev = models.CharField(max_length=3)
    flfssvc = models.BooleanField(db_column='flFSSvc')  # Field name made lowercase.
    forigqty = models.DecimalField(db_column='fOrigQty', max_digits=15, decimal_places=5)  # Field name made lowercase.
    fcsource = models.CharField(db_column='fcSource', max_length=10)  # Field name made lowercase.
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True) No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M.

    class Meta:
        managed = IS_TEST
        db_table = 'inboms'


class Inopds(TruncatedModel):
    fdescnum = models.CharField(max_length=4)
    fcpro_id = models.CharField(max_length=7)
    fnstd_prod = models.DecimalField(max_digits=11, decimal_places=6)
    fnstd_set = models.DecimalField(max_digits=7, decimal_places=2)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(unique=True, primary_key=True)
    fopmemo = models.TextField()
    fac = models.CharField(max_length=20)
    # createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  No longer exists withing M2M
    # modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True) No longer exists withing M2M

    class Meta:
        managed = IS_TEST
        db_table = 'inopds'


class Jocbom(TruncatedModel):
    fjobno = models.CharField(max_length=20)
    fseqno = models.CharField(max_length=3)
    fbomdesc = models.TextField()
    fbomqty = models.DecimalField(max_digits=17, decimal_places=5)
    finumber = models.CharField(max_length=3)
    fmatlcost = models.DecimalField(max_digits=21, decimal_places=6)
    fneed_dt = models.DateTimeField()
    fresponse = models.CharField(max_length=1)
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jocbom'


class Jodbom(TruncatedModel):
    fitem = models.CharField(max_length=6)
    fbompart = models.CharField(max_length=25)
    fbomrev = models.CharField(max_length=3)
    fbomdesc = models.TextField()
    fparent = models.CharField(max_length=25)
    fparentrev = models.CharField(max_length=3)
    factqty = models.DecimalField(max_digits=15, decimal_places=5)
    fbomlcost = models.DecimalField(max_digits=14, decimal_places=5)
    fbommeas = models.CharField(max_length=3)
    fbomocost = models.DecimalField(max_digits=14, decimal_places=5)
    fbomrec = models.IntegerField()
    fbomsource = models.CharField(max_length=1)
    fbook = models.DecimalField(max_digits=15, decimal_places=5)
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    finumber = models.CharField(max_length=3)
    fjobno = models.CharField(max_length=20)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    flabsetcos = models.DecimalField(max_digits=17, decimal_places=5)
    flastoper = models.IntegerField()
    flextend = models.BooleanField()
    fltooling = models.BooleanField()
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fneed_dt = models.DateTimeField()
    fnumopers = models.IntegerField()
    fbominum = models.CharField(max_length=4)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovrhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovrhdsetc = models.DecimalField(max_digits=17, decimal_places=5)
    fpono = models.CharField(max_length=10)
    fpoqty = models.DecimalField(max_digits=15, decimal_places=5)
    fqtytopurc = models.DecimalField(max_digits=15, decimal_places=5)
    fqty_iss = models.DecimalField(max_digits=15, decimal_places=5)
    fresponse = models.CharField(max_length=1)
    fsubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fsub_job = models.CharField(max_length=20)
    fsub_rel = models.BooleanField()
    ftotptime = models.DecimalField(max_digits=9, decimal_places=2)
    ftotqty = models.DecimalField(max_digits=20, decimal_places=10)
    ftotstime = models.DecimalField(max_digits=9, decimal_places=2)
    ftransinv = models.DecimalField(max_digits=15, decimal_places=5)
    fvendno = models.CharField(max_length=6)
    fllotreqd = models.BooleanField()
    fclotext = models.CharField(max_length=1)
    fnretpoqty = models.DecimalField(max_digits=15, decimal_places=5)
    fnoperno = models.IntegerField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fstdmemo = models.TextField()
    fpneed_dt = models.DateTimeField()
    cfac = models.CharField(db_column='Cfac', max_length=20)  # Field name made lowercase.
    fcbomudrev = models.CharField(max_length=3)
    fcparudrev = models.CharField(max_length=3)
    fiissdpcs = models.IntegerField()
    fipopieces = models.IntegerField()
    fndbrmod = models.IntegerField()
    fnqtylnd = models.DecimalField(max_digits=17, decimal_places=5)
    pfac = models.CharField(db_column='Pfac', max_length=20)  # Field name made lowercase.
    forigqty = models.DecimalField(db_column='fOrigQty', max_digits=15, decimal_places=5)  # Field name made lowercase.
    scheddate = models.DateTimeField(db_column='SchedDate')  # Field name made lowercase.
    fnisoqty = models.DecimalField(db_column='fnISOQty', max_digits=15, decimal_places=5)  # Field name made lowercase.
    fcsource = models.CharField(db_column='fcSource', max_length=10)  # Field name made lowercase.
    freqd = models.CharField(db_column='FREQD', max_length=1)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jodbom'


class Jodbomdl(TruncatedModel):
    fnsize4 = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)
    fnqty = models.IntegerField()
    identity_column = models.AutoField(primary_key=True)
    fijodbomid = models.IntegerField()
    fium5 = models.IntegerField(blank=True, null=True)
    fnsize1 = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)
    fitype = models.IntegerField()
    flpartial = models.BooleanField()
    fnsize3 = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)
    ficount = models.IntegerField()
    fium1 = models.IntegerField(blank=True, null=True)
    fium2 = models.IntegerField(blank=True, null=True)
    fium3 = models.IntegerField(blank=True, null=True)
    fium4 = models.IntegerField(blank=True, null=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fnsize2 = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)
    fnsize5 = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jodbomdl'


class Jodrtg(TruncatedModel):
    fnlflushqty = models.DecimalField(max_digits=15, decimal_places=5)
    fjobno = models.CharField(max_length=20)
    foperno = models.IntegerField()
    factschdfn = models.DateTimeField()
    factschdst = models.DateTimeField()
    fbominum = models.CharField(max_length=4)
    fchngrates = models.CharField(max_length=1)
    fcomp_date = models.DateTimeField()
    fcstat = models.CharField(max_length=1)
    fstrtdate = models.DateTimeField()
    fddue_date = models.DateTimeField()
    fdescnum = models.CharField(max_length=4)
    fdrel_date = models.DateTimeField()
    felpstime = models.DecimalField(max_digits=8, decimal_places=2)
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    fflushed = models.CharField(max_length=1)
    finumber = models.CharField(max_length=3)
    flastlab = models.DateTimeField()
    flschedule = models.BooleanField()
    fmovetime = models.DecimalField(max_digits=8, decimal_places=2)
    fndelay = models.IntegerField()
    fndue_time = models.IntegerField()
    fneed_dt = models.DateTimeField()
    fnnext_evt = models.IntegerField()
    fnpct_comp = models.IntegerField()
    fnqty_comp = models.DecimalField(max_digits=15, decimal_places=5)
    fnqty_move = models.DecimalField(max_digits=15, decimal_places=5)
    fnqty_togo = models.DecimalField(max_digits=15, decimal_places=5)
    fnque_time = models.IntegerField()
    fnrel_time = models.IntegerField()
    fnshft = models.IntegerField()
    fnsh_date = models.DateTimeField()
    fnsh_time = models.IntegerField()
    fnstrttime = models.IntegerField()
    foperqty = models.DecimalField(max_digits=15, decimal_places=5)
    foper_strt = models.CharField(max_length=1)
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fpono = models.CharField(max_length=10)
    fpoqty = models.DecimalField(max_digits=17, decimal_places=5)
    fnretpoqty = models.DecimalField(max_digits=17, decimal_places=5)
    flead_tim = models.DecimalField(max_digits=8, decimal_places=2)
    flead_stim = models.DecimalField(max_digits=8, decimal_places=2)
    fprod_tim = models.DecimalField(max_digits=8, decimal_places=2)
    fprod_val = models.DecimalField(max_digits=17, decimal_places=5)
    fpro_id = models.CharField(max_length=7)
    fresponse = models.CharField(max_length=1)
    fsetuptime = models.DecimalField(max_digits=7, decimal_places=2)
    fsetup_tim = models.DecimalField(max_digits=8, decimal_places=2)
    fsetup_val = models.DecimalField(max_digits=17, decimal_places=5)
    fshipmt = models.CharField(max_length=1)
    fsource = models.CharField(max_length=1)
    fsplit = models.BooleanField()
    fsubcont = models.CharField(max_length=1)
    ftduedate = models.DateTimeField()
    ftfnshdate = models.CharField(max_length=15)
    ftfnshtime = models.IntegerField()
    ftimetogo = models.DecimalField(max_digits=10, decimal_places=2)
    ftot_app = models.DecimalField(max_digits=15, decimal_places=5)
    ftot_rew = models.DecimalField(max_digits=15, decimal_places=5)
    ftot_scr = models.DecimalField(max_digits=15, decimal_places=5)
    ftquetime = models.IntegerField()
    ftreldate = models.DateTimeField()
    ftstrtdate = models.CharField(max_length=15)
    ftstrttime = models.IntegerField()
    fulabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fuovrhdcos = models.DecimalField(max_digits=17, decimal_places=5)
    fuprodtime = models.DecimalField(max_digits=16, decimal_places=10)
    fusubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fvendno = models.CharField(max_length=6)
    fllotreqd = models.BooleanField()
    fcschdpct = models.CharField(max_length=1)
    flfreeze = models.BooleanField()
    fnsimulops = models.IntegerField()
    fccharcode = models.CharField(max_length=10)
    fdplanstdt = models.DateTimeField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fopermemo = models.TextField()
    fac = models.CharField(max_length=20)
    flsaveprec = models.BooleanField()
    flusesetup = models.BooleanField()
    fndbrmod = models.IntegerField()
    fnlatestrt = models.IntegerField()
    fnmachine = models.IntegerField()
    fcfreezetype = models.CharField(max_length=15)
    fcmachineuse = models.CharField(max_length=100)
    fcsyncmisc = models.CharField(max_length=20)
    usebuffer = models.BooleanField(db_column='UseBuffer')  # Field name made lowercase.
    nextbuffop = models.IntegerField(db_column='NextBuffOp')  # Field name made lowercase.
    bufferstrt = models.DateTimeField(db_column='BufferStrt')  # Field name made lowercase.
    bufferend = models.DateTimeField(db_column='BufferEnd')  # Field name made lowercase.
    arrivetime = models.DateTimeField(db_column='ArriveTime')  # Field name made lowercase.
    flbflabor = models.BooleanField(db_column='flBFLabor')  # Field name made lowercase.
    cycleunits = models.DecimalField(db_column='CycleUnits', max_digits=13, decimal_places=3)  # Field name made lowercase.
    unitsize = models.DecimalField(db_column='UnitSize', max_digits=13, decimal_places=3)  # Field name made lowercase.
    latestrtdt = models.DateTimeField(db_column='LateStrtDt')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jodrtg'


class Joitem(TruncatedModel):
    fjobno = models.CharField(max_length=20)
    fitem = models.CharField(max_length=3)
    fpartno = models.CharField(max_length=25)
    fpartrev = models.CharField(max_length=3)
    fsono = models.CharField(max_length=10)
    finumber = models.CharField(max_length=3)
    fjob = models.BooleanField()
    fkey = models.CharField(max_length=3)
    fbook = models.DecimalField(max_digits=15, decimal_places=5)
    fbqty = models.DecimalField(max_digits=15, decimal_places=5)
    fcost_est = models.DecimalField(max_digits=17, decimal_places=5)
    fcustpart = models.CharField(max_length=25)
    fcustptrev = models.CharField(max_length=3)
    fduedate = models.DateTimeField()
    fgroup = models.CharField(max_length=6)
    fhour_est = models.DecimalField(max_digits=9, decimal_places=2)
    flshipdate = models.DateTimeField()
    fmeasure = models.CharField(max_length=3)
    fmqty = models.DecimalField(max_digits=15, decimal_places=5)
    fmultiple = models.CharField(max_length=1)
    forderqty = models.DecimalField(max_digits=15, decimal_places=5)
    fpartyld1 = models.DecimalField(max_digits=8, decimal_places=3)
    fprodcl = models.CharField(max_length=4)
    frtgqty = models.DecimalField(max_digits=17, decimal_places=5)
    fshipqty = models.DecimalField(max_digits=15, decimal_places=5)
    fsource = models.CharField(max_length=1)
    fstandpart = models.BooleanField()
    fstatus = models.CharField(max_length=1)
    fulabcost1 = models.DecimalField(max_digits=17, decimal_places=5)
    fuprice = models.DecimalField(max_digits=17, decimal_places=5)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fdesc = models.TextField()
    fdescmemo = models.TextField()
    fac = models.CharField(max_length=20)
    fidoshpqty = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    fcudrev = models.CharField(max_length=3)
    fndbrmod = models.IntegerField()
    fdelivery = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'joitem'


class Jolbck(TruncatedModel):
    fctrans_id = models.CharField(max_length=10)
    fcjobno = models.CharField(max_length=20)
    fnoperno = models.IntegerField()
    fcpro_id = models.CharField(max_length=7)
    fddate = models.DateTimeField()
    fnsethrs = models.DecimalField(max_digits=11, decimal_places=4)
    fnprodhrs = models.DecimalField(max_digits=11, decimal_places=4)
    fnulabcost = models.DecimalField(max_digits=17, decimal_places=5)
    fnuovhdcost = models.DecimalField(max_digits=7, decimal_places=2)
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fac = models.CharField(max_length=20, blank=True, null=True)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jolbck'


class Jomast(TruncatedModel):
    fjobno = models.CharField(max_length=20)
    fpartno = models.CharField(max_length=25)
    fpartrev = models.CharField(max_length=3)
    fsono = models.CharField(max_length=10)
    fstatus = models.CharField(max_length=10)
    factschdfn = models.DateTimeField()
    factschdst = models.DateTimeField()
    fact_rel = models.DateTimeField()
    fassy_comp = models.IntegerField()
    fassy_req = models.IntegerField()
    fbilljob = models.CharField(max_length=8)
    fbominum = models.CharField(max_length=4)
    fbomrec = models.IntegerField()
    fcas_bom = models.BooleanField()
    fckeyfield = models.CharField(max_length=20)
    fcompany = models.CharField(max_length=35)
    fcomp_schl = models.BooleanField()
    fconfirm = models.BooleanField()
    fcus_id = models.CharField(max_length=6)
    fdduedtime = models.IntegerField()
    fddue_date = models.DateTimeField()
    fdesc = models.BooleanField()
    fdescript = models.CharField(max_length=70)
    fdet_bom = models.BooleanField()
    fdet_rtg = models.BooleanField()
    fdstart = models.DateTimeField()
    fdfnshdate = models.DateTimeField()
    ffst_job = models.BooleanField()
    fglacct = models.CharField(max_length=25)
    fhold_by = models.CharField(max_length=23)
    fhold_dt = models.DateTimeField()
    fitems = models.IntegerField()
    fitype = models.CharField(max_length=1)
    fjob_name = models.CharField(max_length=86)
    fkey = models.CharField(max_length=6)
    flastlab = models.DateTimeField()
    fmatlpcnt = models.IntegerField()
    fmeasure = models.CharField(max_length=3)
    fmethod = models.CharField(max_length=1)
    fmultiple = models.BooleanField()
    fnassy_com = models.IntegerField()
    fnassy_req = models.IntegerField()
    fnfnshtime = models.IntegerField()
    fnontime = models.IntegerField()
    fnpct_comp = models.DecimalField(max_digits=6, decimal_places=1)
    fnpct_idle = models.DecimalField(max_digits=6, decimal_places=1)
    fnrel_time = models.IntegerField()
    fnshft = models.IntegerField()
    fopen_dt = models.DateTimeField()
    fpartdesc = models.CharField(max_length=40)
    fpick_dt = models.DateTimeField()
    fpick_st = models.BooleanField()
    fpo_comp = models.CharField(max_length=1)
    ftrave_dt = models.DateTimeField()
    ftrave_st = models.BooleanField()
    fpriority = models.CharField(max_length=11)
    fprocessby = models.CharField(max_length=12)
    fprodcl = models.CharField(max_length=4)
    fpro_plan = models.BooleanField()
    fquantity = models.DecimalField(max_digits=15, decimal_places=5)
    frel_dt = models.DateTimeField()
    fremtime = models.IntegerField()
    fresponse = models.CharField(max_length=1)
    fresu_by = models.CharField(max_length=19)
    fresu_dt = models.DateTimeField()
    frouting = models.DecimalField(max_digits=17, decimal_places=5)
    fr_dt = models.DateTimeField()
    fr_rev = models.CharField(max_length=2)
    fr_type = models.CharField(max_length=1)
    fschbefjob = models.CharField(max_length=20)
    fschdflag = models.CharField(max_length=1)
    fschdprior = models.CharField(max_length=1)
    fschresdt = models.DateTimeField()
    fsign_off = models.BooleanField()
    fsplit = models.BooleanField()
    fsplitfrom = models.CharField(max_length=20)
    fsplitinfo = models.CharField(max_length=12)
    fstandpart = models.BooleanField()
    fstarted = models.BooleanField()
    fstrt_date = models.DateTimeField()
    fstrt_time = models.IntegerField()
    fsub_from = models.CharField(max_length=20)
    fsub_rel = models.BooleanField()
    fsummary = models.BooleanField()
    ftduedate = models.DateTimeField()
    ftfnshdate = models.CharField(max_length=15)
    ftfnshtime = models.IntegerField()
    ftot_assy = models.IntegerField()
    ftreldt = models.DateTimeField()
    ftschresdt = models.DateTimeField()
    ftstrtdate = models.CharField(max_length=15)
    ftstrttime = models.IntegerField()
    ftype = models.CharField(max_length=1)
    fcusrchr1 = models.CharField(max_length=20)
    fcusrchr2 = models.CharField(max_length=40)
    fcusrchr3 = models.CharField(max_length=40)
    fnusrqty1 = models.DecimalField(max_digits=15, decimal_places=5)
    fnusrcur1 = models.DecimalField(max_digits=17, decimal_places=5)
    fdusrdate1 = models.DateTimeField()
    fnlastopno = models.IntegerField()
    fcdncfile = models.CharField(max_length=80)
    fccadfile1 = models.CharField(max_length=250)
    fccadfile2 = models.CharField(max_length=250)
    fccadfile3 = models.CharField(max_length=250)
    fllotreqd = models.BooleanField()
    fclotext = models.CharField(max_length=1)
    flresync = models.BooleanField()
    fdorgduedt = models.DateTimeField()
    flquick = models.BooleanField()
    flfreeze = models.BooleanField()
    flchgpnd = models.BooleanField()
    fllasteco = models.CharField(max_length=25)
    flisapl = models.BooleanField()
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fjob_mem = models.TextField()
    fmusermemo = models.TextField()
    fac = models.CharField(max_length=20)
    idono = models.CharField(max_length=10, blank=True, null=True)
    sfac = models.CharField(max_length=20, blank=True, null=True)
    fcudrev = models.CharField(max_length=3)
    fdmndrank = models.IntegerField()
    fndbrmod = models.IntegerField()
    fnrouteno = models.IntegerField()
    flplanfreeze = models.BooleanField()
    fcsyncmisc = models.CharField(max_length=20)
    usebuffer = models.BooleanField(db_column='UseBuffer')  # Field name made lowercase.
    bufferstrt = models.DateTimeField(db_column='BufferStrt')  # Field name made lowercase.
    bufferend = models.DateTimeField(db_column='BufferEnd')  # Field name made lowercase.
    demandcat = models.CharField(db_column='DemandCat', max_length=1)  # Field name made lowercase.
    createddate = models.DateTimeField()
    moddate = models.DateTimeField(db_column='ModDate')  # Field name made lowercase.
    fyield = models.DecimalField(db_column='fYield', max_digits=15, decimal_places=5)  # Field name made lowercase.
    fsetyield = models.DecimalField(db_column='fSetYield', max_digits=8, decimal_places=2)  # Field name made lowercase.
    fcrmano = models.CharField(max_length=25)
    firmed = models.BooleanField(db_column='Firmed')  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jomast'


class Jopact(TruncatedModel):
    fjobno = models.CharField(max_length=20)
    faddedocos = models.DecimalField(max_digits=17, decimal_places=5)
    faddedpcos = models.DecimalField(max_digits=17, decimal_places=5)
    faddedltim = models.DecimalField(max_digits=7, decimal_places=2)
    faddedptim = models.DecimalField(max_digits=9, decimal_places=2)
    faddedscos = models.DecimalField(max_digits=17, decimal_places=5)
    faddedstim = models.DecimalField(max_digits=7, decimal_places=2)
    finumber = models.CharField(max_length=3)
    flabact = models.DecimalField(max_digits=17, decimal_places=5)
    flabinv = models.DecimalField(max_digits=17, decimal_places=5)
    flast_ent = models.DateTimeField()
    fmatlact = models.DecimalField(max_digits=17, decimal_places=5)
    fmatlinv = models.DecimalField(max_digits=17, decimal_places=5)
    fothract = models.DecimalField(max_digits=17, decimal_places=5)
    fothrinv = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdact = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdinv = models.DecimalField(max_digits=17, decimal_places=5)
    frtgsetupa = models.DecimalField(max_digits=17, decimal_places=5)
    fsetupact = models.DecimalField(max_digits=17, decimal_places=5)
    fsubact = models.DecimalField(max_digits=17, decimal_places=5)
    fsubinv = models.DecimalField(max_digits=17, decimal_places=5)
    ftoolact = models.DecimalField(max_digits=17, decimal_places=5)
    ftotltime = models.DecimalField(max_digits=14, decimal_places=5)
    ftotptime = models.DecimalField(max_digits=14, decimal_places=5)
    ftotstime = models.DecimalField(max_digits=7, decimal_places=2)
    faddedlsti = models.DecimalField(max_digits=7, decimal_places=2)
    ftotlstime = models.DecimalField(max_digits=14, decimal_places=5)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fpmemo = models.TextField()
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jopact'


class Jopest(TruncatedModel):
    fjobno = models.CharField(max_length=20)
    fbuy_itm = models.IntegerField()
    fcus_itm = models.IntegerField()
    ffixcost = models.DecimalField(max_digits=17, decimal_places=5)
    finoper = models.IntegerField()
    finumber = models.CharField(max_length=3)
    flabcost = models.DecimalField(max_digits=17, decimal_places=5)
    flastoper = models.IntegerField()
    fldhrs = models.DecimalField(max_digits=14, decimal_places=5)
    fmak_itm = models.IntegerField()
    fmatlcost = models.DecimalField(max_digits=17, decimal_places=5)
    fmovehrs = models.DecimalField(max_digits=8, decimal_places=2)
    fno_bom = models.BooleanField()
    fno_rtg = models.BooleanField()
    fnumopers = models.IntegerField()
    fothrcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdcost = models.DecimalField(max_digits=17, decimal_places=5)
    fovhdsc = models.DecimalField(max_digits=17, decimal_places=5)
    fprodhrs = models.DecimalField(max_digits=14, decimal_places=5)
    fsetupcost = models.DecimalField(max_digits=17, decimal_places=5)
    fsetuphrs = models.DecimalField(max_digits=7, decimal_places=2)
    fstk_itm = models.IntegerField()
    fsubcost = models.DecimalField(max_digits=17, decimal_places=5)
    fsubhrs = models.IntegerField()
    fsuboper = models.IntegerField()
    ftoolcost = models.DecimalField(max_digits=17, decimal_places=5)
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'jopest'


class Joqmast(TruncatedModel):
    fcabccd = models.CharField(max_length=1)
    fccompna = models.CharField(max_length=35)
    fcdocrev = models.CharField(max_length=2)
    fcgrpcod = models.CharField(max_length=6)
    fcjonum = models.CharField(max_length=20)
    fcjoopno = models.CharField(max_length=4)
    fcmeasure = models.CharField(max_length=3)
    fcorderact = models.CharField(max_length=1)
    fcpartno = models.CharField(max_length=25)
    fcrev = models.CharField(max_length=3)
    fcplanner = models.CharField(max_length=3)
    fcponum = models.CharField(max_length=10)
    fcprdcls = models.CharField(max_length=4)
    fcqsource = models.CharField(max_length=1)
    fcsoitm = models.CharField(max_length=3)
    fcsonum = models.CharField(max_length=10)
    fcsorls = models.CharField(max_length=3)
    fcsource = models.CharField(max_length=5)
    fcstatus = models.CharField(max_length=10)
    fcsupdem = models.CharField(max_length=6)
    fcvendna = models.CharField(max_length=35)
    fcvendno = models.CharField(max_length=6)
    fdtxndate = models.DateTimeField()
    flmaster = models.BooleanField()
    flautocr = models.BooleanField()
    fnbalqty = models.DecimalField(max_digits=17, decimal_places=5)
    fntxnqty = models.DecimalField(max_digits=17, decimal_places=5)
    fnucost = models.DecimalField(max_digits=17, decimal_places=5)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_column = models.AutoField(primary_key=True)
    fmdesc = models.TextField()
    fac = models.CharField(max_length=20)
    fcidono = models.CharField(db_column='fcIdoNo', max_length=10)  # Field name made lowercase.
    fcudrev = models.CharField(max_length=3)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'joqmast'


class Joresc(TruncatedModel):
    fjobno = models.CharField(max_length=20)
    foperno = models.IntegerField()
    fcres_id = models.CharField(max_length=7)
    fnsimulops = models.DecimalField(max_digits=4, decimal_places=2)
    identity_column = models.AutoField(primary_key=True)
    # timestamp_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    fndbrmod = models.IntegerField()
    fcmachineuse = models.CharField(max_length=100)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST
        db_table = 'joresc'


class MaJobmaterialsummary(TruncatedModel):
    jobno = models.CharField(db_column='JobNo', max_length=20, primary_key=True)  # Field name made lowercase.
    subjobno = models.CharField(db_column='SubJobNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PartNo', max_length=25)  # Field name made lowercase.
    partrev = models.CharField(db_column='PartRev', max_length=3)  # Field name made lowercase.
    partfac = models.CharField(db_column='PartFac', max_length=20)  # Field name made lowercase.
    partsource = models.CharField(db_column='PartSource', max_length=1)  # Field name made lowercase.
    partsourcefromitemmaster = models.CharField(db_column='PartSourceFromItemMaster', max_length=1)  # Field name made lowercase.
    partdescription = models.TextField(db_column='PartDescription')  # Field name made lowercase.
    actualquantity = models.DecimalField(db_column='ActualQuantity', max_digits=17, decimal_places=5)  # Field name made lowercase.
    actualmaterialcost = models.DecimalField(db_column='ActualMaterialCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    actuallaborcost = models.DecimalField(db_column='ActualLaborCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    actualoverheadcost = models.DecimalField(db_column='ActualOverheadCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedquantity = models.DecimalField(db_column='EstimatedQuantity', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedmaterialcost = models.DecimalField(db_column='EstimatedMaterialCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedlaborcost = models.DecimalField(db_column='EstimatedLaborCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedoverheadcost = models.DecimalField(db_column='EstimatedOverheadCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedlaborcomponentcost = models.DecimalField(db_column='EstimatedLaborComponentCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedoverheadcomponentcost = models.DecimalField(db_column='EstimatedOverheadComponentCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    inventorystdlaborcost = models.DecimalField(db_column='InventoryStdLaborCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    inventoryavglaborcost = models.DecimalField(db_column='InventoryAvgLaborCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    inventorystdmaterialcost = models.DecimalField(db_column='InventoryStdMaterialCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    inventoryavgmaterialcost = models.DecimalField(db_column='InventoryAvgMaterialCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    inventorystdoverheadcost = models.DecimalField(db_column='InventoryStdOverheadCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    inventoryavgoverheadcost = models.DecimalField(db_column='InventoryAvgOverheadCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    unitofmeasure = models.CharField(db_column='UnitOfMeasure', max_length=3)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST  # Created from a view. Don't remove.
        db_table = 'MA_JobMaterialSummary'


class MaJoblaborsummary(TruncatedModel):
    jobno = models.CharField(db_column='JobNo', max_length=20, primary_key=True)  # Field name made lowercase.
    operationno = models.IntegerField(db_column='OperationNo')  # Field name made lowercase.
    workcenterid = models.CharField(db_column='WorkCenterId', max_length=9)  # Field name made lowercase.
    workcentername = models.CharField(db_column='WorkCenterName', max_length=16, blank=True, null=True)  # Field name made lowercase.
    workcenterdept = models.CharField(db_column='WorkCenterDept', max_length=4, blank=True, null=True)  # Field name made lowercase.
    requiredquantity = models.DecimalField(db_column='RequiredQuantity', max_digits=15, decimal_places=5)  # Field name made lowercase.
    completedquantity = models.DecimalField(db_column='CompletedQuantity', max_digits=15, decimal_places=5)  # Field name made lowercase.
    estimatedsetuphours = models.DecimalField(db_column='EstimatedSetupHours', max_digits=7, decimal_places=2)  # Field name made lowercase.
    actualsetuphours = models.DecimalField(db_column='ActualSetupHours', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedprodhours = models.DecimalField(db_column='EstimatedProdHours', max_digits=17, decimal_places=5)  # Field name made lowercase.
    actualprodhours = models.DecimalField(db_column='ActualProdHours', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedprodcost = models.DecimalField(db_column='EstimatedProdCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    actualprodcost = models.DecimalField(db_column='ActualProdCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedsetupcost = models.DecimalField(db_column='EstimatedSetupCost', max_digits=25, decimal_places=7)  # Field name made lowercase.
    actualsetupcost = models.DecimalField(db_column='ActualSetupCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    estimatedoverheadcost = models.DecimalField(db_column='EstimatedOverheadCost', max_digits=17, decimal_places=5)  # Field name made lowercase.
    actualoverheadcost = models.DecimalField(db_column='ActualOverheadCost', max_digits=18, decimal_places=5)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = IS_TEST  # Created from a view. Don't remove.
        db_table = 'MA_JobLaborSummary'
