import React, {useEffect, useState} from "react";
import Protocol from "../cards/Protocol";
import ChooseActions from "../cards/ChooseActions";
import Messages from "../cards/Messages";
import ActionGroups from "../cards/ActionGroups";
import {Container, Row, Col} from "react-bootstrap";
import {client, server_ip} from "../../api/client";
import Response from "../cards/Response";
import {AnimatePresence} from "framer-motion";
import Modal from "../modal/Modal";
import useWebSocket, { ReadyState } from 'react-use-websocket';



export default function ProtocolPage({protocol, endpoint, text, timeout, websocketPort}) {

    const [selectedAction, setSelectedAction] = useState({});
    const [actions, setActions] = useState([{}]);
    const [selectedActions, setSelectedActions] = useState([]);

    const [messages, setMessages] = useState([]);
    const [selectedMessage, setSelectedMessage] = useState();
    const [show, setShow] = useState(false);

    const [protocolInfo, setProtocolInfo] = useState({})

    const { sendMessage, lastMessage, readyState } = useWebSocket(`ws://${server_ip}:${websocketPort}`);

    useEffect(() => {
        if (lastMessage !== null) {
            setMessages(prevState => [...prevState, {"protocol": protocol, "response_date": Date.now(), "action": {}, "index": messages.length, "passed": true, "direction": "from", "data": lastMessage.data, "message": lastMessage.data}])
          // setMessageHistory((prev) => prev.concat(lastMessage));
        }
      }, [lastMessage]);

    const handleAddAction = (new_action) => {
        if(!selectedActions.some((element) => element.name === new_action.name)) {
            setSelectedActions([...selectedActions, new_action])
        }
    }


    const sendAction = async (action, index) => {
        // TODO maybe lil bit of optimalization required?
        setMessages(m =>
                m.map((element) => {
                    if(element.index === index) {
                        return {
                            ...element,
                            "direction": "to",
                            "sended": true
                        }
                    }
                    return element
                })
            )

        const data = {}
        data[action.name] = {}
        action.allowed_args.map((element) => {if(element.data && element.data !== "") {data[action.name][element.name] = element.data}})
        try {
            let response;
            if(timeout) {
                response = await client.post(endpoint, data, {timeout: timeout})
            }else {
                response = await client.post(endpoint, data)
            }

            setMessages(m =>
                m.map((element) => {
                    if(element.index === index) {
                        return {
                            ...element,
                            "response_date": Date.now(),
                            "http_status": response.status,
                            "http_status_text": response.statusText,
                            ...response.data
                        }
                    }
                    return element
                })
            )

        } catch (err) {
            // not in 200 response range
            setMessages(m =>
                m.map((element) => {
                    if(element.index === index) {
                        return {
                            ...element,
                            "response_date": Date.now(),
                            "http_status": err.response?.status,
                            "http_status_text": err.response?.statusText,
                            "passed": false,
                            "message": err.response ? err.response?.statusText : ""
                        }
                    }
                    return element
                })
            )
        }
    }

    useEffect(() => {
        messages.map((msg) => {
            if(!msg.sended && msg.direction !== "from") {
                sendAction(msg.action, msg.index)
            }
        })

    }, [messages])

    const handleSendAction = (action, index = -1) => {
        if(index === -1) {
            setMessages(prevState => [...prevState, {"protocol": protocol, "request_date": Date.now(), "action": action, "index": messages.length, "sended": false}])
        } else {
            setMessages(prevState => [...prevState, {"protocol": protocol, "request_date": Date.now(), "action": action, "index": index, "sended": false}])
        }
    }

    const sendActions = (actions) => {
        let curr_index = messages.length
        actions.map((element) => {
            handleSendAction(element, curr_index)
            curr_index += 1
        })
    }

    const removeAction = (action) => {
        // const new_selected_actions = [...selectedActions]
        // setSelectedActions(new_selected_actions.filter((element) => element.name !== action.name))
        setSelectedActions(s => s.filter((element) => element !== action))
    }

    const handleShowMessage = (message) => {
        setSelectedMessage(message)
        setShow(true)
    }

    const handleChooseAction = (action_str) => {
        setSelectedAction(actions.find(element => element.name === action_str))
    }


    useEffect(() => {
        const fetchActions = async () => {
            try {
                const response = await client.post(endpoint, {"help": []})
                setActions(response.data.data)
                setSelectedAction(response.data.data[0])
            } catch (err) {
                // not in 200 response range
                setActions([{}])
            }
        }

         const fetchInfo = async () => {
            try {
                const response = await client.post("control/", {"protocols_info": {}})
                setProtocolInfo(response.data.data[protocol])
            } catch (err) {
                // not in 200 response range
                setProtocolInfo({})
            }
        }

        fetchActions()
        fetchInfo()
    }, [])


    return (
        <div>
            <AnimatePresence mode={"wait"} onExitComplete={() => setShow(false)}>
                {show && selectedMessage &&
                    <Modal setShow={setShow}>
                        <Response message={selectedMessage} />
                    </Modal>
                }
            </AnimatePresence>
            <Container>
                <Row className={"justify-content-center w-100 mt-5"}>
                    <Col xs={12} lg={3}>
                        <Protocol protocol={protocol} text={text} choose_action={handleChooseAction}/>
                    </Col>


                    <Col xs={12} lg={5} className={"mt-3 mt-lg-0"}>
                        <ChooseActions actions={actions} setActions={setActions} sendAction={handleSendAction} addAction={handleAddAction} selected={selectedAction} setSelected={setSelectedAction} />
                    </Col>
                    <Col xs={12} lg={4} className={"mt-3 mt-lg-0"} style={{minHeight: "300px"}}>
                        <ActionGroups selected_actions={selectedActions} select_action={setSelectedAction} select_actions={setSelectedActions} remove_action={removeAction} send_actions={sendActions} />
                    </Col>
                    <Col xs={12} className={"mt-3"} style={{height: "500px"}}>
                        <Messages messages={messages} setMessages={setMessages} selectMessage={handleShowMessage} />
                    </Col>
                </Row>
            </Container>
        </div>
    )
}