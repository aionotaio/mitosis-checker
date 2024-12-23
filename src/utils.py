class Utils:
    @staticmethod
    def read_strings_from_file(path: str) -> list:
        strings = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    strings.append(line)
        return strings
    