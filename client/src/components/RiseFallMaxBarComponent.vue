<template>
  <div>
    <div class='zdp-cell'>
      <p class="zdp-title">涨跌停板</p>
      <div class='zdp-bar-box' :class="{flash : isUpdating}">
        <p class="zdp-bar-up" :style="{width: dynamicWidth('zt')}">{{up}}</p>
        <p class="zdp-bar-down" :style="{width: dynamicWidth('dt')}">{{down}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RiseFallMaxBarComponent',
  props: [
    'zdt'
  ],
  data () {
    return {
      up: 0,
      down: 0,
      upDict: {},
      downDict: {},
      isUpdating: true
    }
  },
  computed: {
    dynamicCount (key) {
      if (key === 'zt' && this.upDict.hasOwnProperty('finalW')) {
        return parseFloat(this.upDict[key]['count'])
      } else if (key === 'dt' && this.downDict.hasOwnProperty('finalW')) {
        return parseFloat(this.downDict[key]['count'])
      } else {
        return 0
      }
    }
  },
  methods: {
    dynamicWidth (key) {
      if (key === 'zt' && this.upDict.hasOwnProperty('finalW')) {
        return parseFloat(this.upDict['finalW']) + 'px'
      } else if (key === 'dt' && this.downDict.hasOwnProperty('finalW')) {
        return parseFloat(this.downDict['finalW']) + 'px'
      } else {
        return 21.1
      }
    }
  },
  watch: {
    zdt: {
      handler (newValue, oldValue) {
        if (typeof (newValue) === 'undefined') {
          return
        }
        // 单个阿拉伯数字的宽度
        let charW = 21.11
        // 值条宽度（vue 是虚拟 dom，无法等到实际 mounted 之后再计算了）
        let zdpBarWidth = 609

        let up = newValue[0].value
        let down = newValue[1].value
        this.up = up
        this.down = down
        let all = up + down
        // 生成涨跌平条的全面数据
        var upDict = {
          'count': up,
          'calW': parseInt(up / all * zdpBarWidth),
          'minW': String(up).length * charW,
          'isCalTooSmall': parseInt(up / all * zdpBarWidth) < String(up).length * charW,
          'finalW': parseInt(up / all * zdpBarWidth) > String(up).length * charW ? parseInt(up / all * zdpBarWidth) : String(up).length * charW
        }
        var downDict = {
          'count': down,
          'calW': parseInt(down / all * zdpBarWidth),
          'minW': String(down).length * charW,
          'isCalTooSmall': parseInt(down / all * zdpBarWidth) < String(down).length * charW,
          'finalW': parseInt(down / all * zdpBarWidth) > String(down).length * charW ? parseInt(down / all * zdpBarWidth) : String(down).length * charW
        }
        // console.log(upDict, downDict)
        var dictArray = [upDict, downDict]
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
        if (downDict['isCalTooSmall']) {
        } else {
          downDict['finalW'] = parseInt(downDict['count']) / leftCount * leftWidth
        }
        this.upDict = upDict
        this.downDict = downDict
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

/* 涨跌条 */
.zdp-bar-box {
  margin: @index-cell-margin;
  width:71.4953%; // 609
  height: @app-cell-height;
  display: inline-flex;
  background-color: pink;
}

/* 涨跌条 - 涨 */
.zdp-bar-up:extend(p) {
  margin: 0px;
  height: 100%;
  min-width: min-content;
  background-color: @app-rise-color;
}

/* 涨跌条 - 跌 */
.zdp-bar-down:extend(p) {
  margin: 0px;
  min-width: min-content;
  height: 100%;
  background-color: @app-fall-color;
}
</style>
