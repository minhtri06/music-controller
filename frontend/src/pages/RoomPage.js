import React, { useState, useEffect } from "react"

import { useParams, useNavigate } from "react-router-dom"

import { Grid, Typography, Button, ButtonGroup } from "@mui/material"

import GuestCanPauseUpdateControl from "../components/GuestCanPauseUpdateControl"
import VotesToSkipUpdateControl from "../components/VotesToSkipUpdateControl"
import MusicPlayer from "../components/MusicPlayer"

const RoomPage = () => {
    let [room, setRoom] = useState(null)
    let [isUpdate, setIsUpdate] = useState(false)

    const { roomCode } = useParams()
    const navigate = useNavigate()

    const changeVotesToSkip = (value) => {
        setRoom({ ...room, votesToSkip: value })
    }

    const changeGuestCanPause = (value) => {
        setRoom({ ...room, guestCanPause: value })
    }

    const toggleIsUpdate = () => {
        setIsUpdate(!isUpdate)
    }

    const updateRoom = async () => {
        if (room.isHost === false) {
            return
        }

        let response = await fetch(`http://localhost:8000/api/${roomCode}/`, {
            method: "patch",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                votes_to_skip: room.votesToSkip,
                guest_can_pause: room.guestCanPause,
            }),
            credentials: "include",
        })
        return response.ok
    }

    const handleLeaveRoomBtnOnClick = async () => {
        await fetch("/api/room/leave-room/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
        }).then((_) => navigate("/"))
    }

    const handleModifyRoomOnClick = () => {
        if (isUpdate) {
            const isOk = updateRoom()

            if (isOk) {
                toggleIsUpdate()
            } else {
                console.log("update error")
            }
        } else {
            toggleIsUpdate()
        }
    }

    const getSpotifyAuthenticate = async () => {
        let response = await fetch("/api/spotify/get-auth-url/", {
            credentials: "include",
        })

        let url = (await response.json()).url
        console.log(url)
        window.location.replace(url)
    }

    useEffect(() => {
        const refreshSpotifyToken = async () => {
            let response = await fetch(
                `http://localhost:8000/api/spotify/refresh-token/${roomCode}/`,
                {
                    method: "patch",
                    credentials: "include",
                }
            )
            console.log(await response.json())
        }

        const getRoom = async () => {
            const response = await fetch(
                `http://localhost:8000/api/${roomCode}/`,
                {
                    credentials: "include",
                }
            )

            if (response.ok === false) {
                console.log(await response.json())
                navigate("/")
            }

            const data = await response.json()
            console.log("data", data)

            setRoom({
                code: data.code,
                createdAt: data.created_at,
                guestCanPause: data.guest_can_pause,
                host: data.host,
                id: data.id,
                isHost: data.is_host,
                votesToSkip: data.votes_to_skip,
                spotifyToken: data.spotify_token,
            })

            if (data.spotify_token == null) {
                getSpotifyAuthenticate()
            } else {
                refreshSpotifyToken()
            }
        }

        getRoom()
    }, [navigate, roomCode])

    return (
        <Grid container spacing={1} justifyContent="center" alignItems="center">
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Code: {room?.code}
                </Typography>
            </Grid>

            {isUpdate ? (
                <>
                    <Grid item xs={12} align="center">
                        <VotesToSkipUpdateControl
                            votesToSkip={room.votesToSkip}
                            changeVotesToSkip={changeVotesToSkip}
                        />
                    </Grid>

                    <Grid item xs={12} align="center">
                        <GuestCanPauseUpdateControl
                            guestCanPause={room?.guestCanPause}
                            changeGuestCanPause={changeGuestCanPause}
                        />
                    </Grid>
                </>
            ) : (
                <Grid item xs={6} align="center">
                    <MusicPlayer />
                </Grid>
            )}

            <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    {room?.isHost ? "HOST" : "GUEST"}
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <ButtonGroup variant="contained" color="primary">
                    {room?.isHost && (
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => handleModifyRoomOnClick()}
                        >
                            Modify Room
                        </Button>
                    )}
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={() => handleLeaveRoomBtnOnClick()}
                    >
                        Leave Room
                    </Button>
                </ButtonGroup>
            </Grid>
        </Grid>
    )
}

export default RoomPage
