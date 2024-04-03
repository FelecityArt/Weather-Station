import { defineStore } from "pinia";
import { ref, reactive } from 'vue';
import mqtt from 'mqtt';

export const useMqttStore = defineStore('mqttStore', () => {
  const brokerUrl = 'ws://broker.emqx.io:8083/mqtt';
  const mqttClient = ref(null);
  const cardData = reactive({});

  const connectionOptions = {
    clean: true,
  };

  function connect() {
    console.log('Connecting...');
    mqttClient.value = mqtt.connect(brokerUrl, connectionOptions);
    mqttClient.value.on('connect', function () {
      console.log('Connected');
      mqttClient.value.subscribe('demo', function (err) {
        if (!err) {
          mqttClient.value.publish('demo', 'Hello mqtt');
        }
      });
    });

    mqttClient.value.on('disconnect', function () {
      console.log('Disconnected');
    });

    mqttClient.value.on('message', function (topic, message) {
      console.log(message.toString());
      if (topic == 'demo') {
        const msg = message.toString();
        try {
          if (IsJsonString(msg)) {
            cardData.value = JSON.parse(msg);
            console.log(cardData.value.temperature);
          }
        } catch (error) {
          console.log(error);
        }
      }
    });
    
    function IsJsonString(str) {
      try {
        JSON.parse(str);
      } catch (e) {
        return false;
      }
      return true;
    }
  }

  function disconnect() {
    if (mqttClient.value != null) {
      mqttClient.value.end();
    }
  }

  return { connect, cardData, disconnect };
});