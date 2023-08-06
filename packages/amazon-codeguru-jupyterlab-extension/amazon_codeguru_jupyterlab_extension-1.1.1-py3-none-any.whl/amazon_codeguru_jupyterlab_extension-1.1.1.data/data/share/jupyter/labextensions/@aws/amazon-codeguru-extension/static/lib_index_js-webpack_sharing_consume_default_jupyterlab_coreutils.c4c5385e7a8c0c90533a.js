"use strict";
(self["webpackChunk_aws_amazon_codeguru_extension"] = self["webpackChunk_aws_amazon_codeguru_extension"] || []).push([["lib_index_js-webpack_sharing_consume_default_jupyterlab_coreutils"],{

/***/ "./style/icons/cg-icon.svg":
/*!*********************************!*\
  !*** ./style/icons/cg-icon.svg ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"16\" height=\"17\" viewBox=\"0 0 16 17\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M9.96047 14.861H6.11001C5.93183 14.861 5.84259 15.0765 5.96859 15.2025L6.7018 15.9357C6.73931 15.9732 6.79018 15.9943 6.84322 15.9943H9.22726C9.2803 15.9943 9.33118 15.9732 9.36868 15.9357L10.1019 15.2025C10.2279 15.0765 10.1387 14.861 9.96047 14.861Z\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<path d=\"M5.82716 13.8223H10.2433C10.3538 13.8223 10.4433 13.7327 10.4433 13.6223V11.5728C10.4433 11.5036 10.4789 11.44 10.5361 11.401C11.2203 10.9334 12.4264 9.65462 12.4264 7.77847C12.4264 5.32318 10.4433 3.34006 8.08246 3.34006C5.7216 3.34006 3.64404 4.85101 3.64404 7.77847C3.64404 9.97931 4.81158 11.0738 5.50089 11.4067C5.57562 11.4428 5.62716 11.5163 5.62716 11.5992V13.6223C5.62716 13.7327 5.71671 13.8223 5.82716 13.8223Z\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<line x1=\"13.4653\" y1=\"7.52457\" x2=\"15.1652\" y2=\"7.52457\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<line x1=\"12.0634\" y1=\"3.68832\" x2=\"13.0077\" y2=\"2.55511\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<line y1=\"-0.35\" x2=\"1.69982\" y2=\"-0.35\" transform=\"matrix(-1 0 0 1 2.69971 7.87457)\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<line y1=\"-0.35\" x2=\"1.47511\" y2=\"-0.35\" transform=\"matrix(-0.640184 -0.768221 -0.768221 0.640184 3.83301 3.91238)\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<line x1=\"8.33828\" y1=\"0.507812\" x2=\"8.33828\" y2=\"2.20763\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<path d=\"M8.17505 5.035L7.60844 10.5122\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<path d=\"M6.47721 6.73727L5.34399 7.87049L6.47721 9.0037\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n<path d=\"M9.68783 6.73727L10.821 7.87049L9.68783 9.0037\" stroke=\"var(--jp-ui-font-color0)\" stroke-width=\"0.7\"/>\n</svg>\n");

/***/ }),

/***/ "./lib/components/About.js":
/*!*********************************!*\
  !*** ./lib/components/About.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AboutCodeGuru": () => (/* binding */ AboutCodeGuru),
/* harmony export */   "Markdown": () => (/* binding */ Markdown)
/* harmony export */ });
/* harmony import */ var _cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @cloudscape-design/components */ "webpack/sharing/consume/default/@cloudscape-design/components/@cloudscape-design/components");
/* harmony import */ var _cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @cloudscape-design/components/box */ "./node_modules/@cloudscape-design/components/box/index.js");
/* harmony import */ var _cloudscape_design_components_link__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @cloudscape-design/components/link */ "./node_modules/@cloudscape-design/components/link/index.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react_markdown_lib_react_markdown__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! react-markdown/lib/react-markdown */ "./node_modules/react-markdown/lib/react-markdown.js");
/* harmony import */ var _constants_icons__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../constants/icons */ "./lib/constants/icons.js");
/* harmony import */ var _constants_policy__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../constants/policy */ "./lib/constants/policy.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../utils */ "./lib/utils/index.js");










