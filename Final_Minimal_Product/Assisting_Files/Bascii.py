"""Original dictionary-based TABS text encoding and decoding."""

import math
from .ModelHandling import MODEL_DIR, readmodel, modelpath

class ENTABIS:
    def __init__(self, message=None, secretmessage_filepath=None, model_filename=None, main_dict=False, bestmodel=False, includewordlists=True):
        self.include_wordlists = includewordlists
        self.message = message
        self.filepath = secretmessage_filepath
        self.decimal_list = []
        self.error = False
        if secretmessage_filepath:
            self.processfile()
        if model_filename:
            self.model_filepath = model_filename
            self.main_dict = readmodel(model_filename)
        elif bestmodel:
            self.bestmodel()
        elif main_dict:
            self.main_dict = main_dict
        else:
            self.bestmodel()
        self.end = len(self.main_dict)
        self.ASCII5_en()

    def processfile(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            self.message = file.read()

    def locateENTER(self):
        for key, value in self.main_dict.items():
            if value == "ENTER":
                return [int(key)]
            if isinstance(value, dict):
                for subkey, letter in value.items():
                    if letter == "ENTER":
                        return [int(key), int(subkey)]
        return []

    def modelnumber(self):
        self.modelnumber = int(modelpath(self.model_filepath).stem.rsplit("_", 1)[1])

    def bestmodel(self):
        self.model_filepath = None
        bestmodelvalue = None
        for file in sorted(MODEL_DIR.glob("*.json")):
            modeltest = ENTABIS(model_filename=file, message=self.message,
                               includewordlists=self.include_wordlists)
            cost = len(modeltest.givinglikesanta()) * modeltest.bytelen_used()
            if not modeltest.check_error() and (bestmodelvalue is None or cost < bestmodelvalue):
                self.model_filepath = file
                bestmodelvalue = cost
        if self.model_filepath is None:
            raise ValueError("No model supports this message. Use printable ASCII and newlines.")
        self.main_dict = readmodel(self.model_filepath)

    def calculatemainpage(self):
        self.letterdict = []
        for i in self.main_dict:
            if type(self.main_dict[i]) == dict:
                if all(isinstance(value, int) for value in self.main_dict[i].values()):
                    self.hoofdpagina_karakters = int(i)-1
                    return None
                else:
                    self.letterdict.append(int(i))
        self.hoofdpagina_karakters = self.end

    def givinglikesanta(self):
        return self.decimal_list

    def error_happened(self):
        self.error = True

    def check_error(self):
        return self.error

    def model_used(self):
        return self.model_filepath

    def bytelen_used(self):
        return math.ceil(math.log2(max(int(k) for k in self.main_dict) + 1))

    def ASCII5_en(self):
        decimal_list = []
        exampletekst = self.message
        self.calculatemainpage()
        locateENTER = self.locateENTER()
        i = 0
        while i < len(exampletekst):
            processed = False
            if self.include_wordlists:
                for list_idx in range(self.hoofdpagina_karakters + 1 + len(self.letterdict), self.end):
                    subdic = self.main_dict[str(list_idx)]
                    if self.main_dict[str(list_idx)] is None:
                        self.error_happened()
                        break
                    for word in self.main_dict[str(list_idx)]:
                        if word == exampletekst[:len(word)]:
                            decimal_list.append(list_idx)
                            decimal_list.append(subdic[word])
                            exampletekst = exampletekst.replace(word, "", 1)
                            processed = True
                            break
                        if processed:
                            break
                    if processed:
                        break

            if not processed:
                for idx in range(0, self.hoofdpagina_karakters):
                    if exampletekst[i] == self.main_dict[str(idx)]:
                        decimal_list.append(idx)
                        exampletekst = exampletekst.replace(exampletekst[i], "", 1)
                        processed = True
                        break
                    elif exampletekst[i] == "\n":
                        for path in locateENTER:
                            decimal_list.append(path)
                        exampletekst = exampletekst.replace(exampletekst[i], "", 1)
                        processed = True
                        break
                    if processed:
                        break

            if not processed:
                for list_idx in self.letterdict:
                    subdic = self.main_dict[str(list_idx)]
                    for idx in range(0, len(subdic)):
                        if exampletekst[i] == subdic[str(idx)]:
                            decimal_list.append(int(list_idx))
                            decimal_list.append(int(idx))
                            exampletekst = exampletekst.replace(exampletekst[i], "", 1)
                            processed = True
                            break
                    if processed:
                        break
            if not processed:
                self.error_happened()
                i+=1
        self.modelnumber()
        decimal_list.insert(0, self.modelnumber)
        self.decimal_list = decimal_list


#########################################################################
# Takes a decimallist and a model (Either the model or the model filepath)
# Returns the decrypted message

# Example usage:
# test = DETABIS(filepath="Model\\testfile.txt", decimal_list=[1,0,2,0,3])


class DETABIS:
    def __init__(self, main_dict=None, filepath=None, decimal_list=None):
        self.main_dict = main_dict or {}
        self.filepath = filepath
        self.decimal_list = decimal_list or []
        if filepath:
            self.processfile(filepath)

        if self.main_dict == {}:
            self.modelnumber()
        self.decrypted_message = self.decryptor()

    def modelnumber(self):
        if not self.decimal_list:
            raise ValueError("The TABS data has no model identifier.")
        identifier = self.decimal_list[0]
        for file in MODEL_DIR.glob("*.json"):
            if int(file.stem.rsplit("_", 1)[1]) == identifier:
                self.processfile(file)
                self.decimal_list = self.decimal_list[1:]
                return
        raise ValueError(f"Unknown TABS model identifier: {identifier}")

    def processfile(self, filepath):
        self.main_dict = readmodel(filepath)

    def decryptor(self):
        decrypted_message = ""
        idx = 0
        while idx < len(self.decimal_list):
            key = str(self.decimal_list[idx])
            if key not in self.main_dict or self.main_dict[key] is None:
                raise ValueError("Invalid TABS character code.")
            value = self.main_dict[key]
            idx += 1
            if isinstance(value, dict):
                if idx >= len(self.decimal_list):
                    raise ValueError("Incomplete TABS dictionary code.")
                code = self.decimal_list[idx]
                idx += 1
                if all(isinstance(v, int) for v in value.values()):
                    value = {v: k for k, v in value.items()}.get(code)
                else:
                    value = value.get(str(code))
                if not isinstance(value, str):
                    raise ValueError("Invalid TABS dictionary code.")
            decrypted_message += "\n" if value == "ENTER" else value
        return decrypted_message

    def givinglikesanta(self):
        return self.decrypted_message

#########################################################################


