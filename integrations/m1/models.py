from django.db import models
from baseintegration.utils.truncated_model import TruncatedModel
from m1.settings import IS_TEST


class Salesorders(TruncatedModel):
    ompsalesorderid = models.CharField(db_column='ompSalesOrderID', unique=True,
                                       max_length=10)  # Field name made lowercase.
    ompplantid = models.CharField(db_column='ompPlantID', max_length=5,
                                  )  # Field name made lowercase.
    ompplantdepartmentid = models.CharField(db_column='ompPlantDepartmentID', max_length=5,
                                            )  # Field name made lowercase.
    ompcustomerorganizationid = models.CharField(db_column='ompCustomerOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    omparinvoicelocationid = models.CharField(db_column='ompARInvoiceLocationID', max_length=5,
                                              )  # Field name made lowercase.
    omparinvoicecontactid = models.CharField(db_column='ompARInvoiceContactID', max_length=5,
                                             )  # Field name made lowercase.
    ompquotelocationid = models.CharField(db_column='ompQuoteLocationID', max_length=5,
                                          )  # Field name made lowercase.
    ompquotecontactid = models.CharField(db_column='ompQuoteContactID', max_length=5,
                                         )  # Field name made lowercase.
    ompshiporganizationid = models.CharField(db_column='ompShipOrganizationID', max_length=10,
                                             )  # Field name made lowercase.
    ompshiplocationid = models.CharField(db_column='ompShipLocationID', max_length=5,
                                         )  # Field name made lowercase.
    ompshipcontactid = models.CharField(db_column='ompShipContactID', max_length=5,
                                        )  # Field name made lowercase.
    ompcustomerpo = models.CharField(db_column='ompCustomerPO', max_length=40,
                                     )  # Field name made lowercase.
    omprequestedshipdate = models.DateTimeField(db_column='ompRequestedShipDate', blank=True,
                                                null=True)  # Field name made lowercase.
    omporderdate = models.DateTimeField(db_column='ompOrderDate', blank=True, null=True)  # Field name made lowercase.
    ompfreeonboarddescription = models.CharField(db_column='ompFreeOnBoardDescription', max_length=15,
                                                 )  # Field name made lowercase.
    ompshippingmethodid = models.CharField(db_column='ompShippingMethodID', max_length=5,
                                           )  # Field name made lowercase.
    ompshippingpaymenttypeid = models.CharField(db_column='ompShippingPaymentTypeID', max_length=5,
                                                )  # Field name made lowercase.
    omppaymenttermid = models.CharField(db_column='ompPaymentTermID', max_length=5,
                                        )  # Field name made lowercase.
    ompresellerorganizationid = models.CharField(db_column='ompResellerOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    ompresellerlocationid = models.CharField(db_column='ompResellerLocationID', max_length=5,
                                             )  # Field name made lowercase.
    ompresellercontactid = models.CharField(db_column='ompResellerContactID', max_length=5,
                                            )  # Field name made lowercase.
    ompordercommentsrtf = models.TextField(db_column='ompOrderCommentsRTF', blank=True,
                                           null=True)  # Field name made lowercase.
    ompordercommentstext = models.TextField(db_column='ompOrderCommentsText',
                                            blank=True, null=True)  # Field name made lowercase.
    ompcreatedfromweb = models.BooleanField(db_column='ompCreatedFromWeb')  # Field name made lowercase.
    ompreadytoprint = models.BooleanField(db_column='ompReadyToPrint')  # Field name made lowercase.
    ompstandardmessageid = models.CharField(db_column='ompStandardMessageID', max_length=10,
                                            )  # Field name made lowercase.
    ompcurrencyrateid = models.CharField(db_column='ompCurrencyRateID', max_length=5,
                                         )  # Field name made lowercase.
    ompcustomrate = models.BooleanField(db_column='ompCustomRate')  # Field name made lowercase.
    ompexchangerate = models.DecimalField(db_column='ompExchangeRate', max_digits=13,
                                          decimal_places=6)  # Field name made lowercase.
    ompfullordersubtotalbase = models.DecimalField(db_column='ompFullOrderSubtotalBase', max_digits=19,
                                                   decimal_places=4)  # Field name made lowercase.
    ompfullordersubtotalforeign = models.DecimalField(db_column='ompFullOrderSubtotalForeign', max_digits=19,
                                                      decimal_places=4)  # Field name made lowercase.
    ompdiscounttotalbase = models.DecimalField(db_column='ompDiscountTotalBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    ompdiscounttotalforeign = models.DecimalField(db_column='ompDiscountTotalForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    ompordersubtotalbase = models.DecimalField(db_column='ompOrderSubtotalBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    ompordersubtotalforeign = models.DecimalField(db_column='ompOrderSubTotalForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    ompfreightsubtotalbase = models.DecimalField(db_column='ompFreightSubtotalBase', max_digits=19,
                                                 decimal_places=4)  # Field name made lowercase.
    ompfreightsubtotalforeign = models.DecimalField(db_column='ompFreightSubtotalForeign', max_digits=19,
                                                    decimal_places=4)  # Field name made lowercase.
    omptotalorderweight = models.DecimalField(db_column='ompTotalOrderWeight', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    ompfreightamountbase = models.DecimalField(db_column='ompFreightAmountBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    ompfreightamountforeign = models.DecimalField(db_column='ompFreightAmountForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    ompfreighttotalbase = models.DecimalField(db_column='ompFreightTotalBase', max_digits=19,
                                              decimal_places=4)  # Field name made lowercase.
    ompfreighttotalforeign = models.DecimalField(db_column='ompFreightTotalForeign', max_digits=19,
                                                 decimal_places=4)  # Field name made lowercase.
    ompfreighttaxcodeid = models.CharField(db_column='ompFreightTaxCodeID', max_length=5,
                                           )  # Field name made lowercase.
    ompfreighttaxamountbase = models.DecimalField(db_column='ompFreightTaxAmountBase', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    ompfreighttaxamountforeign = models.DecimalField(db_column='ompFreightTaxAmountForeign', max_digits=19,
                                                     decimal_places=4)  # Field name made lowercase.
    ompsecondfreighttaxcodeid = models.CharField(db_column='ompSecondFreightTaxCodeID', max_length=5,
                                                 )  # Field name made lowercase.
    ompsecondfreighttaxamtbase = models.DecimalField(db_column='ompSecondFreightTaxAmtBase', max_digits=19,
                                                     decimal_places=4)  # Field name made lowercase.
    ompsecondfreighttaxamtforeign = models.DecimalField(db_column='ompSecondFreightTaxAmtForeign', max_digits=19,
                                                        decimal_places=4)  # Field name made lowercase.
    ompordertaxamountbase = models.DecimalField(db_column='ompOrderTaxAmountBase', max_digits=19,
                                                decimal_places=4)  # Field name made lowercase.
    ompordertaxamountforeign = models.DecimalField(db_column='ompOrderTaxAmountForeign', max_digits=19,
                                                   decimal_places=4)  # Field name made lowercase.
    ompordertotalbase = models.DecimalField(db_column='ompOrderTotalBase', max_digits=19,
                                            decimal_places=4)  # Field name made lowercase.
    ompordertotalforeign = models.DecimalField(db_column='ompOrderTotalForeign', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    ompstatus = models.SmallIntegerField(db_column='ompStatus')  # Field name made lowercase.
    ompapprovalrequestdate = models.DateTimeField(db_column='ompApprovalRequestDate', blank=True,
                                                  null=True)  # Field name made lowercase.
    ompapprovaldecisiondate = models.DateTimeField(db_column='ompApprovalDecisionDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    ompnextapprovalemployeeid = models.CharField(db_column='ompNextApprovalEmployeeID', max_length=10,
                                                 )  # Field name made lowercase.
    ompprojectid = models.CharField(db_column='ompProjectID', max_length=10,
                                    )  # Field name made lowercase.
    ompclosed = models.BooleanField(db_column='ompClosed')  # Field name made lowercase.
    ompcloseddate = models.DateTimeField(db_column='ompClosedDate', blank=True, null=True)  # Field name made lowercase.
    ompdeposit = models.BooleanField(db_column='ompDeposit')  # Field name made lowercase.
    ompdepositpercent = models.DecimalField(db_column='ompDepositPercent', max_digits=6,
                                            decimal_places=2)  # Field name made lowercase.
    ompdepositcreated = models.BooleanField(db_column='ompDepositCreated')  # Field name made lowercase.
    ompdepositamountbase = models.DecimalField(db_column='ompDepositAmountBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    ompdepositamountforeign = models.DecimalField(db_column='ompDepositAmountForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    ompcallid = models.CharField(db_column='ompCallID', max_length=10,
                                 )  # Field name made lowercase.
    ompavalarataxcalculated = models.BooleanField(db_column='ompAvalaraTaxCalculated')  # Field name made lowercase.
    ompcreatedby = models.CharField(db_column='ompCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    ompcreateddate = models.DateTimeField(db_column='ompCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    ompuniqueid = models.AutoField(db_column='ompUniqueID', unique=True, primary_key=True)
    # ompuniqueid = models.CharField(db_column='ompUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    ompupsaccountnumber = models.CharField(db_column='ompUPSAccountNumber', max_length=6,
                                           )  # Field name made lowercase.
    ompfedexaccountnumber = models.CharField(db_column='ompFedExAccountNumber', max_length=15,
                                             )  # Field name made lowercase.
    ompeasyorderenabled = models.BooleanField(db_column='ompEasyOrderEnabled')  # Field name made lowercase.
    ompcreatedbyedi = models.BooleanField(db_column='ompCreatedByEDI')  # Field name made lowercase.
    ompeasyorderid = models.CharField(db_column='ompEasyOrderID', max_length=50,
                                      )  # Field name made lowercase.
    ompupsbillingoption = models.CharField(db_column='ompUPSBillingOption', max_length=20,
                                           )  # Field name made lowercase.
    ompfedexbillingoption = models.CharField(db_column='ompFedExBillingOption', max_length=20,
                                             )  # Field name made lowercase.
    ompfedex3rdpartyorganizationid = models.CharField(db_column='ompFedEx3rdPartyOrganizationID', max_length=10,
                                                      )  # Field name made lowercase.
    ompfedex3rdpartylocationid = models.CharField(db_column='ompFedEx3rdPartyLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    ompups3rdpartyorganizationid = models.CharField(db_column='ompUPS3rdPartyOrganizationID', max_length=10,
                                                    )  # Field name made lowercase.
    ompups3rdpartylocationid = models.CharField(db_column='ompUPS3rdPartyLocationID', max_length=5,
                                                )  # Field name made lowercase.
    ompeasyorderstatus = models.SmallIntegerField(db_column='ompEasyOrderStatus')  # Field name made lowercase.
    omptaxsubtotalbase = models.DecimalField(db_column='ompTaxSubtotalBase', max_digits=19,
                                             decimal_places=4)  # Field name made lowercase.
    omptaxsubtotalforeign = models.DecimalField(db_column='ompTaxSubtotalForeign', max_digits=19,
                                                decimal_places=4)  # Field name made lowercase.
    ompsplitpercenttotal = models.DecimalField(db_column='ompSplitPercentTotal', max_digits=6,
                                               decimal_places=2)  # Field name made lowercase.
    ompeasyorderexternalstatus = models.CharField(db_column='ompEasyOrderExternalStatus', max_length=3,
                                                  )  # Field name made lowercase.
    ompeasyorderpaid = models.BooleanField(db_column='ompEasyOrderPaid')  # Field name made lowercase.

    # omprowversion = models.TextField(db_column='ompRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'SalesOrders'


class Salesorderlines(TruncatedModel):
    omlsalesorderid = models.CharField(db_column='omlSalesOrderID', max_length=10)  # Field name made lowercase.
    omlsalesorderlineid = models.SmallIntegerField(db_column='omlSalesOrderLineID')  # Field name made lowercase.
    omlpartid = models.CharField(db_column='omlPartID', max_length=30,
                                 )  # Field name made lowercase.
    omlorgpartid = models.CharField(db_column='omlOrgPartID', max_length=30,
                                    )  # Field name made lowercase.
    omlpartrevisionid = models.CharField(db_column='omlPartRevisionID', max_length=15,
                                         )  # Field name made lowercase.
    omlunitofmeasure = models.CharField(db_column='omlUnitOfMeasure', max_length=2,
                                        )  # Field name made lowercase.
    omlpartgroupid = models.CharField(db_column='omlPartGroupID', max_length=5,
                                      )  # Field name made lowercase.
    omlpartshortdescription = models.CharField(db_column='omlPartShortDescription', max_length=50,
                                               )  # Field name made lowercase.
    omlorgpartshortdescription = models.CharField(db_column='omlOrgPartShortDescription', max_length=50,
                                                  )  # Field name made lowercase.
    omlpartlongdescriptionrtf = models.TextField(db_column='omlPartLongDescriptionRTF',
                                                 blank=True,
                                                 null=True)  # Field name made lowercase.
    omlpartlongdescriptiontext = models.TextField(db_column='omlPartLongDescriptionText',
                                                  blank=True,
                                                  null=True)  # Field name made lowercase.
    omlorderquantity = models.DecimalField(db_column='omlOrderQuantity', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    omlfullunitpricebase = models.DecimalField(db_column='omlFullUnitPriceBase', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    omlfullunitpriceforeign = models.DecimalField(db_column='omlFullUnitPriceForeign', max_digits=15,
                                                  decimal_places=5)  # Field name made lowercase.
    omldiscountpercent = models.DecimalField(db_column='omlDiscountPercent', max_digits=6,
                                             decimal_places=2)  # Field name made lowercase.
    omlunitdiscountbase = models.DecimalField(db_column='omlUnitDiscountBase', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    omlunitdiscountforeign = models.DecimalField(db_column='omlUnitDiscountForeign', max_digits=15,
                                                 decimal_places=5)  # Field name made lowercase.
    omlunitpricebase = models.DecimalField(db_column='omlUnitPriceBase', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    omlunitpriceforeign = models.DecimalField(db_column='omlUnitPriceForeign', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    omlfullextendedpricebase = models.DecimalField(db_column='omlFullExtendedPriceBase', max_digits=19,
                                                   decimal_places=4)  # Field name made lowercase.
    omlfullextendedpriceforeign = models.DecimalField(db_column='omlFullExtendedPriceForeign', max_digits=19,
                                                      decimal_places=4)  # Field name made lowercase.
    omlextendeddiscountbase = models.DecimalField(db_column='omlExtendedDiscountBase', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    omlextendeddiscountforeign = models.DecimalField(db_column='omlExtendedDiscountForeign', max_digits=19,
                                                     decimal_places=4)  # Field name made lowercase.
    omlextendedpricebase = models.DecimalField(db_column='omlExtendedPriceBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    omlextendedpriceforeign = models.DecimalField(db_column='omlExtendedPriceForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    omlfreightamountbase = models.DecimalField(db_column='omlFreightAmountBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    omlfreightamountforeign = models.DecimalField(db_column='omlFreightAmountForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    omltaxcodeid = models.CharField(db_column='omlTaxCodeID', max_length=5,
                                    )  # Field name made lowercase.
    omlnontaxreasonid = models.CharField(db_column='omlNonTaxReasonID', max_length=5,
                                         )  # Field name made lowercase.
    omltaxamountbase = models.DecimalField(db_column='omlTaxAmountBase', max_digits=19,
                                           decimal_places=4)  # Field name made lowercase.
    omltaxamountforeign = models.DecimalField(db_column='omlTaxAmountForeign', max_digits=19,
                                              decimal_places=4)  # Field name made lowercase.
    omlsecondtaxcodeid = models.CharField(db_column='omlSecondTaxCodeID', max_length=5,
                                          )  # Field name made lowercase.
    omlsecondtaxamountbase = models.DecimalField(db_column='omlSecondTaxAmountBase', max_digits=19,
                                                 decimal_places=4)  # Field name made lowercase.
    omlsecondtaxamountforeign = models.DecimalField(db_column='omlSecondTaxAmountForeign', max_digits=19,
                                                    decimal_places=4)  # Field name made lowercase.
    omlpaycommission = models.BooleanField(db_column='omlPayCommission')  # Field name made lowercase.
    omltimeandmaterial = models.BooleanField(db_column='omlTimeAndMaterial')  # Field name made lowercase.
    omlquantityshipped = models.DecimalField(db_column='omlQuantityShipped', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    omlquoteid = models.CharField(db_column='omlQuoteID', max_length=10,
                                  )  # Field name made lowercase.
    omlquotelineid = models.SmallIntegerField(db_column='omlQuoteLineID')  # Field name made lowercase.
    omlquotequantityid = models.SmallIntegerField(db_column='omlQuoteQuantityID')  # Field name made lowercase.
    omlleadid = models.CharField(db_column='omlLeadID', max_length=10,
                                 )  # Field name made lowercase.
    omlleadlineid = models.SmallIntegerField(db_column='omlLeadLineID')  # Field name made lowercase.
    omlrmaclaimid = models.CharField(db_column='omlRMAClaimID', max_length=10,
                                     )  # Field name made lowercase.
    omlrmaclaimlineid = models.SmallIntegerField(db_column='omlRMAClaimLineID')  # Field name made lowercase.
    omlconfigured = models.BooleanField(db_column='omlConfigured')  # Field name made lowercase.
    omlprojectid = models.CharField(db_column='omlProjectID', max_length=10,
                                    )  # Field name made lowercase.
    omlprojectareaid = models.CharField(db_column='omlProjectAreaID', max_length=15,
                                        )  # Field name made lowercase.
    omlweight = models.DecimalField(db_column='omlWeight', max_digits=15,
                                    decimal_places=5)  # Field name made lowercase.
    omlpossessionid = models.CharField(db_column='omlPOSSessionID', max_length=10,
                                       )  # Field name made lowercase.
    omlpostransactionid = models.CharField(db_column='omlPOSTransactionID', max_length=10,
                                           )  # Field name made lowercase.
    omlpostransactionlineid = models.SmallIntegerField(
        db_column='omlPOSTransactionLineID')  # Field name made lowercase.
    omlclosed = models.BooleanField(db_column='omlClosed')  # Field name made lowercase.
    omlpriceoverride = models.BooleanField(db_column='omlPriceOverride')  # Field name made lowercase.
    omldeposit = models.BooleanField(db_column='omlDeposit')  # Field name made lowercase.
    omldepositpercent = models.DecimalField(db_column='omlDepositPercent', max_digits=6,
                                            decimal_places=2)  # Field name made lowercase.
    omldepositamountbase = models.DecimalField(db_column='omlDepositAmountBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    omldepositamountforeign = models.DecimalField(db_column='omlDepositAmountForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    omldepositcreated = models.BooleanField(db_column='omlDepositCreated')  # Field name made lowercase.
    omldepositcredited = models.BooleanField(db_column='omlDepositCredited')  # Field name made lowercase.
    omldocuments = models.TextField(db_column='omlDocuments', blank=True,
                                    null=True)  # Field name made lowercase.
    omlavalaraignoreline = models.BooleanField(db_column='omlAvalaraIgnoreLine')  # Field name made lowercase.
    omlcreatedby = models.CharField(db_column='omlCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    omlcreateddate = models.DateTimeField(db_column='omlCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    omluniqueid = models.AutoField(db_column='omlUniqueID', unique=True, primary_key=True)
    # omluniqueid = models.CharField(db_column='omlUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    omlextendedweight = models.DecimalField(db_column='omlExtendedWeight', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    omldeliveryquantitytotal = models.DecimalField(db_column='omlDeliveryQuantityTotal', max_digits=15,
                                                   decimal_places=5)  # Field name made lowercase.
    omleasyorderexternalstatus = models.CharField(db_column='omlEasyOrderExternalStatus', max_length=3,
                                                  )  # Field name made lowercase.
    omlreleasenumber = models.CharField(db_column='omlReleaseNumber', max_length=20,
                                        )  # Field name made lowercase.

    # omlrowversion = models.TextField(db_column='omlRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'SalesOrderLines'
        unique_together = (('omlsalesorderid', 'omlsalesorderlineid'),)


class Salesorderdeliveries(TruncatedModel):
    omdsalesorderid = models.CharField(db_column='omdSalesOrderID', max_length=10)  # Field name made lowercase.
    omdsalesorderlineid = models.SmallIntegerField(db_column='omdSalesOrderLineID')  # Field name made lowercase.
    omdsalesorderdeliveryid = models.SmallIntegerField(
        db_column='omdSalesOrderDeliveryID')  # Field name made lowercase.
    omdpartid = models.CharField(db_column='omdPartID', max_length=30,
                                 )  # Field name made lowercase.
    omdpartrevisionid = models.CharField(db_column='omdPartRevisionID', max_length=15,
                                         )  # Field name made lowercase.
    omdpartwarehouselocationid = models.CharField(db_column='omdPartWarehouseLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    omdpartbinid = models.CharField(db_column='omdPartBinID', max_length=15,
                                    )  # Field name made lowercase.
    omddeliveryquantity = models.DecimalField(db_column='omdDeliveryQuantity', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    omddeliverydate = models.DateTimeField(db_column='omdDeliveryDate', blank=True,
                                           null=True)  # Field name made lowercase.
    omddeliverytype = models.SmallIntegerField(db_column='omdDeliveryType')  # Field name made lowercase.
    omdfirm = models.BooleanField(db_column='omdFirm')  # Field name made lowercase.
    omdamounttoinvoice = models.DecimalField(db_column='omdAmountToInvoice', max_digits=19,
                                             decimal_places=4)  # Field name made lowercase.
    omdamounttoinvoiceforeign = models.DecimalField(db_column='omdAmountToInvoiceForeign', max_digits=19,
                                                    decimal_places=4)  # Field name made lowercase.
    omddifferentlocation = models.BooleanField(db_column='omdDifferentLocation')  # Field name made lowercase.
    omdcustomerorganizationid = models.CharField(db_column='omdCustomerOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    omdshiplocationid = models.CharField(db_column='omdShipLocationID', max_length=5,
                                         )  # Field name made lowercase.
    omdshipcontactid = models.CharField(db_column='omdShipContactID', max_length=5,
                                        )  # Field name made lowercase.
    omdshippingmethodid = models.CharField(db_column='omdShippingMethodID', max_length=5,
                                           )  # Field name made lowercase.
    omdshippingpaymenttypeid = models.CharField(db_column='omdShippingPaymentTypeID', max_length=5,
                                                )  # Field name made lowercase.
    omdfreightamountbase = models.DecimalField(db_column='omdFreightAmountBase', max_digits=19,
                                               decimal_places=4)  # Field name made lowercase.
    omdfreightamountforeign = models.DecimalField(db_column='omdFreightAmountForeign', max_digits=19,
                                                  decimal_places=4)  # Field name made lowercase.
    omdquantityshipped = models.DecimalField(db_column='omdQuantityShipped', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    omdquantityinvoiced = models.DecimalField(db_column='omdQuantityInvoiced', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    omdshippedcomplete = models.BooleanField(db_column='omdShippedComplete')  # Field name made lowercase.
    omdinvoicedcomplete = models.BooleanField(db_column='omdInvoicedComplete')  # Field name made lowercase.
    omdclosed = models.BooleanField(db_column='omdClosed')  # Field name made lowercase.
    omdrequiresinspection = models.BooleanField(db_column='omdRequiresInspection')  # Field name made lowercase.
    omdpurchaseunitcostbase = models.DecimalField(db_column='omdPurchaseUnitCostBase', max_digits=15,
                                                  decimal_places=5)  # Field name made lowercase.
    omdpickinprogress = models.BooleanField(db_column='omdPickInProgress')  # Field name made lowercase.
    omdpurchaseunitcostforeign = models.DecimalField(db_column='omdPurchaseUnitCostForeign', max_digits=15,
                                                     decimal_places=5)  # Field name made lowercase.
    omdsupplierorganizationid = models.CharField(db_column='omdSupplierOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    omdpurchaselocationid = models.CharField(db_column='omdPurchaseLocationID', max_length=5,
                                             )  # Field name made lowercase.
    omdquantityreceived = models.DecimalField(db_column='omdQuantityReceived', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    omdreceivedcomplete = models.BooleanField(db_column='omdReceivedComplete')  # Field name made lowercase.
    omdavalaranontaxreasonid = models.CharField(db_column='omdAvalaraNonTaxReasonID', max_length=5,
                                                )  # Field name made lowercase.
    omdcreatedby = models.CharField(db_column='omdCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    omdcreateddate = models.DateTimeField(db_column='omdCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    omduniqueid = models.AutoField(db_column='omdUniqueID', unique=True, primary_key=True)
    # omduniqueid = models.CharField(db_column='omdUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    omdkitpart = models.BooleanField(db_column='omdKitPart')  # Field name made lowercase.
    omdquantityallocated = models.DecimalField(db_column='omdQuantityAllocated', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    omdquantityonorder = models.DecimalField(db_column='omdQuantityOnOrder', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    omdweight = models.DecimalField(db_column='omdWeight', max_digits=15,
                                    decimal_places=5)  # Field name made lowercase.
    omdextendedweight = models.DecimalField(db_column='omdExtendedWeight', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.

    # omdrowversion = models.TextField(db_column='omdRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'SalesOrderDeliveries'
        unique_together = (('omdsalesorderid', 'omdsalesorderlineid', 'omdsalesorderdeliveryid'),)


class Salesorderjoblinks(TruncatedModel):
    omjsalesorderid = models.CharField(db_column='omjSalesOrderID', max_length=10,
                                       )  # Field name made lowercase.
    omjsalesorderlineid = models.SmallIntegerField(db_column='omjSalesOrderLineID')  # Field name made lowercase.
    omjsalesorderjoblinkid = models.IntegerField(db_column='omjSalesOrderJobLinkID')  # Field name made lowercase.
    omjlinktype = models.SmallIntegerField(db_column='omjLinkType')  # Field name made lowercase.
    omjsalesorderdeliveryid = models.SmallIntegerField(
        db_column='omjSalesOrderDeliveryID')  # Field name made lowercase.
    omjjobid = models.CharField(db_column='omjJobID', max_length=20,
                                )  # Field name made lowercase.
    omjclosed = models.BooleanField(db_column='omjClosed')  # Field name made lowercase.
    omjcreatedby = models.CharField(db_column='omjCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    omjcreateddate = models.DateTimeField(db_column='omjCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    omjuniqueid = models.AutoField(db_column='omjUniqueID', unique=True, primary_key=True)

    # omjuniqueid = models.CharField(db_column='omjUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    # omjrowversion = models.TextField(db_column='omjRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'SalesOrderJobLinks'
        unique_together = (('omjsalesorderid', 'omjsalesorderlineid', 'omjsalesorderjoblinkid'),)


class Parts(TruncatedModel):
    imppartid = models.CharField(db_column='impPartID', unique=True, max_length=30)  # Field name made lowercase.
    impshortdescription = models.CharField(db_column='impShortDescription', max_length=50,
                                           )  # Field name made lowercase.
    implongdescriptionrtf = models.TextField(db_column='impLongDescriptionRTF',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    implongdescriptiontext = models.TextField(db_column='impLongDescriptionText',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    impparttype = models.SmallIntegerField(db_column='impPartType')  # Field name made lowercase.
    imppartgroupid = models.CharField(db_column='impPartGroupID', max_length=5,
                                      )  # Field name made lowercase.
    imppartclassid = models.CharField(db_column='impPartClassID', max_length=5,
                                      )  # Field name made lowercase.
    impcyclecodeid = models.CharField(db_column='impCycleCodeID', max_length=5,
                                      )  # Field name made lowercase.
    impnonstockeditem = models.BooleanField(db_column='impNonStockedItem')  # Field name made lowercase.
    impoemorganizationid = models.CharField(db_column='impOEMOrganizationID', max_length=10,
                                            )  # Field name made lowercase.
    impwebsellabletoall = models.BooleanField(db_column='impWebSellableToAll')  # Field name made lowercase.
    impalwaysnontaxable = models.BooleanField(db_column='impAlwaysNonTaxable')  # Field name made lowercase.
    impsecondtaxcodeid = models.CharField(db_column='impSecondTaxCodeID', max_length=5,
                                          )  # Field name made lowercase.
    imptaxcodeid = models.CharField(db_column='impTaxCodeID', max_length=5,
                                    )  # Field name made lowercase.
    impnontaxreasonid = models.CharField(db_column='impNonTaxReasonID', max_length=5,
                                         )  # Field name made lowercase.
    impcontractlength = models.SmallIntegerField(db_column='impContractLength')  # Field name made lowercase.
    impcontractlengthtype = models.CharField(db_column='impContractLengthType', max_length=1,
                                             )  # Field name made lowercase.
    impdeliverytype = models.SmallIntegerField(db_column='impDeliveryType')  # Field name made lowercase.
    imptrackserialnumbers = models.BooleanField(db_column='impTrackSerialNumbers')  # Field name made lowercase.
    impnextserialnumberidformula = models.TextField(db_column='impNextSerialNumberIDFormula',
                                                    blank=True,
                                                    null=True)  # Field name made lowercase.
    imptracklotnumbers = models.BooleanField(db_column='impTrackLotNumbers')  # Field name made lowercase.
    impnonphysicalshipment = models.BooleanField(db_column='impNonPhysicalShipment')  # Field name made lowercase.
    impphantomorkitpart = models.BooleanField(db_column='impPhantomOrKitPart')  # Field name made lowercase.
    impbuyforinventory = models.BooleanField(db_column='impBuyForInventory')  # Field name made lowercase.
    impinactive = models.BooleanField(db_column='impInactive')  # Field name made lowercase.
    impinactivedate = models.DateTimeField(db_column='impInactiveDate', blank=True,
                                           null=True)  # Field name made lowercase.
    impcreatedby = models.CharField(db_column='impCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    impcreateddate = models.DateTimeField(db_column='impCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    impuniqueid = models.AutoField(db_column='impUniqueID', unique=True, primary_key=True)
    # impuniqueid = models.CharField(db_column='impUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    impreordermethod = models.SmallIntegerField(db_column='impReorderMethod')  # Field name made lowercase.

    # improwversion = models.TextField(db_column='impRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'Parts'


class Partrevisions(TruncatedModel):
    imrpartid = models.CharField(db_column='imrPartID', max_length=30)  # Field name made lowercase.
    imrpartrevisionid = models.CharField(db_column='imrPartRevisionID', max_length=15)  # Field name made lowercase.
    imrshortdescription = models.CharField(db_column='imrShortDescription', max_length=50,
                                           )  # Field name made lowercase.
    imrlongdescriptionrtf = models.TextField(db_column='imrLongDescriptionRTF',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    imrlongdescriptiontext = models.TextField(db_column='imrLongDescriptionText',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    imrlongdescriptionhtml = models.TextField(db_column='imrLongDescriptionHTML',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    imruniversalproductcode = models.CharField(db_column='imrUniversalProductCode', max_length=13,
                                               )  # Field name made lowercase.
    imreffectivestartdate = models.DateTimeField(db_column='imrEffectiveStartDate', blank=True,
                                                 null=True, auto_now=True)  # Field name made lowercase.
    imreffectiveenddate = models.DateTimeField(db_column='imrEffectiveEndDate', blank=True,
                                               null=True)  # Field name made lowercase.
    imrwebsuppresswhensold = models.BooleanField(db_column='imrWebSuppressWhenSold')  # Field name made lowercase.
    imrinventoryunitofmeasure = models.CharField(db_column='imrInventoryUnitOfMeasure', max_length=2,
                                                 )  # Field name made lowercase.
    imrpurchaseunitofmeasure = models.CharField(db_column='imrPurchaseUnitOfMeasure', max_length=2,
                                                )  # Field name made lowercase.
    imrquantityonhand = models.DecimalField(db_column='imrQuantityOnHand', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    imrquantityallocated = models.DecimalField(db_column='imrQuantityAllocated', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    imrquantitytoinspect = models.DecimalField(db_column='imrQuantityToInspect', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    imrquantitytoreturn = models.DecimalField(db_column='imrQuantityToReturn', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    imrminimumquantity = models.DecimalField(db_column='imrMinimumQuantity', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    imrmaximumquantity = models.DecimalField(db_column='imrMaximumQuantity', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    imrmanufacturinglotsize = models.DecimalField(db_column='imrManufacturingLotSize', max_digits=15,
                                                  decimal_places=5)  # Field name made lowercase.
    imraveragelaborcost = models.DecimalField(db_column='imrAverageLaborCost', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    imraverageoverheadcost = models.DecimalField(db_column='imrAverageOverheadCost', max_digits=15,
                                                 decimal_places=5)  # Field name made lowercase.
    imraveragematerialcost = models.DecimalField(db_column='imrAverageMaterialCost', max_digits=15,
                                                 decimal_places=5)  # Field name made lowercase.
    imraveragesubcontractcost = models.DecimalField(db_column='imrAverageSubcontractCost', max_digits=15,
                                                    decimal_places=5)  # Field name made lowercase.
    imrlastlaborcost = models.DecimalField(db_column='imrLastLaborCost', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    imrlastoverheadcost = models.DecimalField(db_column='imrLastOverheadCost', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    imrlastmaterialcost = models.DecimalField(db_column='imrLastMaterialCost', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    imrlastsubcontractcost = models.DecimalField(db_column='imrLastSubcontractCost', max_digits=15,
                                                 decimal_places=5)  # Field name made lowercase.
    imrstandardlaborcost = models.DecimalField(db_column='imrStandardLaborCost', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    imrstandardoverheadcost = models.DecimalField(db_column='imrStandardOverheadCost', max_digits=15,
                                                  decimal_places=5)  # Field name made lowercase.
    imrstandardmaterialcost = models.DecimalField(db_column='imrStandardMaterialCost', max_digits=15,
                                                  decimal_places=5)  # Field name made lowercase.
    imrstandardsubcontractcost = models.DecimalField(db_column='imrStandardSubcontractCost', max_digits=15,
                                                     decimal_places=5)  # Field name made lowercase.
    imrleadtime = models.SmallIntegerField(db_column='imrLeadTime')  # Field name made lowercase.
    imrconversionfactor = models.DecimalField(db_column='imrConversionFactor', max_digits=14,
                                              decimal_places=8)  # Field name made lowercase.
    imrconfigured = models.BooleanField(db_column='imrConfigured')  # Field name made lowercase.
    imrusequoteprice = models.BooleanField(db_column='imrUseQuotePrice')  # Field name made lowercase.
    imrsupplierorganizationid = models.CharField(db_column='imrSupplierOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    imrpurchaselocationid = models.CharField(db_column='imrPurchaseLocationID', max_length=5,
                                             )  # Field name made lowercase.
    imrpreferredrefexists = models.BooleanField(db_column='imrPreferredRefExists')  # Field name made lowercase.
    imrproductionnotesrtf = models.TextField(db_column='imrProductionNotesRTF',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    imrproductionnotestext = models.TextField(db_column='imrProductionNotesText',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    imrdocuments = models.TextField(db_column='imrDocuments', blank=True,
                                    null=True)  # Field name made lowercase.
    imrsourcemethodid = models.CharField(db_column='imrSourceMethodID', max_length=30,
                                         )  # Field name made lowercase.
    imrsourcerevisionid = models.CharField(db_column='imrSourceRevisionID', max_length=15,
                                           )  # Field name made lowercase.
    imrinactive = models.BooleanField(db_column='imrInactive')  # Field name made lowercase.
    imrpartimagefilename = models.CharField(db_column='imrPartImageFileName', max_length=70,
                                            )  # Field name made lowercase.
    imrlastreceiptdate = models.DateTimeField(db_column='imrLastReceiptDate', blank=True,
                                              null=True)  # Field name made lowercase.
    imrformid = models.CharField(db_column='imrFormID', max_length=75,
                                 )  # Field name made lowercase.
    imrinspectionnotestext = models.TextField(db_column='imrInspectionNotesText',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    imrinspectionnotesrtf = models.TextField(db_column='imrInspectionNotesRTF',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    imrsheetsizex = models.DecimalField(db_column='imrSheetSizeX', max_digits=12,
                                        decimal_places=3)  # Field name made lowercase.
    imrsheetsizey = models.DecimalField(db_column='imrSheetSizeY', max_digits=12,
                                        decimal_places=3)  # Field name made lowercase.
    imrbarlength = models.DecimalField(db_column='imrBarLength', max_digits=12,
                                       decimal_places=3)  # Field name made lowercase.
    imrweight = models.DecimalField(db_column='imrWeight', max_digits=15,
                                    decimal_places=5)  # Field name made lowercase.
    imrfdxpackaging = models.CharField(db_column='imrFdxPackaging', max_length=14,
                                       )  # Field name made lowercase.
    imrfdxpackagelength = models.IntegerField(db_column='imrFdxPackageLength')  # Field name made lowercase.
    imrfdxpackagewidth = models.IntegerField(db_column='imrFdxPackageWidth')  # Field name made lowercase.
    imrfdxpackageheight = models.IntegerField(db_column='imrFdxPackageHeight')  # Field name made lowercase.
    imrfdxhandlingcost = models.DecimalField(db_column='imrFdxHandlingCost', max_digits=7,
                                             decimal_places=2)  # Field name made lowercase.
    imrfdxpackagingcost = models.DecimalField(db_column='imrFdxPackagingCost', max_digits=7,
                                              decimal_places=2)  # Field name made lowercase.
    imrfdxshipcostmarkuppct = models.DecimalField(db_column='imrFdxShipCostMarkupPct', max_digits=5,
                                                  decimal_places=2)  # Field name made lowercase.
    imrfdxoneitempershipment = models.BooleanField(db_column='imrFdxOneItemPerShipment')  # Field name made lowercase.
    imrfdxnonstandardcontainer = models.BooleanField(
        db_column='imrFdxNonstandardContainer')  # Field name made lowercase.
    imrquantityonordersales = models.DecimalField(db_column='imrQuantityOnOrderSales', max_digits=15,
                                                  decimal_places=5)  # Field name made lowercase.
    imrquantityonorderpurchases = models.DecimalField(db_column='imrQuantityOnOrderPurchases', max_digits=15,
                                                      decimal_places=5)  # Field name made lowercase.
    imrwebshowtopartorgref = models.BooleanField(db_column='imrWebShowToPartOrgRef')  # Field name made lowercase.
    imrpurchasableitem = models.BooleanField(db_column='imrPurchasableItem')  # Field name made lowercase.
    imrwebsellabletoall = models.BooleanField(db_column='imrWebSellableToAll')  # Field name made lowercase.
    imraveragedutycost = models.DecimalField(db_column='imrAverageDutyCost', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    imraveragefreightcost = models.DecimalField(db_column='imrAverageFreightCost', max_digits=15,
                                                decimal_places=5)  # Field name made lowercase.
    imraveragemisccost = models.DecimalField(db_column='imrAverageMiscCost', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    imrlastdutycost = models.DecimalField(db_column='imrLastDutyCost', max_digits=15,
                                          decimal_places=5)  # Field name made lowercase.
    imrlastfreightcost = models.DecimalField(db_column='imrLastFreightCost', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    imrlastmisccost = models.DecimalField(db_column='imrLastMiscCost', max_digits=15,
                                          decimal_places=5)  # Field name made lowercase.
    imrstandarddutycost = models.DecimalField(db_column='imrStandardDutyCost', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    imrstandardfreightcost = models.DecimalField(db_column='imrStandardFreightCost', max_digits=15,
                                                 decimal_places=5)  # Field name made lowercase.
    imrstandardmisccost = models.DecimalField(db_column='imrStandardMiscCost', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    imrvolume = models.DecimalField(db_column='imrVolume', max_digits=15,
                                    decimal_places=5)  # Field name made lowercase.
    imrproductcategoryid = models.CharField(db_column='imrProductCategoryID', max_length=30,
                                            )  # Field name made lowercase.
    imrproductcategorylineid = models.SmallIntegerField(
        db_column='imrProductCategoryLineID')  # Field name made lowercase.
    imrcreatedby = models.CharField(db_column='imrCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    imrcreateddate = models.DateTimeField(db_column='imrCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    imruniqueid = models.AutoField(db_column='imrUniqueID', unique=True, primary_key=True)
    # imruniqueid = models.CharField(db_column='imrUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    imreasyorderpartid = models.CharField(db_column='imrEasyOrderPartID', max_length=30,
                                          )  # Field name made lowercase.
    imrcountryofmanufacture = models.CharField(db_column='imrCountryOfManufacture', max_length=2,
                                               )  # Field name made lowercase.
    imrcommoditycode = models.CharField(db_column='imrCommodityCode', max_length=20,
                                        )  # Field name made lowercase.
    imrweightunitofmeasure = models.CharField(db_column='imrWeightUnitOfMeasure', max_length=3,
                                              )  # Field name made lowercase.
    imrcommoditydescription = models.CharField(db_column='imrCommodityDescription', max_length=35,
                                               )  # Field name made lowercase.
    imrblanketperiodbegin = models.DateTimeField(db_column='imrBlanketPeriodBegin', blank=True,
                                                 null=True)  # Field name made lowercase.
    imrblanketperiodend = models.DateTimeField(db_column='imrBlanketPeriodEnd', blank=True,
                                               null=True)  # Field name made lowercase.
    imrnetcostcode = models.CharField(db_column='imrNetCostCode', max_length=2,
                                      )  # Field name made lowercase.
    imrpreferencecriteria = models.CharField(db_column='imrPreferenceCriteria', max_length=1,
                                             )  # Field name made lowercase.
    imrproducerdetermination = models.CharField(db_column='imrProducerDetermination', max_length=5,
                                                )  # Field name made lowercase.
    imrnetcostbegindate = models.DateTimeField(db_column='imrNetCostBeginDate', blank=True,
                                               null=True)  # Field name made lowercase.
    imrnetcostenddate = models.DateTimeField(db_column='imrNetCostEndDate', blank=True,
                                             null=True)  # Field name made lowercase.
    imrlasttransactiondate = models.DateTimeField(db_column='imrLastTransactionDate', blank=True,
                                                  null=True)  # Field name made lowercase.
    imrexpensesplitpercenttotal = models.DecimalField(db_column='imrExpenseSplitPercentTotal', max_digits=6,
                                                      decimal_places=2)  # Field name made lowercase.
    imrlastrundatepurchaseplanner = models.DateTimeField(db_column='imrLastRunDatePurchasePlanner', blank=True,
                                                         null=True)  # Field name made lowercase.
    imrwebconfigmode = models.BooleanField(db_column='imrWebConfigMode')  # Field name made lowercase.
    imrsuppressshortdescription = models.BooleanField(
        db_column='imrSuppressShortDescription')  # Field name made lowercase.
    imrwebconfigpricerule = models.BooleanField(db_column='imrWebConfigPriceRule')  # Field name made lowercase.
    imrquantitytoreturnjob = models.DecimalField(db_column='imrQuantityToReturnJob', max_digits=15,
                                                 decimal_places=5)  # Field name made lowercase.
    imrrequiresinspection = models.SmallIntegerField(db_column='imrRequiresInspection')  # Field name made lowercase.

    # imrrowversion = models.TextField(db_column='imrRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'PartRevisions'
        unique_together = (('imrpartid', 'imrpartrevisionid'),)


class Jobs(TruncatedModel):
    jmpjobid = models.CharField(db_column='jmpJobID', unique=True, max_length=20)  # Field name made lowercase.
    jmpplantdepartmentid = models.CharField(db_column='jmpPlantDepartmentID', max_length=5,
                                            )  # Field name made lowercase.
    jmpplantid = models.CharField(db_column='jmpPlantID', max_length=5,
                                  )  # Field name made lowercase.
    jmpproductionduedate = models.DateTimeField(db_column='jmpProductionDueDate', blank=True, null=True,
                                                )  # Field name made lowercase.
    jmpcustomerorganizationid = models.CharField(db_column='jmpCustomerOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    jmpjobdate = models.DateTimeField(db_column='jmpJobDate', blank=True, null=True,
                                      auto_now=True)  # Field name made lowercase.
    jmppartid = models.CharField(db_column='jmpPartID', max_length=30,
                                 )  # Field name made lowercase.
    jmppartrevisionid = models.CharField(db_column='jmpPartRevisionID', max_length=15,
                                         )  # Field name made lowercase.
    jmppartwarehouselocationid = models.CharField(db_column='jmpPartWareHouseLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    jmppartbinid = models.CharField(db_column='jmpPartBinID', max_length=15,
                                    )  # Field name made lowercase.
    jmpcallid = models.CharField(db_column='jmpCallID', max_length=10,
                                 )  # Field name made lowercase.
    jmpunitofmeasure = models.CharField(db_column='jmpUnitOfMeasure', max_length=2,
                                        )  # Field name made lowercase.
    jmppartshortdescription = models.CharField(db_column='jmpPartShortDescription', max_length=50,
                                               )  # Field name made lowercase.
    jmppartlongdescriptionrtf = models.TextField(db_column='jmpPartLongDescriptionRTF',
                                                 blank=True,
                                                 null=True)  # Field name made lowercase.
    jmppartlongdescriptiontext = models.TextField(db_column='jmpPartLongDescriptionText',
                                                  blank=True,
                                                  null=True)  # Field name made lowercase.
    jmporderquantity = models.DecimalField(db_column='jmpOrderQuantity', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    jmpinventoryquantity = models.DecimalField(db_column='jmpInventoryQuantity', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmpscrapquantity = models.DecimalField(db_column='jmpScrapQuantity', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    jmpreworkquantity = models.DecimalField(db_column='jmpReworkQuantity', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmpreworkdate = models.DateTimeField(db_column='jmpReworkDate', blank=True, null=True)  # Field name made lowercase.
    jmpproductionquantity = models.DecimalField(db_column='jmpProductionQuantity', max_digits=15,
                                                decimal_places=5)  # Field name made lowercase.
    jmpscheduledstartdate = models.DateTimeField(db_column='jmpScheduledStartDate', blank=True,
                                                 null=True)  # Field name made lowercase.
    jmpscheduledstarthour = models.DecimalField(db_column='jmpScheduledStartHour', max_digits=5,
                                                decimal_places=2)  # Field name made lowercase.
    jmpscheduledduedate = models.DateTimeField(db_column='jmpScheduledDueDate', blank=True,
                                               null=True)  # Field name made lowercase.
    jmpscheduledduehour = models.DecimalField(db_column='jmpScheduledDueHour', max_digits=5,
                                              decimal_places=2)  # Field name made lowercase.
    jmpfirm = models.BooleanField(db_column='jmpFirm')  # Field name made lowercase.
    jmptimeandmaterial = models.BooleanField(db_column='jmpTimeAndMaterial')  # Field name made lowercase.
    jmpplanningcomplete = models.BooleanField(db_column='jmpPlanningComplete')  # Field name made lowercase.
    jmpplanneremployeeid = models.CharField(db_column='jmpPlannerEmployeeID', max_length=10,
                                            )  # Field name made lowercase.
    jmpschedulecomplete = models.BooleanField(db_column='jmpScheduleComplete')  # Field name made lowercase.
    jmpschedulelocked = models.BooleanField(db_column='jmpScheduleLocked')  # Field name made lowercase.
    jmpreleasedtofloor = models.BooleanField(db_column='jmpReleasedToFloor')  # Field name made lowercase.
    jmponhold = models.BooleanField(db_column='jmpOnHold')  # Field name made lowercase.
    jmpreadytoprint = models.BooleanField(db_column='jmpReadyToPrint')  # Field name made lowercase.
    jmpproductioncomplete = models.BooleanField(db_column='jmpProductionComplete')  # Field name made lowercase.
    jmpquantitycompleted = models.DecimalField(db_column='jmpQuantityCompleted', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmpcompleteddate = models.DateTimeField(db_column='jmpCompletedDate', blank=True,
                                            null=True)  # Field name made lowercase.
    jmpquantityshipped = models.DecimalField(db_column='jmpQuantityShipped', max_digits=15,
                                             decimal_places=5)  # Field name made lowercase.
    jmpquantityreceivedtoinventory = models.DecimalField(db_column='jmpQuantityReceivedToInventory', max_digits=15,
                                                         decimal_places=5)  # Field name made lowercase.
    jmpquoteid = models.CharField(db_column='jmpQuoteID', max_length=10,
                                  )  # Field name made lowercase.
    jmpquotelineid = models.SmallIntegerField(db_column='jmpQuoteLineID')  # Field name made lowercase.
    jmpsourcemethodid = models.CharField(db_column='jmpSourceMethodID', max_length=30,
                                         )  # Field name made lowercase.
    jmpsourcerevisionid = models.CharField(db_column='jmpSourceRevisionID', max_length=15,
                                           )  # Field name made lowercase.
    jmprmaclaimid = models.CharField(db_column='jmpRMAClaimID', max_length=10,
                                     )  # Field name made lowercase.
    jmprmaclaimlineid = models.SmallIntegerField(db_column='jmpRMAClaimLineID')  # Field name made lowercase.
    jmpprojectid = models.CharField(db_column='jmpProjectID', max_length=10,
                                    )  # Field name made lowercase.
    jmpproductionnotesrtf = models.TextField(db_column='jmpProductionNotesRTF', blank=True,
                                             null=True)  # Field name made lowercase.
    jmpproductionnotestext = models.TextField(db_column='jmpProductionNotesText', blank=True,
                                              null=True)  # Field name made lowercase.
    jmpdocuments = models.TextField(db_column='jmpDocuments', blank=True,
                                    null=True)  # Field name made lowercase.
    jmpclosed = models.BooleanField(db_column='jmpClosed')  # Field name made lowercase.
    jmpcloseddate = models.DateTimeField(db_column='jmpClosedDate', blank=True, null=True)  # Field name made lowercase.
    jmpprojectareaid = models.CharField(db_column='jmpProjectAreaID', max_length=15,
                                        )  # Field name made lowercase.
    jmpscrapquantitycompleted = models.DecimalField(db_column='jmpScrapQuantityCompleted', max_digits=15,
                                                    decimal_places=5)  # Field name made lowercase.
    jmpshiporganizationid = models.CharField(db_column='jmpShipOrganizationID', max_length=10,
                                             )  # Field name made lowercase.
    jmpnonconformanceid = models.CharField(db_column='jmpNonConformanceID', max_length=10,
                                           )  # Field name made lowercase.
    jmpshiplocationid = models.CharField(db_column='jmpShipLocationID', max_length=5,
                                         )  # Field name made lowercase.
    jmppartforecastyearid = models.SmallIntegerField(db_column='jmpPartForecastYearID')  # Field name made lowercase.
    jmppartforecastperiodid = models.SmallIntegerField(
        db_column='jmpPartForecastPeriodID')  # Field name made lowercase.
    jmpcreatedby = models.CharField(db_column='jmpCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    jmpcreateddate = models.DateTimeField(db_column='jmpCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    jmpuniqueid = models.AutoField(db_column='jmpUniqueID', unique=True, primary_key=True)
    # jmpuniqueid = models.CharField(db_column='jmpUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    jmpjobpriorityid = models.SmallIntegerField(db_column='jmpJobPriorityID')  # Field name made lowercase.

    # jmprowversion = models.TextField(db_column='jmpRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'Jobs'


class Joboperations(TruncatedModel):
    jmojobid = models.CharField(db_column='jmoJobID', max_length=20,
                                )  # Field name made lowercase.
    jmojobassemblyid = models.IntegerField(db_column='jmoJobAssemblyID')  # Field name made lowercase.
    jmojoboperationid = models.IntegerField(db_column='jmoJobOperationID')  # Field name made lowercase.
    jmooperationtype = models.SmallIntegerField(db_column='jmoOperationType')  # Field name made lowercase.
    jmoaddedoperation = models.BooleanField(db_column='jmoAddedOperation')  # Field name made lowercase.
    jmoprototypeoperation = models.BooleanField(db_column='jmoPrototypeOperation')  # Field name made lowercase.
    jmoplantdepartmentid = models.CharField(db_column='jmoPlantDepartmentID', max_length=5,
                                            )  # Field name made lowercase.
    jmoplantid = models.CharField(db_column='jmoPlantID', max_length=5,
                                  )  # Field name made lowercase.
    jmoworkcenterid = models.CharField(db_column='jmoWorkCenterID', max_length=5,
                                       )  # Field name made lowercase.
    jmoprocessid = models.CharField(db_column='jmoProcessID', max_length=5,
                                    )  # Field name made lowercase.
    jmoprocessshortdescription = models.CharField(db_column='jmoProcessShortDescription', max_length=50,
                                                  )  # Field name made lowercase.
    jmoprocesslongdescriptionrtf = models.TextField(db_column='jmoProcessLongDescriptionRTF',
                                                    blank=True,
                                                    null=True)  # Field name made lowercase.
    jmoprocesslongdescriptiontext = models.TextField(db_column='jmoProcessLongDescriptionText',
                                                     blank=True,
                                                     null=True)  # Field name made lowercase.
    jmoquantityperassembly = models.DecimalField(db_column='jmoQuantityPerAssembly', max_digits=13,
                                                 decimal_places=6)  # Field name made lowercase.
    jmoqueuetime = models.DecimalField(db_column='jmoQueueTime', max_digits=6,
                                       decimal_places=2)  # Field name made lowercase.
    jmosetuphours = models.DecimalField(db_column='jmoSetupHours', max_digits=8,
                                        decimal_places=2)  # Field name made lowercase.
    jmoproductionstandard = models.DecimalField(db_column='jmoProductionStandard', max_digits=10,
                                                decimal_places=4)  # Field name made lowercase.
    jmostandardfactor = models.CharField(db_column='jmoStandardFactor', max_length=2,
                                         )  # Field name made lowercase.
    jmosetuprate = models.DecimalField(db_column='jmoSetupRate', max_digits=8,
                                       decimal_places=2)  # Field name made lowercase.
    jmoproductionrate = models.DecimalField(db_column='jmoProductionRate', max_digits=8,
                                            decimal_places=2)  # Field name made lowercase.
    jmooverheadrate = models.DecimalField(db_column='jmoOverheadRate', max_digits=8,
                                          decimal_places=2)  # Field name made lowercase.
    jmooperationquantity = models.DecimalField(db_column='jmoOperationQuantity', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmoquantitycomplete = models.DecimalField(db_column='jmoQuantityComplete', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    jmosetuppercentcomplete = models.SmallIntegerField(
        db_column='jmoSetupPercentComplete')  # Field name made lowercase.
    jmoactualsetuphours = models.DecimalField(db_column='jmoActualSetupHours', max_digits=8,
                                              decimal_places=2)  # Field name made lowercase.
    jmoactualproductionhours = models.DecimalField(db_column='jmoActualProductionHours', max_digits=8,
                                                   decimal_places=2)  # Field name made lowercase.
    jmoquantitytoinspect = models.DecimalField(db_column='jmoQuantityToInspect', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmoscrapquantityreceived = models.DecimalField(db_column='jmoScrapQuantityReceived', max_digits=15,
                                                   decimal_places=5)  # Field name made lowercase.
    jmoquantitytoreturn = models.DecimalField(db_column='jmoQuantityToReturn', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    jmomovetime = models.DecimalField(db_column='jmoMoveTime', max_digits=6,
                                      decimal_places=2)  # Field name made lowercase.
    jmosetupcomplete = models.BooleanField(db_column='jmoSetupComplete')  # Field name made lowercase.
    jmoproductioncomplete = models.BooleanField(db_column='jmoProductionComplete')  # Field name made lowercase.
    jmooverlapsourcelink = models.SmallIntegerField(db_column='jmoOverlapSourceLink')  # Field name made lowercase.
    jmooverlapdestinationlink = models.SmallIntegerField(
        db_column='jmoOverlapDestinationLink')  # Field name made lowercase.
    jmooverlap = models.SmallIntegerField(db_column='jmoOverlap')  # Field name made lowercase.
    jmooverlapoperationid = models.IntegerField(db_column='jmoOverlapOperationID')  # Field name made lowercase.
    jmooverlapoffsettime = models.DecimalField(db_column='jmoOverlapOffsetTime', max_digits=8,
                                               decimal_places=2)  # Field name made lowercase.
    jmomachinetype = models.SmallIntegerField(db_column='jmoMachineType')  # Field name made lowercase.
    jmoworkcentermachineid = models.SmallIntegerField(db_column='jmoWorkCenterMachineID')  # Field name made lowercase.
    jmopartid = models.CharField(db_column='jmoPartID', max_length=30,
                                 )  # Field name made lowercase.
    jmopartrevisionid = models.CharField(db_column='jmoPartRevisionID', max_length=15,
                                         )  # Field name made lowercase.
    jmopartwarehouselocationid = models.CharField(db_column='jmoPartWarehouseLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    jmopartbinid = models.CharField(db_column='jmoPartBinID', max_length=15,
                                    )  # Field name made lowercase.
    jmounitofmeasure = models.CharField(db_column='jmoUnitOfMeasure', max_length=2,
                                        )  # Field name made lowercase.
    jmosupplierorganizationid = models.CharField(db_column='jmoSupplierOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    jmopurchaselocationid = models.CharField(db_column='jmoPurchaseLocationID', max_length=5,
                                             )  # Field name made lowercase.
    jmofirm = models.BooleanField(db_column='jmoFirm')  # Field name made lowercase.
    jmopurchaseorderid = models.CharField(db_column='jmoPurchaseOrderID', max_length=10,
                                          )  # Field name made lowercase.
    jmoestimatedunitcost = models.DecimalField(db_column='jmoEstimatedUnitCost', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmominimumcharge = models.DecimalField(db_column='jmoMinimumCharge', max_digits=8,
                                           decimal_places=2)  # Field name made lowercase.
    jmosetupcharge = models.DecimalField(db_column='jmoSetupCharge', max_digits=9,
                                         decimal_places=2)  # Field name made lowercase.
    jmocalculatedunitcost = models.DecimalField(db_column='jmoCalculatedUnitCost', max_digits=15,
                                                decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak1 = models.DecimalField(db_column='jmoQuantityBreak1', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost1 = models.DecimalField(db_column='jmoUnitCost1', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak2 = models.DecimalField(db_column='jmoQuantityBreak2', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost2 = models.DecimalField(db_column='jmoUnitCost2', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak3 = models.DecimalField(db_column='jmoQuantityBreak3', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost3 = models.DecimalField(db_column='jmoUnitCost3', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak4 = models.DecimalField(db_column='jmoQuantityBreak4', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost4 = models.DecimalField(db_column='jmoUnitCost4', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak5 = models.DecimalField(db_column='jmoQuantityBreak5', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost5 = models.DecimalField(db_column='jmoUnitCost5', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak6 = models.DecimalField(db_column='jmoQuantityBreak6', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost6 = models.DecimalField(db_column='jmoUnitCost6', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak7 = models.DecimalField(db_column='jmoQuantityBreak7', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost7 = models.DecimalField(db_column='jmoUnitCost7', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak8 = models.DecimalField(db_column='jmoQuantityBreak8', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost8 = models.DecimalField(db_column='jmoUnitCost8', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmoquantitybreak9 = models.DecimalField(db_column='jmoQuantityBreak9', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmounitcost9 = models.DecimalField(db_column='jmoUnitCost9', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmostartdate = models.DateTimeField(db_column='jmoStartDate', blank=True, null=True)  # Field name made lowercase.
    jmoduedate = models.DateTimeField(db_column='jmoDueDate', blank=True, null=True)  # Field name made lowercase.
    jmostarthour = models.DecimalField(db_column='jmoStartHour', max_digits=5,
                                       decimal_places=2)  # Field name made lowercase.
    jmoduehour = models.DecimalField(db_column='jmoDueHour', max_digits=5,
                                     decimal_places=2)  # Field name made lowercase.
    jmoestimatedproductionhours = models.DecimalField(db_column='jmoEstimatedProductionHours', max_digits=8,
                                                      decimal_places=2)  # Field name made lowercase.
    jmocompletedsetuphours = models.DecimalField(db_column='jmoCompletedSetupHours', max_digits=8,
                                                 decimal_places=2)  # Field name made lowercase.
    jmocompletedproductionhours = models.DecimalField(db_column='jmoCompletedProductionHours', max_digits=8,
                                                      decimal_places=2)  # Field name made lowercase.
    jmodocuments = models.TextField(db_column='jmoDocuments', blank=True,
                                    null=True)  # Field name made lowercase.
    jmosfemessagertf = models.TextField(db_column='jmoSFEMessageRTF',
                                        blank=True, null=True)  # Field name made lowercase.
    jmosfemessagetext = models.TextField(db_column='jmoSFEMessageText',
                                         blank=True, null=True)  # Field name made lowercase.
    jmoclosed = models.BooleanField(db_column='jmoClosed')  # Field name made lowercase.
    jmoinspectioncomplete = models.BooleanField(db_column='jmoInspectionComplete')  # Field name made lowercase.
    jmoinspectionstatus = models.SmallIntegerField(db_column='jmoInspectionStatus')  # Field name made lowercase.
    jmoinspectiontype = models.SmallIntegerField(db_column='jmoInspectionType')  # Field name made lowercase.
    jmorfqid = models.CharField(db_column='jmoRFQID', max_length=10,
                                )  # Field name made lowercase.
    jmomachinestoschedule = models.SmallIntegerField(db_column='jmoMachinesToSchedule')  # Field name made lowercase.
    jmocreatedby = models.CharField(db_column='jmoCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    jmocreateddate = models.DateTimeField(db_column='jmoCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    jmouniqueid = models.AutoField(db_column='jmoUniqueID', unique=True, primary_key=True)

    # jmouniqueid = models.CharField(db_column='jmoUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    # jmorowversion = models.TextField(db_column='jmoRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'JobOperations'
        unique_together = (('jmojobid', 'jmojobassemblyid', 'jmojoboperationid'),)


class Jobassemblies(TruncatedModel):
    jmajobid = models.CharField(db_column='jmaJobID', max_length=20,
                                )  # Field name made lowercase.
    jmajobassemblyid = models.IntegerField(db_column='jmaJobAssemblyID')  # Field name made lowercase.
    jmalevel = models.SmallIntegerField(db_column='jmaLevel')  # Field name made lowercase.
    jmaparentassemblyid = models.IntegerField(db_column='jmaParentAssemblyID')  # Field name made lowercase.
    jmasourcemethodid = models.CharField(db_column='jmaSourceMethodID', max_length=30,
                                         )  # Field name made lowercase.
    jmasourcerevisionid = models.CharField(db_column='jmaSourceRevisionID', max_length=15,
                                           )  # Field name made lowercase.
    jmapartid = models.CharField(db_column='jmaPartID', max_length=30,
                                 )  # Field name made lowercase.
    jmapartrevisionid = models.CharField(db_column='jmaPartRevisionID', max_length=15,
                                         )  # Field name made lowercase.
    jmapartwarehouselocationid = models.CharField(db_column='jmaPartWareHouseLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    jmapartbinid = models.CharField(db_column='jmaPartBinID', max_length=15,
                                    )  # Field name made lowercase.
    jmaunitofmeasure = models.CharField(db_column='jmaUnitOfMeasure', max_length=2,
                                        )  # Field name made lowercase.
    jmapartshortdescription = models.CharField(db_column='jmaPartShortDescription', max_length=50,
                                               )  # Field name made lowercase.
    jmapartlongdescriptionrtf = models.TextField(db_column='jmaPartLongDescriptionRTF',
                                                 blank=True,
                                                 null=True)  # Field name made lowercase.
    jmapartlongdescriptiontext = models.TextField(db_column='jmaPartLongDescriptionText',
                                                  blank=True,
                                                  null=True)  # Field name made lowercase.
    jmaquantityperparent = models.DecimalField(db_column='jmaQuantityPerParent', max_digits=12,
                                               decimal_places=5)  # Field name made lowercase.
    jmaestimatedunitcost = models.DecimalField(db_column='jmaEstimatedUnitCost', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmaorderquantity = models.DecimalField(db_column='jmaOrderQuantity', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    jmainventoryquantity = models.DecimalField(db_column='jmaInventoryQuantity', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmascrapquantity = models.DecimalField(db_column='jmaScrapQuantity', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    jmareworkquantity = models.DecimalField(db_column='jmaReworkQuantity', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmaquantitytoinspect = models.DecimalField(db_column='jmaQuantityToInspect', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmaquantitytoreturn = models.DecimalField(db_column='jmaQuantityToReturn', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    jmascheduledstarthour = models.DecimalField(db_column='jmaScheduledStartHour', max_digits=5,
                                                decimal_places=2)  # Field name made lowercase.
    jmaquantityreceivedtoinventory = models.DecimalField(db_column='jmaQuantityReceivedToInventory', max_digits=15,
                                                         decimal_places=5)  # Field name made lowercase.
    jmareceivedcomplete = models.BooleanField(db_column='jmaReceivedComplete')  # Field name made lowercase.
    jmascheduledduehour = models.DecimalField(db_column='jmaScheduledDueHour', max_digits=5,
                                              decimal_places=2)  # Field name made lowercase.
    jmaproductionquantity = models.DecimalField(db_column='jmaProductionQuantity', max_digits=15,
                                                decimal_places=5)  # Field name made lowercase.
    jmaquantitytomake = models.DecimalField(db_column='jmaQuantityToMake', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmaquantitytopull = models.DecimalField(db_column='jmaQuantityToPull', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmaquantityissued = models.DecimalField(db_column='jmaQuantityIssued', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmapullallfromstock = models.BooleanField(db_column='jmaPullAllFromStock')  # Field name made lowercase.
    jmaissuedcomplete = models.BooleanField(db_column='jmaIssuedComplete')  # Field name made lowercase.
    jmaproductionnotesrtf = models.TextField(db_column='jmaProductionNotesRTF',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    jmaproductionnotestext = models.TextField(db_column='jmaProductionNotesText',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    jmascheduledstartdate = models.DateTimeField(db_column='jmaScheduledStartDate', blank=True,
                                                 null=True)  # Field name made lowercase.
    jmascheduledduedate = models.DateTimeField(db_column='jmaScheduledDueDate', blank=True,
                                               null=True)  # Field name made lowercase.
    jmaoverlapsourceoperationid = models.IntegerField(
        db_column='jmaOverlapSourceOperationID')  # Field name made lowercase.
    jmaassemblyoverlap = models.SmallIntegerField(db_column='jmaAssemblyOverlap')  # Field name made lowercase.
    jmaoverlapsourcelink = models.SmallIntegerField(db_column='jmaOverlapSourceLink')  # Field name made lowercase.
    jmaoverlapdestinationlink = models.SmallIntegerField(
        db_column='jmaOverlapDestinationLink')  # Field name made lowercase.
    jmaoverlapoffsettime = models.DecimalField(db_column='jmaOverlapOffsetTime', max_digits=8,
                                               decimal_places=2)  # Field name made lowercase.
    jmaoverlapoperationid = models.IntegerField(db_column='jmaOverlapOperationID')  # Field name made lowercase.
    jmaoverlaptype = models.SmallIntegerField(db_column='jmaOverlapType')  # Field name made lowercase.
    jmadocuments = models.TextField(db_column='jmaDocuments', blank=True,
                                    null=True)  # Field name made lowercase.
    jmaproductioncomplete = models.BooleanField(db_column='jmaProductionComplete')  # Field name made lowercase.
    jmaquantitycompleted = models.DecimalField(db_column='jmaQuantityCompleted', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmacompleteddate = models.DateTimeField(db_column='jmaCompletedDate', blank=True,
                                            null=True)  # Field name made lowercase.
    jmareworkdate = models.DateTimeField(db_column='jmaReworkDate', blank=True, null=True)  # Field name made lowercase.
    jmaclosed = models.BooleanField(db_column='jmaClosed')  # Field name made lowercase.
    jmascrapquantitycompleted = models.DecimalField(db_column='jmaScrapQuantityCompleted', max_digits=15,
                                                    decimal_places=5)  # Field name made lowercase.
    jmacreatedby = models.CharField(db_column='jmaCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    jmacreateddate = models.DateTimeField(db_column='jmaCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    jmauniqueid = models.AutoField(db_column='jmaUniqueID', unique=True, primary_key=True)

    # jmauniqueid = models.CharField(db_column='jmaUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    # jmarowversion = models.TextField(db_column='jmaRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'JobAssemblies'
        unique_together = (('jmajobid', 'jmajobassemblyid'),)


class Jobmaterials(TruncatedModel):
    jmmjobid = models.CharField(db_column='jmmJobID', max_length=20,
                                )  # Field name made lowercase.
    jmmjobassemblyid = models.IntegerField(db_column='jmmJobAssemblyID')  # Field name made lowercase.
    jmmjobmaterialid = models.IntegerField(db_column='jmmJobMaterialID')  # Field name made lowercase.
    jmmpartid = models.CharField(db_column='jmmPartID', max_length=30,
                                 )  # Field name made lowercase.
    jmmpartrevisionid = models.CharField(db_column='jmmPartRevisionID', max_length=15,
                                         )  # Field name made lowercase.
    jmmpartwarehouselocationid = models.CharField(db_column='jmmPartWarehouseLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    jmmpartbinid = models.CharField(db_column='jmmPartBinID', max_length=15,
                                    )  # Field name made lowercase.
    jmmunitofmeasure = models.CharField(db_column='jmmUnitOfMeasure', max_length=2,
                                        )  # Field name made lowercase.
    jmmpartshortdescription = models.CharField(db_column='jmmPartShortDescription', max_length=50,
                                               )  # Field name made lowercase.
    jmmpartlongdescriptionrtf = models.TextField(db_column='jmmPartLongDescriptionRTF',
                                                 blank=True,
                                                 null=True)  # Field name made lowercase.
    jmmpartlongdescriptiontext = models.TextField(db_column='jmmPartLongDescriptionText',
                                                  blank=True,
                                                  null=True)  # Field name made lowercase.
    jmmquantityperassembly = models.DecimalField(db_column='jmmQuantityPerAssembly', max_digits=13,
                                                 decimal_places=6)  # Field name made lowercase.
    jmmscrappercent = models.DecimalField(db_column='jmmScrapPercent', max_digits=6,
                                          decimal_places=2)  # Field name made lowercase.
    jmmscrapquantity = models.DecimalField(db_column='jmmScrapQuantity', max_digits=15,
                                           decimal_places=5)  # Field name made lowercase.
    jmmestimatedquantity = models.DecimalField(db_column='jmmEstimatedQuantity', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmmestimatedunitcost = models.DecimalField(db_column='jmmEstimatedUnitCost', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmmminimumcharge = models.DecimalField(db_column='jmmMinimumCharge', max_digits=8,
                                           decimal_places=2)  # Field name made lowercase.
    jmmcalculatedunitcost = models.DecimalField(db_column='jmmCalculatedUnitCost', max_digits=15,
                                                decimal_places=5)  # Field name made lowercase.
    jmmkitpart = models.BooleanField(db_column='jmmKitPart')  # Field name made lowercase.
    jmmquantitybreak1 = models.DecimalField(db_column='jmmQuantityBreak1', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost1 = models.DecimalField(db_column='jmmUnitCost1', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak2 = models.DecimalField(db_column='jmmQuantityBreak2', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost2 = models.DecimalField(db_column='jmmUnitCost2', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak3 = models.DecimalField(db_column='jmmQuantityBreak3', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost3 = models.DecimalField(db_column='jmmUnitCost3', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak4 = models.DecimalField(db_column='jmmQuantityBreak4', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost4 = models.DecimalField(db_column='jmmUnitCost4', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak5 = models.DecimalField(db_column='jmmQuantityBreak5', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost5 = models.DecimalField(db_column='jmmUnitCost5', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak6 = models.DecimalField(db_column='jmmQuantityBreak6', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost6 = models.DecimalField(db_column='jmmUnitCost6', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak7 = models.DecimalField(db_column='jmmQuantityBreak7', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost7 = models.DecimalField(db_column='jmmUnitCost7', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak8 = models.DecimalField(db_column='jmmQuantityBreak8', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost8 = models.DecimalField(db_column='jmmUnitCost8', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmquantitybreak9 = models.DecimalField(db_column='jmmQuantityBreak9', max_digits=15,
                                            decimal_places=5)  # Field name made lowercase.
    jmmunitcost9 = models.DecimalField(db_column='jmmUnitCost9', max_digits=15,
                                       decimal_places=5)  # Field name made lowercase.
    jmmsupplierorganizationid = models.CharField(db_column='jmmSupplierOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    jmmpurchaselocationid = models.CharField(db_column='jmmPurchaseLocationID', max_length=5,
                                             )  # Field name made lowercase.
    jmmfirm = models.BooleanField(db_column='jmmFirm')  # Field name made lowercase.
    jmmpurchaseorderid = models.CharField(db_column='jmmPurchaseOrderID', max_length=10,
                                          )  # Field name made lowercase.
    jmmleadtime = models.SmallIntegerField(db_column='jmmLeadTime')  # Field name made lowercase.
    jmmdueindate = models.DateTimeField(db_column='jmmDueInDate', blank=True, null=True)  # Field name made lowercase.
    jmmorderbydate = models.DateTimeField(db_column='jmmOrderByDate', blank=True,
                                          null=True)  # Field name made lowercase.
    jmmquantityallocated = models.DecimalField(db_column='jmmQuantityAllocated', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmmquantitytoreturn = models.DecimalField(db_column='jmmQuantityToReturn', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    jmmrequireddate = models.DateTimeField(db_column='jmmRequiredDate', blank=True,
                                           null=True)  # Field name made lowercase.
    jmmquantityreceived = models.DecimalField(db_column='jmmQuantityReceived', max_digits=15,
                                              decimal_places=5)  # Field name made lowercase.
    jmmscrapquantityreceived = models.DecimalField(db_column='jmmScrapQuantityReceived', max_digits=15,
                                                   decimal_places=5)  # Field name made lowercase.
    jmmreceivedcomplete = models.BooleanField(db_column='jmmReceivedComplete')  # Field name made lowercase.
    jmmrelatedjoboperationid = models.IntegerField(db_column='jmmRelatedJobOperationID')  # Field name made lowercase.
    jmmbackflush = models.BooleanField(db_column='jmmBackflush')  # Field name made lowercase.
    jmmclosed = models.BooleanField(db_column='jmmClosed')  # Field name made lowercase.
    jmmquantitytoinspect = models.DecimalField(db_column='jmmQuantityToInspect', max_digits=15,
                                               decimal_places=5)  # Field name made lowercase.
    jmmrfqid = models.CharField(db_column='jmmRFQID', max_length=10,
                                )  # Field name made lowercase.
    jmmdocuments = models.TextField(db_column='jmmDocuments', blank=True,
                                    null=True)  # Field name made lowercase.
    jmmleadtime1 = models.SmallIntegerField(db_column='jmmLeadTime1')  # Field name made lowercase.
    jmmleadtime2 = models.SmallIntegerField(db_column='jmmLeadTime2')  # Field name made lowercase.
    jmmleadtime3 = models.SmallIntegerField(db_column='jmmLeadTime3')  # Field name made lowercase.
    jmmleadtime4 = models.SmallIntegerField(db_column='jmmLeadTime4')  # Field name made lowercase.
    jmmleadtime5 = models.SmallIntegerField(db_column='jmmLeadTime5')  # Field name made lowercase.
    jmmleadtime6 = models.SmallIntegerField(db_column='jmmLeadTime6')  # Field name made lowercase.
    jmmleadtime7 = models.SmallIntegerField(db_column='jmmLeadTime7')  # Field name made lowercase.
    jmmleadtime8 = models.SmallIntegerField(db_column='jmmLeadTime8')  # Field name made lowercase.
    jmmleadtime9 = models.SmallIntegerField(db_column='jmmLeadTime9')  # Field name made lowercase.
    jmmcostoverride = models.BooleanField(db_column='jmmCostOverride')  # Field name made lowercase.
    jmmpurchasetojobquantity = models.DecimalField(db_column='jmmPurchaseToJobQuantity', max_digits=15,
                                                   decimal_places=5)  # Field name made lowercase.
    jmmpullfromstockquantity = models.DecimalField(db_column='jmmPullFromStockQuantity', max_digits=15,
                                                   decimal_places=5)  # Field name made lowercase.
    jmmpullallfromstock = models.BooleanField(db_column='jmmPullAllFromStock')  # Field name made lowercase.
    jmmcreatedby = models.CharField(db_column='jmmCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    jmmcreateddate = models.DateTimeField(db_column='jmmCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    jmmuniqueid = models.AutoField(db_column='jmmUniqueID', unique=True, primary_key=True)

    # jmmuniqueid = models.CharField(db_column='jmmUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    # jmmrowversion = models.TextField(db_column='jmmRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'JobMaterials'
        unique_together = (('jmmjobid', 'jmmjobassemblyid', 'jmmjobmaterialid'),)


class Organizations(TruncatedModel):
    cmoorganizationid = models.CharField(db_column='cmoOrganizationID', unique=True,
                                         max_length=10)  # Field name made lowercase.
    cmoname = models.CharField(db_column='cmoName', max_length=50,
                               )  # Field name made lowercase.
    cmoaddressline1 = models.CharField(db_column='cmoAddressLine1', max_length=50,
                                       )  # Field name made lowercase.
    cmoaddressline2 = models.CharField(db_column='cmoAddressLine2', max_length=50,
                                       )  # Field name made lowercase.
    cmoaddressline3 = models.CharField(db_column='cmoAddressLine3', max_length=50,
                                       )  # Field name made lowercase.
    cmocity = models.CharField(db_column='cmoCity', max_length=30,
                               )  # Field name made lowercase.
    cmocounty = models.CharField(db_column='cmoCounty', max_length=30,
                                 )  # Field name made lowercase.
    cmostate = models.CharField(db_column='cmoState', max_length=3,
                                )  # Field name made lowercase.
    cmopostcode = models.CharField(db_column='cmoPostCode', max_length=10,
                                   )  # Field name made lowercase.
    cmocountry = models.CharField(db_column='cmoCountry', max_length=20,
                                  )  # Field name made lowercase.
    cmophonenumber = models.CharField(db_column='cmoPhoneNumber', max_length=20,
                                      )  # Field name made lowercase.
    cmoalternatephonenumber = models.CharField(db_column='cmoAlternatePhoneNumber', max_length=20,
                                               )  # Field name made lowercase.
    cmofaxnumber = models.CharField(db_column='cmoFaxNumber', max_length=20,
                                    )  # Field name made lowercase.
    cmoemailaddress = models.TextField(db_column='cmoEMailAddress',
                                       blank=True, null=True)  # Field name made lowercase.
    cmowebaddress = models.CharField(db_column='cmoWebAddress', max_length=50,
                                     )  # Field name made lowercase.
    cmoorganizationaccountid = models.CharField(db_column='cmoOrganizationAccountID', max_length=20,
                                                )  # Field name made lowercase.
    cmoarinvoicecontactid = models.CharField(db_column='cmoARInvoiceContactID', max_length=5,
                                             )  # Field name made lowercase.
    cmoquotecontactid = models.CharField(db_column='cmoQuoteContactID', max_length=5,
                                         )  # Field name made lowercase.
    cmoshipcontactid = models.CharField(db_column='cmoShipContactID', max_length=5,
                                        )  # Field name made lowercase.
    cmopurchasecontactid = models.CharField(db_column='cmoPurchaseContactID', max_length=5,
                                            )  # Field name made lowercase.
    cmoestablisheddate = models.DateTimeField(db_column='cmoEstablishedDate', blank=True, null=True,
                                              auto_now=True)  # Field name made lowercase.
    cmoapinvoicecontactid = models.CharField(db_column='cmoAPInvoiceContactID', max_length=5,
                                             )  # Field name made lowercase.
    cmoprintstatement = models.BooleanField(db_column='cmoPrintStatement')  # Field name made lowercase.
    cmoemployeecount = models.IntegerField(db_column='cmoEmployeeCount')  # Field name made lowercase.
    cmofinancecompany = models.BooleanField(db_column='cmoFinanceCompany')  # Field name made lowercase.
    cmocompetitor = models.BooleanField(db_column='cmoCompetitor')  # Field name made lowercase.
    cmolongdescriptionrtf = models.TextField(db_column='cmoLongDescriptionRTF',
                                             blank=True,
                                             null=True)  # Field name made lowercase.
    cmolongdescriptiontext = models.TextField(db_column='cmoLongDescriptionText',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    cmocustomerstatus = models.SmallIntegerField(db_column='cmoCustomerStatus')  # Field name made lowercase.
    cmocustomerprospectdate = models.DateTimeField(db_column='cmoCustomerProspectDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    cmocustomeractivedate = models.DateTimeField(db_column='cmoCustomerActiveDate', blank=True, null=True,
                                                 auto_now=True)  # Field name made lowercase.
    cmocustomerinactivedate = models.DateTimeField(db_column='cmoCustomerInactiveDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    cmosupplierstatus = models.SmallIntegerField(db_column='cmoSupplierStatus')  # Field name made lowercase.
    cmosupplierprospectdate = models.DateTimeField(db_column='cmoSupplierProspectDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    cmosupplieractivedate = models.DateTimeField(db_column='cmoSupplierActiveDate', blank=True,
                                                 null=True)  # Field name made lowercase.
    cmosupplierinactivedate = models.DateTimeField(db_column='cmoSupplierInactiveDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    cmorequires1099 = models.BooleanField(db_column='cmoRequires1099')  # Field name made lowercase.
    cmosupplierpaymenttermid = models.CharField(db_column='cmoSupplierPaymentTermID', max_length=5,
                                                )  # Field name made lowercase.
    cmosuppliershippingmethodid = models.CharField(db_column='cmoSupplierShippingMethodID', max_length=5,
                                                   )  # Field name made lowercase.
    cmosuppliertaxable = models.BooleanField(db_column='cmoSupplierTaxable')  # Field name made lowercase.
    cmosuppliertaxcodeid = models.CharField(db_column='cmoSupplierTaxCodeID', max_length=5,
                                            )  # Field name made lowercase.
    cmosuppliersecondtaxcodeid = models.CharField(db_column='cmoSupplierSecondTaxCodeID', max_length=5,
                                                  )  # Field name made lowercase.
    cmoaccountmanageremployeeid = models.CharField(db_column='cmoAccountManagerEmployeeID', max_length=10,
                                                   )  # Field name made lowercase.
    cmocustomergroupid = models.CharField(db_column='cmoCustomerGroupID', max_length=5,
                                          )  # Field name made lowercase.
    cmocustomertaxable = models.BooleanField(db_column='cmoCustomerTaxable')  # Field name made lowercase.
    cmocustomertaxcodeid = models.CharField(db_column='cmoCustomerTaxCodeID', max_length=5,
                                            )  # Field name made lowercase.
    cmocustomersecondtaxcodeid = models.CharField(db_column='cmoCustomerSecondTaxCodeID', max_length=5,
                                                  )  # Field name made lowercase.
    cmocustomerpaymenttermsid = models.CharField(db_column='cmoCustomerPaymentTermsID', max_length=5,
                                                 )  # Field name made lowercase.
    cmocalculatefinancecharges = models.BooleanField(
        db_column='cmoCalculateFinanceCharges')  # Field name made lowercase.
    cmoincludefreightinprice = models.BooleanField(db_column='cmoIncludeFreightInPrice')  # Field name made lowercase.
    cmocurrencyrateid = models.CharField(db_column='cmoCurrencyRateID', max_length=5,
                                         )  # Field name made lowercase.
    cmocredithold = models.BooleanField(db_column='cmoCreditHold')  # Field name made lowercase.
    cmocustomercreditlimit = models.DecimalField(db_column='cmoCustomerCreditLimit', max_digits=19,
                                                 decimal_places=4)  # Field name made lowercase.
    cmodefaultquotelocationid = models.CharField(db_column='cmoDefaultQuoteLocationID', max_length=5,
                                                 )  # Field name made lowercase.
    cmodefaultshiplocationid = models.CharField(db_column='cmoDefaultShipLocationID', max_length=5,
                                                )  # Field name made lowercase.
    cmodefaultarinvoicelocationid = models.CharField(db_column='cmoDefaultARInvoiceLocationID', max_length=5,
                                                     )  # Field name made lowercase.
    cmodefaultpurchaselocationid = models.CharField(db_column='cmoDefaultPurchaseLocationID', max_length=5,
                                                    )  # Field name made lowercase.
    cmodefaultapinvoicelocationid = models.CharField(db_column='cmoDefaultAPInvoiceLocationID', max_length=5,
                                                     )  # Field name made lowercase.
    cmodropshiporganizationid = models.CharField(db_column='cmoDropShipOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    cmodropshiplocationid = models.CharField(db_column='cmoDropShipLocationID', max_length=5,
                                             )  # Field name made lowercase.
    cmoeftdescription = models.CharField(db_column='cmoEFTDescription', max_length=20,
                                         )  # Field name made lowercase.
    cmotaxexemptnumber = models.CharField(db_column='cmoTaxExemptNumber', max_length=16,
                                          )  # Field name made lowercase.
    cmodirectpayment = models.BooleanField(db_column='cmoDirectPayment')  # Field name made lowercase.
    cmofederalid = models.CharField(db_column='cmoFederalID', max_length=20,
                                    )  # Field name made lowercase.
    cmobankinitials = models.CharField(db_column='cmoBankInitials', max_length=3,
                                       )  # Field name made lowercase.
    cmobsbnumber = models.CharField(db_column='cmoBSBNumber', max_length=10,
                                    )  # Field name made lowercase.
    cmobankaccountname = models.CharField(db_column='cmoBankAccountName', max_length=50,
                                          )  # Field name made lowercase.
    cmobankaccountnumber = models.CharField(db_column='cmoBankAccountNumber', max_length=24,
                                            )  # Field name made lowercase.
    cmonontaxreasonid = models.CharField(db_column='cmoNonTaxReasonID', max_length=5,
                                         )  # Field name made lowercase.
    cmocustomershippingmethodid = models.CharField(db_column='cmoCustomerShippingMethodID', max_length=5,
                                                   )  # Field name made lowercase.
    cmocustomershippaymenttypeid = models.CharField(db_column='cmoCustomerShipPaymentTypeID', max_length=5,
                                                    )  # Field name made lowercase.
    cmoarinvoicepershipmentline = models.BooleanField(
        db_column='cmoARInvoicePerShipmentLine')  # Field name made lowercase.
    cmocreatedfromweb = models.BooleanField(db_column='cmoCreatedFromWeb')  # Field name made lowercase.
    cmoresellerstatus = models.SmallIntegerField(db_column='cmoResellerStatus')  # Field name made lowercase.
    cmoresellerprospectdate = models.DateTimeField(db_column='cmoResellerProspectDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    cmoreselleractivedate = models.DateTimeField(db_column='cmoResellerActiveDate', blank=True,
                                                 null=True)  # Field name made lowercase.
    cmoresellerinactivedate = models.DateTimeField(db_column='cmoResellerInactiveDate', blank=True,
                                                   null=True)  # Field name made lowercase.
    cmoresellerorganizationid = models.CharField(db_column='cmoResellerOrganizationID', max_length=10,
                                                 )  # Field name made lowercase.
    cmoresellerlocationid = models.CharField(db_column='cmoResellerLocationID', max_length=5,
                                             )  # Field name made lowercase.
    cmoresellercontactid = models.CharField(db_column='cmoResellerContactID', max_length=5,
                                            )  # Field name made lowercase.
    cmoresellercommissionrate = models.DecimalField(db_column='cmoResellerCommissionRate', max_digits=5,
                                                    decimal_places=2)  # Field name made lowercase.
    cmorequiresinspection = models.BooleanField(db_column='cmoRequiresInspection')  # Field name made lowercase.
    cmoupsacctnumber = models.CharField(db_column='cmoUPSAcctNumber', max_length=6,
                                        )  # Field name made lowercase.
    cmoupsbillingoption = models.CharField(db_column='cmoUPSBillingOption', max_length=20,
                                           )  # Field name made lowercase.
    cmoresidentialaddress = models.BooleanField(db_column='cmoResidentialAddress')  # Field name made lowercase.
    cmoattachmentfilefolder = models.TextField(db_column='cmoAttachmentFileFolder',
                                               blank=True,
                                               null=True)  # Field name made lowercase.
    cmosupplieraccredited = models.BooleanField(db_column='cmoSupplierAccredited')  # Field name made lowercase.
    cmosupplieraccrediteddate = models.DateTimeField(db_column='cmoSupplierAccreditedDate', blank=True,
                                                     null=True)  # Field name made lowercase.
    cmosupplierratingid = models.CharField(db_column='cmoSupplierRatingID', max_length=5,
                                           )  # Field name made lowercase.
    cmobankaccounttype = models.CharField(db_column='cmoBankAccountType', max_length=2,
                                          )  # Field name made lowercase.
    cmofreeonboarddescription = models.CharField(db_column='cmoFreeOnBoardDescription', max_length=15,
                                                 )  # Field name made lowercase.
    cmocreatedby = models.CharField(db_column='cmoCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    cmocreateddate = models.DateTimeField(db_column='cmoCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    cmouniqueid = models.AutoField(db_column='cmoUniqueID', unique=True, primary_key=True)
    # cmouniqueid = models.CharField(db_column='cmoUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    cmocountrycode = models.CharField(db_column='cmoCountryCode', max_length=2,
                                      )  # Field name made lowercase.
    cmohdattachmentfilepath = models.TextField(db_column='cmoHDAttachmentFilePath',
                                               blank=True,
                                               null=True)  # Field name made lowercase.
    cmoapincludetaxinretention = models.BooleanField(
        db_column='cmoAPIncludeTaxInRetention')  # Field name made lowercase.
    cmoarincludetaxinretention = models.BooleanField(
        db_column='cmoARIncludeTaxInRetention')  # Field name made lowercase.
    cmoups3rdpartyorganizationid = models.CharField(db_column='cmoUPS3rdPartyOrganizationID', max_length=10,
                                                    )  # Field name made lowercase.
    cmoups3rdpartylocationid = models.CharField(db_column='cmoUPS3rdPartyLocationID', max_length=5,
                                                )  # Field name made lowercase.
    cmoform1099box = models.SmallIntegerField(db_column='cmoForm1099Box')  # Field name made lowercase.
    cmoeftcode = models.CharField(db_column='cmoEFTCode', max_length=12,
                                  )  # Field name made lowercase.
    cmoeftparticulars = models.CharField(db_column='cmoEFTParticulars', max_length=12,
                                         )  # Field name made lowercase.
    cmoavalarausecodes = models.CharField(db_column='cmoAvalaraUseCodes', max_length=1,
                                          )  # Field name made lowercase.
    cmoavalaraaddressvalidated = models.BooleanField(
        db_column='cmoAvalaraAddressValidated')  # Field name made lowercase.
    cmocontractor = models.BooleanField(db_column='cmoContractor')  # Field name made lowercase.
    cmotaxreportable = models.BooleanField(db_column='cmoTaxReportable')  # Field name made lowercase.
    cmolastname = models.CharField(db_column='cmoLastName', max_length=30,
                                   )  # Field name made lowercase.
    cmofirstgivenname = models.CharField(db_column='cmoFirstGivenName', max_length=15,
                                         )  # Field name made lowercase.
    cmosecondgivenname = models.CharField(db_column='cmoSecondGivenName', max_length=15,
                                          )  # Field name made lowercase.
    cmotradingname = models.TextField(db_column='cmoTradingName',
                                      blank=True, null=True)  # Field name made lowercase.
    cmocreatedfrommobile = models.BooleanField(db_column='cmoCreatedFromMobile')  # Field name made lowercase.
    cmoignoreavalara = models.BooleanField(db_column='cmoIgnoreAvalara')  # Field name made lowercase.
    cmosuperfund = models.BooleanField(db_column='cmoSuperFund')  # Field name made lowercase.
    cmosuperfundname = models.CharField(db_column='cmoSuperFundName', max_length=60,
                                        )  # Field name made lowercase.
    cmosuperfundemployerid = models.CharField(db_column='cmoSuperFundEmployerID', max_length=16,
                                              )  # Field name made lowercase.
    cmoupsvalidated = models.BooleanField(db_column='cmoUPSValidated')  # Field name made lowercase.
    cmobarecostofduty = models.BooleanField(db_column='cmoBareCostOfDuty')  # Field name made lowercase.
    cmobaretransportationcost = models.BooleanField(db_column='cmoBareTransportationCost')  # Field name made lowercase.
    cmoediintegrated = models.BooleanField(db_column='cmoEDIIntegrated')  # Field name made lowercase.
    cmofedexaccountnumber = models.CharField(db_column='cmoFedExAccountNumber', max_length=15,
                                             )  # Field name made lowercase.
    cmofedex3rdpartyorganizationid = models.CharField(db_column='cmoFedEx3rdPartyOrganizationID', max_length=10,
                                                      )  # Field name made lowercase.
    cmofedex3rdpartylocationid = models.CharField(db_column='cmoFedEx3rdPartyLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    cmofedexbillingoption = models.CharField(db_column='cmoFedExBillingOption', max_length=20,
                                             )  # Field name made lowercase.
    cmoiban = models.CharField(db_column='cmoIBAN', max_length=50,
                               )  # Field name made lowercase.
    cmobic = models.CharField(db_column='cmoBIC', max_length=50,
                              )  # Field name made lowercase.
    cmoupswsbillingoption = models.CharField(db_column='cmoUPSWSBillingOption', max_length=20,
                                             )  # Field name made lowercase.
    cmointracompanydatasetid = models.CharField(db_column='cmoIntraCompanyDatasetID', max_length=40,
                                                )  # Field name made lowercase.
    cmoaddressvalidationresult = models.TextField(db_column='cmoAddressValidationResult',
                                                  blank=True,
                                                  null=True)  # Field name made lowercase.
    cmocustomershippingcarrier = models.CharField(db_column='cmoCustomerShippingCarrier', max_length=5,
                                                  )  # Field name made lowercase.
    cmosplitpercenttotal = models.DecimalField(db_column='cmoSplitPercentTotal', max_digits=6,
                                               decimal_places=2)  # Field name made lowercase.
    cmoexpensesplitpercenttotal = models.DecimalField(db_column='cmoExpenseSplitPercentTotal', max_digits=6,
                                                      decimal_places=2)  # Field name made lowercase.
    cmojobpriorityid = models.SmallIntegerField(db_column='cmoJobPriorityID')  # Field name made lowercase.

    # cmorowversion = models.TextField(db_column='cmoRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'Organizations'


class Organizationcontacts(TruncatedModel):
    cmcorganizationid = models.CharField(db_column='cmcOrganizationID', max_length=10)  # Field name made lowercase.
    cmclocationid = models.CharField(db_column='cmcLocationID', max_length=5)  # Field name made lowercase.
    cmccontactid = models.CharField(db_column='cmcContactID', max_length=5)  # Field name made lowercase.
    cmccontacttitleid = models.CharField(db_column='cmcContactTitleID', max_length=5,
                                         )  # Field name made lowercase.
    cmcname = models.CharField(db_column='cmcName', max_length=50,
                               )  # Field name made lowercase.
    cmcphonenumber = models.CharField(db_column='cmcPhoneNumber', max_length=20,
                                      )  # Field name made lowercase.
    cmcalternatephonenumber = models.CharField(db_column='cmcAlternatePhoneNumber', max_length=20,
                                               )  # Field name made lowercase.
    cmcmobilenumber = models.CharField(db_column='cmcMobileNumber', max_length=20,
                                       )  # Field name made lowercase.
    cmcfaxnumber = models.CharField(db_column='cmcFaxNumber', max_length=20,
                                    )  # Field name made lowercase.
    cmcemailaddress = models.TextField(db_column='cmcEMailAddress',
                                       blank=True, null=True)  # Field name made lowercase.
    cmcwebloginenabled = models.BooleanField(db_column='cmcWebLoginEnabled')  # Field name made lowercase.
    cmcwebuserid = models.CharField(db_column='cmcWebUserID', max_length=10,
                                    )  # Field name made lowercase.
    cmcwebpassword = models.CharField(db_column='cmcWebPassword', max_length=80,
                                      )  # Field name made lowercase.
    cmcwebtemplate = models.CharField(db_column='cmcWebTemplate', max_length=20,
                                      )  # Field name made lowercase.
    cmcwebexpirationdate = models.DateTimeField(db_column='cmcWebExpirationDate', blank=True,
                                                null=True)  # Field name made lowercase.
    cmcnomailings = models.BooleanField(db_column='cmcNoMailings')  # Field name made lowercase.
    cmccorrespondencemethod = models.CharField(db_column='cmcCorrespondenceMethod', max_length=1,
                                               )  # Field name made lowercase.
    cmcnotertf = models.TextField(db_column='cmcNoteRTF', blank=True,
                                  null=True)  # Field name made lowercase.
    cmcnotetext = models.TextField(db_column='cmcNoteText', blank=True,
                                   null=True)  # Field name made lowercase.
    cmcinactive = models.BooleanField(db_column='cmcInactive')  # Field name made lowercase.
    cmcinactivedate = models.DateTimeField(db_column='cmcInactiveDate', blank=True,
                                           null=True)  # Field name made lowercase.
    cmccreatedfrommobile = models.BooleanField(db_column='cmcCreatedFromMobile')  # Field name made lowercase.
    cmccreatedby = models.CharField(db_column='cmcCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    cmccreateddate = models.DateTimeField(db_column='cmcCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    cmcuniqueid = models.AutoField(db_column='cmcUniqueID', unique=True, primary_key=True)
    # cmcuniqueid = models.CharField(db_column='cmcUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    cmceasyorderenabled = models.BooleanField(db_column='cmcEasyOrderEnabled')  # Field name made lowercase.
    cmccreatedbyeasyorder = models.BooleanField(db_column='cmcCreatedByEasyOrder')  # Field name made lowercase.
    cmceoinitials = models.CharField(db_column='cmcEOInitials', max_length=20,
                                     )  # Field name made lowercase.
    cmceoprefix = models.CharField(db_column='cmcEOPrefix', max_length=20,
                                   )  # Field name made lowercase.
    cmceosurname = models.CharField(db_column='cmcEOSurname', max_length=20,
                                    )  # Field name made lowercase.
    cmceopassword = models.CharField(db_column='cmcEOPassword', max_length=20,
                                     )  # Field name made lowercase.
    cmceouserrole = models.CharField(db_column='cmcEOUserRole', max_length=20,
                                     )  # Field name made lowercase.
    cmceodefsupervisor = models.CharField(db_column='cmcEODefSupervisor', max_length=5,
                                          )  # Field name made lowercase.
    cmceosubsupervisor = models.CharField(db_column='cmcEOSubSupervisor', max_length=5,
                                          )  # Field name made lowercase.
    cmceocustomergroup = models.CharField(db_column='cmcEOCustomerGroup', max_length=100,
                                          )  # Field name made lowercase.
    cmceomultishipaddress = models.CharField(db_column='cmcEOMultiShipAddress', max_length=1,
                                             )  # Field name made lowercase.
    cmceoreceiveorderconfirmation = models.CharField(db_column='cmcEOReceiveOrderConfirmation', max_length=1,
                                                     )  # Field name made lowercase.
    cmceoeditshippingaddress = models.BooleanField(db_column='cmcEOEditShippingAddress')  # Field name made lowercase.
    cmceoreceiveemails = models.BooleanField(db_column='cmcEOReceiveEMails')  # Field name made lowercase.
    cmceohtmlmail = models.BooleanField(db_column='cmcEOHTMLMail')  # Field name made lowercase.
    cmceoreminderofopenorders = models.BooleanField(db_column='cmcEOReminderOfOpenOrders')  # Field name made lowercase.
    cmceoorderauthorisationmessage = models.BooleanField(
        db_column='cmcEOOrderAuthorisationMessage')  # Field name made lowercase.
    cmceoauthorisationrequest = models.BooleanField(db_column='cmcEOAuthorisationRequest')  # Field name made lowercase.
    cmceomaynotcreordtemp = models.BooleanField(db_column='cmcEOMayNotCreOrdTemp')  # Field name made lowercase.
    cmceofirstname = models.CharField(db_column='cmcEOFirstName', max_length=20,
                                      )  # Field name made lowercase.

    # cmcrowversion = models.TextField(db_column='cmcRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'OrganizationContacts'
        unique_together = (('cmcorganizationid', 'cmclocationid', 'cmccontactid'),)


class Organizationlocations(TruncatedModel):
    cmlorganizationid = models.CharField(db_column='cmlOrganizationID', max_length=10)  # Field name made lowercase.
    cmllocationid = models.CharField(db_column='cmlLocationID', max_length=5)  # Field name made lowercase.
    cmlfinanceorganizationid = models.CharField(db_column='cmlFinanceOrganizationID', max_length=10,
                                                )  # Field name made lowercase.
    cmlname = models.CharField(db_column='cmlName', max_length=50,
                               )  # Field name made lowercase.
    cmladdressline1 = models.CharField(db_column='cmlAddressLine1', max_length=50,
                                       )  # Field name made lowercase.
    cmladdressline2 = models.CharField(db_column='cmlAddressLine2', max_length=50,
                                       )  # Field name made lowercase.
    cmladdressline3 = models.CharField(db_column='cmlAddressLine3', max_length=50,
                                       )  # Field name made lowercase.
    cmlcity = models.CharField(db_column='cmlCity', max_length=30,
                               )  # Field name made lowercase.
    cmlcounty = models.CharField(db_column='cmlCounty', max_length=30,
                                 )  # Field name made lowercase.
    cmlstate = models.CharField(db_column='cmlState', max_length=3,
                                )  # Field name made lowercase.
    cmlpostcode = models.CharField(db_column='cmlPostCode', max_length=10,
                                   )  # Field name made lowercase.
    cmlcountry = models.CharField(db_column='cmlCountry', max_length=20,
                                  )  # Field name made lowercase.
    cmlphonenumber = models.CharField(db_column='cmlPhoneNumber', max_length=20,
                                      )  # Field name made lowercase.
    cmlalternatephonenumber = models.CharField(db_column='cmlAlternatePhoneNumber', max_length=20,
                                               )  # Field name made lowercase.
    cmlfaxnumber = models.CharField(db_column='cmlFaxNumber', max_length=20,
                                    )  # Field name made lowercase.
    cmlemailaddress = models.TextField(db_column='cmlEMailAddress',
                                       blank=True, null=True)  # Field name made lowercase.
    cmlquotelocation = models.BooleanField(db_column='cmlQuoteLocation')  # Field name made lowercase.
    cmlquotecontactid = models.CharField(db_column='cmlQuoteContactID', max_length=5,
                                         )  # Field name made lowercase.
    cmlshiplocation = models.BooleanField(db_column='cmlShipLocation')  # Field name made lowercase.
    cmlshipcontactid = models.CharField(db_column='cmlShipContactID', max_length=5,
                                        )  # Field name made lowercase.
    cmlarinvoicelocation = models.BooleanField(db_column='cmlARInvoiceLocation')  # Field name made lowercase.
    cmlarinvoicecontactid = models.CharField(db_column='cmlARInvoiceContactID', max_length=5,
                                             )  # Field name made lowercase.
    cmlpurchaselocation = models.BooleanField(db_column='cmlPurchaseLocation')  # Field name made lowercase.
    cmlpurchasecontactid = models.CharField(db_column='cmlPurchaseContactID', max_length=5,
                                            )  # Field name made lowercase.
    cmlapinvoicelocation = models.BooleanField(db_column='cmlAPInvoiceLocation')  # Field name made lowercase.
    cmlapinvoicecontactid = models.CharField(db_column='cmlAPInvoiceContactID', max_length=5,
                                             )  # Field name made lowercase.
    cmlcustomertaxable = models.BooleanField(db_column='cmlCustomerTaxable')  # Field name made lowercase.
    cmlcustomertaxcodeid = models.CharField(db_column='cmlCustomerTaxCodeID', max_length=5,
                                            )  # Field name made lowercase.
    cmlcustomersecondtaxcodeid = models.CharField(db_column='cmlCustomerSecondTaxCodeID', max_length=5,
                                                  )  # Field name made lowercase.
    cmlcustomershippingmethodid = models.CharField(db_column='cmlCustomerShippingMethodID', max_length=5,
                                                   )  # Field name made lowercase.
    cmlcustomershippaymenttypeid = models.CharField(db_column='cmlCustomerShipPaymentTypeID', max_length=5,
                                                    )  # Field name made lowercase.
    cmltaxexemptnumber = models.CharField(db_column='cmlTaxExemptNumber', max_length=16,
                                          )  # Field name made lowercase.
    cmlnontaxreasonid = models.CharField(db_column='cmlNonTaxReasonID', max_length=5,
                                         )  # Field name made lowercase.
    cmlcustomerpaymenttermid = models.CharField(db_column='cmlCustomerPaymentTermID', max_length=5,
                                                )  # Field name made lowercase.
    cmlcurrencyrateid = models.CharField(db_column='cmlCurrencyRateID', max_length=5,
                                         )  # Field name made lowercase.
    cmlarinvoicepershipmentline = models.BooleanField(
        db_column='cmlARInvoicePerShipmentLine')  # Field name made lowercase.
    cmlsupplierpaymenttermid = models.CharField(db_column='cmlSupplierPaymentTermID', max_length=5,
                                                )  # Field name made lowercase.
    cmlsuppliershippingmethodid = models.CharField(db_column='cmlSupplierShippingMethodID', max_length=5,
                                                   )  # Field name made lowercase.
    cmlinactive = models.BooleanField(db_column='cmlInactive')  # Field name made lowercase.
    cmlinactivedate = models.DateTimeField(db_column='cmlInactiveDate', blank=True,
                                           null=True)  # Field name made lowercase.
    cmlupsacctnumber = models.CharField(db_column='cmlUPSAcctNumber', max_length=6,
                                        )  # Field name made lowercase.
    cmlupsbillingoption = models.CharField(db_column='cmlUPSBillingOption', max_length=20,
                                           )  # Field name made lowercase.
    cmlresidentialaddress = models.BooleanField(db_column='cmlResidentialAddress')  # Field name made lowercase.
    cmlcreditcheckforlocation = models.BooleanField(db_column='cmlCreditCheckForLocation')  # Field name made lowercase.
    cmlcustomercreditlimit = models.DecimalField(db_column='cmlCustomerCreditLimit', max_digits=19,
                                                 decimal_places=4)  # Field name made lowercase.
    cmlcredithold = models.BooleanField(db_column='cmlCreditHold')  # Field name made lowercase.
    cmldirectpayment = models.BooleanField(db_column='cmlDirectPayment')  # Field name made lowercase.
    cmlbankinitials = models.CharField(db_column='cmlBankInitials', max_length=3,
                                       )  # Field name made lowercase.
    cmlbsbnumber = models.CharField(db_column='cmlBSBNumber', max_length=10,
                                    )  # Field name made lowercase.
    cmlbankaccountname = models.CharField(db_column='cmlBankAccountName', max_length=50,
                                          )  # Field name made lowercase.
    cmlbankaccountnumber = models.CharField(db_column='cmlBankAccountNumber', max_length=24,
                                            )  # Field name made lowercase.
    cmleftdescription = models.CharField(db_column='cmlEFTDescription', max_length=20,
                                         )  # Field name made lowercase.
    cmlbankaccounttype = models.CharField(db_column='cmlBankAccountType', max_length=2,
                                          )  # Field name made lowercase.
    cmlcountrycode = models.CharField(db_column='cmlCountryCode', max_length=2,
                                      )  # Field name made lowercase.
    cmlhdattachmentfilepath = models.TextField(db_column='cmlHDAttachmentFilePath', blank=True,
                                               null=True)  # Field name made lowercase.
    cmlfreeonboarddescription = models.CharField(db_column='cmlFreeOnBoardDescription', max_length=15,
                                                 )  # Field name made lowercase.
    cmlcreatedby = models.CharField(db_column='cmlCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    cmlcreateddate = models.DateTimeField(db_column='cmlCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    cmluniqueid = models.AutoField(db_column='cmlUniqueID', unique=True, primary_key=True)
    # cmluniqueid = models.CharField(db_column='cmlUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    cmlups3rdpartyorganizationid = models.CharField(db_column='cmlUPS3rdPartyOrganizationID', max_length=10,
                                                    )  # Field name made lowercase.
    cmlups3rdpartylocationid = models.CharField(db_column='cmlUPS3rdPartyLocationID', max_length=5,
                                                )  # Field name made lowercase.
    cmleftcode = models.CharField(db_column='cmlEFTCode', max_length=12,
                                  )  # Field name made lowercase.
    cmleftparticulars = models.CharField(db_column='cmlEFTParticulars', max_length=12,
                                         )  # Field name made lowercase.
    cmlavalarausecodes = models.CharField(db_column='cmlAvalaraUseCodes', max_length=1,
                                          )  # Field name made lowercase.
    cmlavalaraaddressvalidated = models.BooleanField(
        db_column='cmlAvalaraAddressValidated')  # Field name made lowercase.
    cmlcontractor = models.BooleanField(db_column='cmlContractor')  # Field name made lowercase.
    cmltaxreportable = models.BooleanField(db_column='cmlTaxReportable')  # Field name made lowercase.
    cmllastname = models.CharField(db_column='cmlLastName', max_length=30,
                                   )  # Field name made lowercase.
    cmlfirstgivenname = models.CharField(db_column='cmlFirstGivenName', max_length=15,
                                         )  # Field name made lowercase.
    cmlsecondgivenname = models.CharField(db_column='cmlSecondGivenName', max_length=15,
                                          )  # Field name made lowercase.
    cmltradingname = models.TextField(db_column='cmlTradingName',
                                      blank=True, null=True)  # Field name made lowercase.
    cmlcreatedfrommobile = models.BooleanField(db_column='cmlCreatedFromMobile')  # Field name made lowercase.
    cmlbarecostofduty = models.BooleanField(db_column='cmlBareCostOfDuty')  # Field name made lowercase.
    cmlbaretransportationcost = models.BooleanField(db_column='cmlBareTransportationCost')  # Field name made lowercase.
    cmlignoreavalara = models.BooleanField(db_column='cmlIgnoreAvalara')  # Field name made lowercase.
    cmlupsvalidated = models.BooleanField(db_column='cmlUPSValidated')  # Field name made lowercase.
    cmlediintegrated = models.BooleanField(db_column='cmlEDIIntegrated')  # Field name made lowercase.
    cmlfedexaccountnumber = models.CharField(db_column='cmlFedExAccountNumber', max_length=15,
                                             )  # Field name made lowercase.
    cmlfedex3rdpartyorganizationid = models.CharField(db_column='cmlFedEx3rdPartyOrganizationID', max_length=10,
                                                      )  # Field name made lowercase.
    cmlfedex3rdpartylocationid = models.CharField(db_column='cmlFedEx3rdPartyLocationID', max_length=5,
                                                  )  # Field name made lowercase.
    cmlfedexbillingoption = models.CharField(db_column='cmlFedExBillingOption', max_length=20,
                                             )  # Field name made lowercase.
    cmlbic = models.CharField(db_column='cmlBIC', max_length=50,
                              )  # Field name made lowercase.
    cmliban = models.CharField(db_column='cmlIBAN', max_length=50,
                               )  # Field name made lowercase.
    cmlupswsbillingoption = models.CharField(db_column='cmlUPSWSBillingOption', max_length=20,
                                             )  # Field name made lowercase.
    cmladdressvalidationresult = models.TextField(db_column='cmlAddressValidationResult', blank=True,
                                                  null=True)  # Field name made lowercase.
    cmlcustomershippingcarrier = models.CharField(db_column='cmlCustomerShippingCarrier', max_length=5,
                                                  )  # Field name made lowercase.
    cmlsplitpercenttotal = models.DecimalField(db_column='cmlSplitPercentTotal', max_digits=6,
                                               decimal_places=2)  # Field name made lowercase.
    cmledilocationid = models.CharField(db_column='cmlEDILocationID', max_length=30,
                                        )  # Field name made lowercase.

    # cmlrowversion = models.TextField(db_column='cmlRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'OrganizationLocations'
        unique_together = (('cmlorganizationid', 'cmllocationid'),)


class Paymentterms(TruncatedModel):
    xatpaymenttermid = models.CharField(db_column='xatPaymentTermID', unique=True,
                                        max_length=5)  # Field name made lowercase.
    xatdescription = models.CharField(db_column='xatDescription', max_length=20)  # Field name made lowercase.
    xatdaysdue = models.SmallIntegerField(db_column='xatDaysDue')  # Field name made lowercase.
    xatdiscountdays = models.SmallIntegerField(db_column='xatDiscountDays')  # Field name made lowercase.
    xatdiscountpercent = models.DecimalField(db_column='xatDiscountPercent', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xatgraceperiod = models.SmallIntegerField(db_column='xatGracePeriod')  # Field name made lowercase.
    xatcalculationtype = models.SmallIntegerField(db_column='xatCalculationType')  # Field name made lowercase.
    xatimmediatepaymentrequired = models.BooleanField(
        db_column='xatImmediatePaymentRequired')  # Field name made lowercase.
    xatcalculationdayofmonth = models.SmallIntegerField(
        db_column='xatCalculationDayOfMonth')  # Field name made lowercase.
    xatdiscountdayofmonth = models.SmallIntegerField(db_column='xatDiscountDayOfMonth')  # Field name made lowercase.
    xatcreatedby = models.CharField(db_column='xatCreatedBy', max_length=20,
                                    )  # Field name made lowercase.
    xatcreateddate = models.DateTimeField(db_column='xatCreatedDate', blank=True, null=True,
                                          auto_now=True)  # Field name made lowercase.
    xatuniqueid = models.AutoField(db_column='xatUniqueID', unique=True, primary_key=True)

    # xatuniqueid = models.CharField(db_column='xatUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    # xatrowversion = models.TextField(db_column='xatRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'PaymentTerms'


class Workcenters(models.Model):
    xawworkcenterid = models.CharField(db_column='xawWorkCenterID', unique=True,
                                       max_length=5)  # Field name made lowercase.
    xawdescription = models.CharField(db_column='xawDescription', max_length=50)  # Field name made lowercase.
    xawplantid = models.CharField(db_column='xawPlantID', max_length=5)  # Field name made lowercase.
    xawproductiondepartmentid = models.CharField(db_column='xawProductionDepartmentID',
                                                 max_length=5)  # Field name made lowercase.
    xawprocessid = models.CharField(db_column='xawProcessID', max_length=5)  # Field name made lowercase.
    xawsetuphours = models.DecimalField(db_column='xawSetupHours', max_digits=8,
                                        decimal_places=2)  # Field name made lowercase.
    xawstandardfactor = models.CharField(db_column='xawStandardFactor', max_length=2)  # Field name made lowercase.
    xawproductionstandard = models.DecimalField(db_column='xawProductionStandard', max_digits=10,
                                                decimal_places=4)  # Field name made lowercase.
    xawnumberofmachines = models.SmallIntegerField(db_column='xawNumberOfMachines')  # Field name made lowercase.
    xawpeoplepermachineprod = models.SmallIntegerField(
        db_column='xawPeoplePerMachineProd')  # Field name made lowercase.
    xawexcludefromshopload = models.BooleanField(db_column='xawExcludeFromShopLoad')  # Field name made lowercase.
    xawhoursmon = models.DecimalField(db_column='xawHoursMon', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawhourstue = models.DecimalField(db_column='xawHoursTue', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawhourswed = models.DecimalField(db_column='xawHoursWed', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawhoursthu = models.DecimalField(db_column='xawHoursThu', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawhoursfri = models.DecimalField(db_column='xawHoursFri', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawhourssat = models.DecimalField(db_column='xawHoursSat', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawhourssun = models.DecimalField(db_column='xawHoursSun', max_digits=5,
                                      decimal_places=2)  # Field name made lowercase.
    xawdaystarttimemon = models.DecimalField(db_column='xawDayStartTimeMon', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawdaystarttimetue = models.DecimalField(db_column='xawDayStartTimeTue', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawdaystarttimewed = models.DecimalField(db_column='xawDayStartTimeWed', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawdaystarttimethu = models.DecimalField(db_column='xawDayStartTimeThu', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawdaystarttimefri = models.DecimalField(db_column='xawDayStartTimeFri', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawdaystarttimesat = models.DecimalField(db_column='xawDayStartTimeSat', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawdaystarttimesun = models.DecimalField(db_column='xawDayStartTimeSun', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawqueuetime = models.DecimalField(db_column='xawQueueTime', max_digits=6,
                                       decimal_places=2)  # Field name made lowercase.
    xawmovetime = models.DecimalField(db_column='xawMoveTime', max_digits=6,
                                      decimal_places=2)  # Field name made lowercase.
    xawoutsideprocessing = models.BooleanField(db_column='xawOutsideProcessing')  # Field name made lowercase.
    xawfinitetolerance = models.DecimalField(db_column='xawFiniteTolerance', max_digits=5,
                                             decimal_places=2)  # Field name made lowercase.
    xawoverheadrate = models.DecimalField(db_column='xawOverheadRate', max_digits=8,
                                          decimal_places=2)  # Field name made lowercase.
    xawquotingrate = models.DecimalField(db_column='xawQuotingRate', max_digits=8,
                                         decimal_places=2)  # Field name made lowercase.
    xawoverheadcalculationtype = models.SmallIntegerField(
        db_column='xawOverheadCalculationType')  # Field name made lowercase.
    xawsplitmachinehours = models.BooleanField(db_column='xawSplitMachineHours')  # Field name made lowercase.
    xawsetmachinetolaborhours = models.BooleanField(db_column='xawSetMachineToLaborHours')  # Field name made lowercase.
    xawexporttocalendar = models.BooleanField(db_column='xawExportToCalendar')  # Field name made lowercase.
    xawcalendarlocation = models.TextField(db_column='xawCalendarLocation', blank=True,
                                           null=True)  # Field name made lowercase.
    xawcalendarcolor = models.SmallIntegerField(db_column='xawCalendarColor')  # Field name made lowercase.
    xawstarthour = models.DecimalField(db_column='xawStartHour', max_digits=5,
                                       decimal_places=2)  # Field name made lowercase.
    xawinactive = models.BooleanField(db_column='xawInactive')  # Field name made lowercase.
    xawinactivedate = models.DateTimeField(db_column='xawInactiveDate', blank=True,
                                           null=True)  # Field name made lowercase.
    xawcreatedby = models.CharField(db_column='xawCreatedBy', max_length=20)  # Field name made lowercase.
    xawcreateddate = models.DateTimeField(db_column='xawCreatedDate', blank=True,
                                          null=True)  # Field name made lowercase.
    xawuniqueid = models.AutoField(db_column='xawUniqueID', unique=True, primary_key=True)
    # xawuniqueid = models.CharField(db_column='xawUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    xawpeoplepermachinesetup = models.SmallIntegerField(
        db_column='xawPeoplePerMachineSetup')  # Field name made lowercase.
    xawinfinitecapacity = models.BooleanField(db_column='xawInfiniteCapacity')  # Field name made lowercase.
    xawenablecalendar = models.BooleanField(db_column='xawEnableCalendar')  # Field name made lowercase.

    # xawrowversion = models.TextField(db_column='xawRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'WorkCenters'


class Processes(models.Model):
    xacprocessid = models.CharField(db_column='xacProcessID', unique=True, max_length=5)  # Field name made lowercase.
    xacshortdescription = models.CharField(db_column='xacShortDescription', max_length=50)  # Field name made lowercase.
    xaclongdescriptionrtf = models.TextField(db_column='xacLongDescriptionRTF', blank=True,
                                             null=True)  # Field name made lowercase.
    xaclongdescriptiontext = models.TextField(db_column='xacLongDescriptionText', blank=True,
                                              null=True)  # Field name made lowercase.
    xacprintinspectionline = models.BooleanField(db_column='xacPrintInspectionLine')  # Field name made lowercase.
    xacprojectedsetuprate = models.DecimalField(db_column='xacProjectedSetupRate', max_digits=8,
                                                decimal_places=2)  # Field name made lowercase.
    xacprojectedproductionrate = models.DecimalField(db_column='xacProjectedProductionRate', max_digits=8,
                                                     decimal_places=2)  # Field name made lowercase.
    xacsetuphours = models.DecimalField(db_column='xacSetupHours', max_digits=8,
                                        decimal_places=2)  # Field name made lowercase.
    xacstandardfactor = models.CharField(db_column='xacStandardFactor', max_length=2)  # Field name made lowercase.
    xacproductionstandard = models.DecimalField(db_column='xacProductionStandard', max_digits=10,
                                                decimal_places=4)  # Field name made lowercase.
    xacinactive = models.BooleanField(db_column='xacInactive')  # Field name made lowercase.
    xacinactivedate = models.DateTimeField(db_column='xacInactiveDate', blank=True,
                                           null=True)  # Field name made lowercase.
    xacinspectiontype = models.SmallIntegerField(db_column='xacInspectionType')  # Field name made lowercase.
    xacexcludefromtmjobs = models.BooleanField(db_column='xacExcludeFromTMJobs')  # Field name made lowercase.
    xaccreatedby = models.CharField(db_column='xacCreatedBy', max_length=20)  # Field name made lowercase.
    xaccreateddate = models.DateTimeField(db_column='xacCreatedDate', blank=True,
                                          null=True)  # Field name made lowercase.
    xacuniqueid = models.AutoField(db_column='xacUniqueID', unique=True, primary_key=True)
    # xacuniqueid = models.CharField(db_column='xacUniqueID', unique=True, max_length=36)  # Field name made lowercase.
    xacignorecalendarqueue = models.BooleanField(db_column='xacIgnoreCalendarQueue')  # Field name made lowercase.
    xacignorecalendarmove = models.BooleanField(db_column='xacIgnoreCalendarMove')  # Field name made lowercase.

    # xacrowversion = models.TextField(db_column='xacRowVersion', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = IS_TEST
        db_table = 'Processes'
