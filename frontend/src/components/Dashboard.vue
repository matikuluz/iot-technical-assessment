<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

// --- Chart JS Registration (Boilerplate) ---
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// --- State ---
const currentTemp = ref(0)
const currentHum = ref(0)
const isConnected = ref(false)
let socket = null

// --- Chart Configuration ---
// The UI is pre-configured, but the 'data' arrays are empty.
const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Temperature',
      borderColor: '#ff6b6b',
      backgroundColor: 'rgba(255, 107, 107, 0.2)',
      pointBackgroundColor: '#ff6b6b',
      borderWidth: 2,
      pointRadius: 3,
      tension: 0.4,
      fill: true,
      data: []
    },
    {
      label: 'Humidity',
      borderColor: '#4ecdc4',
      backgroundColor: 'rgba(78, 205, 196, 0.2)',
      pointBackgroundColor: '#4ecdc4',
      borderWidth: 2,
      pointRadius: 3,
      tension: 0.4,
      fill: true,
      data: []
    }
  ]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      labels: { color: '#2c3e50', font: { size: 12, family: "'Inter', sans-serif" } }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      titleColor: '#2c3e50',
      bodyColor: '#2c3e50',
      borderColor: '#ddd',
      borderWidth: 1
    }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: '#8898aa', maxTicksLimit: 8 }
    },
    y: {
      border: { display: false },
      grid: { color: '#f0f0f0' },
      ticks: { color: '#8898aa' }
    }
  }
}

const updateChart = (temp, hum, timestamp) => {
    const date = new Date(timestamp)
    const timeLabel = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })

    currentTemp.value = temp
    currentHum.value = hum

    const newLabels = [...chartData.value.labels, timeLabel]
    const newTempData = [...chartData.value.datasets[0].data, temp]
    const newHumData = [...chartData.value.datasets[1].data, hum]

    if (newLabels.length > 20) {
        newLabels.shift()
        newTempData.shift()
        newHumData.shift()
    }

    chartData.value = {
        labels: newLabels,
        datasets: [
            { ...chartData.value.datasets[0], data: newTempData },
            { ...chartData.value.datasets[1], data: newHumData }
        ]
    }
}

// --- YOUR TASKS START HERE ---

const fetchHistory = async () => {
    // TODO: Task 2.1
    // Fetch the last 50 readings from GET http://127.0.0.1:8000/api/readings
    // Populate the chart with this historical data.
}

const connectWebSocket = () => {
    // TODO: Task 2.2 & 2.3
    // Connect to ws://127.0.0.1:8000/ws
    // Handle 'onopen', 'onmessage', and 'onclose'.
    // Update 'isConnected' state and push new readings to the chart.
}

onMounted(() => {
    // Initialize data and connections here
})

onUnmounted(() => {
    if (socket) socket.close()
})
</script>

<template>
  <div class="dashboard-wrapper">
    <header class="top-bar">
      <div class="logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m8 22 4-10 4 10"/></svg>
        <span>Sensor Dashboard</span>
      </div>
      
      <div class="status-pill" :class="{ 'online': isConnected, 'offline': !isConnected }">
        <span class="dot"></span>
        {{ isConnected ? 'System Online' : 'Offline' }}
      </div>
    </header>

    <main class="content">
      <div class="grid-container">
        
        <div class="stat-card temp-card">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>
          </div>
          <div class="card-info">
            <h3>Temperature</h3>
            <div class="value">{{ currentTemp.toFixed(1) }}<span>°C</span></div>
          </div>
        </div>

        <div class="stat-card hum-card">
          <div class="card-icon">
             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
          </div>
          <div class="card-info">
            <h3>Humidity</h3>
            <div class="value">{{ currentHum.toFixed(1) }}<span>%</span></div>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3>Live Telemetry</h3>
            <span class="live-tag">REALTIME</span>
          </div>
          <div class="chart-wrapper">
             <Line :data="chartData" :options="chartOptions" />
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped src="./dashboard.css"></style>
