<template>
    <v-container>
        <!-- row 1 -->
        <v-row>
            <!-- col 1 -->
            <v-col>
                <v-sheet class="pd-2" height="250">
                    <p>Enter date range for Analysis</p>
                    <v-divider></v-divider>
                    <v-text-field label="Start date" class="mr-5" type="Date" density="compact" variant="solo-inverted" flat style="max-width: 300px;" v-model="start"></v-text-field>
                    <v-text-field label="End date" type="Date" density="compact" variant="solo-inverted" flat style="max-width: 300px;" v-model="end"></v-text-field>
                    <v-spacer></v-spacer>
                    <v-btn class="text-caption" text="Analyze" color="primary" variant="tonal" @click="updateLineCharts();updateCards();updateHistogramCharts();updateScatterCharts();"></v-btn>
                </v-sheet>
            </v-col>

        </v-row>
        
        <!-- ROW 2 -->
        <v-row style="max-width: 1200px;">
            <!-- COLUMN 1 -->
            <v-col cols="12">
                <figure class="highcharts-figure">
                    <div id="container"></div>
                </figure>
            </v-col>
            <!-- COLUMN 2 -->
            <v-col cols="12">
                <figure class="highcharts-figure">
                    <div id="container0"></div>
                </figure>
            </v-col>
        </v-row> 
        <!-- ROW 3 -->
        <v-row style="max-width: 1200px;">
            <!-- COLUMN 1 -->
            <v-col style="border: 1;" cols="12">
                <figure class="highcharts-figure">
                    <div id="container1"></div>
                </figure>
            </v-col>
            <!-- COLUMN 2 -->
            <v-col cols="12">
                <figure class="highcharts-figure">
                    <div id="container2"></div>
                </figure>
            </v-col>
            <!-- COLUMN 3 -->
            <v-col cols="12">
                <figure class="highcharts-figure">
                    <div id="container3"></div>
                </figure>
            </v-col>
            <!-- COLUMN 3 -->
            <v-col cols="12">
                <figure class="highcharts-figure">
                    <div id="container4"></div>
                </figure>
            </v-col>
        </v-row>
    </v-container>
</template>
  
<script setup>
/** JAVASCRIPT HERE */
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
import { withDirectives } from "vue";
Exporting(Highcharts);
more(Highcharts);
  
// IMPORTS
 
import { useMqttStore } from "@/store/mqttStore"; // Import Mqtt Store
import { storeToRefs } from "pinia";
  
import { useAppStore } from "@/store/appStore";
import { ref, reactive, watch, onMounted, onBeforeUnmount, computed, } from "vue";
import { useRoute, useRouter } from "vue-router";
  
// VARIABLES
const router        = useRouter();
const route         = useRoute();
const Mqtt          = useMqttStore();
const AppStore      = useAppStore();
const lineChart     = ref(null);        // Line Chart object
const scatterChart  = ref(null);        // Scatter Chart object
var start           = ref(null);
var end             = ref(null);
var reserve         = ref(null);
var temperature     = ref(null);
var humidity        = ref(null);
var heatIndex       = ref(null);
var scatter         = ref(null);
var freqDistroChart = ref(null);
var tempHiChart     = ref(null);
var humiChart       = ref(null);
var tempHiSChart    = ref(null);
var humiHiSChart    = ref(null);


onMounted(() => {
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    CreateCharts();

    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout(() => {
        // Subscribe to each topic
        // Mqtt.subscribe("620151149");
        // Mqtt.subscribe("620151149_sub");
    }, 3000);
});

onBeforeUnmount(() => {
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    // Mqtt.unsubcribeAll();
});

