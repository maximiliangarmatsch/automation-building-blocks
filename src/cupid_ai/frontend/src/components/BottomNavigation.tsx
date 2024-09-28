import React, { useState } from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Groups2Icon from "@mui/icons-material/Groups2";
import PersonIcon from "@mui/icons-material/Person";
import { Box, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { PATHS } from "../utils";
import { BottomNavigation_FabButton } from "./BottomNavigation_FabButtons";

export function BottomNavigation() {
  const [currentPath, setCurrentPath] = useState(
    () => window.location.pathname
  );

  return (
    <React.Fragment>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar
          position="fixed"
          color="primary"
          sx={{ top: "auto", bottom: 0 }}
        >
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
                  <Groups2Icon />
                  <br /> Matches
                </Typography>
              </IconButton>
            </Link>
            <BottomNavigation_FabButton />
            <Link
              to={PATHS.PROFILE}
              onClick={() => setCurrentPath(PATHS.PROFILE)}
            >
              <IconButton
                color="inherit"
                disabled={currentPath === PATHS.PROFILE}
              >
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
    </React.Fragment>
  );
}
