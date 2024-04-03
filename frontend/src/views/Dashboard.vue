<template>
    <v-container>
        <v-container class="values">
            <v-row class="rounded-border fill-height">
                <!-- col 1 -->
                <v-col justify="center" cols="3">
                    <v-card class="mb-5 altitude outlined altitude-img">
                    <v-card-text class="text-center">
                        <v-icon left>mdi-map-marker</v-icon>
                        Mona, Kingston
                    </v-card-text>
                    <v-sheet>
                        <v-slider class="altitude-img" direction="vertical" v-model="altitude" :max="altitudeUnit === 'm' ? 1000 : 3280" :min="0" step="1" thumb-label="always" color="white" :label="`Altitude (${altitudeUnit})`" track-size="60"></v-slider>
                    </v-sheet>
                    <v-card-actions class="no-background">
                        <v-select
                        v-model="altitudeUnit"
                        :items="['m', 'ft']"
                        :item-text="itemText"
                        ></v-select>
                    </v-card-actions>
                    </v-card>
                </v-col>

                <v-col justify="center" cols="3">
                    <v-card class="mb-5 temperature temperature-img" outlined>
                        <v-card-text class="text-center">
                            <v-icon left>mdi-thermometer</v-icon>
                            Temperature
                            <v-spacer></v-spacer>
                            <div class="display-1" v-text="`${temperature}`"></div>
                        </v-card-text>
                        <v-card-item>
                            <v-select 
                            v-model="tempUnit"
                            :items="['°C', '°F']"
                            :item-text="itemText"
                            ></v-select>
                            <div class="display-1" v-text="`${temperature}${tempUnit}`"></div>
                        </v-card-item>
                    </v-card>
                </v-col>

                <v-col justify="center" cols="3">
                    <v-card class="mb-5 heat-index heat-index-img" outlined>
                        <v-card-text class="text-center">
                            <v-icon left>mdi-thermometer-alert</v-icon>
                            Heat Index
                            <v-spacer></v-spacer>
                            <div class="display-2" v-text="`${heatindex}`"></div>
                        </v-card-text>
                        <v-select 
                        v-model="heatUnit"
                        :items="['°C', '°F']"
                        :item-text="itemText"
                        ></v-select>
                    </v-card>
                </v-col>

                <v-col justify="center" cols="3">
                    <v-card class="mb-5 humidity humidity-img" outlined>
                        <v-card-text class="text-center">
                            <v-icon left>mdi-water-percent</v-icon>
                            Humidity
                            <v-spacer></v-spacer>
                            <div class="display-3" v-text="`${humidity}%`"></div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
        <!-- row 2 -->
        <v-row>
            <!-- col 1 -->
            <v-col cols="8">
                <v-sheet>
                    <figure class="highcharts-figure">
                        <div id="container1"></div>
                    </figure>
                </v-sheet>
            </v-col>

            <!-- col 2 -->
            <v-col cols="4">
                <v-sheet max-width="350px">
                    <v-card class="mb-5" style="max-width: 350px" variant="outlined" color="primary" density="compact" rounded="lg" title="Soil Moisture" subtitle="Capacity Remaining">
                        <div id="container2"></div>
                    </v-card>
                </v-sheet>
            </v-col>
        </v-row>

        <v-dialog width="500" v-model="isActive">
            <template v-slot:default="{ isActive }">
                <v-card title="WARNING !" color="warning" background-color="primary darken-1">
                    <v-card-text>Tank is over maximum capacity. Open overflow valve now to resolve issue.</v-card-text> 
                    <v-card-actions>
                        <v-spacer></v-spacer>
                    </v-card-actions>
                </v-card>
            </template>
        </v-dialog>
    </v-container>
</template>
  
<script setup>
/** JAVASCRIPT HERE */
  
// IMPORTS
import { useMqttStore } from "@/store/mqttStore"; // Import Mqtt Store
import { storeToRefs } from "pinia";
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
import { ref, reactive, watch, onMounted, onBeforeUnmount, computed, } from "vue";
import { useRoute, useRouter } from "vue-router";

