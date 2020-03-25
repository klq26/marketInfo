<template>
  <div id="app">
    <TimeComponent />
    <!-- 资金区 -->
    <SectionHeaderComponent
      title="资金"
      @shouldShow="showMoney = !showMoney"
      :isOpenning="isMoneyOpenning"
    />
    <transition name="fade">
      <div v-if="showMoney">
        <MoneyComponent :moneyinfo="moneyinfo" />
        <!-- 板块资金区 -->
        <IndustryMoneyChartComponent :industryMoneyInfo="industryMoneyInfo" />
      </div>
    </transition>
    <!-- 涨跌平区 -->
    <SectionHeaderComponent
      title="涨跌"
      @shouldShow="showZDP = !showZDP"
      :isOpenning="isZDPOpenning"
    />
    <transition name="fade">
      <div v-if="showZDP">
        <!-- 涨跌平区 -->
        <RiseFallBarComponent :zdpinfo="zdpinfo" />
        <!-- 涨跌停区 -->
        <RiseFallMaxBarComponent :zdt="zdt" />
        <!-- 涨跌分布区 -->
        <RiseFallChartComponent :values="zdfb" />
      </div>
    </transition>
    <!-- 指数区 -->
    <SectionHeaderComponent
      title="中国"
      ref="中国_header"
      showStyleButton="1"
      @changeShowType="changeShowType"
      @shouldShow="headerConfig['中国_header']['shouldShow'] = !headerConfig['中国_header']['shouldShow']"
      :isOpenning="isChinaOpenning"
    />
    <transition name="fade">
      <div v-if="headerConfig['中国_header']['shouldShow']">
        <IndexComponent ref="中国" :indexInfos="china" />
      </div>
    </transition>
    <SectionHeaderComponent
      title="澳洲"
      showStyleButton="1"
      @changeShowType="changeShowType"
      @shouldShow="showAustralia = !showAustralia"
      :isOpenning="isAustraliaOpenning"
    />
    <transition name="fade">
      <div v-if="showAustralia">
        <IndexComponent ref="澳洲" :indexInfos="australia" />
      </div>
    </transition>
    <SectionHeaderComponent
      ref="亚洲_header"
      title="亚洲"
      showStyleButton="1"
      showSortButton="1"
      @shouldShow="headerConfig['亚洲_header']['shouldShow'] = !headerConfig['亚洲_header']['shouldShow']"
      @changeShowType="changeShowType"
      :sortType="indexSortConfig['亚洲']['sortType']"
      @changeSortType="changeSortType(arguments)"
      :isOpenning="isAsianOpenning"
    />
    <transition name="fade">
      <div v-if="headerConfig['亚洲_header']['shouldShow']">
        <IndexComponent ref="亚洲" :indexInfos="asian" />
      </div>
    </transition>
    <SectionHeaderComponent
      ref="欧洲_header"
      title="欧洲"
      showStyleButton="1"
      showSortButton="1"
      @shouldShow="headerConfig['欧洲_header']['shouldShow'] = !headerConfig['欧洲_header']['shouldShow']"
      @changeShowType="changeShowType"
      :sortType="indexSortConfig['欧洲']['sortType']"
      @changeSortType="changeSortType(arguments)"
      :isOpenning="isEuroOpenning"
    />
    <transition name="fade">
      <div v-if="headerConfig['欧洲_header']['shouldShow']">
        <IndexComponent ref="欧洲" :indexInfos="euro" />
      </div>
    </transition>
    <SectionHeaderComponent
      ref="美洲_header"
      title="美洲"
      showStyleButton="1"
      showSortButton="1"
      @shouldShow="headerConfig['美洲_header']['shouldShow'] = !headerConfig['美洲_header']['shouldShow']"
      @changeShowType="changeShowType"
      :sortType="indexSortConfig['美洲']['sortType']"
      @changeSortType="changeSortType(arguments)"
      :isOpenning="isAmericaOpenning"
    />
    <transition name="fade">
      <div v-if="headerConfig['美洲_header']['shouldShow']">
        <IndexComponent ref="美洲" :indexInfos="america" />
      </div>
    </transition>
    <SectionHeaderComponent
      title="期货"
      @shouldShow="showGoods = !showGoods"
      showStyleButton="1"
      @changeShowType="changeShowType"
      :isOpenning="isGoodsOpenning"
    />
    <transition name="fade">
      <div v-if="showGoods">
        <IndexComponent ref="期货" :indexInfos="goods" :demical="3" />
      </div>
    </transition>
    <SectionHeaderComponent
      title="外汇"
      @shouldShow="showExchanges = !showExchanges"
      showStyleButton="1"
      @changeShowType="changeShowType"
      :isOpenning="isExchangesOpenning"
    />
    <transition name="fade">
      <div v-if="showExchanges">
        <IndexComponent ref="外汇" :indexInfos="exchanges" :demical="4" />
      </div>
    </transition>
    <SectionHeaderComponent
      title="固收"
      @shouldShow="showBond = !showBond"
      showStyleButton="1"
      @changeShowType="changeShowType"
      :isOpenning="isBondOpenning"
    />
    <transition name="fade">
      <div v-if="showBond">
        <IndexComponent ref="固收" :indexInfos="bond" />
      </div>
    </transition>
  </div>
