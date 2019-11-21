/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "./dist/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/全局.coffee");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/file-loader/dist/cjs.js?!./node_modules/resolve-url-loader/index.js?!./node_modules/sass-loader/dist/cjs.js?!./src/_統合.sass":
/*!********************************************************************************************************************************************************************!*\
  !*** ./node_modules/file-loader/dist/cjs.js??ref--5-1!./node_modules/resolve-url-loader??ref--5-2!./node_modules/sass-loader/dist/cjs.js??ref--5-3!./src/_統合.sass ***!
  \********************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("module.exports = __webpack_require__.p + \"_統合.css\";\n\n//# sourceURL=webpack:///./src/_%E7%B5%B1%E5%90%88.sass?./node_modules/file-loader/dist/cjs.js??ref--5-1!./node_modules/resolve-url-loader??ref--5-2!./node_modules/sass-loader/dist/cjs.js??ref--5-3");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoLinkTag.js":
/*!***************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoLinkTag.js ***!
  \***************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\n\nvar getTarget = function getTarget() {\n  var memo = {};\n  return function memorize(target) {\n    if (typeof memo[target] === 'undefined') {\n      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself\n\n      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {\n        try {\n          // This will throw an exception if access to iframe is blocked\n          // due to cross-origin restrictions\n          styleTarget = styleTarget.contentDocument.head;\n        } catch (e) {\n          // istanbul ignore next\n          styleTarget = null;\n        }\n      }\n\n      memo[target] = styleTarget;\n    }\n\n    return memo[target];\n  };\n}();\n\nmodule.exports = function (url, options) {\n  options = options || {};\n  options.attributes = typeof options.attributes === 'object' ? options.attributes : {};\n\n  if (typeof options.attributes.nonce === 'undefined') {\n    var nonce =  true ? __webpack_require__.nc : undefined;\n\n    if (nonce) {\n      options.attributes.nonce = nonce;\n    }\n  }\n\n  var link = document.createElement('link');\n  link.rel = 'stylesheet';\n  link.href = url;\n  Object.keys(options.attributes).forEach(function (key) {\n    link.setAttribute(key, options.attributes[key]);\n  });\n\n  if (typeof options.insert === 'function') {\n    options.insert(link);\n  } else {\n    var target = getTarget(options.insert || 'head');\n\n    if (!target) {\n      throw new Error(\"Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.\");\n    }\n\n    target.appendChild(link);\n  }\n\n  return function (newUrl) {\n    if (typeof newUrl === 'string') {\n      link.href = newUrl;\n    } else {\n      link.parentNode.removeChild(link);\n    }\n  };\n};\n\n//# sourceURL=webpack:///./node_modules/style-loader/dist/runtime/injectStylesIntoLinkTag.js?");

/***/ }),

/***/ "./src/_統合.sass":
/*!**********************!*\
  !*** ./src/_統合.sass ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var options = {\"injectType\":\"linkTag\"};\n\noptions.insert = \"head\";\n\nvar update = __webpack_require__(/*! ../node_modules/style-loader/dist/runtime/injectStylesIntoLinkTag.js */ \"./node_modules/style-loader/dist/runtime/injectStylesIntoLinkTag.js\")(__webpack_require__(/*! !../node_modules/file-loader/dist/cjs.js??ref--5-1!../node_modules/resolve-url-loader??ref--5-2!../node_modules/sass-loader/dist/cjs.js??ref--5-3!./_統合.sass */ \"./node_modules/file-loader/dist/cjs.js?!./node_modules/resolve-url-loader/index.js?!./node_modules/sass-loader/dist/cjs.js?!./src/_統合.sass\"), options);\n\n\n//# sourceURL=webpack:///./src/_%E7%B5%B1%E5%90%88.sass?");

/***/ }),

