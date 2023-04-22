import React, { useState, useEffect } from "react"

import { Link, useNavigate } from "react-router-dom"

import {
  Button,
  Grid,
  Typography,
  FormControl,
  FormHelperText,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField,
} from "@mui/material"

const CreateRoomPage = () => {
  let [newRoom, setNewRoom] = useState([])
  const navigate = useNavigate()

  const handleGuestCanPauseChange = (value) => {
    setNewRoom({
      guestCanPause: value === "true" ? true : false,
      votesToSkip: newRoom.votesToSkip,
    })
  }

  const handleVotesChange = (value) => {
    setNewRoom({
      guestCanPause: newRoom.guestCanPause,
      votesToSkip: value,
    })
  }

  const handleCreateRoomOnClick = async () => {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        votes_to_skip: newRoom.votesToSkip,
        guest_can_pause: newRoom.guestCanPause,
      }),
      credentials: "include",
    }

    const response = await fetch("http://localhost:8000/api/", requestOptions)
    const data = await response.json()
    console.log(data)
    if ((await response.status) === 201) {
      navigate(`/room/${data.code}`)
    } else {
      console.log(await data)
    }
  }

  useEffect(() => {
    setNewRoom({
      guestCanPause: true,
      votesToSkip: 2,
    })
  }, [])

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          Create A Room
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <FormHelperText>Guest Control Of Playback State</FormHelperText>
          <RadioGroup
            row
            value={newRoom.guestCanPause ?? ""}
            onChange={(e) => handleGuestCanPauseChange(e.target.value)}
          >
            <FormControlLabel
              value="true"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
            />
            <FormControlLabel
              value="false"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            value={newRoom.votesToSkip ?? ""}
            onChange={(e) => {
              handleVotesChange(e.target.value)
            }}
            inputProps={{
              min: 1,
              style: {
                textAlign: "center",
              },
            }}
          />
          <FormHelperText>Votes Required To Skip Song</FormHelperText>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={() => handleCreateRoomOnClick()}
        >
          Create A Room
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  )
}

export default CreateRoomPage