class AboutCodeGuru extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    render() {
        const steps = [
            {
                header: 'Step 1: Provide necessary permissions',
                description: `Go to the [AWS IAM Console](https://us-east-1.console.aws.amazon.com/iamv2/home#/home) to update the permissions policy for each role or user that will use this extension. Use an AWS managed policy or create a policy with the following permissions:

\`\`\`
${_constants_policy__WEBPACK_IMPORTED_MODULE_4__.codeGuruSecurityScanAccessPolicy}
\`\`\`
`
            },
            {
                header: 'Step 2: Configure credentials',
                headerDescription: 'This step is only required for JupyterLab users. SageMaker Studio users can skip this step.',
                description: `Refresh your AWS credentials using the AWS CLI. Run the following command to update your AWS configuration:

\`\`\`
aws configure
\`\`\`
`
            }
        ];
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { padding: "xxl", className: `about-codeguru ${(0,_utils__WEBPACK_IMPORTED_MODULE_6__.isLightThemeActive)() ? '' : 'awsui-dark-mode'}` },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__.SpaceBetween, { direction: "vertical", size: "m" },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "h1" }, "Amazon CodeGuru extension"),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__.ColumnLayout, { borders: "horizontal", columns: 1 },
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], null,
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "h2" }, "About"),
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "p" },
                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(Markdown, { content: `This extension scans code, detects security vulnerabilities, and
                  recommends code quality improvements, helping you to create and
                  deploy secure, high quality ML models. With this new feature,
                  you can quickly identify vulnerable lines of code and
                  inefficient machine learning methods within a notebook. In
                  addition, you will get recommendations that clearly show how to
                  fix the identified vulnerabilities and improve the ML methods.
                  [Learn more]("https://docs.aws.amazon.com/codeguru/latest/security-ug/")` }))),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], null,
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "h2" }, "Complete CodeGuru extension installation"),
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "p" }, "Once you install this extension, you must complete these steps to begin scanning your code."),
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__.Grid, { gridDefinition: [{ colspan: 6 }, { colspan: 6 }] }, steps.map(step => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__.Container, { header: react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components__WEBPACK_IMPORTED_MODULE_0__.Header, { variant: "h2", description: step.headerDescription }, step.header), fitHeight: true },
                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(Markdown, { content: step.description })))))),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "h2" }, "Using the extension"),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], null,
                        "After you install the extension, you can begin using the code scanning feature. You can run a scan by choosing any code cell in your file and then choosing the CodeGuru icon",
                        ' ',
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_constants_icons__WEBPACK_IMPORTED_MODULE_7__.codeGuruIcon.react, { className: "cg-icon-inline" }),
                        " in the top task bar. Once a scan is complete, you see findings underlined in your code. To view details about the findings, you can open the context (right-click) menu for any cell and choose Show diagnostics panel. You can also hold your cursor over the underlined code to see a popover with a summary. For more information on using the extension, see",
                        ' ',
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_link__WEBPACK_IMPORTED_MODULE_8__["default"], { href: "#", external: true }, "Getting started with the Amazon CodeGuru extension"),
                        "."),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_box__WEBPACK_IMPORTED_MODULE_5__["default"], null,
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(Markdown, { content: `
## Pricing

The cost of the CodeGuru extension is determined by the frequency of scans in your notebook file. By default, scans run every 120 seconds. To understand how this impacts billing, visit our [pricing policy]("https://docs.aws.amazon.com/codeguru/latest/security-ug/jupyter-sagemaker-extension"). You can change the frequency of scans in the Advanced Settings Editor.
              ` }))))));
    }
}
function Markdown({ content }) {
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(react_markdown_lib_react_markdown__WEBPACK_IMPORTED_MODULE_9__.ReactMarkdown, { components: {
            a: ({ children, href }) => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_cloudscape_design_components_link__WEBPACK_IMPORTED_MODULE_8__["default"], { external: true, href: href }, children)),
            code: ({ children }) => (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("pre", null,
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-InputArea-editor cg-code-editor" },
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("code", null, children)),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.Button, { className: "cg-button", onClick: () => copyToClipboard(children) }, "Copy"))))
        } }, content));
}
function copyToClipboard(text) {
    return navigator.clipboard.writeText(text);
}


