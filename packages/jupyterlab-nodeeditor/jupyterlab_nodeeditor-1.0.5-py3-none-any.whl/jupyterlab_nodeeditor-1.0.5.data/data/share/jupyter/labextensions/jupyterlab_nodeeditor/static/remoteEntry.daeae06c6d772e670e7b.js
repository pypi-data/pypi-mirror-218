var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/jupyterlab_nodeeditor":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-flume_node_modules_prop-types_index_js-node_modules_process_browser_js"), __webpack_require__.e("webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-flume_node_modules_prop-types_index_js-node_modules_process_browser_js"), __webpack_require__.e("webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./style": () => {
		return __webpack_require__.e("style_index_js").then(() => (() => ((__webpack_require__(/*! ./style/index.js */ "./style/index.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/amd options */
/******/ 	(() => {
/******/ 		__webpack_require__.amdO = {};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-flume_node_modules_prop-types_index_js-node_modules_process_browser_js":"42651e68d03e160d6f50","webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react":"37d5d2afd4bb8756aacf","lib_index_js":"fcc62e78977ee568769f","style_index_js":"81c2517e7d07af255c14","vendors-node_modules_monaco-editor_esm_vs_editor_editor_main_js":"2f82887a25519ad5606c","node_modules_process_browser_js-data_image_png_base64_iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAAC-c7fe92":"426b74ce6f751a6627be","vendors-node_modules_react-portal_es_index_js":"e0238c949efe3800e101","vendors-node_modules_uuid_dist_esm-browser_index_js":"50ddbbbe16d9fbb8e598","data_image_png_base64_iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5_AAAAAXNSR0IArs4c6QAAAARnQU1-5f4412":"8573e56b3e457c1d826b","vendors-node_modules_monaco-editor_esm_vs_basic-languages_abap_abap_js":"b9acd748da7ff3350995","node_modules_monaco-editor_esm_vs_basic-languages_apex_apex_js":"9982e0769f40abee234a","node_modules_monaco-editor_esm_vs_basic-languages_azcli_azcli_js":"182cee8a9aa456f6febd","node_modules_monaco-editor_esm_vs_basic-languages_bat_bat_js":"55db1a421d24f3d884a7","node_modules_monaco-editor_esm_vs_basic-languages_bicep_bicep_js":"1d144118bc30d3f19464","node_modules_monaco-editor_esm_vs_basic-languages_cameligo_cameligo_js":"1674e1b671d71f42a4c2","vendors-node_modules_monaco-editor_esm_vs_basic-languages_clojure_clojure_js":"a5f8283882d0bdb93925","node_modules_monaco-editor_esm_vs_basic-languages_coffee_coffee_js":"5203585c44a43b4dd973","node_modules_monaco-editor_esm_vs_basic-languages_cpp_cpp_js":"0fa4bdcecb4b3a69eb94","node_modules_monaco-editor_esm_vs_basic-languages_csharp_csharp_js":"d17276a727e138d62758","node_modules_monaco-editor_esm_vs_basic-languages_csp_csp_js":"7d0541c505bba64c05d9","node_modules_monaco-editor_esm_vs_basic-languages_css_css_js":"ee8ef84415cbaf78afb7","node_modules_monaco-editor_esm_vs_basic-languages_cypher_cypher_js":"a0c83171cb974949a02c","node_modules_monaco-editor_esm_vs_basic-languages_dart_dart_js":"4420e06db9a150d9b45c","node_modules_monaco-editor_esm_vs_basic-languages_dockerfile_dockerfile_js":"2f95d8158ea4f41996f4","node_modules_monaco-editor_esm_vs_basic-languages_ecl_ecl_js":"0f56bcbc2002bbee3a30","vendors-node_modules_monaco-editor_esm_vs_basic-languages_elixir_elixir_js":"2979134714531778d948","node_modules_monaco-editor_esm_vs_basic-languages_flow9_flow9_js":"ee19c04e3556e2f3320e","node_modules_monaco-editor_esm_vs_basic-languages_fsharp_fsharp_js":"7a7fd32fad2f13d0265b","vendors-node_modules_monaco-editor_esm_vs_basic-languages_freemarker2_freemarker2_js":"7d62e95fa6c125a74bf5","node_modules_monaco-editor_esm_vs_basic-languages_go_go_js":"5be77765d5a4b7ffa983","node_modules_monaco-editor_esm_vs_basic-languages_graphql_graphql_js":"4a586f64f410b2ee3f6a","vendors-node_modules_monaco-editor_esm_vs_basic-languages_handlebars_handlebars_js":"f2c604f0bc3f6423e8c7","node_modules_monaco-editor_esm_vs_basic-languages_hcl_hcl_js":"230c7d363321015f2c60","node_modules_monaco-editor_esm_vs_basic-languages_html_html_js":"6d7d95bee6027181f0af","node_modules_monaco-editor_esm_vs_basic-languages_ini_ini_js":"b4cd6fd84ced941317a1","node_modules_monaco-editor_esm_vs_basic-languages_java_java_js":"b5a0555fb9f413aebaf1","vendors-node_modules_monaco-editor_esm_vs_basic-languages_javascript_javascript_js":"c3c5914a19d6e077645e","vendors-node_modules_monaco-editor_esm_vs_basic-languages_julia_julia_js":"660cedb0abb2fe3e27a7","node_modules_monaco-editor_esm_vs_basic-languages_kotlin_kotlin_js":"84d331c6922c4b011779","node_modules_monaco-editor_esm_vs_basic-languages_less_less_js":"0cefe82e77a5f720a3a8","node_modules_monaco-editor_esm_vs_basic-languages_lexon_lexon_js":"5856d26bc8d67dadde9e","node_modules_monaco-editor_esm_vs_basic-languages_lua_lua_js":"7bb5d5716d12f5c2174e","node_modules_monaco-editor_esm_vs_basic-languages_liquid_liquid_js":"ccc8e1bb782d3bdb55c0","node_modules_monaco-editor_esm_vs_basic-languages_m3_m3_js":"afda01e1b4bcc050d4f2","node_modules_monaco-editor_esm_vs_basic-languages_markdown_markdown_js":"1fb78cdc3130ad3eaba3","node_modules_monaco-editor_esm_vs_basic-languages_mips_mips_js":"1bf6111c8b5601cd2b20","node_modules_monaco-editor_esm_vs_basic-languages_msdax_msdax_js":"64aeebc1b0c103ab96af","vendors-node_modules_monaco-editor_esm_vs_basic-languages_mysql_mysql_js":"4dcbef8818f057aeaab3","node_modules_monaco-editor_esm_vs_basic-languages_objective-c_objective-c_js":"8c0d01235bc1d630adfa","node_modules_monaco-editor_esm_vs_basic-languages_pascal_pascal_js":"df74d1d4ca179e1b1afd","node_modules_monaco-editor_esm_vs_basic-languages_pascaligo_pascaligo_js":"ff3af5a55838b031f360","vendors-node_modules_monaco-editor_esm_vs_basic-languages_perl_perl_js":"92abc34c6cf667e58d20","vendors-node_modules_monaco-editor_esm_vs_basic-languages_pgsql_pgsql_js":"0964523139d4821964b6","vendors-node_modules_monaco-editor_esm_vs_basic-languages_php_php_js":"89c54b836095365cbd76","node_modules_monaco-editor_esm_vs_basic-languages_pla_pla_js":"1932e28a5d8475c1ee52","vendors-node_modules_monaco-editor_esm_vs_basic-languages_postiats_postiats_js":"39e416b365187b825ab1","vendors-node_modules_monaco-editor_esm_vs_basic-languages_powerquery_powerquery_js":"794f25521bfb793e2592","node_modules_monaco-editor_esm_vs_basic-languages_powershell_powershell_js":"e3c2ee7998ea24edb731","vendors-node_modules_monaco-editor_esm_vs_basic-languages_protobuf_protobuf_js":"109b1979e218a3fccb2a","node_modules_monaco-editor_esm_vs_basic-languages_pug_pug_js":"9926ff3fec177afe4c34","node_modules_monaco-editor_esm_vs_basic-languages_python_python_js":"f9cd61ae70cb69be71d9","node_modules_monaco-editor_esm_vs_basic-languages_qsharp_qsharp_js":"3159e1b26ee42f37dc9e","node_modules_monaco-editor_esm_vs_basic-languages_r_r_js":"08cb4e804cb3e9a28ace","vendors-node_modules_monaco-editor_esm_vs_basic-languages_razor_razor_js":"963081f3fb1d7074c622","node_modules_monaco-editor_esm_vs_basic-languages_redis_redis_js":"8ae88e112ec72cfcf9f7","vendors-node_modules_monaco-editor_esm_vs_basic-languages_redshift_redshift_js":"2bec585aca61add92a63","node_modules_monaco-editor_esm_vs_basic-languages_restructuredtext_restructuredtext_js":"562d4848347010a99e0e","vendors-node_modules_monaco-editor_esm_vs_basic-languages_ruby_ruby_js":"f1d2de0d3708113d1047","node_modules_monaco-editor_esm_vs_basic-languages_rust_rust_js":"7c87889f44878696136b","node_modules_monaco-editor_esm_vs_basic-languages_sb_sb_js":"ae2f354ae4f12d7bd72b","vendors-node_modules_monaco-editor_esm_vs_basic-languages_scala_scala_js":"17d63d898fcd57883055","node_modules_monaco-editor_esm_vs_basic-languages_scheme_scheme_js":"e36dc0d354f0f5b3fbf0","node_modules_monaco-editor_esm_vs_basic-languages_scss_scss_js":"35f4327ac70035ac003a","node_modules_monaco-editor_esm_vs_basic-languages_shell_shell_js":"d8464c269c4488a6b1fe","vendors-node_modules_monaco-editor_esm_vs_basic-languages_solidity_solidity_js":"60c54c6dab98bc84fed9","node_modules_monaco-editor_esm_vs_basic-languages_sophia_sophia_js":"e3f378c1653b0a1e984f","node_modules_monaco-editor_esm_vs_basic-languages_sparql_sparql_js":"d0d19d5b847835e9b1e3","vendors-node_modules_monaco-editor_esm_vs_basic-languages_sql_sql_js":"e41c82d9fa334693ad98","vendors-node_modules_monaco-editor_esm_vs_basic-languages_st_st_js":"da9aa70576309f2d7607","node_modules_monaco-editor_esm_vs_basic-languages_swift_swift_js":"47b7cefa925e9c066b7c","vendors-node_modules_monaco-editor_esm_vs_basic-languages_systemverilog_systemverilog_js":"d4906f14a72eeea290d0","node_modules_monaco-editor_esm_vs_basic-languages_tcl_tcl_js":"d48ef01cf0e13cf29944","node_modules_monaco-editor_esm_vs_basic-languages_twig_twig_js":"d82831f1acc1c666fb3d","node_modules_monaco-editor_esm_vs_basic-languages_typescript_typescript_js":"0ae9761d4b0d1e6cfa16","node_modules_monaco-editor_esm_vs_basic-languages_vb_vb_js":"a4905a4081d413b6d210","node_modules_monaco-editor_esm_vs_basic-languages_wgsl_wgsl_js":"645eabcb3aff15176c38","node_modules_monaco-editor_esm_vs_basic-languages_xml_xml_js":"aacaca7fd9d934e1d513","node_modules_monaco-editor_esm_vs_basic-languages_yaml_yaml_js":"f54c221e346beb62289c","vendors-node_modules_monaco-editor_esm_vs_language_css_cssMode_js":"0e78e528ecf4b44f65e3","vendors-node_modules_monaco-editor_esm_vs_language_html_htmlMode_js":"4d082c3f023de51f874a","vendors-node_modules_monaco-editor_esm_vs_language_json_jsonMode_js":"3877344c5bc28d2c62f1","vendors-node_modules_monaco-editor_esm_vs_language_typescript_tsMode_js":"532242b4e273f33ae96d"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "jupyterlab_nodeeditor:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 		
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => {
/******/ 				if (typeof console !== "undefined" && console.warn) console.warn(msg);
/******/ 			};
/******/ 			var uniqueName = "jupyterlab_nodeeditor";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("jupyterlab_nodeeditor", "1.0.4", () => (Promise.all([__webpack_require__.e("vendors-flume_node_modules_prop-types_index_js-node_modules_process_browser_js"), __webpack_require__.e("webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("monaco-editor", "0.39.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_monaco-editor_esm_vs_editor_editor_main_js"), __webpack_require__.e("node_modules_process_browser_js-data_image_png_base64_iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAAC-c7fe92")]).then(() => (() => (__webpack_require__(/*! ./node_modules/monaco-editor/esm/vs/editor/editor.main.js */ "./node_modules/monaco-editor/esm/vs/editor/editor.main.js"))))));
/******/ 					register("react-portal", "4.2.2", () => (Promise.all([__webpack_require__.e("vendors-node_modules_react-portal_es_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react")]).then(() => (() => (__webpack_require__(/*! ./node_modules/react-portal/es/index.js */ "./node_modules/react-portal/es/index.js"))))));
/******/ 					register("uuid", "9.0.0", () => (__webpack_require__.e("vendors-node_modules_uuid_dist_esm-browser_index_js").then(() => (() => (__webpack_require__(/*! ./node_modules/uuid/dist/esm-browser/index.js */ "./node_modules/uuid/dist/esm-browser/index.js"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src;
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) {
/******/ 					var i = scripts.length - 1;
/******/ 					while (i > -1 && !scriptUrl) scriptUrl = scripts[i--].src;
/******/ 				}
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warn = (msg) => {
/******/ 			if (typeof console !== "undefined" && console.warn) console.warn(msg);
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react-dom": () => (loadSingletonVersionCheck("default", "react-dom", [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersionCheck("default", "react", [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/application": () => (loadSingletonVersionCheck("default", "@jupyterlab/application", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": () => (loadSingletonVersionCheck("default", "@jupyterlab/apputils", [1,4,1,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/settingregistry": () => (loadSingletonVersionCheck("default", "@jupyterlab/settingregistry", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/@lumino/coreutils": () => (loadSingletonVersionCheck("default", "@lumino/coreutils", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docregistry": () => (loadVersionCheck("default", "@jupyterlab/docregistry", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/translation": () => (loadSingletonVersionCheck("default", "@jupyterlab/translation", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook": () => (loadSingletonVersionCheck("default", "@jupyterlab/notebook", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": () => (loadSingletonVersionCheck("default", "@jupyterlab/services", [1,7,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/outputarea": () => (loadVersionCheck("default", "@jupyterlab/outputarea", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime": () => (loadSingletonVersionCheck("default", "@jupyterlab/rendermime", [1,4,0,2])),
/******/ 			"webpack/sharing/consume/default/react-portal/react-portal": () => (loadStrictVersionCheckFallback("default", "react-portal", [1,4,2,2], () => (__webpack_require__.e("vendors-node_modules_react-portal_es_index_js").then(() => (() => (__webpack_require__(/*! react-portal */ "./node_modules/react-portal/es/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/uuid/uuid": () => (loadStrictVersionCheckFallback("default", "uuid", [1,9,0,0], () => (__webpack_require__.e("vendors-node_modules_uuid_dist_esm-browser_index_js").then(() => (() => (__webpack_require__(/*! uuid */ "./node_modules/uuid/dist/esm-browser/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/monaco-editor/monaco-editor": () => (loadStrictVersionCheckFallback("default", "monaco-editor", [2,0,39,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_monaco-editor_esm_vs_editor_editor_main_js"), __webpack_require__.e("data_image_png_base64_iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5_AAAAAXNSR0IArs4c6QAAAARnQU1-5f4412")]).then(() => (() => (__webpack_require__(/*! monaco-editor */ "./node_modules/monaco-editor/esm/vs/editor/editor.main.js")))))))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react-dom",
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"lib_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/application",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/settingregistry",
/******/ 				"webpack/sharing/consume/default/@lumino/coreutils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/translation",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/outputarea",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime",
/******/ 				"webpack/sharing/consume/default/react-portal/react-portal",
/******/ 				"webpack/sharing/consume/default/uuid/uuid",
/******/ 				"webpack/sharing/consume/default/monaco-editor/monaco-editor"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		__webpack_require__.b = document.baseURI || self.location.href;
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"jupyterlab_nodeeditor": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if("webpack_sharing_consume_default_react-dom-webpack_sharing_consume_default_react" != chunkId) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkjupyterlab_nodeeditor"] = self["webpackChunkjupyterlab_nodeeditor"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/jupyterlab_nodeeditor");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB).jupyterlab_nodeeditor = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.daeae06c6d772e670e7b.js.map