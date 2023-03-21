import React, {useEffect, useState} from "react";
import {Row, Col, Button, Tooltip, OverlayTrigger} from "react-bootstrap"
import {AiOutlineClose, AiOutlineSelect, AiOutlineSend} from "react-icons/ai";


const ActionGroups = ({selected_actions, select_action, select_actions, remove_action, send_actions}) => {

    const messagesEndRef = React.createRef()

    useEffect(() => {
         messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [selected_actions])

return (
    <div className={"card-gray p-4 h-100"}>
        <div className={"card-title"}>
            <span><strong>Action Groups</strong></span>
        </div>
        {selected_actions && selected_actions.length === 0
        ?

        <Row className={"justify-content-center h-100 align-items-center text-center"}>
            <Col xs={12}>
                <span className={"text-muted"}><strong>No actions selected</strong></span>
            </Col>
        </Row>
        :
        <Row className={"justify-content-center h-100"}>
            <Col xs={12} className={"mt-1"} style={{overflowY: "auto", maxHeight: "200px"}}>
            { selected_actions.map((action, number) => {
                return (
                    <Row className={"row-dark p-1 mt-1"} key={action.name + number}>
                        <Col xs={12}>
                            <span><span className={"text-muted"}>{number + 1}.</span> <strong className={"ps-2"}>{action.name}</strong> </span>
                            <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"unique"}>Remove action from group</Tooltip>}>
                                <Button variant={""} className={"button-danger-nb float-end py-0 px-1"}><AiOutlineClose className={"card-icon-tiny"} style={{marginBottom: "3px"}} onClick={() => remove_action(action)}/></Button>
                            </OverlayTrigger>
                            <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"unique"}>Reselect action</Tooltip>}>
                                <Button variant={""} className={"float-end py-0 px-1"} style={{color: "white"}}><AiOutlineSelect className={"card-icon-tiny"} style={{marginBottom: "3px"}} onClick={() => select_action(action)}/></Button>
                            </OverlayTrigger>
                        </Col>
                    </Row>
                )
            })}
                <div ref={messagesEndRef} />
            </Col>
            <Col xs={12} className={"align-self-end mt-3"}>
                <Row className={"align-items-center"}>
                    <Col xs={12}  lg={6} className={"text-center text-lg-start"}>
                        <span className={"text-muted align-middle"}><strong>{Object.keys(selected_actions).length} actions</strong></span>
                    </Col>
                    <Col xs={12} lg={6} className={"text-center text-lg-end"}>
                        <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"delete-all-actions"}>Delete all actions</Tooltip>}>
                            <Button variant={""} className={"button-danger me-2"} onClick={() => select_actions([])}><AiOutlineClose style={{marginBottom: "3px"}} /></Button>
                        </OverlayTrigger>
                        <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-all-actions"}>Send all actions</Tooltip>}>
                            <Button variant={""} className={"button-green"} onClick={() => send_actions(selected_actions)}><AiOutlineSend style={{marginBottom: "3px"}} /></Button>
                        </OverlayTrigger>
                    </Col>
                </Row>
            </Col>
        </Row>
        }
    </div>
)

}

export default ActionGroups