/***/ }),

/***/ "./lib/components/CodeScanButton.js":
/*!******************************************!*\
  !*** ./lib/components/CodeScanButton.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CreateCodeScanButtonExtension": () => (/* binding */ CreateCodeScanButtonExtension)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../constants */ "./lib/constants/index.js");
/* harmony import */ var _constants_icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../constants/icons */ "./lib/constants/icons.js");





class CreateCodeScanButtonExtension {
    constructor(app) {
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this.app = app;
        this.handleClick = this.handleClick.bind(this);
    }
    emitStatusChange(response) {
        this._stateChanged.emit(response);
    }
    handleClick() {
        this.app.commands.execute(`lsp:${_constants__WEBPACK_IMPORTED_MODULE_3__.RUN_CODEGURU_SCAN_ID}-notebook`);
    }
    createNew(panel) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _constants_icons__WEBPACK_IMPORTED_MODULE_4__.codeGuruIcon,
            onClick: this.handleClick,
            tooltip: _constants__WEBPACK_IMPORTED_MODULE_3__.CODEGURU_RUN_SCAN_LABEL
        });
        panel.toolbar.insertItem(10, _constants__WEBPACK_IMPORTED_MODULE_3__.CODEGURU_RUN_SCAN_LABEL, button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
    get stateChanged() {
        return this._stateChanged;
    }
}


/***/ }),

/***/ "./lib/components/CodeScanErrorPopup.js":
/*!**********************************************!*\
  !*** ./lib/components/CodeScanErrorPopup.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeScanErrorWidget": () => (/* binding */ CodeScanErrorWidget),
/* harmony export */   "ErrorType": () => (/* binding */ ErrorType)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants_policy__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../constants/policy */ "./lib/constants/policy.js");
/* harmony import */ var _About__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./About */ "./lib/components/About.js");




var ErrorType;
(function (ErrorType) {
    ErrorType["INSUFFICIENT_ACCESS_PERMISSIONS"] = "INSUFFICIENT_ACCESS_PERMISSIONS";
    ErrorType["MISSING_AWS_CREDENTIALS"] = "MISSING_AWS_CREDENTIALS";
})(ErrorType || (ErrorType = {}));
const CodeScanErrorComponent = ({ errorType }) => {
    const missingPermissionsContent = `
 ### Missing permissions for CodeGuru extension


 You do not have the necessary permissions to run a CodeGuru scan. [Learn more](#)

Go to the [AWS IAM Console](https://us-east-1.console.aws.amazon.com/iamv2/home#/home) to update the permissions policy for each user that will use this extension.

Use an AWS managed policy or create a policy with the following permissions:

 \`\`\`
${_constants_policy__WEBPACK_IMPORTED_MODULE_2__.codeGuruSecurityScanAccessPolicy}
 \`\`\`
   `;
    const missingCredentialsContent = `
 ### Missing AWS credentials for CodeGuru extension


 To use Amazon CodeGuru scan, provide AWS credentials by pasting

 the following script in your command prompt window.

 \`\`\`
 aws configure
 \`\`\`
   `;
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "cg-popover" },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "cg-popover-content cg-text" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_About__WEBPACK_IMPORTED_MODULE_3__.Markdown, { content: errorType === ErrorType.INSUFFICIENT_ACCESS_PERMISSIONS
                    ? missingPermissionsContent
                    : missingCredentialsContent }))));
};
class CodeScanErrorWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(props) {
        super();
        this.addClass('jp-ReactWidget');
        this.errorType = props.errorType;
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(CodeScanErrorComponent, { errorType: this.errorType });
    }
}


