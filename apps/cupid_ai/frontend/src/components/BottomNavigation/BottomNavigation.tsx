import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Groups2Icon from "@mui/icons-material/Groups2";
import PersonIcon from "@mui/icons-material/Person";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { isLocalhost, PATHS } from "../../utils";
import { BottomNavigationFilterButton } from "./BottomNavigationFilterButton";
import { useAuth } from "../../utils/contexts/AuthContext";
import { BottomNavigationMatchButtons } from "./BottomNavigationMatchButtons";

const FloatNavigation: React.FC<{ currentPath: string }> = ({
  currentPath,
}) => {
  switch (currentPath) {
    case PATHS.MATCHES:
      return <BottomNavigationFilterButton />;
    case PATHS.PROFILE:
      return <BottomNavigationMatchButtons />;
    default:
      return null;
  }
};

export const BottomNavigation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const auth = useAuth();

  if (!auth.user && !isLocalhost) return null;

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="fixed" color="primary" sx={{ top: "auto", bottom: 0 }}>
        <Toolbar className="mx-3 flex justify-around">
          <Link to={PATHS.MATCHES}>
            <IconButton color="inherit" aria-label="Matches">
              <Typography>
                <Groups2Icon />
                <br /> Matches
              </Typography>
            </IconButton>
          </Link>
          <Box marginTop={-12}>
            <FloatNavigation currentPath={location.pathname} />
          </Box>
          <Link to={PATHS.PROFILE}>
            <IconButton color="inherit" aria-label="Me">
              <Typography>
                <PersonIcon />
                <br />
                Me
              </Typography>
            </IconButton>
          </Link>
        </Toolbar>
      </AppBar>
    </Box>
  );
};
