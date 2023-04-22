import React, { useState, useEffect } from "react"

import {
    Grid,
    Typography,
    Card,
    IconButton,
    LinearProgress,
} from "@mui/material"
import PlayArrowRoundedIcon from "@mui/icons-material/PlayArrowRounded"
import PauseCircleOutlineRoundedIcon from "@mui/icons-material/PauseCircleOutlineRounded"
import SkipNextRoundedIcon from "@mui/icons-material/SkipNextRounded"

const MusicPlayer = () => {
    let [song, setSong] = useState({})
    const songProgress = (song.progress / song.duration) * 100

    const playSong = async () => {
        await fetch("/api/spotify/play-song/", {
            method: "put",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
        })
    }

    const pauseSong = async () => {
        let response = await fetch("/api/spotify/pause-song/", {
            method: "put",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
        })
        console.log(await response.status)
    }

    const forwardSong = async () => {
        await fetch("/api/spotify/forward-song/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
        })
    }

    useEffect(() => {
        const fetchCurrentSong = async () => {
            let response = await fetch("/api/spotify/get-current-song/")

            if (response.status !== 200) {
                console.log("can not get the song")
                return
            } else {
                console.log("got the song")
                setSong(await response.json())
            }
        }

        let interval = setInterval(fetchCurrentSong, 1000)
        return () => clearInterval(interval)
    })

    return (
        <Card>
            <Grid container alignItems="center">
                <Grid item align="center" xs={4}>
                    <img
                        src={song.image_url}
                        height="100%"
                        width="100%"
                        alt=""
                    />
                </Grid>

                <Grid item align="center" xs={8}>
                    <Typography component="h5" variant="h5">
                        {song.title}
                    </Typography>

                    <Typography color="textSecondary" variant="subtitle1">
                        {song.artist}
                    </Typography>

                    <div>
                        <IconButton
                            onClick={() => {
                                song.is_playing ? pauseSong() : playSong()
                            }}
                        >
                            {song.is_playing ? (
                                <PauseCircleOutlineRoundedIcon />
                            ) : (
                                <PlayArrowRoundedIcon />
                            )}
                        </IconButton>

                        <IconButton onClick={() => forwardSong()}>
                            <SkipNextRoundedIcon />
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress} />
        </Card>
    )
}

export default MusicPlayer
