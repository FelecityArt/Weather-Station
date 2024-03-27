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
      <v-container fluit class="bg-surface outside-img" align="center">
      <v-row>
        <v-col cols="9">
          <figure class="highcharts-figure">
            <div id="container"></div>
          </figure>
        </v-col>
        <v-col cols="3">
            </v-col>
        </v-row>
        <!-- ROW 2 -->
        <v-row>
            <!-- COLUMN 1 -->
            <v-col cols="9">
              <figure class="highcharts-figure">
                    <div id="container1"></div>
                </figure>
            </v-col>
        </v-row>
    </v-container>
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
  
  const payload = ref(null);
  
  // VARIABLES
  const Mqtt        = useMqttStore();
  const AppStore    = useAppStore();
  const router      = useRouter();
  const route       = useRoute();
  const soilChart     = ref(null);
  const tempHiChart = ref(null);
  const humiChart = ref(null);
  const points = ref(10);
  const shift = ref(false);

// WATCHERS
watch(Mqtt.cardData, (data) => {
  console.log(Mqtt.cardData.value.temperature, data.timestamp);
  if (points.value > 0) {
    points.value--;
  } else {
    shift.value = true;
  }

  const currentTime = new Date().getTime();

  soilChart.value.series[0].addPoint(
    {
      y: parseFloat(Mqtt.cardData.value.soil),
      x: currentTime,
    },
    true,
    shift.value
  );

  tempHiChart.value.series[0].addPoint(
    {
      y: parseFloat(Mqtt.cardData.value.temperature),
      x: currentTime,
    },
    true,
    shift.value
  );

  tempHiChart.value.series[1].addPoint(
    {
      y: parseFloat(Mqtt.cardData.value.heatindex),
      x: currentTime,
    },
    true,
    shift.value
  );

  humiChart.value.series[0].addPoint(
    {
      y: parseFloat(Mqtt.cardData.value.humidity),
      x: currentTime,
    },
    true,
    shift.value
  );
});

  // FUNCTIONS
  onMounted(() => {
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    Mqtt.connect();
    CreateCharts();
    // Mqtt.connect(); // Connect to Broker located on the backend
    // setTimeout(() => {
    //   // Subscribe to each topic
    //   Mqtt.subscribe("620151149");
    //   Mqtt.subscribe("620151149_sub");
    // }, 3000);
  });
    
  onBeforeUnmount(() => {
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    // Mqtt.unsubcribeAll();
  });

  const CreateCharts = async () => {
    // AREA GRAPH FOR RESERVE VARIABLE:
    soilChart.value = Highcharts.chart("container0", {
        chart: { zoomType: "x" },
        title: { text: "Soil Moisture Analysis (Live)", align: "left" },
        yAxis: {
            title: { text: "Soil Moisture Content", style: { color: "#000000" } },
            labels: { format: "{value}" },
        },
        xAxis: {
            type: "datetime",
            title: { text: "Time", style: { color: "#000000" } },
        },
        tooltip: { shared: true },
        series: [
            {
                name: "Moisture",
                type: "area",
                data: [],
                turboThreshold: 0,
                color: Highcharts.getOptions().colors[1],
            },
        ],
    });
// TEMPERATURE CHART
tempHiChart.value = Highcharts.chart("container", {
      chart: { zoomType: "x" },
      title: { text: "Temperature Analysis (Live)", align: "left" },
      yAxis: {
        labels: { format: "{value} °C" },
      },
      xAxis: {
        type: "datetime",
        title: { text: "Time", style: { color: "#000000" } },
      },
      tooltip: { shared: true },
      series: [
        {
          name: "Temperature",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[0],
        },
        {
          name: "Heat Index",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[1],
        },
      ],
    });

    // HUMIDITY CHART
    humiChart.value = Highcharts.chart("container1", {
      chart: { zoomType: "x" },
      title: { text: "Humidity Analysis (Live)", align: "left" },
      yAxis: {
        labels: { format: "{value}" },
      },
      xAxis: {
        type: "datetime",
        title: { text: "Time", style: { color: "#000000" } },
      },
      tooltip: { shared: true },
      series: [
        {
          name: "Humidity",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[1],
        },
      ],
    });
  }
 
  </script>

  <style scoped>
    figure {
    border: 2px solid black;
  }
  .outside-img {
    background: url('../assets/outside.jpg');
    background-size: cover;
}
  </style>