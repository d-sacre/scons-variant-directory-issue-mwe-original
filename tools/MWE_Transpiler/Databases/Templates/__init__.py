import json
import os

class Base:
    def __init__(self):
        pass

    def _export(self, a_data : dict, a_exportFilePath : str) -> None:
        with open(a_exportFilePath, 'w') as databaseExportFile:
            json.dump(a_data, databaseExportFile, indent = 4, ensure_ascii = True)

class FromCSV(Base):
    def __init__(self):
        pass

    # DESCRIPTION: Loads csv data from a file
    def _loadFromCSV(self, a_filePath : str) -> list:
        _tmp_data : list = []

        with open(a_filePath, 'r') as _file:
            _tmp_data : list = _file.readlines()

        return _tmp_data

    def _processSingleLine(self, a_header : list, a_lineData : str) -> dict:
        # DESCRIPTION: Clean the string by removing the trailing newline
        _tmp_entryString : str = a_lineData.replace("\n", "")

        # DESCRIPTION: Separate the cleaned string into the respective data chunks
        # by spliting at "," and store the data with suitable keys in a dictionary
        _tmp_entryList : list = _tmp_entryString.split(",")

        _tmp_entry : dict = {}
        for _i,_id in enumerate(a_header):
            _tmp_entry[_id] = _tmp_entryList[_i]

        return _tmp_entry

    # DESCRIPTION: Parse the csv data into a dictionary format
    def _parseRawData(self, a_rawData : list) -> dict:
        _tmp_database : dict = {}

        # DESCRIPTION: Get the header for later use as keys
        _tmp_header = (a_rawData[0].replace("\n", "")).split(",")

        # DESCRIPTION: Sort the rest of the entries according to the header
        # data
        for i in range(1, len(a_rawData)):
            _tmp_entry : dict = self._processSingleLine(
                _tmp_header, a_rawData[i]
            )
            _tmp_database[_tmp_entry["uuid"]] = _tmp_entry

        return _tmp_database

    def generate(self, target, source, env):
        _tmp_rawData : list = self._loadFromCSV(str(os.path.normpath(str(source[0]))))
        _tmp_data : dict = self._parseRawData(_tmp_rawData)

        self._export(_tmp_data, str(os.path.normpath(str(target[0]))))

class FromJSON(Base):
    def __init__(self):
        pass

    def _loadFromJSON(self, a_filePath : str) -> dict:
        _tmp_database : dict = {}

        with open(a_filePath, 'r') as _file:
           _tmp_database : dict = json.loads(_file.read())

        return _tmp_database

class Merging:
    def __init__(self):
        pass

    def _addKeyValuePair(self, a_target : dict, a_key : str, a_value : dict) -> None:
        _tmp_targetKeys : list = list(a_target.keys())

        if a_key not in _tmp_targetKeys:
            a_target[a_key] = a_value

        else:
            _tmp_message : str = "The entry IDs are not unique. Aborting!\n"
            _tmp_message += "The ID \"{id}\" was already defined in \"{original}\""
            _tmp_message += " and conflicts with \"{new}\"."
            raise Exception(
                _tmp_message.format(
                    id = _key,
                    original = a_target[_key]["meta_data"]["source"],
                    new = a_value["meta_data"]["source"]
                )
            )

    def _mergeDatabases(self, a_target : dict, a_sources : list) -> None:
        # DESCRIPTION: Verify if the keys in the source are not already
        # existing in the target. If not, add them to the target;
        # otherwise: abort with an error
        # REMARK: Assumes that all the keys in the source data base
        # are unique (as they in theory should be) and skips those checks
        for _source in a_sources:
            _tmp_targetKeys : list = list(a_target.keys())

            for _key in list(_source.keys()):
                self._addKeyValuePair(a_target, _key, _source[_key])

class MergeFromFileJSON(FromJSON, Merging):
    def __init__(self):
        FromJSON.__init__(self)
        Merging.__init__(self)

    def generate(self, target, source, env):
        _tmp_sourceDataList : list = []
        _tmp_merged : dict = {}

        for _source in source:
            _tmp_sourceDataList.append(
                self._loadFromJSON(str(_source))
            )

        self._mergeDatabases(_tmp_merged, _tmp_sourceDataList)
        self._export(_tmp_merged, str(target[0]))