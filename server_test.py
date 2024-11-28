from flask import Flask
from flask import render_template
from flask import url_for
from flask import request


import asyncio

# app = Flask(__name__)

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from aiortc.rtcrtpsender import RTCRtpSender
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from schemas import Offer

from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse


pcs = set()

app = FastAPI()



app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('video.html', {"request": request})



@app.post("/offer")
async def offer(params: Offer):

    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()

    pcs.add(pc)



    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)


    player = MediaPlayer("1109668_Stairs_Standard_1280x720.mp4")

    # player2 = MediaPlayer("1109668_Stairs_Standard_1280x720.mp4")
    # pc.addTrack(player.video)

    # player2 = MediaPlayer('rtsp://rtspstream:853f25dc3a217ea0fa5aec30e90d45d7@zephyr.rtsp.stream/pattern')

    pc.addTrack(player.video)

    # pc.addTrack(player2.video)


    await pc.setRemoteDescription(offer)

    # print('&&&&&&&&#########################################3')

    answer = await pc.createAnswer()

    # print(answer)

    # print('============================')
    await pc.setLocalDescription(answer)


    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')


    # print(pc.localDescription.sdp)
    # print(pc.localDescription.type)


    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}



# @app.route("/")
# def index():
#     return render_template("video.html")


# @app.route("/offer", methods=["POST"])
# async def offer():

#     params = request.json

#     # print(params)
#     offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

#     pc = RTCPeerConnection()

#     @pc.on("connectionstatechange")
#     async def on_connectionstatechange():
#         print("Connection state is %s" % pc.connectionState)
#         if pc.connectionState == "failed":
#             await pc.close()


#     player = MediaPlayer("1109668_Stairs_Standard_1280x720.mp4")

#     pc.addTrack(player.video)

#     # force_codec(pc, video_sender, 'video/H264')

#     await pc.setRemoteDescription(offer)

#     answer = await pc.createAnswer()
#     await pc.setLocalDescription(answer)

#     print('================')
#     print(pc.iceConnectionState)
#     print('================')

#     return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}





# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     app.run(host='0.0.0.0', port=8080, debug=True)