const CreateCharts = async () => {
    // LINE CHART FOR RESERVE VARIABLE
    lineChart.value = Highcharts.chart("container0", {
        chart: { zoomType: "x" },
        title: { text: "Soil Moisture Analysis", align: "left" },
        yAxis: {
            title: { text: "Soil Moisture Content", style: { color: "#000000" } },
            labels: { format: "{value} Percentage" },
        },
    
        tooltip: {
            pointFormat: "Time: {point.x} s <br/> Soil Moisture Content: {point.y} Percentage",
        },
        
        xAxis: {
            type: "datetime",
            title: { text: "Time", style: { color: "#000000" } },
        },
        
        tooltip: { shared: true },
        series: [
            {
                name: "Moisture",
                type: "line",
                data: [],
                turboThreshold: 0,
                color: Highcharts.getOptions().colors[0],
            },
        ],
    });

    tempHiChart.value = Highcharts.chart('container', {
        chart: { zoomType: 'x' },
        title: { text: 'Temperature & Heat Index Analysis', align: 'left' },
        subtitle: { text: 'The heat index, also known as the "apparent temperature," is a measure that combines air temperature and \
        relative humidity to assess how hot it feels to the human body. The relationship between heat index and air temperature is \
        influenced by humidity levels. As humidity increases, the heat  index also rises, making the perceived temperature higher \
        than the actual air temperature.', align: 'left'},
        yAxis: {
            title: { text: 'Air Temperature & Heat Index' , style:{color:'#000000'}},
            labels: { format: '{value} °C' }
        },
        xAxis: {
            type: 'datetime',
            title: { text: 'Time', style:{color:'#000000'} },
            //labels: { format: '{value} °C' }
        },
        tooltip: { 
            shared:true,
            pointFormat: 'Humidity: {point.x} % <br/> Temperature: {point.y} °C' },
        series: [
        {
            name: 'Temperature',
            type: 'spline',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[0]
        },
        {
            name: 'Heat Index',
            type: 'spline',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[1]
        } ],
    });
    // HUMIDITY CHART
    humiChart.value = Highcharts.chart('container4', {
        chart: { zoomType: 'x' },
        title: { text: 'Humidity Analysis', align: 'left' },
        // subtitle: { text: 'Visualize the relationship between Temperature and Heat Index as well as revealing patterns or trends in the data'},
        yAxis: {
            title: { text: 'Air Temperature & Heat Index' , style:{color:'#000000'}},
            labels: { format: '{value} %' }
        },
        xAxis: {
            type: 'datetime',
            title: { text: 'Time', style:{color:'#000000'} },
            //labels: { format: '{value} °C' }
        },
        tooltip: { 
            shared:true, 
            pointFormat: 'Humidity: {point.x} % <br/> Temperature: {point.y} °C'
        },
        series: [
        {
            name: 'Humidity',
            type: 'spline',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[0]
        }],
    });
    // FREQUENCY DISTRIBUTION CHART
    freqDistroChart.value = Highcharts.chart('container1', {
        chart: { zoomType: 'x' },
        title: { text: 'Frequency Distribution Analysis', align: 'left' },
        // subtitle: { text: 'Visualize the relationship between Temperature and Heat Index as well as revealing patterns or trends in the data'},
        yAxis: {
            title: { text: 'Frequency' , style:{color:'#000000'}},
            labels: { format: '{value}' }
        },
        xAxis: {
            //type: 'datetime',
            title: { text: 'Values', style:{color:'#000000'} },
            //labels: { format: '{value} °C' }
        },
        tooltip: { 
            shared:true, 
            //pointFormat: 'Humidity: {point.x} % <br/> Temperature: {point.y} °C'
        },
        series: [
        {
            name: 'Temperature',
            type: 'column',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[0]
        },
        {
            name: 'Humidity',
            type: 'column',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[1]
        },
        {
            name: 'Heat Index',
            type: 'column',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[2]
        } ],
    });
    // TEMPERATURE AND HEAT INDEX SCATTER CHART
    tempHiSChart.value = Highcharts.chart('container2', {
        chart: { zoomType: 'x' },
        title: { text: 'Temperature & Heat Index Correlation Analysis', align: 'left'},
        subtitle: { text: 'Visualize the relationship between Temperature \
        and Heat Index as well as revealing patterns or trends in the data', align: 'left'},
        yAxis: {
            title: { text: 'Heat Index' , style:{color:'#000000'}},
            labels: { format: '{value} °C' }
        },
        xAxis: {
            type: 'datetime',
            title: { text: 'Temperature', style:{color:'#000000'} },
            labels: { format: '{value} °C' }
        },
        tooltip: { 
            shared:true, 
            pointFormat: 'Temperature: {point.x} °C <br/> Heat Index: {point.y} °C' },
        series: [
        {
            name: 'Analysis',
            type: 'scatter',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[0]
        }]
    });
    // HUMIDITY AND HEAT INDEX SCATTER CHART
    humiHiSChart.value = Highcharts.chart('container3', {
        chart: { zoomType: 'x' },
        title: { text: 'Humidity & Heat Index Correlation Analysis', align: 'left' },
        subtitle: { text: 'Visualize the relationship between Humidity\
         and Heat Index as well as revealing patterns or trends in the data', align: 'left'},
        yAxis: {
            title: { text: 'Heat Index' , style:{color:'#000000'}},
            labels: { format: '{value} °C' }
        },
        xAxis: {
            //type: 'datetime',
            title: { text: 'Humidity', style:{color:'#000000'} },
            labels: { format: '{value} %' }
        },
        tooltip: { 
            shared:true, 
            pointFormat: 'Humidity: {point.x} % <br/> Heat Index: {point.y} °C'
        },
        series: [
        {
            name: 'Analysis',
            type: 'scatter',
            data: [],
            turboThreshold: 0,
            color: Highcharts.getOptions().colors[1]
        } ],
    });
  
};
  
// FUNCTIONS
const updateCards = async () => {
    if (!!start.value && !!end.value) {
        // 1. Convert start and end dates collected fron TextFields to 10 digit timestamps
        let startDate = new Date(start.value).getTime() / 1000;
        let endDate = new Date(end.value).getTime() / 1000;
        // 2. Fetch data from backend by calling the API functions
        const Gallon = await AppStore.update_Card(startDate, endDate);
        console.log(Gallon[0].average.toFixed(1));
        reserve.value = Gallon[0].average.toFixed(1);
    }
};
  
const updateLineChart = async () => {
    if (!!start.value && !!end.value) {
        // Convert output from Textfield components to 10 digit timestamps
        let startDate = new Date(start.value).getTime() / 1000;
        let endDate = new Date(end.value).getTime() / 1000;
        // Fetch data from backend
        const data = await AppStore.getReserve(startDate, endDate);
        // Create arrays for each plot
        let reserve = [];
        let scatter = [];
        // Iterate through data variable and transform object to format recognized by highcharts
        data.forEach((row) => {
        reserve.push({
            x: row.timestamp * 1000,
            y: parseFloat(row.reserve.toFixed(2)),
        });
        });
        data.forEach((row) => {
        scatter.push({
            x: parseFloat(row.waterheight.toFixed(2)),
            y: parseFloat(row.radar.toFixed(2)),
        });
        });
        // Add data to line and scatter chart
        lineChart.value.series[0].setData(reserve);
        scatterChart.value.series[0].setData(scatter);
    }
};
</script>

<style scoped>
/** CSS STYLE HERE */
</style>