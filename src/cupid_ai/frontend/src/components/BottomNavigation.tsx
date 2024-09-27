import * as React from "react";
import AppBar from "@mui/material/AppBar";
import CssBaseline from "@mui/material/CssBaseline";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Groups2Icon from "@mui/icons-material/Groups2";
import PersonIcon from "@mui/icons-material/Person";
import { Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { PATHS } from "../utils";

export function BottomNavigation() {
  const [currentPath, setCurrentPath] = React.useState(
    () => window.location.pathname
  );

  return (
    <React.Fragment>
      <CssBaseline />
      <AppBar position="fixed" color="primary" sx={{ top: "auto", bottom: 0 }}>
        <Toolbar className="mx-3 flex justify-around">
          <Link
            to={PATHS.MATCHES}
            onClick={() => setCurrentPath(PATHS.MATCHES)}
          >
            <IconButton
              color="inherit"
              aria-label="open drawer"
              disabled={currentPath === PATHS.MATCHES}
            >
              <Typography>
                <Groups2Icon /> <br /> Matches
              </Typography>
            </IconButton>
          </Link>
          <Link
            to={PATHS.PROFILE}
            onClick={() => setCurrentPath(PATHS.PROFILE)}
          >
            <IconButton
              color="inherit"
              disabled={currentPath === PATHS.PROFILE}
            >
              <Typography>
                <PersonIcon /> <br /> Me
              </Typography>
            </IconButton>
          </Link>
        </Toolbar>
      </AppBar>
    </React.Fragment>
  );
}
