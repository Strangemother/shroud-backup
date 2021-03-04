/*

The main welcome screen for the first boot.

1. configure pointed drives.
 */

const WelcomePanelComponent = {
    data(){
        return {
            instanceName: 'Constantinople Warlock'
        }
    }
    , mounted(){
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
            console.log('Welcome>selectedDrives', selected)
        }

        , selectedDrives(event) {
            let drives = store.state.selectedDrives
            console.log('Welcome>selectedDrives', drives)
        }
    }

}

const ActionTrackApp = Vue.createApp(ActionTrackComponent)
const actionTrackApp = ActionTrackApp.mount('#action_track')
