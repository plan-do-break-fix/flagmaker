import logging, os, tarfile
from survey.survey import survey


class AbstractPipeline:

    def __init__(self, datapath="/media/flagmaker"):
        self.datapath = datapath
        self.input = ""
        self.output = ""
        self.to_process = []

    def run(self) -> None:
        _path = f"{self.datapath}/imagesets/{self.output}"
        if os.path.isdir(_path) or os.path.isfile(f"{_path}.tar"):
            print(f"Data set named {self.output} already exists.")
            return False
        self.load_data_set()
        self.process()
        survey(self.output)

    def load_data_set(self) -> bool:
        """Populates Pipeline.to_process with image file paths."""
        _path = f"{self.datapath}/imagesets/{self.input}"
        if not os.path.isdir(_path):
            print(f"{self.input} folder not found.")
            if not os.path.isfile(f"{_path}.tar"):
                print(f"{self.input} archive not found.")
                raise RuntimeError
            with open(f"{_path}.tar") as _tar:
                _tar.extractall(path=_path)
        self.to_process = [_f for _f in os.listdir(_path) if os.path.isfile(f"{_path}/{_f}")]