/***/ }),

/***/ "./lib/components/CodeScanStatus.js":
/*!******************************************!*\
  !*** ./lib/components/CodeScanStatus.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeScanStatus": () => (/* binding */ CodeScanStatus),
/* harmony export */   "parseError": () => (/* binding */ parseError)
/* harmony export */ });
/* harmony import */ var _cloudscape_design_components_status_indicator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @cloudscape-design/components/status-indicator */ "./node_modules/@cloudscape-design/components/status-indicator/index.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _CodeScanErrorPopup__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./CodeScanErrorPopup */ "./lib/components/CodeScanErrorPopup.js");





const statusCleanupTimeout = {
    completed: 5000,
    error: 30000,
    idle: 0
};
function CodeScanStatusComponent(props) {
    const [status, setStatus] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(props.status);
    const [message, setMessage] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)();
    props.listener.connect((_, { status, message }) => {
        if (status !== 'pending') {
            setTimeout(() => {
                setStatus('idle'); // It will remove the status from footer
            }, statusCleanupTimeout[status]);
        }
        setStatus(status);
        setMessage(message);
    });
    switch (status) {
        case 'pending': {
            const title = 'CodeGuru: Scan in progress';
            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_cloudscape_design_components_status_indicator__WEBPACK_IMPORTED_MODULE_3__["default"], { type: "in-progress", colorOverride: "blue" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: title })));
        }
        case 'error': {
            const errorType = parseError(String(message));
            const title = errorType === _CodeScanErrorPopup__WEBPACK_IMPORTED_MODULE_4__.ErrorType.INSUFFICIENT_ACCESS_PERMISSIONS
                ? 'CodeGuru: Missing permissions'
                : errorType === _CodeScanErrorPopup__WEBPACK_IMPORTED_MODULE_4__.ErrorType.MISSING_AWS_CREDENTIALS
                    ? 'CodeGuru: Missing credentials'
                    : 'CodeGuru: Scan failed';
            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { onClick: () => props.handleClick(errorType) },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_cloudscape_design_components_status_indicator__WEBPACK_IMPORTED_MODULE_3__["default"], { type: "warning" },
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: title }))));
        }
        case 'completed': {
            const title = 'CodeGuru: Scan completed';
            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_cloudscape_design_components_status_indicator__WEBPACK_IMPORTED_MODULE_3__["default"], { type: "success", colorOverride: "blue" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: title })));
        }
        case 'idle':
        default:
            return react__WEBPACK_IMPORTED_MODULE_2___default().createElement((react__WEBPACK_IMPORTED_MODULE_2___default().Fragment), null);
    }
}
class CodeScanStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(props) {
        super();
        this._popup = null;
        this.status = props.status;
        this.listener = props.listener;
        this.handleClick = this.handleClick.bind(this);
    }
    handleClick(errorType) {
        var _a;
        if (!errorType) {
            return;
        }
        if ((_a = this._popup) === null || _a === void 0 ? void 0 : _a.isVisible) {
            this._popup.close();
        }
        else {
            if (this._popup) {
                this._popup.dispose();
            }
            this._popup = (0,_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.showPopup)({
                body: new _CodeScanErrorPopup__WEBPACK_IMPORTED_MODULE_4__.CodeScanErrorWidget({ errorType }),
                anchor: this,
                align: 'left'
            });
        }
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(CodeScanStatusComponent, { status: this.status, listener: this.listener, handleClick: this.handleClick }));
    }
}
function parseError(message) {
    if (!message) {
        return;
    }
    if (message.includes('AccessDeniedException') &&
        message.includes('not authorized to perform: codeguru-security')) {
        return _CodeScanErrorPopup__WEBPACK_IMPORTED_MODULE_4__.ErrorType.INSUFFICIENT_ACCESS_PERMISSIONS;
    }
    if ((message.includes('UnrecognizedClientException') ||
        message.includes('ExpiredTokenException')) &&
        message.includes('The security token included in the request is ')) {
        return _CodeScanErrorPopup__WEBPACK_IMPORTED_MODULE_4__.ErrorType.MISSING_AWS_CREDENTIALS;
    }
    return;
}


