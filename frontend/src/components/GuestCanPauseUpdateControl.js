import React from "react"
import {
  FormControl,
  FormHelperText,
  RadioGroup,
  FormControlLabel,
  Radio,
} from "@mui/material"

const GuestCanPauseUpdateControl = ({ guestCanPause, changeGuestCanPause }) => {
  return (
    <FormControl>
      <FormHelperText>Guest Control Of Playback State</FormHelperText>
      <RadioGroup
        row
        value={guestCanPause ?? ""}
        onChange={(e) => changeGuestCanPause(e.target.value)}
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
  )
}

export default GuestCanPauseUpdateControl
