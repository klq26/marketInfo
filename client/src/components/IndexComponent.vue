<template>
  <div>
    <div v-for="item in indexInfos" :key="item.index">
      <div class='indexCell'>
        <!-- 样式1 -->
        <!-- 标题区 -->
        <div class="index-title-container" @click="indexTitleClicked(item.indexName)">
          <img class="index-title-flag-icon" :src="indexFlagConverter(item.indexName)"/>
          <p class="index-title-name" v-if="showType == 0">{{item.indexName}}</p>
          <p class="index-title-name" v-else>
            {{item.indexCode}}
          </p>
        </div>
        <!-- 点数区 -->
        <p class="index-value" :class="bgColorWithValue(item.dailyChangValue)" @click="indexValueClicked(item)">{{formatNumber(item.current, demical)}}</p>
        <!-- 日变化区 -->
        <p class="index-value" :class="bgColorWithValue(item.dailyChangValue)" @click="indexRefreshCellClicked" v-if="showType == 0">
          {{item.dailyChangRate}}
        </p>
        <p class="index-value" :class="bgColorWithValue(item.dailyChangValue)" @click="indexRefreshCellClicked" v-else>
          {{formatNumber(item.dailyChangValue, demical)}}
        </p>
        <!-- 自动刷新变化区 -->
        <div :class="{flash : isUpdating}" @click="indexRefreshCellClicked">
        <div class="refresh-value" v-if="showType == 0">
          <img class="change-icon" :src="iconWithValue(changeValueFromLastRequest(item))"/>
          <p class="refresh-value align-center" :class="changeColorFromLastRequest(item)">
            {{changeValueFromLastRequest(item) != 0 ? (changeValueFromLastRequest(item) / item.current * 100).toFixed(2) + '%' : '0.00%'}}
          </p>
        </div>
        <div class="refresh-value" v-else>
          <img class="change-icon" :src="iconWithValue(changeValueFromLastRequest(item))"/>
          <p class="refresh-value align-center" :class="changeColorFromLastRequest(item)">
            {{changeValueFromLastRequest(item)}}
          </p>
        </div>
        </div>
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
    },
    headerRef: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      lastIndexInfos: [],
      isUpdating: true
    }
  },
  methods: {
    indexTitleClicked (title) {
      this.$emit('indexTitleClicked', title)
    },
    indexValueClicked (item) {
      this.$emit('indexValueClicked', item)
    },
    indexRefreshCellClicked () {
      this.$emit('indexRefreshCellClicked', this.headerRef)
    },
    indexFlagConverter (value) {
      // require 是高级语法，不可以 require 变量，必须直接是路径
      let american = ['道琼斯', '标普500', '纳斯达克', '油气XOP']
      let china = ['国证A指', '上证指数', '深证成指', '创业板指', '科创50', '红利指数', '中证红利', '上证50', '沪深300', '中证500', '中证1000', '800等权', '中小100', '全指可选', '全指消费', '食品饮料', '全指医药', '全指金融', '全指信息', '中证军工', '证券公司', '中证银行', '养老产业', '中证传媒', '中证环保', '国债指数', '中证转债']
      let hongkong = ['恒生指数', '国企指数', '红筹指数']
      if (american.indexOf(value) > -1) {
        value = '美国'
      } else if (china.indexOf(value) > -1) {
        value = '中国大陆'
      } else if (hongkong.indexOf(value) > -1) {
        value = '中国香港'
      }
      // 如果 require 有错误，使用通用图标
      try {
        let path = require('../assets/flags/' + value + '.gif')
        return path
      } catch (error) {
        let path = require('../assets/flags/通用.gif')
        return path
      }
    },

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
      var val = parseFloat(value)
      if (val > 0) {
        return iconUp
      } else if (val === 0.0) {
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
    }
  },
  watch: {
    indexInfos: {
      handler (newValue, oldValue) {
        if (typeof (oldValue) !== 'undefined') {
          this.lastIndexInfos = oldValue
        }
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

// 标题区容器
.index-title-container {
  width: @index-title-width;
  height: @app-cell-height;
  margin: @index-cell-margin;
  padding: @index-cell-padding;
  background-color: @index-title-bg-color;
  align-items: center;
  display: flex;
}

// 指数图标
.index-title-flag-icon {
  width:@index-flag-width;
  height:@index-flag-height;
  margin: @index-cell-margin;
  padding: @index-cell-padding;
}

// 指数标题
.index-title-name {
  width: @index-title-width - @index-flag-width - @index-cell-margin * 4;
  max-width: @index-title-width - @index-flag-width  - @index-cell-margin * 4;
  height: @app-cell-height;
  margin: @index-cell-margin;
  padding: @index-cell-padding;
  font-size: @app-value-text-size;
  text-align: left;
  overflow:hidden;
  text-overflow: ellipsis;
  color: @index-title-text-color;
  background-color: @index-title-bg-color;
  display: flex;
  justify-items: center;
  align-items: center;
}

// 值
.index-value {
  margin: @index-cell-margin;
  padding: @index-cell-padding;
  width: @index-value-width;
  height: @app-cell-height;
  font-size: @app-value-text-size;
  text-align: right;
  color: @index-title-text-color;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

// 刷新值区
.refresh-value {
  margin: @index-cell-margin;
  padding: @index-cell-padding;
  width: @index-value-width;
  height: @app-cell-height;
  font-size: @app-value-text-size;
  background-color: @index-refresh-change-bg-color;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

// 对齐方案
.align-center {
  justify-content: center;
}
.align-right {
  justify-content: flex-end;
}

// icon 尺寸
.change-icon {
  width: @app-cell-height;
  height: @app-cell-height;
  margin-left: @app-cell-height / 2;
}

</style>
