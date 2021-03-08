
var cutTemplate = function(selector) {
    let node = document.querySelector(selector)
    node.remove()
    return node.innerHTML
    return node.outerHTML
}
