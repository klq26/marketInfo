<template>
  <div>
    <div v-for="item in indexInfos" :key="item.index">
      <div class='indexCell'>
        <p>{{item.indexName}}</p>
        <p class="daliy-value" :class="bgColorWithValue(item.dailyChangValue)">{{setDemical(item.current, 2) }}</p>
        <p class="daliy-value" :class="bgColorWithValue(item.dailyChangValue)">{{item.dailyChangRate}}</p>
        <p class="refresh-value" v-if="showType == 0">
          <img :src="iconWithValue(item.dailyChangValue)"/>
        </p>
        <p class="refresh-value" v-else>
          {{setDemical(item.dailyChangValue, 2)}}
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
  props: [
    // 'indexName',
    // 'indexCode',
    // 'current',
    // 'lastClose',
    // 'dailyChangValue',
    // 'dailyChangRate'
    'indexInfos',
    'showType'
  ],
  data () {
    // var indexInfos = [] 
    // var that = this
    // this.$axios.get('http://112.125.25.230/api/indexs/china').then(function (response) {
    //   that.indexInfos = response.data.data
    //   // console.log(that.indexInfos)
    // });
    // return {indexInfos : indexInfos, showType : 0}
    return {
      indexInfos: [{
        indexName: '中证500',
        indexCode: '399905',
        current: 5800.34,
        lastClose: 5789.53,
        dailyChangValue: 20.13,
        dailyChangRate: '0.28%',
        showType: 1
      }, {
        indexName: '中证1000',
        indexCode: '000852',
        current: 15800.01,
        lastClose: 15789.53,
        dailyChangValue: -120.13,
        dailyChangRate: '-0.28%',
        showType: 1
      }, {
        indexName: '等权800',
        indexCode: '000842',
        current: 8800.099,
        lastClose: 7789.53,
        dailyChangValue: 0,
        dailyChangRate: '0%',
        showType: 1
      }]
    }
  },
  methods: {
    // 根据数值决定背景色
    bgColorWithValue (value) {
      if (value > 0) {
        return 'rise-color'
      } else if (value == 0) {
        return 'normal-color'
      } else {
        return 'fall-color'
      }
    },
    // 根据数值决定所使用的 icon
    iconWithValue (value) {
      if (value > 0) {
        return iconUp
      } else if( value == 0) {
        return iconEqual
      } else {
        return iconDown
      }
    },
    // 设置数值显示精度（保留小数点后几位）
    setDemical(value, demical) {
      return parseFloat(value).toFixed(demical);
    }
  }
  // created: function() {
  //   this.$axios.get('http://112.125.25.230/api/indexs/china').then(function (response) {
  //     console.log(response.data.data)
  //     this.$indexInfos = response.data.data
  //   });
  // }

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

.refresh-value:extend(p) {
  background-color: @index-refresh-change-bg-color;
  width: @index-value-width;
  text-align: center;
}

// icon 尺寸
img {
  width: @app-cell-height;
  height: @app-cell-height;
}

</style>
