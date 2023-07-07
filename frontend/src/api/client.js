import axios from "axios"


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

export const server_ip = window.location.hostname
// export const server_ip = "192.168.88.209"
const addr = `http://${server_ip}:8000/`
export const client = axios.create({
    baseURL: addr,
    timeout: 18000,
    headers: {"Content-Type": "text/plain", 'X-CSRFTOKEN': csrftoken},
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
})
// export const client = axios.create({
//     baseURL: "http://192.168.88.209:8000/",
//     timeout: 1800,
//     headers: {"Content-Type": "application/json", 'X-CSRFToken': csrftoken},
//     credentials: 'include'
// })