/***/ "./src/全局.coffee":
/*!***********************!*\
  !*** ./src/全局.coffee ***!
  \***********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _coffee__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./演出.coffee */ \"./src/演出.coffee\");\n/* harmony import */ var _coffee__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./控制.coffee */ \"./src/控制.coffee\");\n/* harmony import */ var _sass__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./_統合.sass */ \"./src/_統合.sass\");\n/* harmony import */ var _sass__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_sass__WEBPACK_IMPORTED_MODULE_2__);\nvar 在線運行, 從虛擬核心提取資源, 本地運行;\n\n\n\n\n\n\n\nwindow._py演出 = _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"];\n\nwindow.onload = function() {\n  if (window.山彥) {\n    window.本地 = console.log('在本地演出');\n    本地運行();\n  } else {\n    console.log('在瀏覽器上演出');\n    在線運行();\n  }\n  return _coffee__WEBPACK_IMPORTED_MODULE_1__[\"default\"].控制初始化();\n};\n\n本地運行 = function() {\n  window.v = new Vue({\n    el: '#總畫面',\n    data: {\n      本地運行: true,\n      圖片文件夾: '',\n      音樂文件夾: '',\n      視頻文件夾: '',\n      臨時立繪文件夾: '',\n      自定css: '',\n      主題css: '',\n      解析度: '',\n      邊界: '',\n      用戶設置: {\n        文字速度: {\n          類型: 'number',\n          值: 35,\n          範圍: [0, 100],\n          提示: ['須臾', '永恆']\n        },\n        對話框背景透明度: {\n          類型: 'number',\n          值: 0.8,\n          範圍: [0, 1],\n          提示: ['通透', '固實']\n        },\n        總體音量: {\n          類型: 'number',\n          值: 1,\n          範圍: [0, 1],\n          提示: ['小聲', '大聲(沒用)']\n        },\n        自動收起控制面板: {\n          類型: 'boolean',\n          值: false\n        }\n      }\n    },\n    watch: {\n      $data: {\n        handler: function(val, oldVal) {\n          return 山彥.vue更新(val);\n        },\n        deep: true\n      }\n    }\n  });\n  山彥.vue連接初始化(function(x) {\n    var a, b, results;\n    results = [];\n    for (a in x) {\n      b = x[a];\n      results.push(v[a] = b);\n    }\n    return results;\n  });\n  return 山彥.初始化();\n};\n\n從虛擬核心提取資源 = function(心) {\n  var data, i, j, k, l, len, len1, len2, ref, ref1, 人, 圖層, 步, 集合;\n  集合 = {};\n  步 = JSON.parse(JSON.stringify(心.演出步));\n  for (j = 0, len = 步.length; j < len; j++) {\n    data = 步[j];\n    if (data.背景) {\n      集合[`${v.圖片文件夾}/${data.背景[0]}`] = true;\n    }\n    if (data.cg) {\n      集合[`${v.圖片文件夾}/${data.cg[0]}`] = true;\n    }\n    if (data.插入圖) {\n      集合[`${v.圖片文件夾}/${data.插入圖}`] = true;\n    }\n    if (data.背景音樂) {\n      集合[v.音樂文件夾 + '/' + data.背景音樂[0]] = true;\n    }\n    ref = data.立繪;\n    for (k = 0, len1 = ref.length; k < len1; k++) {\n      人 = ref[k];\n      ref1 = 人.圖層;\n      for (l = 0, len2 = ref1.length; l < len2; l++) {\n        圖層 = ref1[l];\n        集合[`${v.臨時立繪文件夾}/${圖層.文件}`] = true;\n      }\n    }\n  }\n  return (function() {\n    var results;\n    results = [];\n    for (i in 集合) {\n      results.push(i);\n    }\n    return results;\n  })();\n};\n\nwindow.加載完成的初始化 = function() {\n  $('#加載畫面').fadeOut();\n  return 山彥.初始化();\n};\n\n在線運行 = function() {\n  var isChrome, j, len, ua, 資源, 資源組;\n  if (typeof 虛擬核心 === \"undefined\") {\n    alert('無法加載虛擬核心。');\n    return;\n  }\n  ua = window.navigator.userAgent;\n  isChrome = ua.indexOf(\"Chrome\") && window.chrome;\n  if (!isChrome) {\n    alert('只有chrome能用。');\n    return;\n  }\n  $('#加載畫面').css('display', 'flex');\n  window.山彥 = {\n    n: 0,\n    更新: function() {\n      return _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].改變演出狀態(虛擬核心.演出步[this.n]);\n    },\n    步進: function() {\n      return this.n += 1;\n    },\n    步進更新: function() {\n      this.步進();\n      return this.更新();\n    },\n    設置: function() {\n      return 0;\n    },\n    初始化: function() {\n      return _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].準備工作();\n    },\n    切換全屏: function() {\n      var cancelFullScreen, doc, docEl, requestFullScreen;\n      doc = window.document;\n      docEl = doc.documentElement;\n      requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;\n      cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen;\n      if (!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {\n        return requestFullScreen.call(docEl);\n      } else {\n        return cancelFullScreen.call(doc);\n      }\n    }\n  };\n  window.v = new Vue({\n    el: '#總畫面',\n    data: {\n      本地運行: false,\n      圖片文件夾: 虛擬核心.圖片文件夾,\n      音樂文件夾: 虛擬核心.音樂文件夾,\n      視頻文件夾: 虛擬核心.視頻文件夾,\n      臨時立繪文件夾: 虛擬核心.臨時立繪文件夾,\n      自定css: 虛擬核心.自定css,\n      主題css: 虛擬核心.主題css,\n      解析度: 虛擬核心.解析度,\n      邊界: 虛擬核心.邊界,\n      用戶設置: {\n        文字速度: {\n          類型: 'number',\n          值: 35,\n          範圍: [0, 100],\n          提示: ['須臾', '永恆']\n        },\n        對話框背景透明度: {\n          類型: 'number',\n          值: 0.8,\n          範圍: [0, 1],\n          提示: ['通透', '固實']\n        },\n        總體音量: {\n          類型: 'number',\n          值: 1,\n          範圍: [0, 1],\n          提示: ['小聲', '大聲(沒用)']\n        },\n        自動收起控制面板: {\n          類型: 'boolean',\n          值: false\n        }\n      }\n    }\n  });\n  資源組 = 從虛擬核心提取資源(虛擬核心);\n  window.v加載 = new Vue({\n    el: '#加載畫面',\n    data: {\n      最大值: 資源組.length,\n      計數: 0\n    }\n  });\n  for (j = 0, len = 資源組.length; j < len; j++) {\n    資源 = 資源組[j];\n    $.get(資源, function() {\n      return v加載.計數 += 1;\n    });\n  }\n  return $('title').html(虛擬核心.作品名);\n};\n\n\n//# sourceURL=webpack:///./src/%E5%85%A8%E5%B1%80.coffee?");

/***/ }),