const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);
  
// Highcharts, Load the exporting module and Initialize exporting module.

Exporting(Highcharts);
more(Highcharts);
  
// VARIABLES
const router        = useRouter();
const route         = useRoute();
const areaGraph     = ref(null);    // areaGraph object
const altitude      = ref(0);
const pressureGauge = ref(null); 
const percentage    = ref(null);
const points        = ref(600);
const shift         = ref(false);
const soil          = ref(null);
const heatindex     = ref(null);
const humidity      = ref(null);
const altitudeUnit  = ref('m');
var isActive        = ref(null);
var radar           = ref(null);
var fm              = new FluidMeter();

defineExpose({
  altitude
});

onMounted(() => {
    // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    CreateCharts();

    Mqtt.connect();
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



// WATCHERS
watch(Mqtt.cardData, (data) => {
    console.log(Mqtt.cardData.value.temperature, data.timestamp);
    if (points.value > 0) {
        points.value--;
    } else {
        shift.value = true;
    }


    
    const currentTime = new Date().getTime();

    console.log(Mqtt.cardData.value.pressure);
    const pressure = parseFloat(Mqtt.cardData.value.pressure);

    // Check if the value is a number before updating the gauge
    if (!isNaN(pressure)) {
        pressureGauge.value.series[0].setData([pressure], true);
    }


    console.log(Mqtt.cardData.value.altitude);
    let altitudeValue = parseFloat(Mqtt.cardData.value.altitude);

    // Check if the value is a number before updating the altitude
    if (!isNaN(altitudeValue)) {
        altitude.value = altitudeValue;
        console.log('Updated altitude:', altitude.value);
    }


    console.log(Mqtt.cardData.value.heatindex);
    let heatIndexValue = parseFloat(Mqtt.cardData.value.heatindex);
    // Check if the value is a number before updating the heat index
    if (!isNaN(heatIndexValue)) {
        heatindex.value = heatIndexValue;
        console.log('Updated heat index:', heatindex.value);
    }


    console.log(Mqtt.cardData.value.humidity);
    let humidityValue = parseFloat(Mqtt.cardData.value.humidity);
    // Check if the value is a number before updating the humidity
    if (!isNaN(humidityValue)) {
        humidity.value = humidityValue;
        console.log('Updated humidity:', humidity.value);
    }


    console.log(Mqtt.cardData.value.temperature);
    let temperatureValue = parseFloat(Mqtt.cardData.value.temperature);
    // Check if the value is a number before updating the temperature
    if (!isNaN(temperatureValue)) {
        temperature.value = temperatureValue;
        console.log('Updated temperature:', temperature.value);
    }


    console.log(Mqtt.cardData.value.soil);
    let soilValue = parseFloat(Mqtt.cardData.value.soil);
    // Check if the value is a number before updating the soil
    if (!isNaN(soilValue)) {
        // Calculate the soil moisture percentage
        let soilPercentage = 100 - ((soilValue / 4095.0) * 100.0);
        soil.value = soilPercentage;
        console.log('Updated soil:', soil.value);
        // Update the fillPercentage property of the FluidMeter object
        fm.setPercentage(soil.value);
    }
});

const tempUnit = ref('°C')
const heatUnit = ref('°C')
const temperature = ref(0) // initial temperature in Celsius

watch(tempUnit, (value) => {
    console.log('Temp unit:', value);
    if (value === '°C') {
        temperature.value = parseFloat((temperature.value - 32) / 1.8).toFixed(2);
    } else {
        temperature.value = parseFloat((temperature.value * 1.8 + 32).toFixed(2));
    }
});

watch(heatUnit, (value) => {
    console.log('Heat unit:', value);
    if (value === '°C') {
        heatindex.value = parseFloat((heatindex.value - 32) / 1.8).toFixed(2);
    } else {
        heatindex.value = parseFloat((heatindex.value * 1.8 + 32).toFixed(2));
    }
});

watch(altitudeUnit, (value) => {
    console.log('Altitude unit:', value);
    if (value === 'm') {
        altitude.value = parseFloat(altitude.value / 3.28084).toFixed(2);
    } else {
        altitude.value = parseFloat(altitude.value * 3.28084).toFixed(2);
    }
});

const itemText = (item) => {
    return item === '°C' ? '°C' : '°F';
};

// FUNCTIONS
const CreateCharts = async () => {
    

    // GAUGE GRAPH FOR RESERVE VARIABLE:
    pressureGauge.value = Highcharts.chart("container1", {
        title: { text: "Pressure", align: "left" },
        yAxis: { 
            min: 0,
            max: 150000,
            tickPixelInterval: 72,
            tickPosition: "inside",
            tickColor: Highcharts.defaultOptions.chart.backgroundColor || "#FFFFFF",
            tickLength: 20,
            tickWidth: 2,
            minorTickInterval: null,
            labels: { distance: 20, style: { fontSize: "14px" } },
            lineWidth: 0,
            plotBands: [
                { from: 0, to: 20000, color: "#DF5353", thickness: 20 },
                { from: 20000, to: 60000, color: "#DDDF0D", thickness: 20 },
                { from: 60000, to: 120000, color: "#55BF3B", thickness: 20 },
                { from: 120000, to: 150000, color: "#DF5353", thickness: 20 },
            ],
        },
        tooltip: { shared: true },
        pane: {
            startAngle: -90,
            endAngle: 89.9,
            background: null,
            center: ["50%", "75%"],
            size: "110%",
        },
        series: [
            {
                type: "gauge",
                name: "Pressure",
                data: [0],
                tooltip: { valueSuffix: " Pa" },
                dataLabels: {
                    format: "{y} Pa",
                    borderWidth: 0,
                    color: (Highcharts.defaultOptions.title && Highcharts.defaultOptions.title.style && Highcharts.defaultOptions.title.style.color) || "#333333",
                    style: { fontSize: "16px" },
                },
                dial: {
                    radius: "80%",
                    backgroundColor: "gray",
                    baseWidth: 12,
                    baseLength: "0%",
                    rearLength: "0%",
                },
                pivot: { backgroundColor: "black", radius: 6 },
            },
        ],
    });

    fm.init({
        targetContainer: document.getElementById("container2"),
        fillPercentage: soil.value,
        options: {
            fontSize: "70px",
            fontFamily: "Arial",
            fontFillStyle: "white",
            drawShadow: true,
            drawText: true,
            drawPercentageSign: true,
            drawBubbles: true,
            size: 300,
            borderWidth: 25,
            backgroundColor: "#A2D9CE",
            foregroundColor: "#fafafa",
            foregroundFluidLayer: {
                fillStyle: "purple",
                angularSpeed: 100,
                maxAmplitude: 12,
                frequency: 30,
                horizontalSpeed: -150,
            },
            backgroundFluidLayer: {
                fillStyle: "pink",
                angularSpeed: 100,
                maxAmplitude: 9,
                frequency: 30,
                horizontalSpeed: 150,
            },
        },
    });
};
</script>

<script>

// temperature.value = computed(() => {
//     if (tempUnit.value === '°C') {
//         return temperature.value;
//     } else {
//         return parseFloat((temperature.value * 1.8 + 32).toFixed(2));
//     }
// });
</script>

<style scoped>
/** CSS STYLE HERE */
figure {
    border: 2px solid black;
}

.rounded-border {
    border: 2px solid black;
    border-radius: 10px;
}

.display-1, .display-2, .display-3{
    font-size: 36px;
    padding-top: 70px;
}

.temperature, .heat-index, .humidity {
    height: 225px;
}

.altitude-img {
    background: url('../assets/altitude.jpg');
    background-size: cover;
}

.temperature-img {
    background: url('../assets/temperature.jpg');
    background-size: cover;
}

.heat-index-img {
    background: url('../assets/heat-index.jpg');
    background-size: cover;
}

.humidity-img {
    background: url('../assets/humidity.jpg');
    background-size: cover;
}

.no-background {
    background: none !important;
    display: flex;
    justify-content: center;
    align-items: center;
}

.button {
    background-color: white;
}

</style>