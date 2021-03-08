/*

The main Drives screen for the first boot.

1. Call to the coms for the base drive list
2. Wait on response and render.
 */


const ExplorerComponent = {
    data(){
        return {
            panels: []
            , dragMode: false
        }
    }

    , mounted(){
        console.log('Explorer')
        this.panels.push({
            title: 'Apples'
        },)
    }

    , methods: {
        newPanelClick(mouseEvent) {
            this.newPanel()
        }
        , newPanel(title='Panel') {
            this.panels.push({
                title
                , uuid: Math.random().toString(32)
            })
        }
        , closePanel(panel) {
            let v = this.panels.indexOf(panel)
            if(v<=-1) {return}
            this.panels.splice(v, 1)
        }
        , spawnPanel(ev) {
            console.log('spawn', ev)
            this.panels.push(ev)
        }
        , dragStart(ev) {
            console.log('Explorer dragStart')
            this.dragMode = true
        }
        , dragStop(ev) {
            console.log('Explorer dragStop')
            this.dragMode = false
        }
    }
    , computed: {
        tabs() {
            let r = []
            this.panels.forEach(function(x){
                r.push(x.title)
            })
            return r
        }
    }
}

const App = Vue.createApp(ExplorerComponent)
