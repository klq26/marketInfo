<template>
  <div @click="changShowType()">
    <div v-for="item in indexInfos" :key="item.index">
      <div class='indexCell'>
        <p>{{item.indexName}}</p>
        <p class="daliy-value" :class="bgColorWithValue(item.dailyChangValue)">{{formatNumber(item.current, demical) }}</p>
        <p class="daliy-value" :class="bgColorWithValue(item.dailyChangValue)" v-if="showType == 0">
          {{item.dailyChangRate}}
        </p>
        <p class="daliy-value" :class="bgColorWithValue(item.dailyChangValue)" v-else>
          {{formatNumber(item.dailyChangValue, demical)}}
        </p>
        <p class="refresh-value" v-if="showType == 0">
          <img :src="iconWithValue(item.dailyChangValue)"/>
        </p>
        <p class="refresh-value align-right" :class="changeColorFromLastRequest(item)" v-else>
          {{changeValueFromLastRequest(item)}}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// 图片资源
import iconUp from '../assets/icon_up.png'
import iconEqual from '../assets/icon_equal.png'
import iconDown from '../assets/icon_down.png'

import Vue from 'vue'
import axios from 'axios'
Vue.prototype.$axios = axios

Vue.config.productionTip = false

export default {
  name: 'IndexComponent',
  props: {
    indexInfos: {
      type: Array,
      default () {
        return []
      }
    },
    showType: {
      type: Number,
      default: 0
    },
    demical: {
      type: Number,
      default: 2
    }
  },
  data () {
    return {
      lastIndexInfos: []
    }
  },
  methods: {
    // 根据数值决定背景色
    bgColorWithValue (value) {
      if (value > 0) {
        return 'rise-color'
      } else if (value === 0) {
        return 'normal-color'
      } else {
        return 'fall-color'
      }
    },
    // 文字颜色
    textColorWithValue (value) {
      if (value > 0) {
        return 'rise-text-color'
      } else if (value === 0) {
        return 'normal-text-color'
      } else {
        return 'fall-text-color'
      }
    },
    // 根据数值决定所使用的 icon
    iconWithValue (value) {
      if (value > 0) {
        return iconUp
      } else if (value === 0) {
        return iconEqual
      } else {
        return iconDown
      }
    },
    // 设置数值显示精度（保留小数点后几位）以及正负号
    formatNumber (value, demical, needPlusMark = false) {
      var number = parseFloat(value).toFixed(demical)
      var hasPercent = String(value).indexOf('%') > 0
      var isPositive = number > 0
      if (needPlusMark) {
        number = (isPositive ? '+' : '') + number
      }
      if (hasPercent) {
        number = number + '%'
      }
      return number
    },
    // 返回与上次刷新变化值的颜色
    changeColorFromLastRequest (item) {
      var lastValue
      for (var index in this.lastIndexInfos) {
        var indexItem = this.lastIndexInfos[index]
        if (indexItem.indexCode === item.indexCode) {
          lastValue = indexItem
          break
        }
      }
      if (lastValue === undefined) {
        return this.textColorWithValue(0)
      } else {
        var change = parseFloat(item.current) - parseFloat(lastValue.current)
        return this.textColorWithValue(change)
      }
    },
    // 返回与上次刷新变化值的值
    changeValueFromLastRequest (item) {
      var lastValue
      for (var index in this.lastIndexInfos) {
        var indexItem = this.lastIndexInfos[index]
        if (indexItem.indexCode === item.indexCode) {
          lastValue = indexItem
          break
        }
      }
      if (lastValue === undefined) {
        return this.formatNumber(0, this.demical, true)
      } else {
        var change = parseFloat(item.current) - parseFloat(lastValue.current)
        return this.formatNumber(change, this.demical, true)
      }
    },
    // 改变显示样式
    changShowType () {
      this.showType = this.showType !== 0 ? 0 : 1
    }
  },
  watch: {
    indexInfos: {
      handler (newValue, oldValue) {
        if (typeof (oldValue) !== 'undefined') {
          this.lastIndexInfos = oldValue
        }
      },
      immediate: true,
      deep: true
    }
  }
}

</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped lang="less" rel="stylesheet/less">

@import '../assets/css/style.less';

// 涨跌平背景色
.normal-color {
  background-color: @index-title-bg-color;
}
.rise-color {
  background-color: @app-rise-color;
}
.fall-color {
  background-color: @app-fall-color;
}
.normal-text-color {
  color: @index-title-text-color;
}
.rise-text-color {
  color: @app-rise-color;
}
.fall-text-color {
  color: @app-fall-color;
}

// 指数容器（整行）
.indexCell {
  width: 100%;
  display: flex;
}

// 指数标题
p {
  margin: @index-cell-margin;
  padding: @index-cell-padding;
  width: @index-title-width;
  height: @app-cell-height;
  font-size: @app-value-text-size;
  text-align: center;
  color: @index-title-text-color;
  background-color: @index-title-bg-color;
}

.align-center {
  text-align: center;
}
.align-right {
  text-align: right;
}

.daliy-value:extend(.align-right) {
  width: @index-value-width;
}

.refresh-value {
  background-color: @index-refresh-change-bg-color;
  width: @index-value-width;
}

// icon 尺寸
img {
  width: @app-cell-height;
  height: @app-cell-height;
}

</style>
