import{I as o,r as t,b as e,d as i,m as r,n as s,s as a,x as n,U as c}from"./index-2bed5a1a.js";import"./c.a3b20324.js";import{o as d}from"./c.1dbdaa29.js";import"./c.8b0a585f.js";import"./c.8b9b80e2.js";import"./c.f521c339.js";import"./c.40f2b612.js";import"./c.75f3beac.js";let l=class extends a{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return n`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?n`
              <a
                slot="secondaryAction"
                href="${c(this.configuration,this.downloadFactoryFirmware)}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:n`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const t=document.createElement("a");t.download=this.configuration+".bin",t.href=c(this.configuration,this.downloadFactoryFirmware),document.body.appendChild(t),t.click(),t.remove()}_handleRetry(){d(this.configuration,this.downloadFactoryFirmware)}_handleClose(){this.parentNode.removeChild(this)}};l.styles=[o,t`
      a {
        text-decoration: none;
      }
    `],e([i()],l.prototype,"configuration",void 0),e([i()],l.prototype,"downloadFactoryFirmware",void 0),e([r()],l.prototype,"_result",void 0),l=e([s("esphome-compile-dialog")],l);
//# sourceMappingURL=c.963d45e5.js.map
