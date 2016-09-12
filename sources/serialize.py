class DomSet:
    def __init__(self, entries):
        if type(entries) is set:
            self.entries = entries

        elif type(entries) is list:
            sets = []
            lel = []
            for entry in entries:
                if type(entry) is set:
                    sets.append(entry)

                elif type(entry) is DomSet:
                    sets.append(entry.entries)

                elif type(entry) is str:
                    lel.append(entry)

                else:
                     raise Exception('Bad type of element {}'.format(type(entry)))

            sets.append(set(lel))
            self.entries = set.union(*sets)

        else:
            raise Exception('Bad type of argument {}'.format(type(entries)))


    def toTxt(self, filename):
        with open(filename, 'w') as f:
            for e in self.entries:
                f.write(e + '\n')

            f.close()

    def __str__(self):
        return '<DomSet entries=' + str(self.entries) + '>'


    def __len__(self):
        return len(self.entries)
