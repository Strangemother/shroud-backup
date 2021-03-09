
// Define a new global component called action-panel
App.component('action-panel', {
    data() {
        return {
            config: {}
            , caption: 'A Caption'
            , tools: []
            , itemsCount: { files: 0, dirs: 0, total: 0 }
            , fileBytes: 0
            , dirBytes: 0
            , fileInfo: { hidden: true }
            , totalBytes: 0
            , popups: []
        }
    }
    , template: cutTemplate('.templates .action-panel-template')
    , emits: ['setdisplaystyle']
    , methods: {
        setContext(data) {
            this.config = data
            this.computeCounts(data)
            this.fileInfo.path = data.path
        }

        , displayStyle(type){
            this.$emit('setdisplaystyle', type)
        }

        , computeCounts(data) {
            let count = [0, 0]
            let items = []
            let size = [0,0]

            if(data.items != undefined) {
                items = data.items

                for (var i = 0; i < items.length; i++) {
                    let item = items[i]
                    count[Number(item[1])] += 1
                    size[Number(item[1])] += item[2]
                }
                this.totalBytes = size[0] + size[1]
                this.dirBytes = size[0]
                this.fileBytes = size[1]

            }

            this.itemsCount = { files: count[1], dirs: count[0], total: items.length }

            if(data.actions) {
                this.computeActions(data)
            }

            if(typeof(data.path) == 'object') {
                // ["thumbs_viewer.exe", true, 88064, 1526547522, 1586298171.1971743]
                this.fileInfo.name = data.path[0]
                this.fileInfo.isFile = data.path[1]
                this.fileInfo.size = data.path[2]
                this.fileInfo.accessed = data.path[3]
                this.fileInfo.modified = data.path[4]
                this.fileInfo.hidden = false
            } else {
                // a dir
                this.fileInfo.isFile = false
                this.fileInfo.name = undefined
                this.fileInfo.hidden = true
            }

            if(this.itemsCount.total == 0) {

            }
        }

        , computeActions(data) {
            let actionContent = data.actions
            this.tools = actionContent.tools
            this.caption = actionContent.caption
        }

        , filterView(filterType){
            this.$emit('filter', { type: filterType})
        }

        , actionClick(action) {
            let _action = action.action || action
            let path = this.config.fullPath || this.fileInfo.path
            let event = {
                type: _action
                , key:'action'
                , path
            }

            console.log('Action',_action, path)
            // this.$refs.addressBar.path.push(file.name)
            socket.send(event, this.actionCalled.bind(this))

            if(_action == 'tag') {
                this.popups.push({
                    type: 'tag-popup'
                    , path
                    , name: this.fileInfo.name
                })
            }
        }

        , actionCalled(ev) {
            console.log('actionCalled', ev)
        }
    }
})
