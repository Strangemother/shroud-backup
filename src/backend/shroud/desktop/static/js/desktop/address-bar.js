
// Define a new global component called button-counter
App.component('address-bar', {
    template: cutTemplate('.templates .address-bar-template')
    , props: ['currentpath']
    , data() {
        return {
            _currentPath: ''
        }
    }
    , mounted() {
        // this.parts = this.currentpath.split('\\')
    }
    , methods: {
        pathPartClick(index, part) {
            console.log('Navigate to', index, part)
            let p = this.path.slice(0, index+1).join('\\')
            let event = {
                type: 'entry'
                , key:'directory'
                , path:p
            }
            // this.currentPath = path
            // this.$refs.addressBar.path.push(file.name)
            socket.send(event, this.directoryContent.bind(this))
        }
        , directoryContent(d) {
            this.$emit('navigate', d)
        }
    }
    , computed: {
         path: {
            get() {
                let spl = this.currentpath.split('\\')
                let res = []
                spl.forEach(function(x) {
                    if(x.length <= 0) {
                        return
                    }

                    res.push(x)
                })

                return res
            }

        }
    }
})

