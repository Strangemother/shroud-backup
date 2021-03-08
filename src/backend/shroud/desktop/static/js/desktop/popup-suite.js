
// Define a new global component called button-counter
App.component('popup-suite', {
    data() {
        return {
            dragging: false
        }
    }
    , props: ['popups']
    , template: cutTemplate('.templates .popup-suite-template')
    , methods: {
        popupdragging(ev) {
            //console.log('dradding', ev)
            this.dragging = ev.dragging
            this.draggingTarget = ev.popup
        }
        , mouseupHandler(ev) {
            this.draggingTarget.stopDrag()
        }
        , mousemoveHandler(ev) {
            if(this.dragging) {
                //console.log(ev)
            }
        }
        , closePopup(ev){
            console.log('closePopup', ev)
            let removed = this.popups.splice(ev.index, 1)
            console.log('Removed', removed)
        }
    }
})
