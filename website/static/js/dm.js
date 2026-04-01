var socket = io()


console.log(`Room ID: ${roomID}`)



//DOM elements
const form = document.getElementById('chatForm')

const msg_input = document.getElementById('msg_content')

const message_div = document.getElementById('messageFeed')

console.log(message_div)

let submit_btn = form.querySelector('button[type="submit"]')



socket.on('connect', function() {

    socket.emit('join', {"room_id": roomID,})
                                }
                                
)




function sendMesssage(){


    let msg_content = msg_input.value.trim()

    console.log(`Message content: ${msg_content}`)

    if(msg_content.length > 0){

        socket.emit('send_message', {
            "room_id": roomID,
            "msg_content": msg_content,
        })

        msg_input.value = ''

    }



}


socket.on('receive_message', function(data){


    console.log(data)
    let msg_content = data.msg_content //The content of the message
    let sender = data.sender //The user id of the sender
    let timestamp = data.timestamp //The timestamp of when the message was sent

    console.log(`Timestamp: ${timestamp}`)

    let new_msg = `
    
                    <div class="message-wrapper ${ (sender == current_user) ? 'sent' : 'received'}">
                        <div class="message-bubble">
                            <p> ${msg_content} </p>
                            <span class="timestamp"> ${timestamp} </span>
                        </div>
                    </div>
    

    `


    message_div.innerHTML += new_msg

    console.log(`Message received: ${msg_content} from ${sender} at ${timestamp}`)




})