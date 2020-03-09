<template>
  <div id="app">
    <!-- 资金区 -->
    <MoneyComponent :moneyinfo="moneyinfo"/>
    <!-- 板块资金区 -->
    <IndustryMoneyChartComponent :industryMoneyInfo="industryMoneyInfo"/>
    <!-- 涨跌平区 -->
    <br/>
    <RiseFallBarComponent :zdpinfo="zdpinfo"/>
    <!-- 涨跌停区 -->
    <RiseFallMaxBarComponent :zdt="zdt"/>
    <!-- 涨跌分布区 -->
    <RiseFallChartComponent :values="zdfb"/>
    <!-- 指数区 -->
    <br/>
    <IndexComponent :indexInfos="china" :showType="0"/>
    <br/>
    <IndexComponent :indexInfos="asian" :showType="1"/>
    <br/>
    <IndexComponent :indexInfos="euro" :showType="1"/>
    <br/>
    <IndexComponent :indexInfos="america" :showType="0"/>
    <br/>
    <IndexComponent :indexInfos="goods" :showType="1"/>
    <br/>
    <IndexComponent :indexInfos="exchanges" :showType="0"/>
    <br/>
    <IndexComponent :indexInfos="bond" :showType="1"/>
  </div>
</template>

<script>

import axios from 'axios'
import Vue from 'vue'

// 资金组件
import MoneyComponent from './components/MoneyComponent'
// 板块资金组件
import IndustryMoneyChartComponent from './components/IndustryMoneyChartComponent'
// 涨跌平组件
import RiseFallBarComponent from './components/RiseFallBarComponent'
// 涨跌停组件
import RiseFallMaxBarComponent from './components/RiseFallMaxBarComponent'
// 涨跌分布组件
import RiseFallChartComponent from './components/RiseFallChartComponent'
// 指数组件
import IndexComponent from './components/IndexComponent'

Vue.prototype.$axios = axios
Vue.config.productionTip = false

export default {
  name: 'App',
  components: {
    MoneyComponent,
    IndustryMoneyChartComponent,
    RiseFallBarComponent,
    RiseFallMaxBarComponent,
    RiseFallChartComponent,
    IndexComponent
  },
  props: [
    'moneyinfo',
    'zdpinfo',
    'zdt',
    'zdfb',
    'industryMoneyInfo',
    'china',
    'asian',
    'euro',
    'america',
    'goods',
    'exchanges',
    'bond'
  ],
  created: function () {
    var that = this
    // 请求资金数据
    this.$axios.get('http://112.125.25.230/api/moneyinfo').then(function (response) {
      that.moneyinfo = response.data.data
      // 行业资金净流入用图标表示
      that.industryMoneyInfo = that.moneyinfo.pop(-1)
      // 两市成交额与融资融券是0，显示灰底。其他是1，显示涨跌底色
      var showTypes = [0, 0, 1, 1, 1]
      for (var index in that.moneyinfo) {
        that.moneyinfo[index].showType = showTypes[index]
      }
    })
    // 请求涨跌数据
    this.$axios.get('http://112.125.25.230/api/zdpinfo').then(function (response) {
      // 指数涨跌平
      that.zdpinfo = response.data.data[2].value
      // 全市场涨跌停
      that.zdt = response.data.data[1].value
      // 全市场涨跌分布
      that.zdfb = response.data.data[0].value
    })
    // 请求中国
    this.$axios.get('http://112.125.25.230/api/indexs/china').then(function (response) {
      that.china = response.data.data
    })
    // 请求亚洲
    this.$axios.get('http://112.125.25.230/api/indexs/asian').then(function (response) {
      that.asian = response.data.data
    })
    // 请求欧洲
    this.$axios.get('http://112.125.25.230/api/indexs/euro').then(function (response) {
      that.euro = response.data.data
    })
    // 请求美洲
    this.$axios.get('http://112.125.25.230/api/indexs/america').then(function (response) {
      that.america = response.data.data
    })
    // 请求期货&外汇
    this.$axios.get('http://112.125.25.230/api/goods_and_exchanges').then(function (response) {
      that.goods = response.data.data.goods
      that.exchanges = response.data.data.exchanges
    })
    // 债券&组合
    this.$axios.get('http://112.125.25.230/api/bondinfo').then(function (response) {
      that.bond = []
      for (var item in response.data.data[0].value) {
        that.bond.push(response.data.data[0].value[item])
      }
      for (item in response.data.data[1].value) {
        that.bond.push(response.data.data[1].value[item])
      }
      for (item in response.data.data[2].value) {
        that.bond.push(response.data.data[2].value[item])
      }
    })
  }
}
</script>

<style lang="less" rel="stylesheet/less">

@import './assets/css/style.less';

#app {
  width: 856px; /* 240 + 4 * 4 + 200 * 3 = 856 */
  background-color: @app-bg-color;
}
</style>
