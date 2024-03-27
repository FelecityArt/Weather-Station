import { defineStore } from "pinia";
import {ref , reactive} from 'vue'
import mqtt from 'mqtt'

export const useMqttStore = defineStore('mqtt_store', () => {

    const url = 'ws://broker.emqx.io:8083/mqtt'
    const client = ref(null);
    const newCardData = reactive({})

    const options = {
        clean: true,
      }


    function disconnect(){
        if(client.value!=null){
            client.value.end()
        }
    }

    function connect(){
        console.log('Connecting...')
        client.value  = mqtt.connect(url, options)
        client.value.on('connect', function () {
            console.log('Connected')
            // Subscribe to a topic
            client.value.subscribe('demo', function (err) {
              if (!err) {
                // Publish a message to a topic
                client.value.publish('demo', 'Hello mqtt')
              }
            })
          
          })

          client.value.on('disconnect', function (packet) {
            console.log('disconnected')
          })
        
          client.value.on('message', function (topic, message) {
            // message is Buffer
            console.log(message.toString())
            if(topic=='demo'){
                try{
                    newCardData.value = JSON.parse(message.toString())
                    console.log(newCardData.value.temperature)
                } catch (e){
                    console.log(e)
                }
                
            }
          })
          
    }

    // connect();
    return { connect , newCardData , disconnect}
  })