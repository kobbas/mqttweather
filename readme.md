This is an implementation for the Makerlife Weatherstation to push data via MQTT to for example Homeassistant. To get it work with homeassistant a MQTT broker has to be configured and filled in to the code. Also some the sensors has to be added to HA. 

The data is pushed every 5 min. The time to can be changed if interval time is changed. The wind measurement is done per 20 secoconds and 15 rounds for each publish.

Example of configuration.yaml:
```yaml
sensor:
  - platform: mqtt
    state_topic: "outside/weather/"
    icon: mdi:weather-windy
    name: 'Windspeed'
    unit_of_measurement: 'm/s'
    value_template: '{{ value_json.windspeed | round(1) }}'
  - platform: mqtt
    state_topic: "outside/weather/"
    icon: mdi:thermometer-lines
    name: 'Temperaure'
    unit_of_measurement: '°C'
    value_template: '{{ value_json.temperature | round(1) }}'
  - platform: mqtt
    state_topic: "outside/weather/"
    icon: mdi:weather-rainy
    name: 'Rain'
    unit_of_measurement: 'mm'
    value_template: '{{ value_json.rain | round(1) }}'
```

Edit the scirpt with your MQTT broker IP and Pass. <br>

Login to the you raspi via SSH. Start the script with:<br>
`nohup python weather.py &` <br>
This enables to logut from the pi without closing the down the script.
 
