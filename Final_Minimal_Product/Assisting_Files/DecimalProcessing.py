"""Original TABS decimal packing with variable chunk bit widths."""

class endecimalprocessing:
    def __init__(self, decimal, chunksize=10, check_bytelen=True, optimization=True):
        self.ideal = None
        self.decimal_list = [num + 1 for num in decimal]
        self.decimal = {1: 2, 2: 4, 3: 8, 4: 16, 5: 32, 6: 64, 7: 128, 8: 256, 9: 512, 10: 1024}
        self.decimalprocessing(chunksize)

        if optimization:
            if check_bytelen:
                self.check_chunklen()
                self.decimalprocessing(self.ideal)
            else:
                self.decimalprocessing(chunksize)
        else:
            self.eninefficientgarbage()

    def eninefficientgarbage(self):
        binarystring = ""
        bytelen = 0

        for i in self.decimal_list:
            if self.classify(i) > bytelen:
                bytelen = self.classify(i)
        binarystring += self.decimal_to_binary(15, bytelen=4)
        binarystring += self.decimal_to_binary(bytelen, bytelen=4)

        for i in self.decimal_list:
            binarystring += self.decimal_to_binary(i, bytelen=bytelen)
        self.binary_string = binarystring


    def check_chunklen(self):
        ideal = None
        ideallen = len(self.decimal_list) * 20
        for i in range(3, 25):
            temp = len(self.decimalprocessing(i))
            if temp < ideallen or ideallen is None:
                ideal = i
                ideallen = temp
        self.ideal = ideal

    def classify(self, value):
        for i in self.decimal:
            if value < self.decimal[i]:
                return i

    def santa(self):
        return self.binary_string

    def decimal_to_binary(self, decimal, bytelen=7):
        binrep = bin(decimal)[2:]
        binrep = binrep.zfill(bytelen)
        return binrep

    def worth_it(self, current_bytelen, maxinchunk_bytelen, chunksize):
        if maxinchunk_bytelen > current_bytelen:
            return True
        calculation = (current_bytelen - maxinchunk_bytelen) * chunksize - current_bytelen - 4
        return True if calculation > 0 else False

    def decimalprocessing(self, chunksize):
        if self.ideal is not None:
            chunksize = self.ideal

        binarystring = ""
        previous = 7

        if self.worth_it(current_bytelen=previous, maxinchunk_bytelen=self.classify(max(self.decimal_list[0:chunksize])), chunksize=chunksize):
            binarystring += self.decimal_to_binary(decimal=self.classify(max(self.decimal_list[0:chunksize])), bytelen=4)
            previous = self.classify(max(self.decimal_list[0:chunksize]))
        else:
            binarystring += self.decimal_to_binary(previous, bytelen=4)
        for j in range(0, len(self.decimal_list), chunksize):
            chunk = self.decimal_list[j:j + chunksize]
            chunkmax = max(chunk)
            if self.worth_it(current_bytelen=previous, maxinchunk_bytelen=self.classify(chunkmax), chunksize=chunksize):
                binarystring += self.decimal_to_binary(0, bytelen=previous)
                binarystring += self.decimal_to_binary(self.classify(chunkmax), bytelen=4)
                previous = self.classify(chunkmax)
            for dec in range(0, chunksize):
                if j + dec == len(self.decimal_list):
                    break
                binarystring += self.decimal_to_binary(self.decimal_list[j + dec], bytelen=previous)
        self.binary_string = binarystring
        return binarystring


class dedecimalprocessing:
    def __init__(self, binarystring, file=None):
        self.binarystring = binarystring
        if file:
            self.binarystring = self.getdatafromfile(file=file)
        binarystring = self.binarystring.strip()
        if len(binarystring) < 5 or set(binarystring) - {"0", "1"}:
            raise ValueError("Enter a complete TABS binary string containing only 0 and 1.")
        dedecimalprocessing.dedecimalprocessing(self, binarystring)

    def getdatafromfile(self, file):
        with open(file, "r") as f:
            return f.read()

    def unsorted_binary_to_decimal(self, binarystring):
        return int(binarystring, 2)

    def santa(self):
        return [num - 1 for num in self.decimal_list]

    def deinefficientgarbage(self, binarystring):
        decimal_list = []
        bytelen = self.unsorted_binary_to_decimal(binarystring[:4])
        if not 1 <= bytelen <= 10 or (len(binarystring) - 4) % bytelen:
            raise ValueError("Invalid or incomplete TABS binary data.")
        for i in range(4, len(binarystring), bytelen):
            chunk = binarystring[i:i + bytelen]
            decimal = self.unsorted_binary_to_decimal(chunk)
            decimal_list.append(decimal)
        self.decimal_list=decimal_list
        return decimal_list

    def dedecimalprocessing(self, binarystring):
        decimal_list = []
        idx = 0
        bytelen = self.unsorted_binary_to_decimal(binarystring[idx:idx + 4])
        if bytelen == 15:
            self.deinefficientgarbage(binarystring[4:])
        else:
            if not 1 <= bytelen <= 10:
                raise ValueError("Invalid TABS bit width.")
            idx += 4
            while idx < len(binarystring):
                chunk = binarystring[idx:idx + bytelen]
                if not chunk:
                    break
                if len(chunk) != bytelen:
                    raise ValueError("Incomplete TABS binary data.")
                decimal = self.unsorted_binary_to_decimal(chunk)
                if decimal == 0:
                    idx += bytelen
                    if idx + 4 > len(binarystring):
                        raise ValueError("Incomplete TABS bit width.")
                    bytelen = self.unsorted_binary_to_decimal(binarystring[idx:idx + 4])
                    if not 1 <= bytelen <= 10:
                        raise ValueError("Invalid TABS bit width.")
                    idx += 4
                else:
                    decimal_list.append(decimal)
                    idx += bytelen
            self.decimal_list=decimal_list

