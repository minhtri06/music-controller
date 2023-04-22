import React, { useEffect } from "react"

import { Grid, Typography, ButtonGroup, Button } from "@mui/material"

import { Link, useNavigate } from "react-router-dom"

const HomePage = () => {
  const navigate = useNavigate()

  useEffect(() => {
    const getRoomCode = async () => {
      let response = await fetch("/api/room/get-room-code/", {
        credentials: "include",
      })

      let data = await response.json()

      if ((await data.room_code) !== null) {
        navigate(`/room/${await data.room_code}`)
      }
    }

    getRoomCode()
  })

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
        <Typography variant="h3" component="h3">
          House Party
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <ButtonGroup variant="contained" color="primary">
          <Button color="primary" to="/join" component={Link}>
            Join a Room
          </Button>
          <Button color="secondary" to="/create" component={Link}>
            Create a Room
          </Button>
        </ButtonGroup>
      </Grid>
    </Grid>
  )
}

export default HomePage
