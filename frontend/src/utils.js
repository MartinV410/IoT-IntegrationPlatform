import {SiWire} from "react-icons/si";
import {MdBluetoothSearching, MdCellTower} from "react-icons/md";
import React from "react";


export const getProtocolColor = (protocol) => {
    let color = "message-box-default";

    switch (protocol) {
        case "1-Wire":
            color = "bg-1wire";
            break;
        case "Bluetooth":
            color = "bg-bluetooth";
            break;
        case "NB-IoT":
            color = "bg-nbiot";
            break;
        case "DMX":
            color = "bg-dmx";
            break;
    }

    return color
}


export const getProtocolIcon = (protocol) => {
    switch (protocol) {
        case "1-Wire":
            return <SiWire />
        case "Bluetooth":
            return <MdBluetoothSearching />
        case "NB-IoT":
            return <MdCellTower />
        case "DMX":
            return <></>
        case "LoRaWan":
            return <></>
    }
}
