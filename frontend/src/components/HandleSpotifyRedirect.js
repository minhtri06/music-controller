import React from "react"
import { useSearchParams, useNavigate } from "react-router-dom"

const HandleSpotifyRedirect = () => {
  let [searchParams] = useSearchParams()
  const navigate = useNavigate()

  let code = searchParams.get("code")

  const sendCode = async () => {
    const response = await fetch("/api/spotify/handle-redirect/", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: code,
      }),
      credentials: "include",
    })
    let responseData = await response.json()
    console.log(responseData)

    navigate(`/room/${responseData.room_code}`)
  }

  sendCode()

  return <div>HandleSpotifyRedirect</div>
}

export default HandleSpotifyRedirect
