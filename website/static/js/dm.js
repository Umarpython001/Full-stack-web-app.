var socket = io()


//DOM elements
const form = document.getElementById('chatForm')

const msg_input = document.getElementById('msg_content')

const message_div = document.getElementById('messageFeed')

let submit_btn = document.getElementById('send-btn')




function sendMesssageHUMAN(){

    let msg_content = msg_input.value.trim()

    if(msg_content.length > 0){

        socket.emit('send_message_to_human', {
            "room_id": roomID,
            "msg_content": msg_content,
            "recepient_id": recepient_id
        })

        msg_input.value = ''

    }



}

submit_btn.onclick = sendMesssageHUMAN

socket.on('receive_message_human', function(data){

    let msg_content = data.msg_content //The content of the message
    let sender = data.sender //The user id of the sender
    let timestamp = data.timestamp //The timestamp of when the message was sent

    let new_msg = `
    
                    <div class="message-wrapper ${ (sender == current_user) ? 'sent' : 'received'}">
                        <div class="message-bubble">
                            <p> ${msg_content} </p>
                            <span class="timestamp"> ${timestamp} </span>
                        </div>
                    </div>
    

    `


    message_div.innerHTML += new_msg

})