(self["webpackChunk_g2nb_nbtools"] = self["webpackChunk_g2nb_nbtools"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _basewidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./basewidget */ "./lib/basewidget.js");
/* harmony import */ var _uioutput__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./uioutput */ "./lib/uioutput.js");
/* harmony import */ var _uibuilder__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./uibuilder */ "./lib/uibuilder.js");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _toolbox__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./toolbox */ "./lib/toolbox.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./registry */ "./lib/registry.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _context__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./context */ "./lib/context.js");
/* harmony import */ var _dataregistry__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./dataregistry */ "./lib/dataregistry.js");














const module_exports = Object.assign(Object.assign(Object.assign({}, _basewidget__WEBPACK_IMPORTED_MODULE_3__), _uioutput__WEBPACK_IMPORTED_MODULE_4__), _uibuilder__WEBPACK_IMPORTED_MODULE_5__);
const EXTENSION_ID = '@g2nb/nbtools:plugin';
const NAMESPACE = 'nbtools';
/**
 * The nbtools plugin.
 */
const nbtools_plugin = {
    id: EXTENSION_ID,
    provides: [_registry__WEBPACK_IMPORTED_MODULE_8__.IToolRegistry, _dataregistry__WEBPACK_IMPORTED_MODULE_13__.IDataRegistry],
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_10__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_10__.ILabShell, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_11__.INotebookTracker],
    activate: activate_widget_extension,
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (nbtools_plugin);
/**
 * Activate the widget extension.
 */
async function activate_widget_extension(app, widget_registry, settings, mainmenu, restorer, shell, notebook_tracker) {
    // Initialize the ContextManager
    init_context(app, notebook_tracker);
    // Initialize settings
    const setting_dict = await init_settings(settings);
    // Create the tool and data registries
    const tool_registry = new _registry__WEBPACK_IMPORTED_MODULE_8__.ToolRegistry(setting_dict);
    const data_registry = new _dataregistry__WEBPACK_IMPORTED_MODULE_13__.DataRegistry();
    // Add items to the help menu
    add_help_links(app, mainmenu);
    // Add keyboard shortcuts
    add_keyboard_shortcuts(app, tool_registry);
    // Add the toolbox
    add_tool_browser(app, restorer);
    // Register the nbtools widgets with the widget registry
    widget_registry.registerWidget({
        name: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME,
        version: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION,
        exports: module_exports,
    });
    // Register the plugin as loaded
    (0,_utils__WEBPACK_IMPORTED_MODULE_9__.usage_tracker)('labextension_load', location.protocol + '//' + location.host + location.pathname);
    // Return the tool registry so that it is provided to other extensions
    return [tool_registry, data_registry];
}
async function init_settings(settings) {
    let setting = null;
    try {
        setting = await settings.load(EXTENSION_ID);
    }
    catch (_a) {
        console.log('Unable to load nbtools settings');
    }
    return { force_render: setting ? setting.get('force_render').composite : true };
}
function init_context(app, notebook_tracker) {
    _context__WEBPACK_IMPORTED_MODULE_12__.ContextManager.jupyter_app = app;
    _context__WEBPACK_IMPORTED_MODULE_12__.ContextManager.notebook_tracker = notebook_tracker;
    _context__WEBPACK_IMPORTED_MODULE_12__.ContextManager.context();
    window.ContextManager = _context__WEBPACK_IMPORTED_MODULE_12__.ContextManager; // Left in for development purposes
}
function add_keyboard_shortcuts(app, tool_registry) {
    app.commands.addCommand("nbtools:insert-tool", {
        label: 'Insert Notebook Tool',
        execute: () => {
            // Open the tool manager, if necessary
            app.shell.activateById('nbtools-browser');
            (0,_utils__WEBPACK_IMPORTED_MODULE_9__.pulse_red)(document.getElementById('nbtools-browser'));
            // If only one tool is available, add it
            const tools = tool_registry.list();
            if (tools.length === 1)
                _toolbox__WEBPACK_IMPORTED_MODULE_7__.Toolbox.add_tool_cell(tools[0]);
            // Otherwise give the search box focus
            else
                document.querySelector('.nbtools-search').focus();
        },
    });
}
function add_tool_browser(app, restorer) {
    const tool_browser = new _toolbox__WEBPACK_IMPORTED_MODULE_7__.ToolBrowser();
    tool_browser.title.iconClass = 'nbtools-icon fa fa-th jp-SideBar-tabIcon';
    tool_browser.title.caption = 'Toolbox';
    tool_browser.id = 'nbtools-browser';
    // Add the tool browser widget to the application restorer
    if (restorer)
        restorer.add(tool_browser, NAMESPACE);
    app.shell.add(tool_browser, 'left', { rank: 102 });
}
/**
 * Add the nbtools documentation and feedback links to the help menu
 *
 * @param {Application<Widget>} app
 * @param {IMainMenu} mainmenu
 */
function add_help_links(app, mainmenu) {
    const feedback = 'nbtools:feedback';
    const documentation = 'nbtools:documentation';
    // Add feedback command to the command palette
    app.commands.addCommand(feedback, {
        label: 'g2nb Help Forum',
        caption: 'Open the g2nb help forum',
        isEnabled: () => !!app.shell,
        execute: () => {
            const url = 'https://community.mesirovlab.org/c/g2nb/';
            let element = document.createElement('a');
            element.href = url;
            element.target = '_blank';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
    });
    // Add documentation command to the command palette
    app.commands.addCommand(documentation, {
        label: 'nbtools Documentation',
        caption: 'Open documentation for nbtools',
        isEnabled: () => !!app.shell,
        execute: () => {
            const url = 'https://github.com/g2nb/nbtools#nbtools';
            let element = document.createElement('a');
            element.href = url;
            element.target = '_blank';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
    });
    // Add documentation link to the help menu
    if (mainmenu)
        mainmenu.helpMenu.addGroup([{ command: feedback }, { command: documentation }], 2);
}


/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.6292de8fa547e3973251.js.map