
// Define a new global component called button-counter
App.component('button-counter', {
  data() {
    return {
      count: 0
    }
  },
  template: cutTemplate('.templates .button-counter')
})