</template>

<script>

import axios from 'axios'
import Vue from 'vue'

// 时间组件
import TimeComponent from './components/TimeComponent'
// 标题板块
import SectionHeaderComponent from './components/SectionHeaderComponent'
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

/* 非对象函数 */

// 是否工作日
var isWorkingDay = true

// var server_ip = 'http://112.125.25.230/'
var server_ip = "http://127.0.0.1:5000/"

// 时间前置补 0
function prefixInteger (num, length) {
  return (Array(length).join('0') + num).slice(-length)
}

// 判断是否在某一时间段之内
function isDuringDate (beginDateStr, endDateStr) {
  var curDate = new Date()
  var beginDate = new Date(beginDateStr)
  var endDate = new Date(endDateStr)
  if (curDate >= beginDate && curDate <= endDate) {
    return true
  }
  return false
}

// 判断今天是不是工作日
function todayIsWorkingDay () {
  axios.get(server_ip + 'api/today').then(function (response) {
    let dayType = response.data['data']['weekday']
    if (dayType === '1') {
      isWorkingDay = true
    } else {
      isWorkingDay = false
    }
  })
  return true
}

// 今天日期字符串(2020/01/01 或 20200101)
function todayString (sep = '') {
  var date = new Date()
  // yesterdayString
  // date.setTime(date.getTime() - 24*60*60*1000)
  // tomorrowString
  // date.setTime(date.getTime() + 24*60*60*1000)
  var year = date.getFullYear()
  var month = prefixInteger(date.getMonth() + 1, 2)
  var day = prefixInteger(date.getDate(), 2)
  return year + sep + month + sep + day
}