/***/ "./src/圖像融合.coffee":
/*!*************************!*\
  !*** ./src/圖像融合.coffee ***!
  \*************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\nvar 圖像融合;\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (圖像融合 = {\n  緩存: {},\n  圖像融合: function(圖片名組, f) {\n    var go, i, j, len, m, t, 圖片組, 緩存;\n    緩存 = this.緩存;\n    if (緩存[圖片名組.toString()]) {\n      t = this.緩存[圖片名組.toString()];\n      f(t[0], t[1]);\n    }\n    m = 0;\n    圖片組 = [];\n    for (j = 0, len = 圖片名組.length; j < len; j++) {\n      i = 圖片名組[j];\n      t = new Image();\n      t.src = i[0];\n      t.setAttribute(\"crossOrigin\", 'Anonymous');\n      t.偏移x = i[1];\n      t.偏移y = i[2];\n      圖片組.push(t);\n      t.onload = function() {\n        m += 1;\n        if (m === 圖片名組.length) {\n          return go(緩存);\n        }\n      };\n    }\n    return go = function(緩存) {\n      var base64, canvas, context, k, len1, 圖片, 極x, 極y;\n      極x = Math.max.apply(Math, (function() {\n        var k, len1, results;\n        results = [];\n        for (k = 0, len1 = 圖片組.length; k < len1; k++) {\n          圖片 = 圖片組[k];\n          results.push(圖片.width + 圖片.偏移x);\n        }\n        return results;\n      })());\n      極y = Math.max.apply(Math, (function() {\n        var k, len1, results;\n        results = [];\n        for (k = 0, len1 = 圖片組.length; k < len1; k++) {\n          圖片 = 圖片組[k];\n          results.push(圖片.height + 圖片.偏移y);\n        }\n        return results;\n      })());\n      canvas = document.createElement(\"canvas\");\n      canvas.width = 極x;\n      canvas.height = 極y;\n      context = canvas.getContext(\"2d\");\n      for (k = 0, len1 = 圖片組.length; k < len1; k++) {\n        圖片 = 圖片組[k];\n        context.drawImage(圖片, 圖片.偏移x, 圖片.偏移y, 圖片.width, 圖片.height);\n      }\n      base64 = canvas.toDataURL(\"image/png\");\n      緩存[圖片名組.toString()] = [[極x, 極y], base64];\n      return f([極x, 極y], base64);\n    };\n  },\n  融合到div: function(圖片名組, 時間, div名) {\n    return this.圖像融合(圖片名組, function(尺寸, base64) {\n      var dv;\n      dv = document.getElementById(div名);\n      dv.style.transition = `background ${時間}s, width ${時間}s, height ${時間}s`;\n      dv.style.width = 尺寸[0];\n      dv.style.height = 尺寸[1];\n      return dv.style.backgroundImage = `url(${base64})`;\n    });\n  }\n});\n\n\n//# sourceURL=webpack:///./src/%E5%9C%96%E5%83%8F%E8%9E%8D%E5%90%88.coffee?");

/***/ }),

