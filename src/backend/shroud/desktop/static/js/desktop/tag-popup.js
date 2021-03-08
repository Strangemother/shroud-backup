
// Define a new global component called button-counter
App.component('tag-popup', {
    data() {
        return {
            styles: {
                zindex: 1
            }
            , dragging: false
            , tags: []
            , newTag: 'bacon'
        }
    }
    , emits: ['popupdragging', 'close']
    , props: ['index', 'popup']
    , template: cutTemplate('.templates .tag-popup-template')

    , mounted(){
        this.styles.zindex=this.index + 1
        let tl = 45 + (2 * this.index)
        this.styles.left = `${tl}%`
        this.styles.top = `${tl}%`
        console.log('New popup', this.index)
    }

    , methods: {

        mousedownHandler(ev) {
            console.log('mousedownHandler', ev)
            ev.preventDefault()
            this.xy = [ev.screenX, ev.screenY]
            this.offsetXY = [ev.offsetX, ev.offsetY]
            this.startDrag()
        }

        , addTag() {
            this.tags.push({ selected: true, label: this.newTag})
            this.newTag = ''
        }

        , saveTags() {
            let tags = this.tags
            let info = this.popup
            // let resStr = JSON.stringify({ tags, path: info.path })
            // let res = JSON.parse(resStr)
            // console.log('Save tags to', res)
            let data = {
                type: 'store_tags'
                , key: 'action'
                , path: info.path
                , tags: tags.filter(x=>x.selected).flatMap(x=>x.label)
            }

            if(data.tags.length == 0 && this.newTag.length > 0){
                data.tags.push(this.newTag)
            }
            socket.send(data, this.savedTags.bind(this))
        }

        , savedTags(ev) {
            this.close({}, {index:this.index})
        }

        , close(ev, item) {
            this.$emit('close', {event: ev, item: this, index:this.index})
        }

        , startDrag(){
            this.dragging = true
            this.$emit(
                'popupdragging',
                {dragging: this.dragging, popup:this}
                )
        }

        , mouseupHandler(ev){
            if(this.dragging){
                console.log('mouseupHandler', ev)
                this.stopDrag()
            }
        }

        , mousemoveHandler(ev){
            if(this.dragging) {
                let xy = this.xy = [ev.clientX, ev.clientY]
                let oxy = this.offsetXY
                this.styles.left = `${xy[0] - oxy[0]}px`
                this.styles.top = `${xy[1] - oxy[1]}px`
                //console.log('mousemoveHandler', this.xy)
            }
        }

        , stopDrag() {
            console.log('stopDrag')
            this.dragging = false
            this.$emit(
                'popupdragging',
                {dragging: this.dragging, popup:this}
                )
        }

    }
})


