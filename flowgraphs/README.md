# Quick Start

```bash
cp OreSat0.cfg-dist OreSat0.cfg
grcc -u hier/*.grc
grcc OreSat0.grc
./OreSat0.grc
```

* See ```./OreSat0.py -h``` for available arguments.
* By default, this starts up sending TXEnable (sequence # 1) every 5 seconds
  * Use ```-d``` to set a different delay in ms between EDL packets
  * Use ```-e none``` to not automatically send any packets
    * ```echo default= >> OreSat0.cfg``` to do the same without the ```-e``` argument

# A note about netcat
Depending on what version you have, you will need different arguments to immediately
exit after sending a UDP packet. See https://stackoverflow.com/a/75431334/7308581

Assuming you are running GNU netcat, send a ping with:

```xxd -r -p <<<c4f53822000900e501 | nc -cu 127.0.0.1 10025```
