/*

The main welcome screen for the first boot.

1. configure pointed drives.
 */

const WelcomePanelComponent = {
    data(){
        return {
            store: store.state
        }
    }
    , mounted(){
        this.store.instanceName = this.store.instanceName || 'Constantinople Warlock'
        console.log('welcome')
    }

}

const WelcomeApp = Vue.createApp(WelcomePanelComponent)
const welcomeApp = WelcomeApp.mount('#welcome')

const ActionTrackComponent = {
    data(){
        return {
            store: store.state
        }
    }
    , mounted(){
        console.log('welcome')
        // bus.$bind('selected-drives', this.selectedDrives.bind(this))
    }

    , methods: {
        selectDefaultDrives(event) {
            let disks = store.state.disks
            console.log('Select default disks', disks)
            let selected = []
            disks.forEach(function(x){
                if(x.suggested) {
                    selected.push(x)
                }
            })
            this.recordDrives(disks)
        }

        , selectedDrives(event) {
            let drives = Object.values(store.state.selectedDrives)
            this.recordDrives(drives)
        }

        , recordDrives(drives) {
            console.log('Welcome>selectedDrives', drives)
            let event = { 'type': 'store', key:'drives', drives }
            socket.send(event, this.storeResponse.bind(this))
        }

        , storeResponse(e) {
            console.log('Store Done', this.store.instanceName)
            let name = this.store.instanceName
            let event = { 'type': 'store', key:'name', name}
            socket.send(event, this.storeNameResponse.bind(this))
        }
        , storeNameResponse(e) {
            console.log('Store name complete')
            window.location.href = '/desktop/configured/';
        }
    }

}

const ActionTrackApp = Vue.createApp(ActionTrackComponent)
const actionTrackApp = ActionTrackApp.mount('#action_track')
