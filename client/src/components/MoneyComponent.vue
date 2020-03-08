<template>
  <div>
    <div>
      <div class='moneyCell' v-for="info in moneyinfo" :key="info.index">
        <p class="title">{{info.name}}</p>
        <div class="value-area">
          <div class="value-box" :class="bgColorWithValue(info.showType, item.value)" v-for="item in info.value" :key="item.index">
            <p class="box-name">{{item.name}}</p>
            <p class="box-value">{{setDemical(info.showType, item.value, 1)}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'moneyinfo'
  ],
  // data () {
  //   return {moneyinfo: [{
  //     name: '沪深两市成交额（亿）',
  //     value: [
  //       {name: '沪', value: 12000},
  //       {name: '深', value: 9000},
  //       {name: '总', value: 22000},
  //       {name: '主', value: 22000},
  //       {name: '特', value: 220}
  //     ],
  //     showType: 0
  //   }, {
  //     name: '沪深两市看看额（亿）',
  //     value: [
  //       {name: '沪', value: 1200},
  //       {name: '深', value: -9000},
  //       {name: '总', value: 220}
  //     ],
  //     showType: 1
  //   }]}
  // },
  methods: {
    // 根据数值决定背景色
    bgColorWithValue (showType, value) {
      if (showType === 0) {
        return 'normal-color'
      } else {
        if (value > 0) {
          return 'rise-color'
        } else if (value < 0) {
          return 'fall-color'
        } else {
          return 'normal-color'
        }
      }
    },
    // 设置数值显示精度（保留小数点后几位）
    setDemical (showType, value, demical) {
      let val = parseFloat(value).toFixed(demical)
      if (showType === 0) {
        return val
      } else {
        if (val > 0) {
          return '+' + val
        } else {
          return val
        }
      }
    }
  }
}
</script>

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
.moneyCell {
  margin: 2px 0px;
  width: 100%;
  display: inline-flex;
}

// 指数标题
p {
  margin: 0px;
  padding: 0px;
  width: @index-title-width;
  font-size: @app-value-text-size;
  text-align: center;
  color: @index-title-text-color;
}

.title {
  margin: 0px 2px;
  min-width: @index-title-width;
  background-color: @index-title-bg-color;
}

.value-area {
  width:616px;
  display: inline-flex;
  flex-wrap: wrap;
  align-items: flex-end;
}

.value-box {
  width: @index-value-width;
  height: @app-cell-height;
  margin: 0px 2px;
  display: inline-flex;
}

.box-name {
  text-align: left;
  padding: 0px 2px;
}

.box-value {
  text-align: right;
  padding: 0px 2px;
}
</style>
