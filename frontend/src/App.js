import "./App.css"

import CreateRoomPage from "./pages/CreateRoomPage"
import HomePage from "./pages/HomePage"
import JoinRoomPage from "./pages/JoinRoomPage"
import RoomPage from "./pages/RoomPage"
import HandleSpotifyRedirect from "./components/HandleSpotifyRedirect"

import { BrowserRouter, Routes, Route } from "react-router-dom"

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreateRoomPage />} />
          <Route path="/join" element={<JoinRoomPage />} />
          <Route path="/room/:roomCode" element={<RoomPage />} />
          <Route
            path="/handle-spotify-code"
            element={<HandleSpotifyRedirect />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
