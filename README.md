# pokebox

[Fing](https://www.fing.io) is a mobile app that allows you to easily scan your current WiFi network from your device.

More recently they launched a device, [Fingbox](https://www.fing.io/fingbox-network-security-appliance/), as a way to continuously monitor your network.  
I found this a useful idea, though, having a couple of Raspberry Pis running, why buy yet another device?

Hence, *PokeBox* comes into picture, a dockerized-application that will continuously scan your network and send you notifications when things change.


### Setup

* `docker run --name pokebox -v pokedata:/var/dbdata -p8080:8080 fopina/pokebox`
* Create the admin user if you haven't before `docker exec pokebox /var/app/manage.py createuser`
