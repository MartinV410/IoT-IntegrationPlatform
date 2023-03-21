import {MdBluetoothSearching, MdCellTower} from "react-icons/md";
import {SiWire} from "react-icons/si";
import {AiOutlineHome} from "react-icons/ai";
import ProtocolPage from "./components/pages/ProtocolPage";
import {GiFogLight} from "react-icons/gi";
import Home from "./components/pages/Home";

export const ROUTES = [
    {
        path: "/",
        name: "Home",
        icon: <AiOutlineHome className={"route-icon"} />,
        component: <Home />
    },
    {
        path: "/onewire",
        name: "1-Wire",
        icon: <SiWire className={"route-icon"} />,
        component: <ProtocolPage protocol={"1-Wire"} endpoint={"onewire/"} text={"Is a serial protocol using a single data line plus ground reference for communication. A 1-Wire master initiates and controls the communication with one or more 1-Wire slave devices on the 1-Wire bus."} />
    },
    {
        path: "/bluetooth",
        name: "Bluetooth",
        icon: <MdBluetoothSearching className={"route-icon"} />,
        component: <ProtocolPage protocol={"Bluetooth"} endpoint={"bluetooth/"} websocketPort={5022} text={"Is a short-range wireless technology standard that is used for exchanging data between fixed and mobile devices over short distances and building personal area networks (PANs)."}/>
    },
    {
        path: "/nbiot",
        name: "NB-IoT",
        icon: <MdCellTower className={"route-icon"} />,
        component: <ProtocolPage protocol={"NB-IoT"} endpoint={"nbiot/"}  text={"Narrowband IoT is a wireless IoT protocol using low-power wide area network (LPWAN) technology. It was developed by 3GPP for cellular wireless communication that enables a wide range of new NB-IoT devices and services"} timeout={60000}/>
    },
    {
        path: "/dmx",
        name: "DMX",
        icon: <GiFogLight className={"route-icon"} />,
        component: <ProtocolPage protocol={"DMX"} endpoint={"dmx/"}  text={"A standard for digital communication networks that are commonly used to control lighting and effects. It quickly became the primary method for linking controllers to dimmers and special effects devices such as fog machines and intelligent lights. "}/>
    },
]