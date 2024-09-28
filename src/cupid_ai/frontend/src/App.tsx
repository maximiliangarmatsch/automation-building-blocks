import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Container } from "@mui/material";
import { PATHS } from "./utils";
import { Profile } from "./pages/profile";
import { Matches } from "./pages/matches";
import { BottomNavigation } from "./components/BottomNavigation";
import { TopNavigation } from "./components/TopNavigation";

function App() {
  const matchesData = [
    {
      title: "24yo | Bartender | Berlin",
      message: "Chat-Date on Friday at 18:30, 29.09.2024",
    },
  ];

  return (
    <BrowserRouter>
      <TopNavigation />
      <Container maxWidth="sm">
        <Routes>
          <Route path={PATHS.PROFILE} element={<Profile />} />
          <Route
            path={PATHS.MATCHES}
            element={<Matches data={matchesData} />}
          />
        </Routes>
      </Container>
      <BottomNavigation />
    </BrowserRouter>
  );
}

export default App;
