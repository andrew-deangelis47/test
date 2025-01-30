from baseintegration.importer.import_processor import BaseImportProcessor
from jobboss.models import Service, VendorService
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient
from baseintegration.utils import custom_table_patch


class OutsideServiceImportProcessor(BaseImportProcessor):

    def _process(self, service_id: str):  # noqa: C901
        base_dict = self._importer.header_dict.copy()
        dict_to_upload = None
        service_instance = Service.objects.filter(service=service_id).first()
        vendor_services = VendorService.objects.filter(service=service_instance.service)
        if not service_instance:
            raise Exception(f"Was not able to import {service_instance} as it could not be found in the Service table")
        if vendor_services is not None:
            for vendor_service in vendor_services:
                vendor_instance = vendor_service.vendor
                if vendor_instance is not None and self.vendor_is_active(vendor_instance):
                    vendor_id = str(vendor_instance.vendor)
                    dict_to_upload = self.get_outside_service_attributes(service_instance, vendor_id, base_dict)

                if dict_to_upload:
                    headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
                    new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
                    data = dict(row_data=new_record)
                    client = PaperlessClient.get_instance()
                    url = f"suppliers/public/custom_tables/{self._importer.table_name}/row"
                    custom_table_patch(client=client, data=data, url=url, identifier=dict_to_upload["osv_unique_key"])

    def get_outside_service_attributes(self, service_instance: Service, vendor_id: str, base_dict: dict):  # noqa: C901
        service_id = str(service_instance.service)
        base_dict["jb_service"] = service_id
        base_dict["jb_vendor"] = vendor_id
        base_dict["lead_days"] = int(service_instance.lead_days)
        base_dict["min_charge"] = round(service_instance.minimum_chg, 2)
        base_dict["service_description"] = str(service_instance.description)
        base_dict["osv_unique_key"] = f"{service_id}-{vendor_id}"
        return base_dict

    @staticmethod
    def vendor_is_active(vendor_instance):
        if vendor_instance is not None and vendor_instance.status == "Active":
            return True
        return False
