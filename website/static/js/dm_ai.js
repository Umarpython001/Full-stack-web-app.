//DOM elements
const form = document.getElementById('chatForm')

const msg_input = document.getElementById('msg_content')

const message_div = document.getElementById('messageFeed')

let send_btn = document.getElementById('send-btn')

//Initialize Socket.IO client
var socket = io()


//Render marked content(markdown content) in the message feed
document.addEventListener("DOMContentLoaded", function() {
    // Find every message content on the page
    document.querySelectorAll('.msg-content').forEach(el => {
        // Convert the text inside the element to Markdown HTML
        el.innerHTML = marked.parse(el.textContent);
    });
});


// Function to send/emit a message to the server when the user clicks the send button
function sendMesssageAI(){

    let msg_content = msg_input.value.trim()


    if(msg_content.length > 0){

        socket.emit('send_message_to_ai', {
            
            "msg_content": msg_content,
            "model_id": modelID,
            "modelName": modelName
        })

        msg_input.value = ''

    }

}

send_btn.onclick = sendMesssageAI



// Socket on events

// Display sent message on screen of user
socket.on('receive_message_from_human', function(data){

    let msg_content = data.msg_content //The content of the message
    let timestamp = data.timestamp //The timestamp of when the message was sent

    const htmlResult = marked.parse(msg_content);

    let new_msg = `
    
                    <div class="message-wrapper sent">
                        <div class="message-bubble">
                            <p class="msg-content"> ${htmlResult} </p>
                            <span class="timestamp"> ${timestamp} </span>
                        </div>
                    </div>
    

    `
    message_div.innerHTML += new_msg


})


// Display the AI's reply on screen
socket.on('ai_reply', function(data){

    let answer = data.answer
    let timestamp = data.timestamp

    const htmlResult = marked.parse(answer);

    console.log(htmlResult)


    new_msg = `
    
                    <div class="message-wrapper received">
                        <div class="message-bubble">
                            <p class="msg-content"> ${htmlResult} </p>
                            <span class="timestamp"> ${timestamp} </span>
                        </div>
                    </div>
    

    `

    message_div.innerHTML += new_msg 
    

})