/***/ "./src/控制.coffee":
/*!***********************!*\
  !*** ./src/控制.coffee ***!
  \***********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _coffee__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./演出.coffee */ \"./src/演出.coffee\");\nvar 控制;\n\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (控制 = {\n  右鍵功能: function() {\n    window.event.returnValue = false;\n    $('#總畫面').attr('歷史', 'off');\n    if ($('#總畫面').attr('對話框') === 'off') {\n      return $('#總畫面').attr('對話框', 'on');\n    } else {\n      return $('#總畫面').attr('對話框', 'off');\n    }\n  },\n  左鍵屏蔽: false,\n  左鍵功能: function() {\n    if (this.左鍵屏蔽 || _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].選擇之刻) {\n      return;\n    }\n    if ($('#總畫面').attr('歷史') === 'on') {\n      $('#總畫面').attr('歷史', 'off');\n    }\n    if ($('#總畫面').attr('對話框') === 'off') {\n      return $('#總畫面').attr('對話框', 'on');\n    } else {\n      if (Date.now() < _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].淡入過期時間) {\n        _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].淡入過期時間 = 0;\n        return _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].早泄();\n      } else {\n        return _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].步進更新();\n      }\n    }\n  },\n  顯示履歷: function() {\n    $('#總畫面').attr('歷史', 'on');\n    $('#總畫面').attr('對話框', 'off');\n    return $('#對話歷史').scrollTop($('#對話歷史')[0].scrollHeight);\n  },\n  正在快進: false,\n  開始快進: function() {\n    if (this.正在快進 === false) {\n      this.正在快進 = true;\n      return this.快進輪迴();\n    }\n  },\n  結束快進: function() {\n    return this.正在快進 = false;\n  },\n  切換快進: function() {\n    if (this.正在快進 === false) {\n      this.正在快進 = true;\n      return this.快進輪迴();\n    } else {\n      return this.正在快進 = false;\n    }\n  },\n  快進輪迴: function() {\n    if (控制.正在快進 === false) {\n\n    } else {\n      控制.左鍵功能();\n      return setTimeout(控制.快進輪迴, 50);\n    }\n  },\n  進入設置: function() {\n    return $('#總畫面').attr('配置面板', 'on');\n  },\n  退出設置: function() {\n    return $('#總畫面').attr('配置面板', 'off');\n  },\n  控制初始化: function() {\n    window.document.onkeydown = function(evt) {\n      var k;\n      k = evt.keyCode;\n      // [ctrl] skip\n      if (k === 17) {\n        console.log('ctrl按下');\n        控制.開始快進();\n      }\n      // [空格 回車 z] 左鍵\n      if (k === 32 || k === 13 || k === 90) {\n        控制.左鍵功能();\n      }\n      // [esc] 右鍵\n      if (k === 27) {\n        控制.右鍵功能();\n      }\n      // [Page_up] 歷史\n      if (k === 33) {\n        return 控制.顯示履歷();\n      }\n    };\n    window.document.onkeyup = function(evt) {\n      // [ctrl] skip\n      if (evt.keyCode === 17) {\n        console.log('ctrl放開');\n        return 控制.結束快進();\n      }\n    };\n    \n    // 滚轮功能\n    $('#主畫面').mousewheel(function(event, delta) {\n      if (delta > 0) {\n        控制.顯示履歷();\n      }\n      if (delta < 0) {\n        return 控制.左鍵功能();\n      }\n    });\n    $(\"#主畫面\").mousedown(function(e) {\n      if (e.which === 3) {\n        return 控制.右鍵功能();\n      } else if (e.which === 1) {\n        return 控制.左鍵功能();\n      }\n    });\n    $('#存檔').click(function() {\n      return 山彥.存檔();\n    });\n    $('#讀檔').click(function() {\n      return 山彥.讀檔();\n    });\n    $('#快速存檔').click(function() {\n      return 山彥.快速存檔();\n    });\n    $('#快速讀檔').click(function() {\n      return 山彥.快速讀檔();\n    });\n    $('#自動模式').click(function() {\n      return alert(\"沒做這個功能\");\n    });\n    $('#切換快進').click(function() {\n      return 控制.切換快進();\n    });\n    $('#進入設置').click(function() {\n      return 控制.進入設置();\n    });\n    $('#回標題').click(function() {\n      return 山彥.回標題();\n    });\n    return $('#退出設置').click(function() {\n      return 控制.退出設置();\n    });\n  }\n});\n\n\n//# sourceURL=webpack:///./src/%E6%8E%A7%E5%88%B6.coffee?");

