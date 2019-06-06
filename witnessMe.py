#!/bin/python3
import argparse
import re


class Host():
    """
    Represents a given host in a gnmap file
    """

    class HTTPPort():
        """
        Represents a port and it's "http type" e.g. https or http
        """

        def __init__(self, httpType, portNum):
            self.type = httpType
            self.portNum = portNum

    def __init__(self):
        self.IP = ""
        self.ports = []

    def parseGnmap(self, gnmap):
        """
        Parse a single line of gnmap input
        """

        # Get the IP from the 2nd column
        hostSplit = gnmap.split(' ')
        self.IP = hostSplit[1]

        """
        Find the term "Ports: ",
        which dictates the start of ports in the string
        """
        frontTrim = gnmap.find("Ports: ")
        if frontTrim == -1:
            return
        frontTrim += 7  # length of "Ports: "

        """
        Sometimes "Ignored State" is on the end of the string and should be stripped
        """
        backTrim = gnmap.find("Ignored State")
        if backTrim == -1:
            # If not there, just sent to the end of the string
            backTrim = len(gnmap)

        # Trim string to just the ports
        ports = gnmap[frontTrim:backTrim]
        ports = ports.strip()
        ports = ports.split(',')

        for port in ports:
            port = port.strip()
            if "http" in port:
                portNum = re.match(r"([0-9]{1,5})", port).group(0)
                if "https" in port or "ssl" in port:
                    self.ports.append(self.HTTPPort("https", portNum))
                else:
                    self.ports.append(self.HTTPPort("http", portNum))

    def prettyPrint(self):
        """
        Print output to stdout in the form:
        {http type}://{IP address}:{port number}
        """
        for port in self.ports:
            print(f"{port.type}://{self.IP}:{port.portNum}")


def main(inputName):
    """
    Open and parse gnmap, drop comment lines, create host objects
    """
    with open(inputName, 'r') as f:
        for line in f:
            line = line.strip()
            if '#' in line or "Status" in line:
                continue
            host = Host()
            host.parseGnmap(line)
            host.prettyPrint()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Parse gnmap output for (non)standard http(s) ports"
        " and print them as a URL"
    )
    parser.add_argument(
        "-i", "--input",
        help="Input gnmap file to parse out",
        required=True
    )
    args = parser.parse_args()

    main(args.input)
