var client_id = Date.now()
var ipAddress = '127.0.0.1'
var port = 8000

var socketApp
var socket


const localSocketAutoMain = function(){
    socketApp = Vue.createApp(RootComponent)
    socket = socketApp.mount('#websockets')
}

const RootComponent = {
    /* options */
    data(){
        return {
            url: `ws://${ipAddress}:${port}/ws/${client_id}`
            , connected: false
            , callbacks: {}
            , outbox: []
        }
    }
    , mounted() {
        this.connect()
    }
    , methods: {

        connect(){
            console.log('Connect')
            let ws = this.ws = new WebSocket(this.url);
            ws.onmessage = this.onmessage.bind(this)
            ws.onopen = this.onopen.bind(this)
            ws.onerror = this.onerror.bind(this)
            ws.onclose = this.onclose.bind(this)
        }
        , reconnect(){
            if(!this.connected) {
                this.connect()
            }
        }

        , onmessage(event) {
            //console.log('event', event)
            // console.log('data ', event.data)
            this.digestMessage(event)
        }

        , onopen(event) {
            console.log('open', event)
            console.log('data ', event.data)
            this.connected = true;
            this.sendOutbox()

        }
        , sendOutbox(){
            console.log('Sending all outbox')
            for (var i = 0; i < this.outbox.length; i++) {
                this.send(this.outbox[i])
            }
            this.outbox = []
        }

        , onerror(event) {
            console.log('error', event)
            console.log('data ', event.data)
        }

        , onclose(event) {
            console.log('close', event)
            console.log('data ', event.data)
            this.connected = false
        }

        , digestMessage(event) {
            let content = event.data
            let data = content
            if(typeof(content) == 'string') {
                try {
                    data = JSON.parse(content)
                } catch(e) {
                    // unparseable
                    data = { content: content }
                }
            }

            this.digest(event, data)
        }

        , digest(event, data) {
            console.log('digest', data)
            let id = data['_id']

            if(this.callbacks[id] != undefined) {
                let _f = this.callbacks[id].callback || this.callbacks[id]
                let weak = this.callbacks[id].weakRef
                _f(data, event)
                if(weak === true) {
                    this.deleteHandler(id)
                }
            }
        }
        , deleteHandler(id) {
            delete this.callbacks[id]
        }
        , request(dataKey, callback, weakRef) {
            this.send({ 'type': 'request', 'key': dataKey}, callback, weakRef)
        }

        , send(message, callback, weakRef) {
            /*
            Send a message object or string as a JSON converted string
            to the websocket server.

                let event = { 'type': 'store', key:'drives', drives }
                socket.send(event, this.driveContent.bind(this))
             */
            let id = message['_id'] || Math.random().toString(32)

            if(typeof(message) == 'string') {
                message = {
                    text: message
                }
            }

            message['_id'] = id
            if(callback) {
                this.callbacks[id] = {weakRef, callback}
            }

            if(this.connected == false) {
                console.log('Stack early message')
                return this.outbox.push(message)
            }

            if(typeof(message) == 'object') {
                message = JSON.stringify(message)
            }
            this.ws.send(message)
        }
    }
}


function sendMessage(value) {
    socket.ws.send(value)
}

;localSocketAutoMain();
