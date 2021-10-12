Enter the name and ip address of the device you want to monitor or the ip address if you want to check your internet connection or monitor a web site. No spaces, you can use an underscore. You can enter a .com if running on a RPi Polyglot however you must use the ip address on Polisy for now.

    Key                       Value
    
    Google                    8.8.8.8           (to ping their dns)
    Google                    www.google.com.   (include the www or the ping will fail)
    Modem                     192.196.196.1
    BlueIris                  192.196.196.105
    Polyglot_2                192.196.196.87


Pinging a url should be used to determine if your internet connection is up or down and not nessecarily to check the status of a website.

After you add a custom parameter hit Save Changes then Restart for your new Parameters to take effect.

The shortPoll is the time between pings, you can change this to suit your needs.

