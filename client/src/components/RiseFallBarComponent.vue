<template>
  <div>
    <div class='zdp-cell' v-for="item in zdpinfo" :key="item.index">
      <p class="zdp-title">{{item.name}}</p>
      <div class='zdp-bar-box' :class="{flash : isUpdating}">
        <p class="zdp-bar-up" :style="{width: dynamicWidth(item.symbol, 'z')}">{{item.z}}</p>
        <p class="zdp-bar-equal" :style="{width: dynamicWidth(item.symbol, 'p')}">{{item.p}}</p>
        <p class="zdp-bar-down" :style="{width: dynamicWidth(item.symbol, 'd')}">{{item.d}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RiseFallBarComponent',
  props: [
    'zdpinfo'
  ],
  data () {
    return {
      isUpdating: true,
      measuredInfo: {

      }
    }
  },
  methods: {
    dynamicWidth (symbol, key) {
      let result = parseFloat(this.measuredInfo[symbol][key]['finalW']) + 'px'
      return result
    }
  },
  watch: {
    zdpinfo: {
      handler (newValue, oldValue) {
        // 单个阿拉伯数字的宽度
        let charW = 21.11
        // 值条宽度（vue 是虚拟 dom，无法等到实际 mounted 之后再计算了）
        let zdpBarWidth = 609
        for (var key in newValue) {
          // 总数
          let up = newValue[key].z
          let equal = newValue[key].p
          let down = newValue[key].d
          let all = up + equal + down
          let symbol = newValue[key].symbol
          // 生成涨跌平条的全面数据
          var upDict = {
            'count': up,
            'calW': parseInt(up / all * zdpBarWidth),
            'minW': String(up).length * charW,
            'isCalTooSmall': parseInt(up / all * zdpBarWidth) < String(up).length * charW,
            'finalW': parseInt(up / all * zdpBarWidth) > String(up).length * charW ? parseInt(up / all * zdpBarWidth) : String(up).length * charW
          }
          var equalDict = {
            'count': equal,
            'calW': parseInt(equal / all * zdpBarWidth),
            'minW': String(equal).length * charW,
            'isCalTooSmall': parseInt(equal / all * zdpBarWidth) < String(equal).length * charW,
            'finalW': parseInt(equal / all * zdpBarWidth) > String(equal).length * charW ? parseInt(equal / all * zdpBarWidth) : String(equal).length * charW
          }
          var downDict = {
            'count': down,
            'calW': parseInt(down / all * zdpBarWidth),
            'minW': String(down).length * charW,
            'isCalTooSmall': parseInt(down / all * zdpBarWidth) < String(down).length * charW,
            'finalW': parseInt(down / all * zdpBarWidth) > String(down).length * charW ? parseInt(down / all * zdpBarWidth) : String(down).length * charW
          }
          // console.log(upDict, equalDict, downDict)
          var dictArray = [upDict, equalDict, downDict]
          var leftCount = 0
          var leftWidth = zdpBarWidth
          // 如果原比例计算的宽度不足以显示内容，则保留字段的最小视觉宽度，放弃之前的三者共同计算比例
          // 每去掉一个比例条，就要相应剪掉其对应的宽度，剩下的条重新计算比例，重新共享宽度
          for (var idx in dictArray) {
            var currentBar = dictArray[idx]
            if (!currentBar['isCalTooSmall']) {
              leftCount = leftCount + currentBar['count']
            } else {
              leftWidth = leftWidth - currentBar['finalW']
            }
          }
          // 根据是最小宽度还是计算宽度，来决定每个元素的最终绘制宽度
          if (upDict['isCalTooSmall']) {
          } else {
            upDict['finalW'] = parseInt(upDict['count']) / leftCount * leftWidth
          }

          if (equalDict['isCalTooSmall']) {
          } else {
            equalDict['finalW'] = parseInt(equalDict['count']) / leftCount * leftWidth
          }

          if (downDict['isCalTooSmall']) {
          } else {
            downDict['finalW'] = parseInt(downDict['count']) / leftCount * leftWidth
          }
          this.measuredInfo[symbol] = {'z': upDict, 'p': equalDict, 'd': downDict}
        }
        // console.log(this.measuredInfo)
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

// 条目容器（整行）
.zdp-cell {
  width: 100%;
  display: flex;
}

// 指数标题
p {
  margin: @index-cell-margin;
  padding: @index-cell-padding;
  height: @app-cell-height;
  font-size: @app-value-text-size;
  text-align: center;
  color: @index-title-text-color;
}

.zdp-title:extend(p) {
  width: @index-title-width;
  background-color: @index-title-bg-color;
}

/* 涨跌平条 */
.zdp-bar-box {
  margin: @index-cell-margin;
  width:71.4953%; // 609
  height: @app-cell-height;
  display: inline-flex;
  background-color: pink;
}

/* 涨跌平条 - 涨 */
.zdp-bar-up:extend(p) {
  margin: 0px;
  height: 100%;
  min-width: min-content;
  background-color: @app-rise-color;
}

/* 涨跌平条 - 平 */
.zdp-bar-equal:extend(p) {
  margin: 0px;
  min-width: min-content;
  height: 100%;
  background-color: @index-title-bg-color;
}

/* 涨跌平条 - 跌 */
.zdp-bar-down:extend(p) {
  margin: 0px;
  min-width: min-content;
  height: 100%;
  background-color: @app-fall-color;
}
</style>