/***/ }),

/***/ "./lib/constants/icons.js":
/*!********************************!*\
  !*** ./lib/constants/icons.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "codeGuruIcon": () => (/* binding */ codeGuruIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_cg_icon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/icons/cg-icon.svg */ "./style/icons/cg-icon.svg");


const codeGuruIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'codeGuruIcon',
    svgstr: _style_icons_cg_icon_svg__WEBPACK_IMPORTED_MODULE_1__["default"]
});



/***/ }),

/***/ "./lib/constants/index.js":
/*!********************************!*\
  !*** ./lib/constants/index.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CODEGURU_RUN_SCAN_LABEL": () => (/* binding */ CODEGURU_RUN_SCAN_LABEL),
/* harmony export */   "PLATFORM_ACRONYM": () => (/* binding */ PLATFORM_ACRONYM),
/* harmony export */   "PLUGIN_ID": () => (/* binding */ PLUGIN_ID),
/* harmony export */   "REGISTER_ID": () => (/* binding */ REGISTER_ID),
/* harmony export */   "RUN_CODEGURU_SCAN_ID": () => (/* binding */ RUN_CODEGURU_SCAN_ID)
/* harmony export */ });
const PLUGIN_ID = '@aws/amazon-codeguru-extension';
var REGISTER_ID;
(function (REGISTER_ID) {
    REGISTER_ID["CREATE_CODE_SCAN"] = "@aws/amazon-codeguru-extension:create_scan_command";
    REGISTER_ID["SCAN_STATUS"] = "@aws/amazon-codeguru-extension:scan_status";
})(REGISTER_ID || (REGISTER_ID = {}));
const RUN_CODEGURU_SCAN_ID = 'run-codeguru-scan';
const CODEGURU_RUN_SCAN_LABEL = 'Run CodeGuru scan';
var PLATFORM_ACRONYM;
(function (PLATFORM_ACRONYM) {
    PLATFORM_ACRONYM["SAGEMAKER"] = "sm";
    PLATFORM_ACRONYM["LOCALHOST"] = "jl";
})(PLATFORM_ACRONYM || (PLATFORM_ACRONYM = {}));


/***/ }),

/***/ "./lib/constants/policy.js":
/*!*********************************!*\
  !*** ./lib/constants/policy.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "codeGuruSecurityScanAccessPolicy": () => (/* binding */ codeGuruSecurityScanAccessPolicy)
/* harmony export */ });
const codeGuruSecurityScanAccessPolicy = `
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AmazonCodeGuruSecurityScanAccess",
      "Effect": "Allow",
      "Action": [
        "codeguru-security:CreateScan",
        "codeguru-security:CreateUploadUrl",
        "codeguru-security:GetScan",
        "codeguru-security:GetFindings"
      ],
      "Resource": "arn:aws:codeguru-security:*:*:scans/*"
    }
  ]
}
`;


/***/ }),

/***/ "./lib/constants/region.js":
/*!*********************************!*\
  !*** ./lib/constants/region.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DEFAULT_AWS_REGION": () => (/* binding */ DEFAULT_AWS_REGION),
