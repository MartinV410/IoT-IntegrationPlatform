import React, {useEffect} from "react";
import {Col, Row, Container, Button, Tooltip, OverlayTrigger, Form} from "react-bootstrap"
import {FiArrowDownLeft, FiArrowUpRight} from "react-icons/fi";
import {AiOutlineClose} from "react-icons/ai";
import Skeleton from "react-loading-skeleton";
import {getProtocolColor} from "../../utils";
import ScrollToBottom from 'react-scroll-to-bottom';



const formatDate = (date) => {
    return `${String(new Date(date).getHours()).padStart(2, '0')}:${String(new Date(date).getMinutes()).padStart(2, '0')}:${String(new Date(date).getSeconds()).padStart(2, '0')}`
}


const Messages = ({messages, setMessages, selectMessage}) => {

    // const messagesEndRef = React.createRef()
    //
    // useEffect(() => {
    //      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' })
    // }, [messages])

    return(
        <div className={"card-gray p-4 h-100"}>
            <div className={"card-title"}>
                <span><strong>Messages</strong></span>
            </div>
            {/*<Container className={"message-container"}>*/}
            <ScrollToBottom  className={"message-container"} initialScrollBehavior={"smooth"} >
                <Container>
                {messages && messages.map((message, index) => {
                    return (
                        <Row className={`row-dark ${index !== 0 && "mt-1"}`} key={index} onClick={() => {if(message.passed !== undefined) {selectMessage(message)}}} style={{cursor: "pointer"}}>
                            <Col xs={12} className={"py-1 d-flex align-items-center"}>
                                 {message.passed !== undefined ?
                                    <div className={`message-box ${message.passed ? "status-success" : "status-error"}`} style={{width: "40px"}}>
                                        <span><strong>{message.passed ? "OK" : "ERR"}</strong></span>
                                    </div>
                                     :
                                     <div className={"message-box"} style={{width: "40px"}}>
                                         <Skeleton width={30} style={{padding: 0, margin: 0}} />
                                     </div>

                                     // <div className={`ms-1 message-box`} style={{width: "40px"}}>
                                     //      <span><Skeleton width={40} containerClassName={"message-box"}/> </span>
                                     // </div>
                                 }
                                <div className={"ms-1 message-box message-box-default"} style={{maxWidth: "70px"}}>
                                    <span><strong>{message.request_date && !message.response_date ? formatDate(message.request_date) : formatDate(message.response_date)}</strong></span>
                                </div>
                                <div className={`message-box ms-1 text-center ${getProtocolColor(message.protocol)}`} style={{maxWidth: "80px"}}>
                                    <span><strong>{message.protocol}</strong></span>
                                </div>
                                {message.message !== undefined ?
                                <div className={"ms-1 message-box"} style={{maxWidth: "400px"}}>
                                    <div className={"d-inline-block text-truncate"}>
                                        <span>{message.message}</span>
                                    </div>
                                </div>
                                    :
                                <div className={"ms-1 message-box"} style={{maxWidth: "400px"}}>
                                    <Skeleton width={390} />
                                </div>
                                }
                                <div className={"d-inline-block ms-auto"}>
                                    {message.direction && message.direction === "to" &&
                                        <FiArrowUpRight  className={"message-icon-small"}/>
                                    }
                                    {message.direction && message.direction === "from" &&
                                        <FiArrowDownLeft  className={"message-icon-small"}/>
                                    }
                                </div>
                            </Col>
                        </Row>
                    )
                })}
                    </Container>
                </ScrollToBottom>
                {/*<div ref={messagesEndRef} />*/}
            {/*</Container>*/}
            <Row className={"mt-2"}>
                <Col xs={12} className={"d-flex align-items-center"}>
                    <div className={"d-inline-flex"}>
                        <span className={"text-muted"}><strong>{messages.length} total messages</strong></span>
                    </div>
                    <div className={"d-inline-flex ms-auto  align-items-centers"}>
                        <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>Delete all messages</Tooltip>}>
                            <Button variant={""} className={"button-danger me-2 float-end"} onClick={() => setMessages([])}><AiOutlineClose style={{marginBottom: "3px"}} /></Button>
                        </OverlayTrigger>
                    </div>
                </Col>
            </Row>

        </div>
    )
}

export default Messages