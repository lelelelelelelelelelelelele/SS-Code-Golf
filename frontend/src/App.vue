<script setup>
import { ref, watch, onMounted } from 'vue';
import Grid from './components/Grid.vue';

// --- 响应式状态定义 ---
// ref() 创建一个响应式变量，当它的值改变时，模板会自动更新
const tasks = ref([]);
const selectedTask = ref(null);
const currentIndex = ref(0);
const maxIndex = ref(0);
const sampleData = ref(null);
const isLoading = ref(false);
const error = ref(null);

const API_BASE_URL = "http://127.0.0.1:8000";

// --- 方法 ---

// 异步函数，用于从后端获取数据
async function fetchSampleData() {
  if (!selectedTask.value) return;
  isLoading.value = true;
  error.value = null;
  sampleData.value = null;

  try {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${selectedTask.value}/${currentIndex.value}`);
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    const data = await response.json();
    sampleData.value = data;
  } catch (e) {
    error.value = e.toString();
  } finally {
    isLoading.value = false;
  }
}

// --- 生命周期和侦听器 ---

// onMounted 是一个钩子，当组件第一次加载到页面时执行
onMounted(async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/tasks`);
    const data = await response.json();
    tasks.value = data.tasks;
    if (tasks.value.length > 0) {
      selectedTask.value = tasks.value[0]; // 默认选中第一个任务
    }
  } catch (e) {
    error.value = "Failed to load task list. Is the backend running?";
  }
});

// watch 侦听一个或多个响应式变量，当它们变化时执行回调
watch([selectedTask, currentIndex], () => {
  // 当任务或索引变化时，重新获取数据
  fetchSampleData();
});

watch(selectedTask, () => {
  // 当任务变化时，索引重置为0
  currentIndex.value = 0;
});

function prev() {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
}

function next() {
  // 这里我们暂时不知道最大索引，可以做得更智能
  // 简单起见，我们只递增
  currentIndex.value++;
}
</script>

<template>
  <div class="app-container">
    <div class="sidebar">
      <h2>Controls</h2>
      
      <!-- 任务选择 -->
      <label for="task-select">Select Task:</label>
      <select id="task-select" v-model="selectedTask">
        <option v-for="task in tasks" :key="task" :value="task">
          {{ task }}
        </option>
      </select>

      <!-- 样本导航 -->
      <div class="navigation">
        <label for="index-input">Current Index:</label>
        <div class="nav-controls">
          <button @click="prev">◀</button>
          <input type="number" id="index-input" v-model.number="currentIndex" min="0" />
          <button @click="next">▶</button>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div v-if="isLoading" class="status-message">Loading...</div>
      <div v-if="error" class="status-message error">{{ error }}</div>
      
      <div v-if="sampleData" class="grids-display">
        <!-- 使用 Grid 组件 -->
        <Grid :grid-data="sampleData.input" title="Input" />
        <Grid :grid-data="sampleData.output" title="Output" />
      </div>
    </div>
  </div>
</template>

<style>
/* 全局样式 */
body {
  font-family: sans-serif;
  margin: 0;
  background-color: #f9f9f9;
}
.app-container {
  display: flex;
}
.sidebar {
  width: 250px;
  padding: 20px;
  background-color: #f0f0f0;
  height: 100vh;
  border-right: 1px solid #ddd;
}
.sidebar h2 {
  margin-top: 0;
}
.sidebar select, .sidebar input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  box-sizing: border-box;
}
.navigation {
  margin-top: 20px;
}
.nav-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 5px;
}
.nav-controls button {
  padding: 8px 12px;
}
.main-content {
  flex-grow: 1;
  padding: 20px;
}
.status-message {
  font-size: 1.5em;
  color: #888;
}
.error {
  color: red;
}
.grids-display {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}
</style>