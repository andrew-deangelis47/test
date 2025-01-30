from typing import Tuple
from baseintegration.datamigration import logger


class Utilities:
    @staticmethod
    def split_part_description(description: str) -> Tuple[str, str]:
        """
        This method splits any description that is longer the 50 characters into a truncated description and an extended
        description.

        @param description: a description string to be split
        @type description: str
        @return: A tuple with the truncated description and extended description
        @rtype: str, str
        """
        des = description
        des_ext = ''
        if description is not None and len(description) > 50:
            des = description[0:46] + '...'
            des_ext = description[46:]

        return des, des_ext

    @staticmethod
    def shorten_part_number(part_number: str) -> str:
        """
        This method truncates any part number that is longer the 30 characters.

        @param part_number: the original part number
        @type part_number: str
        @return: A string with the truncated part number
        @rtype: str
        """
        if part_number is not None and len(part_number) > 30:
            logger.info(f'VisualEstiTrackExporter: part number,{part_number}, is too long (limit 30) for '
                        f'VisualEstiTrack, truncating')
            part_number = part_number[0:29] + '*'
        return part_number

    @staticmethod
    def shorten_revision_number(revision: str) -> str:
        """
        This method truncates any revision number that is longer the 6 characters.

        @param revision: the original revision number
        @type revision: str
        @return: A string with the truncated revision number
        @rtype: str
        """
        if revision is not None and len(revision) > 6:
            logger.info(f'VisualEstiTrackExporter: revision number,{revision}, is too long (limit 6) for '
                        f'VisualEstiTrack, truncating')
            revision = revision[0:5] + '*'
        return revision