/* harmony export */   "Region": () => (/* binding */ Region)
/* harmony export */ });
var Region;
(function (Region) {
    // Wave 1
    Region["ARN"] = "eu-north-1";
    // Wave 2
    Region["SYD"] = "ap-southeast-2";
    // Wave 3
    Region["IAD"] = "us-east-1";
    Region["CMH"] = "us-east-2";
    Region["PDX"] = "us-west-2";
    // Wave 4
    Region["NRT"] = "ap-northeast-1";
    Region["SIN"] = "ap-southeast-1";
    Region["FRA"] = "eu-central-1";
    Region["DUB"] = "eu-west-1";
    Region["LHR"] = "eu-west-2";
})(Region || (Region = {}));
const DEFAULT_AWS_REGION = Region.IAD;


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-lsp/jupyterlab-lsp */ "webpack/sharing/consume/default/@jupyter-lsp/jupyterlab-lsp");
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp_lib_editor_integration_codemirror__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-lsp/jupyterlab-lsp/lib/editor_integration/codemirror */ "./node_modules/@jupyter-lsp/jupyterlab-lsp/lib/editor_integration/codemirror.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _components_About__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./components/About */ "./lib/components/About.js");
/* harmony import */ var _components_CodeScanButton__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./components/CodeScanButton */ "./lib/components/CodeScanButton.js");
/* harmony import */ var _components_CodeScanStatus__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./components/CodeScanStatus */ "./lib/components/CodeScanStatus.js");
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./constants */ "./lib/constants/index.js");
/* harmony import */ var _constants_icons__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./constants/icons */ "./lib/constants/icons.js");
/* harmony import */ var _constants_region__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./constants/region */ "./lib/constants/region.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./utils */ "./lib/utils/index.js");













class CodeGuruCM extends _jupyter_lsp_jupyterlab_lsp_lib_editor_integration_codemirror__WEBPACK_IMPORTED_MODULE_1__.CodeMirrorIntegration {
}
let overriddenRegion = _constants_region__WEBPACK_IMPORTED_MODULE_6__.DEFAULT_AWS_REGION;
const COMMANDS = (button) => [
    {
        id: _constants__WEBPACK_IMPORTED_MODULE_7__.RUN_CODEGURU_SCAN_ID,
        label: _constants__WEBPACK_IMPORTED_MODULE_7__.CODEGURU_RUN_SCAN_LABEL,
        icon: _constants_icons__WEBPACK_IMPORTED_MODULE_8__.codeGuruIcon,
        execute: ({ connection, document }) => {
            const platform = (0,_utils__WEBPACK_IMPORTED_MODULE_9__.getPlatformAcronym)();
            let token;
            if (connection === null || connection === void 0 ? void 0 : connection.isConnected) {
                // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                // @ts-ignore
                const wsConnection = connection.connection;
                void wsConnection.sendRequest('workspace/executeCommand', {
                    command: 'cgs.runScan',
                    arguments: [document.document_info.uri, overriddenRegion, platform]
                });
                wsConnection.onNotification('$/progress', (response) => {
                    if (response.value.title === 'command: runScan') {
                        token = response.token;
                    }
                    if (token === response.token &&
                        response.value.kind === 'report' &&
                        response.value.message) {
                        button.emitStatusChange(response.value.message);
                    }
                });
            }
        },
        is_enabled: () => true,
        rank: 4
    }
];
/**
 * Initialization data for the @aws/amazon-codeguru-extension extension.
 */
