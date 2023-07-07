import {Col, Container, Row} from "react-bootstrap";

import React from "react";
import Voltage from "../cards/Voltage";
import BatteryGauge from "react-battery-gauge";
import LineGraph from "../graphs/LineGraph";
import BarGraph from "../graphs/BarGraph";
import PieGraph from "../graphs/PieGraph";

const dummyVoltage = [
    {
        creation_date: "11:00",
        volt: 5.2,
    },
    {
        creation_date: "12:00",
        volt: 5.0,
    },
    {
        creation_date: "13:00",
        volt: 4.8,
    },
    {
        creation_date: "14:00",
        volt: 5.0,
    },
    {
        creation_date: "15:00",
        volt: 5.1,
    },
    {
        creation_date: "16:00",
        volt: 4.9,
    },
    {
        creation_date: "17:00",
        volt: 5.3,
    },
    {
        creation_date: "18:00",
        volt: 4.8,
    },
    {
        creation_date: "19:00",
        volt: 5.0,
    },
    {
        creation_date: "20:00",
        volt: 4.8,
    },
    {
        creation_date: "21:00",
        volt: 4.8,
    },
]

const dummyPie = [
  { volt: 5.4, percent: 20 },
  { volt: 4.8, percent: 10 },
  { volt: 5.2, percent: 25 },
  { volt: 5.0, percent: 45 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export default function DeepakPIO() {


    return(
        <Container className={"mb-2"}>
            <Row className={"mt-5"}>
                <Col xs={12} className={"text-center card-gray p-2"}>
                    <h1><strong>Deepak PIO</strong></h1>
                </Col>
            </Row>

            <Row className={"justify-content-between mt-2"}>
                <Col xs={2} className={"card-gray border-muted-right"}>
                    <Row className={"align-items-center h-100"}>
                        <Col xs={12} className={""}>
                            <BatteryGauge value={20} size={200} orientation={"vertical"} customization={{batteryMeter: {noOfCells: 10, lowBatteryValue: 35}, batteryBody: {strokeColor: '#ffffff'}, batteryCap: {strokeColor: '#ffffff'}, readingText: {lightContrastColor: '#ffffff', darkContrastColor: '#ffffff'}}} />
                        </Col>
                    </Row>
                </Col>
                <Col xs={4} className={"card-gray border-muted-right border-muted-left"}>
                    <Row className={"align-items-center h-100"}>
                        <Col xs={6}>
                            <Voltage title={"Cell 1 voltage"} value={12.04} unit={"V"} />
                        </Col>
                        <Col xs={6}>
                            <Voltage title={"Cell 2 voltage"} value={12.04} unit={"V"} />
                        </Col>
                        <Col xs={6}>
                            <Voltage title={"Cell 3 voltage"} value={12.04} unit={"V"} />
                        </Col>
                        <Col xs={6}>
                            <Voltage title={"Cell 4 voltage"} value={12.04} unit={"V"} />
                        </Col>
                        <Col xs={6}>
                            <Voltage title={"Cell 5 voltage"} value={12.04} unit={"V"} />
                        </Col>

                        <Col xs={6}>
                            <Voltage title={"Bus voltage"} value={12.04} unit={"V"} />
                        </Col>
                        <Col xs={6}>
                            <Voltage title={"Temp"} value={36.04} unit={"°C"} />
                        </Col>
                        <Col xs={6}>
                            <Voltage title={"Current"} value={12.44} unit={"A"} />
                        </Col>
                    </Row>

                </Col>
                <Col xs={6} className={"card-gray pb-2 border-muted-left"}>
                    <Row className={"card-text-big m-1"}>
                        <Col xs={12} className={""}>
                            <div className={"float-start"}>
                                <span><strong className={"text-muted"}>SOH:</strong></span>
                            </div>
                            <div className={"text-center"}>
                                <span><strong>0</strong></span>
                            </div>

                        </Col>
                    </Row>
                     <Row className={"card-text-big m-1"}>
                        <Col xs={12} className={""}>
                            <div className={"float-start"}>
                                <span><strong className={"text-muted"}>SOC:</strong></span>
                            </div>
                            <div className={"text-center"}>
                                <span><strong>0</strong></span>
                            </div>

                        </Col>
                    </Row>
                     <Row className={"card-text-big m-1"}>
                        <Col xs={12} className={""}>
                            <div className={"float-start"}>
                                <span><strong className={"text-muted"}>RUL:</strong></span>
                            </div>
                            <div className={"text-center"}>
                                <span><strong>0</strong></span>
                            </div>

                        </Col>
                    </Row>
                     <Row className={"card-text-big m-1"}>
                        <Col xs={12} className={""}>
                            <div className={"float-start"}>
                                <span><strong className={"text-muted"}>SOE:</strong></span>
                            </div>
                            <div className={"text-center"}>
                                <span><strong>0</strong></span>
                            </div>

                        </Col>
                    </Row>
                     <Row className={"card-text-big m-1"}>
                        <Col xs={12} className={""}>
                            <div className={"float-start"}>
                                <span><strong className={"text-muted"}>THE:</strong></span>
                            </div>
                            <div className={"text-center"}>
                                <span><strong>0</strong></span>
                            </div>

                        </Col>
                    </Row>
                    <Row className={"mt-2"}>
                        <Col xs={12} className={"text-center card-text-big"}>
                            <span><strong>FAULTS</strong></span>
                        </Col>
                    </Row>

                    <Row className={"px-2 mt-1"}>
                        <Col xs={12} className={"card-darkgray py-2"}>
                            <div className={"fault-alert"}>
                                <span><strong>ALERT</strong></span>
                            </div>
                            <div className={"text-muted"}>
                                <span><strong>Cell 1 voltage over (+1,4V)</strong></span>
                            </div>
                        </Col>
                    </Row>
                    <Row className={"px-2 mt-1"}>
                        <Col xs={12} className={"card-darkgray py-2"}>
                            <div className={"fault-alert"}>
                                <span><strong>ALERT</strong></span>
                            </div>
                            <div className={"text-muted"}>
                                <span><strong>Cell 2 voltage over (+1,4V)</strong></span>
                            </div>
                        </Col>
                    </Row>
                    <Row className={"px-2 mt-1"}>
                        <Col xs={12} className={"card-darkgray py-2"}>
                            <div className={"fault-alert"}>
                                <span><strong>FAULT</strong></span>
                            </div>
                            <div className={"text-muted"}>
                                <span><strong>Battery overvoltage (+0,8V)</strong></span>
                            </div>
                        </Col>
                    </Row>
                </Col>
            </Row>

            <Row className={"mt-2"}>
                <Col xs={6} className={"card-gray  border-muted-right"}>
                    <p className={"text-center card-text-big"}><strong>Volt/Time</strong></p>
                    <div className={"graph-container"}>
                        <LineGraph data={dummyVoltage} dataKey={"creation_date"} lines={[{dataKey: "volt", color: "#ff7400"}]} />
                    </div>
                </Col>
                <Col xs={6} className={"card-gray p-1  border-muted-left"}>
                    <p className={"text-center card-text-big"}><strong>Volt/Time</strong></p>
                    <div className={"graph-container"}>
                        <BarGraph data={dummyVoltage} dataKey={"creation_date"} bars={[{dataKey: "volt", color: "#ff7400"}]} />
                    </div>
                </Col>
                <Col xs={3} className={"card-gray p-1  mt-2"}>
                    <p className={"text-center card-text-big"}><strong>Volt/Percentage</strong></p>
                    <div className={"graph-container"}>
                        <PieGraph data={dummyPie} dataKey={"percent"} colors={COLORS} />
                    </div>
                </Col>
            </Row>
        </Container>
    )
}