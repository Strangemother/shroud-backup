/*

The main Drives screen for the first boot.

1. Call to the coms for the base drive list
2. Wait on response and render.
 */

const DrivesPanelComponent = {
    data(){
        return {
            disks: []
            , selected: new Set
            , store: store.state
        }
    }

    , mounted(){
        console.log('Drives')
        // sendMessage('drives')
        socket.request('drives', this.driveContent.bind(this), false)
    }

    , methods: {
        toggleSelect(disk, index){
            /*
                add or remove the disk from the selection.
             */
            let sl = this.selected;
            if(sl.has(index)) {
                sl.delete(index)
                this.emitSelected()
                return
            }
            sl.add(index)
            this.emitSelected()
        }

        , emitSelected(){
            let r = []
            this.selected.forEach(function(i){
                r.push(this.disks[i])
            }.bind(this))
            this.$emit('selected', r)
            this.store.selectedDrives = r
            return r
        }

        , driveContent(data){
            console.log('driveContent', data)
            if(data.logical == undefined) {
                //socket.callbacks[data._id] = this.driveContent.bind(this)
                this.disks = data.letters
                return
            }

            this.applySuggestions(data.logical)
            this.disks = data.logical
            this.store.disks = this.disks
        }

        , applySuggestions(disks) {
            /* Apply the 'suggested' tag to each drive based upon a choice
            of highlight*/
            for (var i = 0; i < disks.length; i++) {
                disks[i].suggested = disks[i].drive_type == 3
            }
        }
    }

}

const DrivesApp = Vue.createApp(DrivesPanelComponent)
const drivesApp = DrivesApp.mount('#drives')
