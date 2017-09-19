## 事件逻辑
* **Sidebar.js** -- 监听图形组件鼠标事件，核心事件为 `Click` 事件和 `DropStart` 事件，事件最后由 `mxEvent.js` 的 `consume` 方法捕获
* **mxEvent.js** -- 捕获 `Sidebar` 中图形组件的事件，捕获之后内部触发 `stopPropagation` 方法，该方法为 `DOM` 对象方法，为停止事件传播
