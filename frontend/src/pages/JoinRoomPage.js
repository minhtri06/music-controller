import React, { useState, useEffect } from "react"

import { Grid, Typography, TextField, Button } from "@mui/material"

import { Link, useNavigate } from "react-router-dom"

const JoinRoomPage = () => {
  let [roomCode, setRoomCode] = useState([])
  let [error, setError] = useState([])
  const navigate = useNavigate()

  const handleRoomCodeChange = (value) => {
    setRoomCode(value)
  }

  const handleJoinRoomClick = async () => {
    if (roomCode === "") {
      setError({
        isError: true,
        message: "Room code is empty",
      })
      return
    }

    let response = await fetch(`/api/${roomCode}/join/`, {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: roomCode,
      }),
      credentials: "include",
    })

    if (response.ok) {
      navigate(`/room/${roomCode}`)
    } else {
      setError({
        isError: true,
        message: "Not found",
      })
    }
  }

  useEffect(() => {
    setRoomCode("")
    setError({
      isError: false,
      message: "",
    })
  }, [])

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography variant="h4" component="h4">
          Join a Room
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <TextField
          label="Room Code"
          value={roomCode ?? ""}
          error={error.isError ?? true}
          helperText={error.message}
          onChange={(e) => handleRoomCodeChange(e.target.value)}
        />
      </Grid>
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => handleJoinRoomClick()}
        >
          Join Room
        </Button>
        <Button
          variant="contained"
          color="secondary"
          to="/"
          component={Link}
          style={{ marginLeft: "12px" }}
        >
          Back
        </Button>
      </Grid>
    </Grid>
  )
}

export default JoinRoomPage