// 是否处于开盘期
function isMarketOpenning (morningOpen, morningClose, afternoonOpen, afternoonClose) {
  var todayStr = todayString('/')
  var openning = isWorkingDay && (isDuringDate(todayStr + ' ' + morningOpen, todayStr + ' ' + morningClose) || isDuringDate(todayStr + ' ' + afternoonOpen, todayStr + ' ' + afternoonClose))
  return openning
}
export default {
  name: 'App',
  components: {
    TimeComponent,
    SectionHeaderComponent,
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
    'australia',
    'asian',
    'euro',
    'america',
    'goods',
    'exchanges',
    'bond'
  ],
  data () {
    return {
      headerConfig: {
        中国_header: { shouldShow: true },
        亚洲_header: { shouldShow: true },
        欧洲_header: { shouldShow: true },
        美洲_header: {shouldShow: true}
      },
      indexAreaConfig: {
        中国: { showType: 0 },
        澳洲: { showType: 0 },
        亚洲: { showType: 0 },
        欧洲: { showType: 0 },
        美洲: { showType: 0 },
        期货: { showType: 0 },
        外汇: { showType: 0 },
        固收: { showType: 0 }
      },
      indexSortConfig: {
        亚洲: { sortType: "2" },
        欧洲: { sortType: "2" },
        美洲: { sortType: "2" }
      },
      // 显示隐藏面板
      showMoney: true,
      showZDP: true,
      showChina: true,
      showAustralia: true,
      showGoods: true,
      showExchanges: true,
      showBond: true,
      // 是否开盘
      isMoneyOpenning: true,
      isZDPOpenning: true,
      isChinaOpenning: true,
      isAustraliaOpenning: true,
      isAsianOpenning: true,
      isEuroOpenning: true,
      isAmericaOpenning: true,
      isGoodsOpenning: true,
      isExchangesOpenning: true,
      isBondOpenning: true
    }
  },
  methods: {
    changeShowType (title) {
      for (var ref_key in this.$refs) {
        if (title === ref_key) {
          this.$refs[ref_key].showType = this.$refs[ref_key].showType === 1 ? 0 : 1
          break;
        }
      }
    },
    changeSortType (params) {
      var type = parseInt(this.indexSortConfig[params[0]]['sortType'])
      if (type < 5) {
        type += 1
      } else {
        type = 1
      }
      this.indexSortConfig[params[0]]['sortType'] = type.toString()
      this.requestIndexSortInfos(params[0], type)
    },
    /* 网络请求 */
    // 请求资金数据
    requestMoneyInfoIfNeeded (isForce = false) {
      var isOpenning = isMarketOpenning('9:00', '11:35', '13:00', '16:20')
      this.isMoneyOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        this.$axios.get(server_ip + 'api/moneyinfo').then(function (response) {
          that.moneyinfo = response.data.data
          // 行业资金净流入用图标表示
          that.industryMoneyInfo = that.moneyinfo.pop(-1)
          // 两市成交额与融资融券是0，显示灰底。其他是1，显示涨跌底色
          var showTypes = [0, 0, 1, 1, 1]
          for (var index in that.moneyinfo) {
            that.moneyinfo[index].showType = showTypes[index]
          }
        })
      } else {
        // console.log('资金数据未开盘')
      }
    },
    requestZDPInfoIfNeeded (isForce = false) {
      var isOpenning = isMarketOpenning('9:25', '11:35', '13:00', '15:05')
      this.isZDPOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        // 请求涨跌数据
        this.$axios.get(server_ip + 'api/zdpinfo').then(function (response) {
          // 指数涨跌平
          that.zdpinfo = response.data.data[2].value
          // 全市场涨跌停
          that.zdt = response.data.data[1].value
          // 全市场涨跌分布
          that.zdfb = response.data.data[0].value
        })
      } else {
        // console.log('涨跌平数据未开盘')
      }
    },
    requestChinaIfNeeded (isForce = false) {
      var isOpenning = isMarketOpenning('9:00', '11:35', '13:00', '16:20')
      this.isChinaOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        // 请求中国
        this.$axios.get(server_ip + 'api/indexs/china').then(function (response) {
          that.china = response.data.data
        })
      } else {
        // console.log('中国未开盘')
      }
    },
    requestAustraliaIfNeeded (isForce = false) {
      var isOpenning = isMarketOpenning('6:00', '14:00', '6:00', '14:00')
      this.isAustraliaOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        // 请求亚洲
        this.$axios.get(server_ip + 'api/indexs/australia').then(function (response) {
          that.australia = response.data.data
        })
      } else {
        // console.log('澳洲未开盘')
      }
    },
    requestAsianIfNeeded (isForce = false) {
      var isOpenning = isMarketOpenning('9:00', '11:35', '13:00', '16:20')
      this.isAsianOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        // 请求亚洲
        this.$axios.get(server_ip + 'api/indexs/asian?sort=' + this.indexSortConfig['亚洲']['sortType']).then(function (response) {
          that.asian = response.data.data
        })
      } else {
        // console.log('亚洲未开盘')
      }
    },
    requestEuroIfNeeded (isForce = false) {
      var isOpenning = isMarketOpenning('16:00', '23:59', '00:00', '2:30')
      this.isEuroOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        // 请求欧洲
        this.$axios.get(server_ip + 'api/indexs/euro?sort=' + this.indexSortConfig['欧洲']['sortType']).then(function (response) {
          that.euro = response.data.data
        })
      } else {
        // console.log('欧洲未开盘')
      }
    },
    requestAmericaIfNeeded (isForce = false) {
      // 夏令时（3月-11月）为北京时间21:30-次日4:00，交易时长6个半小时，中间无休。
      // 冬令时（11月-次年3月）为北京时间22:30-次日5:00，交易时长6个半小时，中间无休。
      var isOpenning = isMarketOpenning('21:25', '23:59', '00:00', '4:05')
      this.isAmericaOpenning = isOpenning
      if (isForce || isOpenning) {
        var that = this
        // 请求美洲
        this.$axios.get(server_ip + 'api/indexs/america?sort=' + this.indexSortConfig['美洲']['sortType']).then(function (response) {
          that.america = response.data.data
        })
      } else {
        // console.log('美洲未开盘')
      }
    },
    requestGoodsAndExchangesIfNeeded (isForce = false) {
      var that = this
      // 请求期货&外汇
      this.$axios.get(server_ip + 'api/goods_and_exchanges').then(function (response) {
        that.goods = response.data.data.goods
        that.exchanges = response.data.data.exchanges
      })
    },
    requestBondInfoIfNeeded (isForce = false) {
      var that = this
      // 债券&组合
      this.$axios.get(server_ip + 'api/bondinfo').then(function (response) {
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
    },
    requestIndexSortInfos (continent, type) {
      var that = this
      var area = ''
      if (continent === '亚洲') {
        this.requestAsianIfNeeded(true)
      } else if (continent === '欧洲') {
        this.requestEuroIfNeeded(true)
      }
      else if (continent === '美洲') {
        this.requestAmericaIfNeeded(true)
      } else {
        console.log('Wrong continent')
        return
      }
    }
  },
  created: function () {
    // 是否工作日
    todayIsWorkingDay()
    // 初始化数据
    this.requestMoneyInfoIfNeeded(true)
    this.requestZDPInfoIfNeeded(true)
    this.requestChinaIfNeeded(true)
    this.requestAustraliaIfNeeded(true)
    this.requestAsianIfNeeded(true)
    this.requestEuroIfNeeded(true)
    this.requestAmericaIfNeeded(true)
    this.requestGoodsAndExchangesIfNeeded(true)
    this.requestBondInfoIfNeeded(true)
    // 定时刷新
    // 资金流 60s
    setInterval(this.requestMoneyInfoIfNeeded, 60 * 1000)
    // 涨跌平 60s
    setInterval(this.requestZDPInfoIfNeeded, 60 * 1000)
    // 指数 15s
    setInterval(this.requestChinaIfNeeded, 15 * 1000)
    setInterval(this.requestAustraliaIfNeeded, 15 * 1000)
    setInterval(this.requestAsianIfNeeded, 15 * 1000)
    setInterval(this.requestEuroIfNeeded, 15 * 1000)
    setInterval(this.requestAmericaIfNeeded, 15 * 1000)
    // 期货&外汇 15s
    setInterval(this.requestGoodsAndExchangesIfNeeded, 15 * 1000)
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
