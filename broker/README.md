# Installing the broker

We used mosquitto on Ubuntu 22.04 as our broker. It can be installed using
```bash
sudo apt install mosquitto
```

After installation, create the file `/etc/mosquitto/conf.d/default.conf` with the following contents:
```
listener 1883 0.0.0.0
allow_anonymous true
```

Finally, you can restart the broker using the following command:
```
sudo systemctl restart mosquitto.service
```
