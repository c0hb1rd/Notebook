## 原理
背景是一个 `Svg` 画板，`Sidebar` 组件是各个小的 `Svg` 图，这些监听鼠标事件（事件包含对象本身），然后由 `mxUtil.js` 的 `bind` 方法分发，当事件被分发到 `Svg` 画板之后，画本根据事件的属性获取组件类型（各种不同的图形）、坐标，在叠到 `Svg` 画板之上

## 组件对象
由 `mxClient.js` 中的 `mxShape` 作为基础对象定义，通过对象自身的属性比如 `rotation` 定义了旋转角度、`startSize` 和 `endSize` 定义了组件尺寸、`opacity` 定义了组件的透明度等

## 事件逻辑
* **Sidebar.js** -- 监听图形组件鼠标事件，核心事件为 `Click` 事件和 `DropStart` 事件，事件最后由 `mxEvent.js` 的 `consume` 方法捕获
* **mxEvent.js** -- 捕获 `Sidebar` 中图形组件的事件，捕获之后内部触发 `stopPropagation` 方法，该方法为 `DOM` 对象方法，为停止事件传播
* **mxClient.js** -- 在组件事件停止传播时，会调用内部定义的组件对象 `mxShape` 的 `apply` 方法，方法内部获取当前的组件属性，重新描绘出一个新的图形组件
