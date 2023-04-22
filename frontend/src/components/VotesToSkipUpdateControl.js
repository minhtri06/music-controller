import React from "react"

import { FormControl, TextField, FormHelperText } from "@mui/material"

const VotesToSkipUpdateControl = ({ votesToSkip, changeVotesToSkip }) => {
    return (
        <FormControl>
            <TextField
                required={true}
                type="number"
                value={votesToSkip}
                onChange={(e) => {
                    changeVotesToSkip(e.target.value)
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
    )
}

export default VotesToSkipUpdateControl
