import attr
import json
from pathlib import Path
from baseintegration.datamigration import logger


class BaseObject:

    def to_dict(self):
        return attr.asdict(self, recurse=True)

    def write_to_local(self):
        filepath = Path("/Users/reidlance/Desktop/repeat_work/output_data.json")

        json_body = json.dumps(self)

        if filepath.is_file():
            with open("output_data.json", "w") as output:
                output.write(json_body)
        else:
            logger.info("Cannot write file to local storage. Check your filepath.")
