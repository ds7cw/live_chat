import { useState } from 'react';
import useWebSocket from 'react-use-websocket'

const socketUrl = 'ws://127.0.0.1:8000/ws/test';

const Server = () => {
    const [message, setMessage] = useState("");
    const { sendJsonMessage } = useWebSocket(socketUrl, {
        onOpen: () => {
            console.log('Connected!')
        },
        onClose: () => {
            console.log('Closed!')
        },
        onError: () => {
            console.log('Error!')
        },
        onMessage: (msg) => {
            setMessage(msg.data);
        },
    });

    const sendHello = () => {
        const message = { text: "hello"}
        sendJsonMessage(message);
    };

    return (
        <div>
            <button onClick={sendHello}>Send Hello</button>
            <div>Received Data: {message}</div>
        </div>
    )
};

export default Server;