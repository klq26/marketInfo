<template>
  <div>
  <div id="chart-panel">
  <div id="zdp-bar-area">
    <!-- v-for zdp-value-box -->
      <!-- zdp-value-count +  zdp-value-bar -->
    <div class="zdp-value-box" :class="{flash : isUpdating}" v-for="(value, index) in values" :key="value.index">
      <div class="zdp-value-count">{{value}}</div>
      <div class="zdp-value-bar" :class="colorByIndex(index)" :style="{height: dynamicHeight(value)}"></div>
    </div>
  </div>
    <div class="separate-line"/>
    <div class="zdp-label-area">
      <div class="zdp-label" v-for="label in labels" :key="label.index">{{label}}</div>
    </div>
  </div>
  </div>
</template>

<script>

export default {
  name: 'RiseFallChartComponent',
  props: ['values'],
  data () {
    return {
      labels: ['10%', '8%', '6%', '4%', '2%', '0', '-2%', '-4%', '-6%', '-8% ', '-10%'],
      // values: [118, 30, 109, 296, 1046, 1341, 662, 146, 24, 6],
      maxValue: 0,
      isUpdating: true
    }
  },
  methods: {
    colorByIndex (index) {
      if (index >= 5) {
        return 'fall-color'
      } else {
        return 'rise-color'
      }
    },

    dynamicHeight (value) {
      return value / this.maxValue * 150 + 'px'
    }
  },
  watch: {
    values: {
      handler (newValue, oldValue) {
        // 取出最大值
        this.maxValue = 0
        newValue.forEach(element => {
          if (this.maxValue < element) {
            this.maxValue = element
          }
        })
        // console.log(this.labels.reverse())
        this.isUpdating = true
        setTimeout(() => {
          this.isUpdating = false
        }, 1500)
      },
      immediate: true
    }
  }
}
</script>

<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

.rise-color {
  background-color: @app-rise-color;
}
.fall-color {
  background-color: @app-fall-color;
}

/* 涨跌分布 */
#chart-panel {
  width: 100%;
  height: 240px;
  display: inline-flex;
  flex-wrap: nowrap;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

/* 柱状条区域 */
#zdp-bar-area {
  width: 95.79%;
  height: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  align-items: flex-end;
  justify-content: space-around;
}

/* 柱状条 + 个股数的容器 */
.zdp-value-box {
  width: @app-cell-height;
  display: inline-flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: space-between;
}

/* 个股数 */
.zdp-value-count {
  width: @app-cell-height;
  height: 40px;
  font-size: @app-small-text-size;
  color: @app-text-color;
  display: inline-flex;
  justify-content: center;
}

/* 柱状条 */
.zdp-value-bar {
  width: @app-cell-height;
  height: 100px;
  display: inline-flex;
  color: @app-text-color;
  width: @app-cell-height;
  justify-content: center;
  // background-color: pink;
}

/* 分割线 */
.separate-line {
  background-color: @app-text-color;
  width: 100%;
  height: 2px;
}

/* 涨跌幅度标题区域 */
.zdp-label-area {
  margin: 0px 2px;
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
}

/* 涨跌幅度标题 */
.zdp-label {
  margin: 0px;
  padding: @index-cell-padding;
  width: 40px;
  font-size: @app-small-text-size;
  color: @index-title-text-color;
  display: inline-flex;
  justify-content: center;
}

</style>
