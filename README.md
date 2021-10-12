# Ping Node Server

#### What does this do?

This will ping devices on your lan or a .com. If a device does not respond it will be reported as In Fault until it hits 5 faults and then it's reported as Off Network. You can keep tabs on your devices, router, modem, internet connection, etc. and program an ISY controlled switch to cycle Off then On to reset the device or send yourself a notification.

#### Known Issues:

If you are pinging an external url and your modem or internet service goes down and you are running Ping on Polisy it is highly likely that Ping will crash. This problem doesn't appear to exist on a Raspberry Pi installation.

On Polisy ping the ip address only. To determine the ip address from a url you can open a terminal window and execute the command:

ping yoururl.com

Note the ip address and use that to Ping.

1.0.2 Minor bug fix

1.0.3 Fixed crash when external ip is unreachable or modem is down

1.0.5 Works on Polisy now, use ip instead of the domain name. Ex. 8.8.8.8 for Google

1.0.8 Standardize url input for RPi and Polisy, <www.url.com>

1.0.9 Set all as On Network on restart.

1.0.10 Increased missed pings to 1440 max instead of 5, Off network count still 5 missed pings.

1.0.11 Better error handling.

1.0.12 Fixed a bug that would not show Scanning True after setting to off. Added extra debug logging option.

1.0.13 Minor bug fix.

1.0.14 Added visible Query command button on controller page

1.0.15 Fixed bug with Polisy 2.2.11
