import{b as o,d as e,n as s,s as i,x as t}from"./index-2bed5a1a.js";import"./c.a3b20324.js";import"./c.8b0a585f.js";let a=class extends i{render(){return t`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};o([e()],a.prototype,"configuration",void 0),a=o([s("esphome-clean-mqtt-dialog")],a);
//# sourceMappingURL=c.e163e8d8.js.map
