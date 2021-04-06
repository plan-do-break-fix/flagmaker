import logging, os, tarfile
from survey.survey import survey


class AbstractPipeline:

    def __init__(self, datapath="/media/flagmaker"):
        self.datapath = datapath
        self.input = ""
        self.output = ""
        self.to_process = []

    def run(self) -> None:
        if os.path.isdir(f"{self.datapath}/imagesets/{output_name}") \
                   or os.path.isfile(f"{self.datapath}/imagesets/{output_name}.tar"):
            print(f"Data set named {self.output} already exists.")
            return False
        self.load_data_set()
        self.process()
        survey(self.output)

    def load_data_set(self) -> bool:
        """Populates Pipeline.to_process with image file paths."""
        _path = f"{self.datapath}/imagesets/{input_name}"
        if not os.path.isdir(_path):
            if not os.path.isfile(f"{_path}.tar"):
                raise RuntimeError
            with open(f"{_path}.tar") as _tar:
                _tar.extractall(path=_path)
        self.to_process = [_f for _f in os.listdir(_path) if os.path.isfile(_f)]
