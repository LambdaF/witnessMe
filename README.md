# witnessMe
Parse `gnmap` output for (non)standard http(s) ports and print them as a URL.

Useful for passing to other tools such as GoWitness or GoBuster.

## Example usage
### Input command
```
python3 witnessMe.py -i input.gnmap
```
### Example output (stdout)
```
https://127.0.0.1:443
http://127.0.0.1:80
https://127.0.0.1:8443
http://127.0.0.1:65535
```
