import React, {useEffect, useState} from "react";
import {Col, Row, Button, Tooltip, OverlayTrigger} from "react-bootstrap";
import {CiSaveDown2} from "react-icons/ci";
import {JsonViewer} from "@textea/json-viewer";


const Config = ({config, saveConf}) => {


    return(
         <div className={"card-gray p-4 h-100"}>
            <div className={"card-title"}>
                <span><strong>Config</strong></span>
            </div>

             <Row className={"h-100 mt-2"}>
                 <Col xs={12} className={"d-flex"}>
                     <div className={"w-100"} style={{maxHeight: "300px", overflowY: "auto"}}>
                         <JsonViewer rootName={false} value={config} theme="dark" defaultInspectDepth={2} editable={true} onChange={(path, prevValue, newValue) => saveConf(path[0], path[1], newValue)} />
                     </div>
                 </Col>
                 {/*<Col xs={12} className={"align-self-end mt-3 text-end"}>*/}
                 {/*   <OverlayTrigger placement="top" overlay={<Tooltip id={"send-action"}>Save config</Tooltip>}>*/}
                 {/*       <Button variant={""} className={"button-green"}><CiSaveDown2 style={{marginBottom: "3px"}} /></Button>*/}
                 {/*    </OverlayTrigger>*/}
                 {/*</Col>*/}
             </Row>
         </div>
    )
}

export default Config