from typing import Optional

import pgeocode
from pycountry import countries, subdivisions
from pgeocode import Nominatim
from ...baseintegration.datamigration import logger


class AddressUtils:
    @staticmethod
    def get_country_and_state(country_name: str = '', state_province_name: str = '', zipcode: str = '',
                              fallback_country_alpha_3: str = '') -> [str, str]:
        country_alpha_3 = fallback_country_alpha_3
        state_province = state_province_name.strip()

        country = countries.get(name=country_name.strip()) \
            or countries.get(alpha_3=country_name.strip()) \
            or countries.get(alpha_2=country_name.strip()) \
            or countries.get(alpha_3=country_alpha_3)
        if country is not None:
            country_alpha_3 = country.alpha_3
            if country.alpha_2 in pgeocode.COUNTRIES_VALID:
                state_province = AddressUtils.get_state_code(country, zipcode) or state_province
        return country_alpha_3, state_province

    @staticmethod
    def get_state_code(country: any, zip_code: str) -> Optional[str]:
        postal_code = zip_code
        if country.alpha_2 == 'US':
            postal_code = zip_code[0:5]
        try:
            state_name = Nominatim(country.alpha_2).query_postal_code(postal_code).state_name
            if state_name == state_name:  # check for NaN
                subdivisions_of_country = subdivisions.get(country_code=country.alpha_2)
                matching_subdivisions = [
                    subdivision for subdivision in subdivisions_of_country
                    if (subdivision.name or '').lower() == (state_name or '').lower()
                ]
                if matching_subdivisions:
                    subdivision_code = matching_subdivisions[0].code
                    if '-' in subdivision_code:
                        return subdivision_code.split('-')[1]
        except ValueError as e:
            logger.warning('A value error was caught while looking up the zip code:')
            logger.warning(e, exc_info=True)
