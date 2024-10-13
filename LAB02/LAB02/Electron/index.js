const server_addr = "ws://10.0.0.106:65432"; // Update to your server's IP address

const socket = new WebSocket(server_addr);

socket.onopen = function () {
    console.log('Connected to server');
};

socket.onmessage = function (event) {
    const response = JSON.parse(event.data);
    document.getElementById("CPU_temperature").innerText = response.cputemperature;
    document.getElementById("CPU_Usage").innerText = response.cpuusage;
    document.getElementById("GPU_temperature").innerText = response.gputemperature;
    document.getElementById("Battery_Usage").innerText = response.battery;
    document.getElementById("Disk_Usage").innerText = response.Disk;
    document.getElementById("RAM_Usage").innerText = response.RAM;	
    document.getElementById("speed").innerText = response.speed;
    document.getElementById("distance").innerText = response.distance;





};

function moveCar(direction) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(direction);
    } else {
        console.error('WebSocket connection is not open.');
    }
}

function stopCar() {
    moveCar("STOP");
}

