<template>
  <div>
  <div id="chart-panel">
    <div id="industry-bar-area" :class="{flash : isUpdating}">
      <div v-for="item in allItem" :key="item.index">
        <div class="industry-value-box" >
          <div class="industry-value-count">{{item.name}}</div>
          <div class="industry-value-bar" :class="colorByValue(item.value)" :style="{height: dynamicHeight(item.value)}"></div>
        </div>
        <!-- &lt; 就是 < 小于号的原始码 -->
        <div class="industry-label">{{(item.value >= 100 || item.value &lt;= -100) ? item.value.toFixed(0) : item.value}}</div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>

export default {
  name: 'IndustryMoneyChartComponent',
  props: ['industryMoneyInfo'],
  data () {
    return {
      maxValue: 0,
      moneyIn: [],
      moneyOut: [],
      allItem: [],
      isUpdating: true
    }
  },
  methods: {
    colorByValue (value) {
      if (value < 0) {
        return 'fall-color'
      } else {
        return 'rise-color'
      }
    },

    dynamicHeight (value) {
      return Math.abs(value) / this.maxValue * 2.3 + 'rem'
    }
  },
  watch: {
    industryMoneyInfo: {
      handler (newValue, oldValue) {
        // 取出最大值
        this.maxValue = 0
        this.moneyIn = []
        this.moneyOut = []
        this.allItem = []
        // 流入（极端情况下，流入前 5 位可能有负，例如只有三个板块净流入）
        newValue.value.money_in.forEach(element => {
          let val = Math.abs(element['value'])
          if (this.maxValue < val) {
            this.maxValue = val
          }
          this.allItem.push(element)
        })
        this.moneyIn = newValue.value.money_in
        // 流出
        newValue.value.money_out.forEach(element => {
          let val = Math.abs(element['value'])
          if (this.maxValue < val) {
            this.maxValue = val
          }
          this.moneyOut.push(element)
        })
        this.moneyOut.reverse()
        this.moneyOut.forEach(element => {
          this.allItem.push(element)
        })
        this.isUpdating = true
        setTimeout(() => {
          this.isUpdating = false
        }, 1500)
      },
      immediate: true,
      deep: true
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
  height: 2.9rem;
  display: inline-flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: flex-end;
}

/* 柱状条区域 */
#industry-bar-area {
  width: 100%;
  height: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  align-items: flex-end;
  justify-content: space-around;
}

/* 柱状条 + 个股数的容器 */
.industry-value-box {
  width: 1rem;
  display: inline-flex;
  flex-direction: row;
  flex-wrap: nowrap;
  // justify-content: space-between;
  justify-items: center;
  align-items: flex-end;
  // background-color: pink;
}

/* 个股数 */
.industry-value-count {
  width: 0.5rem;
  height: min-content;
  font-size: @app-small-text-size;
  color: @app-text-color;
  display: inline-flex;
  justify-content: center;
}

/* 柱状条 */
.industry-value-bar {
  width: 0.5rem;
  height: 2.3rem;
  display: inline-flex;
  color: @app-text-color;
  justify-content: center;
  // background-color: pink;
}

/* 分割线 */
.separate-line {
  background-color: @app-text-color;
  width: 100%;
  height: @index-cell-margin;
}

/* 涨跌幅度标题区域 */
.industry-label-area {
  margin: 0px @index-cell-margin;
  width: 100%;
  display: inline-flex;
  flex-wrap: nowrap;
  justify-content: space-between;
}

/* 涨跌幅度标题 */
.industry-label {
  margin: 0px;
  padding: @index-cell-padding;
  width: 1rem;
  font-size: @app-small-text-size;
  color: @index-title-text-color;
  display: inline-flex;
  justify-content: center;
  // background-color: pink;
}

</style>
