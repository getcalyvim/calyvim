<script setup>
import { onMounted, ref } from 'vue'
import { sprintBurndownAPI } from '@/utils/api'
import { useNProgress } from '@vueuse/integrations/useNProgress'
import { handleResponseError } from '@/utils/helpers'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
)

const props = defineProps({
  sprintId: {
    type: String,
    required: true,
  },
  boardId: {
    type: String,
    required: true,
  },
})

const { isLoading } = useNProgress(
  {
    loading: true,
  },
  {
    minimum: '0.5',
  }
)

// labels: ['January', 'February', 'March', 'April', 'May', 'June'],
// datasets: [
// {
//     label: 'Data One',
//     backgroundColor: '#42b883',
//     borderColor: '#42b883',
//     data: [40, 39, 10, 40, 39, 80],
// },
// {
//     label: 'Data Two',
//     backgroundColor: '#35495e',
//     borderColor: '#35495e',
//     data: [60, 55, 32, 10, 2, 12],
// },
// ],
const burdownChartData = ref({
  data: [],
  datasets: [],
})

const loadSprintBurndown = async () => {
  try {
    const { data } = await sprintBurndownAPI(props.boardId, props.sprintId)
    burdownChartData.value.labels = data.burndown.labels
    burdownChartData.value.datasets = [
      {
        label: 'Tasks',
        fill: true,
        backgroundColor: 'rgba(125, 82, 233, 0.1)',
        borderColor: '#7D52E9',
        borderWidth: 1.5,
        data: data.burndown.totalTasks,
      },
      {
        label: 'Pending Tasks',
        backgroundColor: 'rgba(128, 128, 128, 0.1)',
        borderColor: '#808080',
        fill: false,
        borderWidth: 1.5,
        borderDash: [3, 3], // Smaller dash pattern for smoother appearance
        tension: 0.3, // Add tension for curved lines
        data: data.burndown.pendingTasks,
      },
    ]
  } catch (error) {
    handleResponseError(error)
  }
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
}

onMounted(async () => {
  isLoading.value = true
  await loadSprintBurndown()
  isLoading.value = false
})
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-gray-700 mb-4">Sprint Burndown</h2>
    <div class="chart-container">
      <Line
        v-if="!isLoading"
        :data="burdownChartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>