const plugin = {
    id: `${_constants__WEBPACK_IMPORTED_MODULE_7__.PLUGIN_ID}:plugin`,
    autoStart: true,
    requires: [_jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.ILSPFeatureManager, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__.IStateDB],
    activate: (app, featureManager, statusBar, settings, state) => {
        const button = new _components_CodeScanButton__WEBPACK_IMPORTED_MODULE_10__.CreateCodeScanButtonExtension(app);
        const statusWidget = new _components_CodeScanStatus__WEBPACK_IMPORTED_MODULE_11__.CodeScanStatus({
            status: 'idle',
            listener: button.stateChanged
        });
        app.docRegistry.addWidgetExtension('Notebook', button);
        featureManager.register({
            feature: {
                editorIntegrationFactory: new Map([['CodeMirrorEditor', CodeGuruCM]]),
                id: _constants__WEBPACK_IMPORTED_MODULE_7__.REGISTER_ID.CREATE_CODE_SCAN,
                name: 'CodeGuru Security',
                commands: COMMANDS(button)
            }
        });
        // Codescan status in footer
        statusBar.registerStatusItem(_constants__WEBPACK_IMPORTED_MODULE_7__.REGISTER_ID.SCAN_STATUS, {
            align: 'middle',
            item: statusWidget,
            rank: 20
        });
        // Settings
        let scanFrequency = 240;
        let autoScan = 'Disabled';
        let timeOutToken;
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        function loadSetting(setting) {
            // Read the settings and convert to the correct type
            scanFrequency = setting.get('scanFrequency').composite;
            autoScan = setting.get('autoScan').composite;
            overriddenRegion = setting.get('region').composite;
            // clearing interval before setting new interval or disabling autoscan
            if (timeOutToken) {
                clearInterval(timeOutToken);
            }
            if (autoScan === 'Enabled' && scanFrequency > 0) {
                timeOutToken = setInterval(() => {
                    app.commands.execute(`lsp:${_constants__WEBPACK_IMPORTED_MODULE_7__.RUN_CODEGURU_SCAN_ID}-notebook`);
                }, scanFrequency * 1000);
            }
        }
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        Promise.all([app.restored, settings.load(`${_constants__WEBPACK_IMPORTED_MODULE_7__.PLUGIN_ID}:plugin`)])
            .then(([, setting]) => {
            // Read the settings
            loadSetting(setting);
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
        })
            .catch(reason => {
            console.error(`Error while reading the settings.\n${reason}`);
        });
        // About page
        const aboutCodeGuruWidget = () => {
            // Create a blank content widget inside of a MainAreaWidget
            const about = new _components_About__WEBPACK_IMPORTED_MODULE_12__.AboutCodeGuru();
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.MainAreaWidget({ content: about });
            widget.id = 'about-codeguru';
            widget.title.label = 'Get started with CodeGuru';
            widget.title.icon = _constants_icons__WEBPACK_IMPORTED_MODULE_8__.codeGuruIcon;
            widget.title.closable = true;
            return widget;
        };
        let widget = aboutCodeGuruWidget();
        app.commands.addCommand(`${_constants__WEBPACK_IMPORTED_MODULE_7__.PLUGIN_ID}:about-codeguru`, {
            label: 'About CodeGuru',
            execute: () => {
                // Regenerate the widget if disposed
                if (widget.isDisposed) {
                    widget = aboutCodeGuruWidget();
                }
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
            }
        });
        // // Uncomment while testing about page
        // app.contextMenu.addItem({
        //   command: `${PLUGIN_ID}:about-codeguru`,
        //   selector: '.jp-Cell'
        // });
        app.restored
            .then(() => state.fetch(`${_constants__WEBPACK_IMPORTED_MODULE_7__.PLUGIN_ID}:plugin`))
            .then(value => {
            let isFirstTime = true;
            try {
                isFirstTime = value['isFirstTime'];
                // eslint-disable-next-line no-empty
            }
            catch (_a) { }
            if (isFirstTime) {
                app.commands.execute(`${_constants__WEBPACK_IMPORTED_MODULE_7__.PLUGIN_ID}:about-codeguru`);
            }
            return state.save(`${_constants__WEBPACK_IMPORTED_MODULE_7__.PLUGIN_ID}:plugin`, {
                isFirstTime: false
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/utils/index.js":
/*!****************************!*\
  !*** ./lib/utils/index.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getPlatformAcronym": () => (/* binding */ getPlatformAcronym),
/* harmony export */   "isLightThemeActive": () => (/* binding */ isLightThemeActive)
/* harmony export */ });
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../constants */ "./lib/constants/index.js");

function isLightThemeActive() {
    return document.body.getAttribute('data-jp-theme-light') === 'true';
}
function getPlatformAcronym() {
    const hostname = window.location.hostname;
    if (hostname.includes('sagemaker')) {
        return _constants__WEBPACK_IMPORTED_MODULE_0__.PLATFORM_ACRONYM.SAGEMAKER;
    }
    return _constants__WEBPACK_IMPORTED_MODULE_0__.PLATFORM_ACRONYM.LOCALHOST;
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_jupyterlab_coreutils.c4c5385e7a8c0c90533a.js.map