/***/ }),

/***/ "./src/演出.coffee":
/*!***********************!*\
  !*** ./src/演出.coffee ***!
  \***********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _coffee__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./控制.coffee */ \"./src/控制.coffee\");\n/* harmony import */ var _coffee__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./圖像融合.coffee */ \"./src/圖像融合.coffee\");\nvar 演出;\n\n\n\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (演出 = {\n  準備工作: function() {\n    var i, j, len, ref;\n    $('<link>').attr({\n      rel: 'stylesheet',\n      type: 'text/css',\n      href: v.主題css\n    }).appendTo(\"head\");\n    ref = v.自定css;\n    for (j = 0, len = ref.length; j < len; j++) {\n      i = ref[j];\n      $('<link>').attr({\n        rel: 'stylesheet',\n        type: 'text/css',\n        href: i\n      }).appendTo('head');\n    }\n    $('#總畫面').css('width', v.解析度[0]);\n    $('#總畫面').css('height', v.解析度[1]);\n    if (v.邊界) {\n      $('div').css('border', '1px solid #22f');\n    }\n    this.縮放調整();\n    return this.更新();\n  },\n  縮放調整: function() {\n    var a, b, t;\n    a = document.body.clientWidth / v.解析度[0];\n    b = document.body.clientHeight / v.解析度[1];\n    t = Math.min(a, b);\n    $('#總畫面').css({\n      \"transform-origin\": \"0% 0%\",\n      \"transform\": \"scale(\" + t + \")\"\n    });\n    return setTimeout(演出.縮放調整, 200);\n  },\n  步進更新: function() {\n    return 山彥.步進更新();\n  },\n  更新: function() {\n    return 山彥.更新();\n  },\n  信息預處理: function(data) {\n    var j, len, ref, results, 人, 圖層;\n    console.log(data);\n    if (data.背景) {\n      data.背景[0] = `url(${v.圖片文件夾}/${data.背景[0]})`;\n    }\n    if (data.cg) {\n      data.cg[0] = `url(${v.圖片文件夾}/${data.cg[0]})`;\n    }\n    if (data.背景音樂) {\n      data.背景音樂[0] = v.音樂文件夾 + '/' + data.背景音樂[0];\n    }\n    if (data.插入圖) {\n      data.插入圖 = `url(${v.圖片文件夾}/${data.插入圖})`;\n    }\n    ref = data.立繪;\n    results = [];\n    for (j = 0, len = ref.length; j < len; j++) {\n      人 = ref[j];\n      results.push((function() {\n        var k, len1, ref1, results1;\n        ref1 = 人.圖層;\n        results1 = [];\n        for (k = 0, len1 = ref1.length; k < len1; k++) {\n          圖層 = ref1[k];\n          results1.push(圖層.文件 = `${v.臨時立繪文件夾}/${圖層.文件}`);\n        }\n        return results1;\n      })());\n    }\n    return results;\n  },\n  瞬間化: false,\n  改變演出狀態: function(data) {\n    var cg, js, 名字, 插入圖, 特效表, 立繪, 背景, 背景音樂, 視頻, 話語, 語者, 選項, 額外信息;\n    this.信息預處理(data);\n    ({特效表, 插入圖, 立繪, 名字, 話語, 額外信息, 語者, 背景, 背景音樂, cg, 選項, js, 視頻} = data);\n    this.特效處理(特效表);\n    if (選項.length > 0) {\n      this.處理選項(選項);\n      return;\n    }\n    if (插入圖) {\n      名字 = '';\n      話語 = '';\n      背景音樂 = null;\n      this.換圖('覆蓋', 插入圖, 0);\n      $('#覆蓋').attr('顯現', 'true');\n    } else {\n      if ($('#覆蓋').attr('顯現') === 'true') {\n        this.瞬間化 = true;\n      }\n      $('#覆蓋').attr('顯現', 'false');\n    }\n    if (額外信息) {\n      if (額外信息[0] === 'load') {\n        this.load特效();\n      }\n    }\n    eval(js);\n    this.放視頻(視頻);\n    this.換cg(cg);\n    this.換背景(背景, this.瞬間化);\n    this.換立繪(立繪, this.瞬間化);\n    this.換背景音樂(背景音樂);\n    this.換人名(語者, 名字);\n    this.換對話(話語, 名字);\n    return this.瞬間化 = false;\n  },\n  特效處理: function(特效表) {\n    var i, j, len, results, 可特效块;\n    可特效块 = ['總畫面', 'adv畫面', '主畫面', '覆蓋', '選項', 'cg', 'bg', '立繪', '對話歷史', '對話框', '名字框', '名字', '名字框背景', '話語框', '話語', '話語框背景', '對話框背景'];\n    for (j = 0, len = 可特效块.length; j < len; j++) {\n      i = 可特效块[j];\n      if ($('#' + i).attr('特效')) {\n        $('#' + i).attr('特效', '');\n      }\n    }\n    results = [];\n    for (i in 特效表) {\n      results.push($('#' + i).attr('特效', 特效表[i]));\n    }\n    return results;\n  },\n  選擇之刻: false,\n  處理選項: function(選項) {\n    var i, j, len, p, tot;\n    tot = '';\n    for (p = j = 0, len = 選項.length; j < len; p = ++j) {\n      i = 選項[p];\n      tot += `<button onclick='演出.點選項(${p});'>${i}</botton>\\n`;\n    }\n    $('#選項').html(tot);\n    $('#選項').show(250);\n    return this.選擇之刻 = true;\n  },\n  點選項: function(x) {\n    $('#選項').hide(250);\n    山彥.選(x);\n    return this.選擇之刻 = false;\n  },\n  放視頻: function(視頻) {\n    var video, 可以跳過, 視頻文件;\n    if (!視頻) {\n      return;\n    }\n    [視頻文件, 可以跳過] = 視頻;\n    video = $('video');\n    video.css('display', 'block');\n    video.attr('src', v.視頻文件夾 + '/' + 視頻文件);\n    video.click(可以跳過 ? function() {\n      video.css('animation', '_黑出 0.5s');\n      video.css('animation-fill-mode', 'forwards');\n      return setTimeout(function() {\n        video.css('animation', '');\n        video.attr('src', '');\n        return video[0].style.display = 'none';\n      }, 600);\n    } : function() {\n      return null;\n    });\n    video[0].addEventListener('ended', function() {\n      return video[0].style.display = 'none';\n    }, false);\n    return video[0].play();\n  },\n  load特效: function() {\n    _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].左鍵屏蔽 = true;\n    $('#總畫面').fadeOut(0);\n    $('#總畫面').fadeIn(1200);\n    return setTimeout(function() {\n      return _coffee__WEBPACK_IMPORTED_MODULE_0__[\"default\"].左鍵屏蔽 = false;\n    }, 1000);\n  },\n  提示: function(x) {\n    $('#提示').html(x);\n    $('#提示').fadeIn(300);\n    return $('#提示').hide(1000);\n  },\n  現在cg: null,\n  換cg: function(cg) {\n    var cg圖片, 淡入時間, 漸變方法;\n    if (cg) {\n      [cg圖片, 淡入時間, 漸變方法] = cg;\n    } else {\n      [cg圖片, 淡入時間, 漸變方法] = ['', 0, ''];\n    }\n    if (cg圖片 === this.現在cg) {\n      return;\n    }\n    this.現在cg = cg圖片;\n    return this.換圖('cg', cg圖片, 淡入時間, 漸變方法);\n  },\n  當前人物: [],\n  換立繪: function(立繪組, 瞬 = false) {\n    var j, k, l, len, len1, len2, len3, len4, m, n, ref, t, 名字, 名字組, 層, 移動時間, 立繪, 組;\n    名字組 = (function() {\n      var j, len, results;\n      results = [];\n      for (j = 0, len = 立繪組.length; j < len; j++) {\n        立繪 = 立繪組[j];\n        results.push(立繪.名字);\n      }\n      return results;\n    })();\n    ref = this.當前人物;\n    for (j = 0, len = ref.length; j < len; j++) {\n      名字 = ref[j];\n      if (名字組.indexOf(名字) === -1) {\n        $(`#立繪--${名字}`).remove();\n        console.log(`去除 ${名字}`);\n      }\n    }\n    for (k = 0, len1 = 名字組.length; k < len1; k++) {\n      名字 = 名字組[k];\n      if (this.當前人物.indexOf(名字) === -1) {\n        $('#立繪').append($(`<div id='立繪--${名字}'><div id='立繪--${名字}--圖像'></div></div>`));\n        console.log(`加入 ${名字}`);\n        for (l = 0, len2 = 立繪組.length; l < len2; l++) {\n          立繪 = 立繪組[l];\n          if (立繪.名字 === 名字) {\n            立繪.特效.push('淡入');\n          }\n        }\n      }\n    }\n    for (m = 0, len3 = 立繪組.length; m < len3; m++) {\n      立繪 = 立繪組[m];\n      t = $(`#立繪--${立繪.名字}`);\n      if (瞬) {\n        t.css('transition', '');\n      } else {\n        移動時間 = 0.5;\n        t.css('transition', `top ${移動時間}s, left ${移動時間}s, transform ${移動時間}s`);\n      }\n      t.css('left', `${立繪.位置[0]}px`);\n      t.css('top', `${立繪.位置[1]}px`);\n      t.css('transform', `scale(${立繪.位置[2]})`);\n      $(`#立繪--${立繪.名字}--圖像`).attr('特效', 立繪.特效.join(\" \"));\n    }\n    for (n = 0, len4 = 立繪組.length; n < len4; n++) {\n      立繪 = 立繪組[n];\n      組 = (function() {\n        var len5, o, ref1, results;\n        ref1 = 立繪.圖層;\n        results = [];\n        for (o = 0, len5 = ref1.length; o < len5; o++) {\n          層 = ref1[o];\n          results.push([層.文件, 層.子位置[0], 層.子位置[1]]);\n        }\n        return results;\n      })();\n      _coffee__WEBPACK_IMPORTED_MODULE_1__[\"default\"].融合到div(組, 0.5, `立繪--${立繪.名字}--圖像`);\n    }\n    return this.當前人物 = 名字組;\n  },\n  現在背景: [null, \"0% 0%\"],\n  換背景: function(背景, 瞬) {\n    var 位置, 淡入時間, 漸變方法, 背景圖片;\n    if (背景) {\n      [背景圖片, 淡入時間, 位置, 漸變方法] = 背景;\n    } else {\n      [背景圖片, 淡入時間, 位置, 漸變方法] = ['', 0, ''];\n    }\n    if (瞬) {\n      淡入時間 = 0;\n    }\n    if (背景圖片 !== this.現在背景[0]) {\n      $('#bg').css('background-position', 位置);\n      this.換圖('bg', 背景圖片, 淡入時間, 漸變方法);\n    } else if (位置 !== this.現在背景[1]) {\n      $('#bg').css('background-position', 位置);\n    }\n    return this.現在背景 = [背景圖片, 位置];\n  },\n  換人名: function(語者, 名字) {\n    if (名字) {\n      $('#名字').html(名字);\n      $('#名字框').css('opacity', 1);\n    } else {\n      $('#名字框').css('opacity', 0);\n    }\n    $('#對話歷史').append(名字 + '<br/>');\n    return $('#對話框').attr('名字', 語者);\n  },\n  淡入過期時間: 0,\n  換對話: function(text, 名字) {\n    var 淡入字;\n    if (名字 !== '') {\n      $('#對話框').attr('對話類型', '對話');\n    } else {\n      $('#對話框').attr('對話類型', '旁白');\n    }\n    淡入字 = 演出.文字淡入(text);\n    $('#話語').html(淡入字.內容);\n    演出.淡入過期時間 = Date.now() + 淡入字.總時間 * 1000;\n    return $('#對話歷史').append(text + '<br/><br/>');\n  },\n  早泄: function() {\n    $('#話語 *').css('animation', 'None');\n    return $('#話語 *').css('opacity', '1');\n  },\n  當前曲名: null,\n  換背景音樂: function(背景音樂) {\n    var i, j, len, ref, 曲名, 音樂, 音量;\n    if (背景音樂) {\n      [曲名, 音量] = 背景音樂;\n    } else {\n      [曲名, 音量] = [null, 0];\n    }\n    if (this.當前曲名 === 曲名) {\n      return;\n    }\n    this.當前曲名 = 曲名;\n    ref = $('#總畫面 > audio');\n    for (j = 0, len = ref.length; j < len; j++) {\n      i = ref[j];\n      if (i.volume === 0) {\n        i.remove();\n      }\n    }\n    $('#總畫面 > audio').animate({\n      volume: 0\n    }, 500);\n    音樂 = $(`<audio src='${曲名}' autoplay loop></audio>`);\n    音樂.volume = 音量;\n    return $('#總畫面').append(音樂);\n  },\n  換圖: function(目標, 新圖, 漸變時間, 漸變方法 = '_淡出') {\n    var 原背景, 舊淡出;\n    目標 = $('#' + 目標);\n    原背景 = 目標.css('background-image');\n    目標.css('background-image', 新圖);\n    目標.html('<div class=\"舊淡出\"></div>');\n    舊淡出 = 目標.children();\n    if (漸變時間 > 0) {\n      舊淡出.css('background-image', 原背景);\n      舊淡出.css('animation', `${漸變方法} ${漸變時間}s`);\n      舊淡出.css('animation-fill-mode', 'forwards');\n      return 舊淡出.css('animation-play-state', 'running');\n    }\n  },\n  文字淡入: function(s, 動畫名 = '_淡入') {\n    var group, i, 內容, 動畫時間, 時間, 時間間隔;\n    時間間隔 = v.用戶設置.文字速度.值 / 800;\n    group = s.replace(/((<.*?>)|(.))/g, \"$2$3\\0\").split('\\0');\n    動畫時間 = 時間間隔 * 8;\n    時間 = 0;\n    內容 = ((function() {\n      var j, len, results;\n      results = [];\n      for (j = 0, len = group.length; j < len; j++) {\n        i = group[j];\n        if (i[0] === '<') {\n          results.push(i);\n        } else {\n          時間 += 時間間隔;\n          results.push(`<span style='animation:${動畫名} ${動畫時間}s;animation-fill-mode:forwards;animation-delay:${時間}s;opacity:0;'>${i}</span>`);\n        }\n      }\n      return results;\n    })()).join('');\n    return {\n      內容,\n      總時間: 時間 + 動畫時間\n    };\n  }\n});\n\n\n//# sourceURL=webpack:///./src/%E6%BC%94%E5%87%BA.coffee?");

/***/ })

/******/ });