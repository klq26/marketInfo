<template>
  <div>
    <div class='zdp-cell'>
      <p class="zdp-title">涨跌停板</p>
      <div class='zdp-bar-box'>
        <p class="zdp-bar-up" :style="{width: dynamicWidth('zt')}">{{zdt[0].value}}</p>
        <p class="zdp-bar-down" :style="{width: dynamicWidth('dt')}">{{zdt[1].value}}</p>
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
      // zdpinfo: [
      //   {name: '全市场', symbol: 'all', 'd':2160,'p':135,'z':1495 },
      //   {name: '中证500', symbol: 'sh000905', 'd':8,'p':49,'z':450 }
      // ],
      measuredInfo: {
        // {
        //   symbol:'all', 'd': {count:2160, rate:0, minWidth:0}, 'p': {count:135, rate:0, minWidth:0}, 'z': {count:1495, rate:0, minWidth:0}
        // },
        // {
        //   symbol:'sh000905', 'd': {count:1, rate:0, minWidth:0}, 'p': {count:49, rate:0, minWidth:0}, 'z': {count:450, rate:0, minWidth:0}
        // }
      }
    }
  },
  methods: {
    dynamicWidth (key) {
      let result = parseFloat(this.measuredInfo[key]["finalW"]) + 'px'
      console.log(result, key)
      return result
    }
  },
  watch: {
    zdt: {
      handler (newValue, oldValue) {
        console.log('康力泉')
        console.log('newValue ' + newValue, oldValue)
        // 单个阿拉伯数字的宽度
        let charW = 21.11
        // 值条宽度（vue 是虚拟 dom，无法等到实际 mounted 之后再计算了）
        let zdpBarWidth = 609
        let up = newValue[0].value
        let down = newValue[1].value
        let all = up + down
        let symbol = 'zdt'
        // 生成涨跌平条的全面数据
        var upDict = {
        "count": up,
        "calW": parseInt(up / all * zdpBarWidth),
        "minW": String(up).length * charW,
        "isCalTooSmall": parseInt(up / all * zdpBarWidth) < String(up).length * charW ? true : false,
        "finalW": parseInt(up / all * zdpBarWidth) > String(up).length * charW ? parseInt(up / all * zdpBarWidth) : String(up).length * charW
        }
        var downDict = {
        "count": down,
        "calW": parseInt(down / all * zdpBarWidth),
        "minW": String(down).length * charW,
        "isCalTooSmall": parseInt(down / all * zdpBarWidth) < String(down).length * charW ? true : false,
        "finalW": parseInt(down / all * zdpBarWidth) > String(down).length * charW ? parseInt(down / all * zdpBarWidth) : String(down).length * charW
        }
        // console.log(upDict, equalDict, downDict)
        var dictArray = [upDict, downDict];
        var leftCount = 0;
        var leftWidth = zdpBarWidth;
        // 如果原比例计算的宽度不足以显示内容，则保留字段的最小视觉宽度，放弃之前的三者共同计算比例
        // 每去掉一个比例条，就要相应剪掉其对应的宽度，剩下的条重新计算比例，重新共享宽度
        for (var idx in dictArray) {
            var currentBar = dictArray[idx];
            if (!currentBar['isCalTooSmall']) {
                leftCount = leftCount + currentBar['count'];
            } else {
                leftWidth = leftWidth - currentBar['finalW'];
            }
        }
        // 根据是最小宽度还是计算宽度，来决定每个元素的最终绘制宽度
        if (upDict['isCalTooSmall']) {
        } else {
            upDict['finalW'] = parseInt(upDict['count']) / leftCount * leftWidth;
        }
        if (downDict['isCalTooSmall']) {
        } else {
            downDict['finalW'] = parseInt(downDict['count']) / leftCount * leftWidth;
        }
        this.measuredInfo['zt'] = upDict
        this.measuredInfo['dt'] = downDict
        console.log(this.measuredInfo)
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
