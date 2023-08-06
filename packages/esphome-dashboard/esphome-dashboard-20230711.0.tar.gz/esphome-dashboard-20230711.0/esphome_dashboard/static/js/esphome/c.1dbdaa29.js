import{e as t,c as e,T as o,L as i,r as s,b as r,d as a,n,s as l,x as c,g as p,N as d,O as h,P as m,Q as u,I as _,J as w,m as v,S as g,E as y,U as f}from"./index-2bed5a1a.js";import{g as b}from"./c.8b9b80e2.js";import"./c.8b0a585f.js";import{o as $,c as P}from"./c.f521c339.js";import{m as S,s as k,b as x}from"./c.40f2b612.js";import{o as C}from"./c.75f3beac.js";class E{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class H{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}const W=t=>!i(t)&&"function"==typeof t.then,j=1073741823;const I=t(class extends e{constructor(){super(...arguments),this._$C_t=j,this._$Cwt=[],this._$Cq=new E(this),this._$CK=new H}render(...t){var e;return null!==(e=t.find((t=>!W(t))))&&void 0!==e?e:o}update(t,e){const i=this._$Cwt;let s=i.length;this._$Cwt=e;const r=this._$Cq,a=this._$CK;this.isConnected||this.disconnected();for(let t=0;t<e.length&&!(t>this._$C_t);t++){const o=e[t];if(!W(o))return this._$C_t=t,o;t<s&&o===i[t]||(this._$C_t=j,s=0,Promise.resolve(o).then((async t=>{for(;a.get();)await a.get();const e=r.deref();if(void 0!==e){const i=e._$Cwt.indexOf(o);i>-1&&i<e._$C_t&&(e._$C_t=i,e.setValue(t))}})))}return o}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}),A=(t,e)=>{import("./c.963d45e5.js");const o=document.createElement("esphome-compile-dialog");o.configuration=t,o.downloadFactoryFirmware=e,document.body.append(o)},T=async(t,e)=>{import("./c.09528d03.js");let o=t.port;if(o)await o.close();else try{o=await navigator.serial.requestPort()}catch(o){return void("NotFoundError"===o.name?$((()=>T(t,e))):alert(`Unable to connect: ${o.message}`))}const i=P(o);e&&e();const s=document.createElement("esphome-install-web-dialog");s.params=t,s.esploader=i,document.body.append(s)},B={info:d,warning:h,error:m,success:u};let D=class extends l{constructor(){super(...arguments),this.title="",this.alertType="info",this.rtl=!1}render(){return c`
      <div
        class="issue-type ${p({rtl:this.rtl,[this.alertType]:!0})}"
        role="alert"
      >
        <div class="icon ${this.title?"":"no-title"}">
          <slot name="icon">
            <esphome-svg-icon
              .path=${B[this.alertType]}
            ></esphome-svg-icon>
          </slot>
        </div>
        <div class="content">
          <div class="main-content">
            ${this.title?c`<div class="title">${this.title}</div>`:""}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action"> </slot>
          </div>
        </div>
      </div>
    `}};D.styles=s`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
      padding-left: var(--esphome-alert-padding-left, 8px);
    }
    .issue-type.rtl {
      flex-direction: row-reverse;
    }
    .issue-type::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      z-index: 1;
    }
    .icon.no-title {
      align-self: center;
    }
    .issue-type.rtl > .content {
      flex-direction: row-reverse;
      text-align: right;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }
    .action {
      z-index: 1;
      width: min-content;
      --mdc-theme-primary: var(--primary-text-color);
    }
    .main-content {
      overflow-wrap: anywhere;
      word-break: break-word;
      margin-left: 8px;
      margin-right: 0;
    }
    .issue-type.rtl > .content > .main-content {
      margin-left: 0;
      margin-right: 8px;
    }
    .title {
      margin-top: 2px;
      font-weight: bold;
    }
    .action mwc-button,
    .action ha-icon-button {
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--alert-info-color);
    }
    .issue-type.info::after {
      background-color: var(--alert-info-color);
    }

    .issue-type.warning > .icon {
      color: var(--alert-warning-color);
    }
    .issue-type.warning::after {
      background-color: var(--alert-warning-color);
    }

    .issue-type.error > .icon {
      color: var(--alert-error-color);
    }
    .issue-type.error::after {
      background-color: var(--alert-error-color);
    }

    .issue-type.success > .icon {
      color: var(--alert-success-color);
    }
    .issue-type.success::after {
      background-color: var(--alert-success-color);
    }
  `,r([a()],D.prototype,"title",void 0),r([a({attribute:"alert-type"})],D.prototype,"alertType",void 0),r([a({type:Boolean})],D.prototype,"rtl",void 0),D=r([n("esphome-alert")],D);let M=class extends l{constructor(){super(...arguments),this._ethernet=!1,this._isPico=!1,this._state="pick_option"}get _platformSupportsWebSerial(){return!this._isPico}render(){let t,e;if("pick_option"===this._state)t=`How do you want to install ${this.configuration} on your device?`,e=c`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>${this._ethernet?"Via the network":"Wirelessly"}</span>
          <span slot="secondary">Requires the device to be online</span>
          ${S}
        </mwc-list-item>

        ${this._error?c`<div class="error">${this._error}</div>`:""}

        <mwc-list-item
          twoline
          hasMeta
          ?disabled=${!this._platformSupportsWebSerial}
          @click=${this._handleBrowserInstall}
        >
          <span>Plug into this computer</span>
          <span slot="secondary">
            ${this._platformSupportsWebSerial?"For devices connected via USB to this computer":"Installing this via the web is not supported yet for this device"}
          </span>
          ${S}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._handleServerInstall}>
          <span>Plug into the computer running ESPHome Dashboard</span>
          <span slot="secondary">
            ${"For devices connected via USB to the server"+(this._isPico?" and running ESPHome":"")}
          </span>
          ${S}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          @click=${()=>{this._state=this._isPico?"download_instructions":"pick_download_type"}}
        >
          <span>Manual download</span>
          <span slot="secondary">
            Install it yourself
            ${this._isPico?"by copying it to the Pico USB drive":"using ESPHome Web or other tools"}
          </span>
          ${S}
        </mwc-list-item>

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `;else if("pick_server_port"===this._state)t="Pick Server Port",e=void 0===this._ports?this._renderProgress("Loading serial devices"):c`
              ${this._isPico?c`
                    <esphome-alert type="warning">
                      Installation via the server requires the Pico to already
                      run ESPHome.
                    </esphome-alert>
                  `:""}
              ${0===this._ports.length?this._renderMessage("👀",c`
                      No serial devices found.
                      <br /><br />
                      This list automatically refreshes if you plug one in.
                    `,!1):c`
                    ${this._ports.map((t=>c`
                        <mwc-list-item
                          twoline
                          hasMeta
                          .port=${t.port}
                          @click=${this._handleLegacyOption}
                        >
                          <span>${t.desc}</span>
                          <span slot="secondary">${t.port}</span>
                          ${S}
                        </mwc-list-item>
                      `))}
                  `}
              <mwc-button
                no-attention
                slot="primaryAction"
                label="Back"
                @click=${()=>{this._state="pick_option"}}
              ></mwc-button>
            `;else if("pick_download_type"===this._state)t="What version do you want to download?",e=c`
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleWebDownload}
        >
          <span>Modern format</span>
          <span slot="secondary">
            For use with ESPHome Web and other tools.
          </span>
          ${S}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleManualDownload}
        >
          <span>Legacy format</span>
          <span slot="secondary">For use with ESPHome Flasher.</span>
          ${S}
        </mwc-list-item>

        ${this._platformSupportsWebSerial?c`
              <a
                href="https://web.esphome.io"
                target="_blank"
                rel="noopener noreferrer"
                class="bottom-left"
                >Open ESPHome Web</a
              >
            `:""}
        <mwc-button
          no-attention
          slot="primaryAction"
          label="Back"
          @click=${()=>{this._state="pick_option"}}
        ></mwc-button>
      `;else if("download_instructions"===this._state){let o;const i=I(this._compileConfiguration,c`<a download disabled href="#">Download project</a>
          preparing&nbsp;download…
          <mwc-circular-progress
            density="-8"
            indeterminate
          ></mwc-circular-progress>`);this._isPico?(t="Install ESPHome via the USB drive",o=c`
          <div>
            You can install your ESPHome project ${this.configuration} on your
            device via your file explorer by following these steps:
          </div>
          <ol>
            <li>Disconnect your Raspberry Pi Pico from your computer</li>
            <li>
              Hold the BOOTSEL button and connect the Pico to your computer. The
              Pico will show up as a USB drive named RPI-RP2
            </li>
            <li>${i}</li>
            <li>
              Drag the downloaded file to the USB drive. The installation is
              complete when the drive disappears
            </li>
            <li>Your Pico now runs your ESPHome project 🎉</li>
          </ol>
        `):(t="Install ESPHome via the browser",o=c`
          <div>
            ESPHome can install ${this.configuration} on your device via the
            browser if certain requirements are met:
          </div>
          <ul>
            <li>ESPHome is visited over HTTPS</li>
            <li>Your browser supports WebSerial</li>
          </ul>
          <div>
            Not all requirements are currently met. The easiest solution is to
            download your project and do the installation with ESPHome Web.
            ESPHome Web works 100% in your browser and no data will be shared
            with the ESPHome project.
          </div>
          <ol>
            <li>${i}</li>
            <li>
              <a href=${"https://web.esphome.io/?dashboard_install"} target="_blank" rel="noopener"
                >Open ESPHome Web</a
              >
            </li>
          </ol>
        `),e=c`
        ${o}

        <mwc-button
          no-attention
          slot="secondaryAction"
          label="Back"
          @click=${()=>{this._state="pick_option"}}
        ></mwc-button>
        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      `}return c`
      <mwc-dialog
        open
        heading=${t}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${!1}
      >
        ${e}
      </mwc-dialog>
    `}_renderProgress(t,e){return c`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===e}
            .progress=${void 0!==e?e/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==e?c`<div class="progress-pct">${e}%</div>`:""}
        </div>
        ${t}
      </div>
    `}_renderMessage(t,e,o){return c`
      <div class="center">
        <div class="icon">${t}</div>
        ${e}
      </div>
      ${o?c`
            <mwc-button
              slot="primaryAction"
              dialogAction="ok"
              label="Close"
            ></mwc-button>
          `:""}
    `}firstUpdated(t){super.firstUpdated(t),this._updateSerialPorts(),g(this.configuration).then((t=>{this._ethernet=t.loaded_integrations.includes("ethernet"),this._isPico="RP2040"===t.esp_platform}))}async _updateSerialPorts(){this._ports=await b()}willUpdate(t){super.willUpdate(t),t.has("_state")&&"download_instructions"===this._state&&!this._compileConfiguration&&(this._abortCompilation=new AbortController,this._compileConfiguration=y(this.configuration).then((()=>c`
            <a
              download
              href="${f(this.configuration,!this._isPico)}"
              >Download project</a
            >
          `),(()=>c`
            <a download disabled href="#">Download project</a>
            <span class="prepare-error">preparation failed:</span>
            <button
              class="link"
              dialogAction="close"
              @click=${()=>{A(this.configuration,!this._isPico)}}
            >
              see what went wrong
            </button>
          `)).finally((()=>{this._abortCompilation=void 0})))}updated(t){if(super.updated(t),t.has("_state"))if("pick_server_port"===this._state){const t=async()=>{await this._updateSerialPorts(),this._updateSerialInterval=window.setTimeout((async()=>{await t()}),5e3)};t()}else"pick_server_port"===t.get("_state")&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0)}_storeDialogWidth(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`)}_handleServerInstall(){this._storeDialogWidth(),this._state="pick_server_port"}_handleManualDownload(){A(this.configuration,!1)}_handleWebDownload(){A(this.configuration,!0)}_handleLegacyOption(t){C(this.configuration,t.currentTarget.port),this._close()}_handleBrowserInstall(){if(!k||!x)return this._storeDialogWidth(),void(this._state="download_instructions");T({configuration:this.configuration},(()=>this._close()))}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){var t;null===(t=this._abortCompilation)||void 0===t||t.abort(),this._updateSerialInterval&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0),this.parentNode.removeChild(this)}};M.styles=[_,w,s`
      mwc-list-item {
        margin: 0 -20px;
      }
      .center {
        text-align: center;
      }
      mwc-circular-progress {
        margin-bottom: 16px;
      }
      li mwc-circular-progress {
        margin: 0;
      }
      .progress-pct {
        position: absolute;
        top: 50px;
        left: 0;
        right: 0;
      }
      .icon {
        font-size: 50px;
        line-height: 80px;
        color: black;
      }
      .show-ports {
        margin-top: 16px;
      }
      .error {
        padding: 8px 24px;
        background-color: #fff59d;
        margin: 0 -24px;
      }
      .prepare-error {
        color: var(--alert-error-color);
      }
      ul,
      ol {
        padding-left: 24px;
      }
      li {
        line-height: 2em;
      }
      li a {
        display: inline-block;
        margin-right: 8px;
      }
      a[disabled] {
        pointer-events: none;
        color: #999;
      }
      ol {
        margin-bottom: 0;
      }
      a.bottom-left {
        z-index: 1;
        position: absolute;
        line-height: 36px;
        bottom: 9px;
      }
      esphome-alert {
        color: black;
        margin: 0 -24px;
        display: block;
        --esphome-alert-padding-left: 20px;
      }
    `],r([a()],M.prototype,"configuration",void 0),r([v()],M.prototype,"_ethernet",void 0),r([v()],M.prototype,"_isPico",void 0),r([v()],M.prototype,"_ports",void 0),r([v()],M.prototype,"_state",void 0),r([v()],M.prototype,"_error",void 0),M=r([n("esphome-install-choose-dialog")],M);var q=Object.freeze({__proto__:null});export{T as a,q as i,A as o};
//# sourceMappingURL=c.1dbdaa29.js.map
