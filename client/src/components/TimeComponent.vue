<template>
  <div class="clock">
    <p class="datetime">{{datetime}}</p>
    <p class="weekday">{{weekday}}</p>
  </div>
</template>

<script>

export default {
  data () {
    return {
      datetime: 'XXXX-XX-XX XX:XX:XX',
      weekday: '周一'
    }
  },
  methods: {
    // 显示时间
    updateTime () {
      var date = new Date()
      var year = date.getFullYear()
      var month = this.prefixInteger(date.getMonth() + 1, 2)
      var day = this.prefixInteger(date.getDate(), 2)
      var hh = this.prefixInteger(date.getHours(), 2)
      var mi = this.prefixInteger(date.getMinutes(), 2)
      var ss = this.prefixInteger(date.getSeconds(), 2)
      var dayTag = '日一二三四五六'.charAt(date.getDay())
      var wk = '周' + dayTag
      this.datetime = year + '-' + month + '-' + day + ' ' + hh + ':' + mi + ':' + ss + ' '
      this.weekday = wk
    },
    // 时间前置补 0
    prefixInteger (num, length) {
      return (Array(length).join('0') + num).slice(-length)
    }
  },
  created: function () {
    setInterval(this.updateTime, 1000)
  }
}
</script>

<style scoped lang="less" rel="stylesheet/less">
@import "../assets/css/style.less";

.clock {
  height: 60px;
  width: 100%;
  background-color: @index-title-bg-color;
  display: inline-flex;
}

.datetime {
  margin: 0px;
  padding: 0px;
  width: 50%;
  height: 60px;
  font-size: @app-title-text-size;
  text-align: left;
  color: @index-title-text-color;
}

.weekday {
  margin: 0px;
  padding: 0px;
  width: 15%;
  height: 60px;
  font-size: @app-title-text-size;
  text-align: center;
  color: @index-title-text-color;
}
</style>
