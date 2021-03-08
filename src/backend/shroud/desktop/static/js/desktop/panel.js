

// Define a new global component called button-counter

const FileDragMixin = {

}

const PanelComponent = {
    template: cutTemplate('.templates .panel-template')
    , mixins: [FileDragMixin]
    , data() {
        return {
            files: []
            , showStartPage: false
            , showDriveList: false
            , disks: []
            , currentPath: 'root'
            , filterType: '__all__'
        }
    }
    , emits: ['select', 'closepanel']
    , props: ['config']
    , mounted(){
        console.log('mounted panel', this.config.title)

        // this.currentPath = this.config.path || 'root'
        if(this.config.path == undefined) {
            this.startPage()
        } else {
            this.navigateToDir(this.config.path)
        }
    }
    , methods: {

        startPage() {
            /*
            The start page provides a _jump point_ for the user, if no preliminary
            location is given.
             */
            this.showStartPage = true
            this.showDriveList = true
            let location = this.config.location

            if(location == undefined) {
                return this.showDrives()
            }

            this.files.push({
                label: 'first file'
                , icon: 5
            })
        }

        , homeReset(){
            if(this.showStartPage) {
                this.showStartPage = false
                this.showDriveList = false
                return
            }
            this.startPage()
        }

        , closePanel(){
            this.$emit('closepanel')
        }
        , showDrives() {
            /*
            Present a list of drives as a standard start location for a panel.
             */
            this.showDriveList = true
            socket.request('drives', this.driveContent.bind(this), false)
        }

        , driveContent(data){
            console.log('Got drives', data)
            if(data.logical) {
                this.disks = data.logical
                socket.deleteHandler(data._id)
            }
        }

        , selectDrive(index) {
            let disk = this.disks[index]
            console.log('Rendering', disk)
            let event = {
                type: 'volume'
                , key:'directory'
                , volumeName: disk.volume_name
                , path: disk.name
            }
            socket.send(event, this.directoryContent.bind(this))
        }

        , addressBarNavigate(data) {
            console.log('addressBarNavigate', data)
            this.directoryContent(data)
        }

        , directoryContent(data) {
            /* The items return as an array of lists, each list item
            represents a file or folder

                [name, is_file, size, created, modified]

            The name is a partial path relative to the data.path.
             */
            let {path, items, actions } = data

            if(items != undefined) {
                console.log('directory', path)
                this.currentPath = path
                this.showItems(path, items)
                this.showDriveList = false;
                data.type='dir'

                this.showStartPage = false;
            } else {
               data.type='file'
               data.fullPath = this.currentPath
            }


            this.$refs.actionpanel.setContext(data)
        }

        , showItems(path, items){
            let files = []
            for (var i = 0; i < items.length; i++) {
                let f = this.normalizeFile.apply(this, [path].concat(items[i]))
                files.push(f)
            }
            this.files = files
        }

        , normalizeFile(parent, name, isFile, size, created, modified) {
            return {parent, name, isFile, size, created, modified}
        }

        , clickItem(file) {
            /* Select the file for forward progress such as track. */
            console.log('Select', file)
            this.$emit('select', file)
            let timein = +(new Date)
            let lastTime = this.lastClick

            this.lastClick = timein
            let delta = timein - lastTime
            console.log('click delta', delta)
            if(delta <= 300) {
                return this.doubleclickItem(file)
            }
            return this.selectEntry(file)
        }

        , doubleclickItem(file) {
            console.log('doubleclickItem')
            let path = [file.parent, file.name].join('\\')
            let event = {
                type: 'open'
                , key:'directory'
                , path
            }

            // this.$refs.addressBar.path.push(file.name)
            socket.send(event, this.actionCalled.bind(this))
        }

        , actionCalled(ev) {
            console.log('Action called.')
        }

        , middleClickItem($event, file) {
            $event.preventDefault()
            let path = [file.parent, file.name].join('\\')
            let event = {
                title: 'spawned'
                , path
            }
            this.$emit('spawn', event)
        }

        , selectEntry(file) {
            console.log('Rendering', file)
            let path = [file.parent, file.name].join('\\')
            this.navigateToDir(path)
            file.selected = !file.selected
            if(this.lastSelectedFile != undefined) {
                this.lastSelectedFile.selected = !this.lastSelectedFile.selected
            }
            this.lastSelectedFile = file

        }

        , navigateToDir(path) {
            let event = {
                type: 'entry'
                , key:'directory'
                , path
            }
            this.currentPath = path
            // this.$refs.addressBar.path.push(file.name)
            socket.send(event, this.directoryContent.bind(this))
        }

        , actionFilterView(ev) {
            let type = { dirs: 0, files: 1}[ev.type]
            let isAll = ev.type == '__all__'
            // this.origFiles = this.files.slice(0)
            this.filterType = ev.type;
            for (var i = 0; i < this.files.length; i++) {
                let f = this.files[i];
                f.hidden = isAll? false: Number(f.isFile) != type
            }
        }

        , entityDragStart(event, file) {
              console.log('Dragging', event)
              event.dataTransfer.effectAllowed = "copy";
              const dt = event.dataTransfer;
              let path = [file.parent, file.name].join('\\')
              dt.setData('text/plain', path, 0);
              d = JSON.stringify(file)
              dt.setData('text/json', d, 0);
              dt.setData('application/object', d, 0);

        }
        , entityDragLeave(event, file){
            event.target.classList.remove('drag-over-accept')
        }

        , entityDragOver(event, file){
            /*
                The user content is dragged over this entity.
             */
            //console.log('drag over', file.isFile)
            if(file.isFile) {return}
            if( event.dataTransfer.types.includes("application/object")) {
                return this.announceDragOverAccept(event,file)
            }
        }
        , entityDragDrop(event, file){
//             console.log('drag drop', file)
            let other = JSON.parse(event.dataTransfer.getData('application/object'))
            let dest = file
            console.log('Ask about', other.name, 'to', dest.name)
        }

        , announceDragOverAccept(event,file){
            event.dataTransfer.effectAllowed = "copy";

            event.preventDefault()
            event.target.classList.add('drag-over-accept')
           return false
        }
    }

};

App.component('panel', PanelComponent);

