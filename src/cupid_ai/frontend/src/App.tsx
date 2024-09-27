import { BrowserRouter, Routes, Route } from "react-router-dom";
import { PATHS } from "./utils";
import { Profile } from "./pages/profile";
import { Matches } from "./pages/matches";
import { BottomNavigation } from "./components/BottomNavigation";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path={PATHS.PROFILE} element={<Profile />} />
          <Route path={PATHS.MATCHES} element={<Matches />} />
        </Routes>
        <BottomNavigation />
      </BrowserRouter>
    </div>
  );
}

export default App;
