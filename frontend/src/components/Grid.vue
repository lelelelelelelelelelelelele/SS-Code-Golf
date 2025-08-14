<script setup>
// 定义该组件可以接收哪些属性 (props)
defineProps({
  gridData: {
    type: Array,
    required: true,
  },
  title: {
    type: String,
    default: 'Grid'
  }
});

// 定义一个颜色数组，索引对应数字0-9
const colors = [
  '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
];
</script>

<template>
  <div class="grid-container">
    <h3>{{ title }}</h3>
    <div class="grid-body">
      <!-- v-for 是 Vue 的循环指令 -->
      <div v-for="(row, rowIndex) in gridData" :key="rowIndex" class="grid-row">
        <div 
          v-for="(cell, colIndex) in row" 
          :key="colIndex" 
          class="grid-cell"
          :style="{ backgroundColor: colors[cell] || '#000' }"
        >
          {{ cell }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* scoped 样式只作用于当前组件 */
.grid-container {
  margin-bottom: 20px;
}
.grid-body {
  display: inline-block;
  border: 1px solid #ccc;
  padding: 5px;
  background-color: #f0f0f0;
}
.grid-row {
  display: flex; /* 让单元格横向排列 */
}
.grid-cell {
  width: 40px;
  height: 40px;
  border: 1px solid #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.2em;
  font-weight: bold;
}
</style>