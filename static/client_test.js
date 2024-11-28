

var pc = null;

function negotiate() {
    pc.addTransceiver('video', { direction: 'recvonly' });
    pc.addTransceiver('audio', { direction: 'recvonly' });
    return pc.createOffer().then((offer) => {
        return pc.setLocalDescription(offer);
    }).then(() => {
        // wait for ICE gathering to complete
        return new Promise((resolve) => {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                const checkState = () => {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                };
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(() => {
        var offer = pc.localDescription;
        return fetch('/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then((response) => {
        return response.json();
    }).then((answer) => { console.log(answer);
        return pc.setRemoteDescription(answer);
    }).catch((e) => {
        alert(e);
    });
}

function start() {
    var config = {
        sdpSemantics: 'unified-plan'
    };



    pc = new RTCPeerConnection(config);

    // connect audio / video
    // pc.addEventListener('track', (evt) => {
    //     if (evt.track.kind == 'video') {
    //         document.getElementById('video').srcObject = evt.streams[0];
    //     } 
    // });

    pc.addEventListener('track', (evt) => {
            document.getElementById('video').srcObject = evt.streams[0];
    });

    // document.getElementById('start').style.display = 'none';
    negotiate();
    // document.getElementById('stop').style.display = 'inline-block';
}


function get_streams() {
    console.log(pc)
};
// function stop() {
//     document.getElementById('stop').style.display = 'none';

//     // close peer connection
//     setTimeout(() => {
//         pc.close();
//     }, 500);
// }






// console.log('Hello')



// async function  Start() {
//     console.log("From function")

//     var config = {
//         sdpSemantics: 'unified-plan'
//     };

//     pc = new RTCPeerConnection(config);

//     pc.addEventListener('track', (evt) => {
//         if (evt.track.kind == 'video') {
//             document.getElementById('video').srcObject = evt.streams[0];
//         } else {
//             document.getElementById('audio').srcObject = evt.streams[0];
//         }
//     });

//     pc.addTransceiver('video', { direction: 'recvonly' });

//     const offer = await pc.createOffer();
    
//     await pc.setLocalDescription(offer);

//     var complete_offer = pc.localDescription;


//     var responce = await fetch("http://127.0.0.1:5000/offer", {
//         method: "POST",
//         body: JSON.stringify({sdp: complete_offer.sdp, type: complete_offer.type,}),
//         headers: {"Content-type": "application/json; charset=UTF-8"}
//     });

//     answer = await responce.json();


//     pc.setRemoteDescription(answer);

// }