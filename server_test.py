from flask import Flask
from flask import render_template
from flask import url_for
from flask import request


import asyncio

# app = Flask(__name__)

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaStreamTrack
from aiortc.rtcrtpsender import RTCRtpSender
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from schemas import Offer

from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse



relay = MediaRelay()


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()
        return frame

    

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
            print("Connection state is %s" % pc.connectionState)
            await pc.close()
            pcs.discard(pc)


    @pc.on("track")
    def on_track(track):
        print("Track %s received" % track.kind)

        if track.kind == "video":
            pc.addTrack(VideoTransformTrack(relay.subscribe(track), None))

    # player = MediaPlayer("1109668_Stairs_Standard_1280x720.mp4")
    # player = MediaPlayer('rtsp://rtspstream:853f25dc3a217ea0fa5aec30e90d45d7@zephyr.rtsp.stream/pattern')
    # pc.addTrack(player.video)

    

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
