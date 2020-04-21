<template>
  <div>
    <div>
      <div class='moneyCell' v-for="info in moneyinfo" :key="info.index">
        <p class="title">{{info.name}}</p>
        <div class="value-area" :class="{flash : isUpdating}">
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
  data () {
    return {
      isUpdating: true
    }
  },
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
  },
  watch: {
    moneyinfo: {
      handler (newValue, oldValue) {
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
  margin: @index-cell-margin 0px;
  width: 100%;
  display: flex;
  align-items:flex-start;
  justify-content:flex-start;
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
  margin: 0px 0px;
  // margin: 0px @index-cell-margin;
  height: @app-cell-height;
  min-width: @index-title-width;
  background-color: @index-title-bg-color;
}

.value-area {
  width:7.2rem;
  margin: 0px @index-cell-margin 0px @index-cell-margin;
  display: inline-flex;
  flex-wrap: wrap;
  align-items: flex-end;
}

.value-box {
  width: @index-value-width;
  height: @app-cell-height;
  margin: 0px @index-cell-margin 0px 0px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.box-name {
  text-align: left;
  padding: 0px @index-cell-margin;
}

.box-value {
  text-align: right;
  padding: 0px @index-cell-margin;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>
