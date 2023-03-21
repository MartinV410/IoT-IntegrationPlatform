import React, {useState} from "react";
import {Col, Row, Button, Tooltip, OverlayTrigger} from "react-bootstrap"
import Form from "react-bootstrap/Form"
import Select from "react-select";
import {BsPatchQuestion} from "react-icons/bs";
import {AiOutlinePlus, AiOutlineSend} from "react-icons/ai";


const ChooseActions = ({actions, setActions, sendAction, addAction, selected, setSelected}) => {

    //const [selected, setSelected] = useState();
    //const [selectedArgs, setSelectedArgs] = useState({})


    function handleInputChange(event, arg_name) {
        const value = event.target.value
        if(value !== "") {
            event.target.labels[0].classList.add("label-active")
        } else {
            event.target.labels[0].classList.remove("label-active")
        }

        const actions_copy = [...actions]
        const action = actions_copy[actions_copy.findIndex((element) => element.name === selected.name)]
        const arg = action.allowed_args.find((element) => element.name === arg_name)

        arg["data"] = value

        setActions([...actions_copy])

        // const args = selectedArgs
        // args[arg_name] = value
        // setSelectedArgs(args)
    }



    const renderAction = ({description, name, optional,standalone, allowed_args}) => {
    return(
        <Form className={"row"} onSubmit={(e) => {e.preventDefault(); sendAction(selected)}}>
            <Col xs={12}>
                <Row>
                    <Col xs={12} className={"mb-2 mt-2"}>
                        <span><strong>{description}</strong></span>
                    </Col>

                    {allowed_args?.map((arg) => {
                            return(
                                <Col xs={12} className={"mt-2"} style={{position: "relative"}} key={arg.name}>
                                    <Form.Group className={"input-container"} controlId={arg.name}>
                                        <Form.Label className={`custom-label ${arg.data ?  "label-active" : ""}`}>{arg.name}({arg.type})</Form.Label>
                                        {/*<Form.Label className={`custom-label ${selectedArgs[arg.name] && selectedArgs[arg.name] !== "" && "label-active"}`}>{arg.name}</Form.Label>*/}
                                        <Form.Control className={`custom-input ${arg.optional ? 'param-optional' : 'param-required'}`} type={"text"} name={arg.name} onChange={(e) => handleInputChange(e, arg.name)} value={arg.data ? arg.data : ""}></Form.Control>
                                    </Form.Group>
                                     <div className={"float-end"} >
                                        <OverlayTrigger placement="top" overlay={<Tooltip id={"unique"}>{arg.description}. This action is {arg.optional ? "optional" : "required!"}</Tooltip>}>
                                            <div>
                                                <BsPatchQuestion className={"card-icon-small"}/>
                                            </div>
                                        </OverlayTrigger>
                                     </div>
                                 </Col>
                            )
                        })
                    }
                    {allowed_args && allowed_args.length === 0 &&
                    <Col xs={12} className={"align-self-center"}>
                        <span className={"text-muted"}><strong>This action has no arguments</strong></span>
                    </Col>
                    }
                </Row>
            </Col>
            <Col xs={12} className={"mt-4 align-self-end"}>
                <Row className={"align-items-center"}>
                    <Col xs={6}>
                        <span className={"small text-muted align-middle"}>{standalone ? "Standalone!" : "Not standalone"}</span>
                    </Col>
                    <Col xs={6} className={"text-end"}>
                        {!standalone &&
                        <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"add-action"}>Add action to collection</Tooltip>}>
                            <Button variant={""} onClick={(e) => addAction(selected)} className={"button-blue me-2"}><AiOutlinePlus style={{marginBottom: "3px"}} /></Button>
                        </OverlayTrigger>
                        }
                        <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>Send action directly</Tooltip>}>
                            <Button variant={""} onClick={(e) => sendAction(selected)}  className={"button-green"}><AiOutlineSend style={{marginBottom: "3px"}} /></Button>
                        </OverlayTrigger>
                    </Col>
                </Row>
            </Col>
        </Form>
    )
}

    return(
        <div className={"card-gray p-4 h-100"}>
            <div className={"card-title"}>
                <span><strong>Actions</strong></span>
            </div>
            <Row className={"justify-content-center h-100"} style={{minHeight: "200px"}}>
                <Col xs={12}>
                    <Select
                            placeholder={"Select action..."}
                            getOptionLabel ={(option)=>option.name}
                            getOptionValue ={(option)=>option.name}
                            options={actions}
                            onChange={(option) => setSelected(option)}
                            value = {selected}
                        styles={{
                            control: (baseStyle, state) => ({...baseStyle, backgroundColor: "#111111", border:"none"}),
                            option: (baseStyle, state) => ({...baseStyle, backgroundColor: state.isFocused && "#2a2b2f", border: "none"}),
                            menu: (baseStyle, state) => ({...baseStyle, backgroundColor: "#111111", border: "none"}),
                            singleValue: (baseStyle, state) => ({...baseStyle,color: "white"}),
                            input: (baseStyle, state) => ({...baseStyle, color: "white"}),
                    }}
                    />
                </Col>
                {
                    selected
                    ?
                    renderAction(selected)
                    :
                    <Col xs={12} className={"text-center"}>
                        <span className={"text-muted"}><strong>No action selected!</strong></span>
                    </Col>
                }

            </Row>
        </div>
    )
}

export default ChooseActions