<template>
    <v-container class="container" justify="center" align="center">
      <v-row justify="center">
        <v-col justify="left" cols="11">
          <v-sheet>
            <figure class="highcharts-figure">
              <div id="container0"></div>
            </figure>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </template>
    
  <script setup>
  /** JAVASCRIPT HERE */
  
  // IMPORTS
  import { ref, reactive, watch, onMounted, onBeforeUnmount, computed, } from "vue";
  import { useRoute, useRouter } from "vue-router";
  import { useAppStore } from "@/store/appStore";
  import { useMqttStore } from "@/store/mqttStore"; // Import Mqtt Store
  import { storeToRefs } from "pinia";

  // Highcharts, Load the exporting module and Initialize exporting module.
  import Highcharts from "highcharts";
  import more from "highcharts/highcharts-more";
  import Exporting from "highcharts/modules/exporting";
  Exporting(Highcharts);
  more(Highcharts);
  
  
  // VARIABLES
  const Mqtt        = useMqttStore();
  const AppStore    = useAppStore();
  const router      = useRouter();
  const route       = useRoute();
  const areaGraph     = ref(null);
  
  
  // FUNCTIONS
  onMounted(() => {
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    
    CreateCharts();
    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout(() => {
      // Subscribe to each topic
      Mqtt.subscribe("620151149");
      Mqtt.subscribe("620151149_sub");
    }, 3000);
  });
    
  onBeforeUnmount(() => {
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    Mqtt.unsubcribeAll();
  });

  const CreateCharts = async () => {
    // AREA GRAPH FOR RESERVE VARIABLE:
    areaGraph.value = Highcharts.chart("container0", {
        chart: { zoomType: "x" },
        title: { text: "Water Reserves (10 min)", align: "left" },
        yAxis: {
            title: { text: "Water Level", style: { color: "#000000" } },
            labels: { format: "{value} Gal" },
        },
        xAxis: {
            type: "datetime",
            title: { text: "Time", style: { color: "#000000" } },
        },
        tooltip: { shared: true },
        series: [
            {
                name: "Water",
                type: "area",
                data: [],
                turboThreshold: 0,
                color: Highcharts.getOptions().colors[0],
            },
        ],
    });
  }
  
  </script>
  
  <style scoped>
    figure {
    border: 2px solid black;
  }
  </style>