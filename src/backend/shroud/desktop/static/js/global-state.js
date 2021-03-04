const { reactive, createApp } = Vue

/*

const ExampleComponent = {
    data(){
        return {
            store: store.state
        }
    }
}
 */
const store = {
    debug: true
    , state: reactive({
        selectedDrives: new Set
        , disks: [],
    })
}

