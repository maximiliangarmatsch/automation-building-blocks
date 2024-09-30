import React, { useState } from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Groups2Icon from "@mui/icons-material/Groups2";
import PersonIcon from "@mui/icons-material/Person";
import { Box, Typography } from "@mui/material";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { isLocalhost, PATHS } from "../../utils";
import { BottomNavigationFilterButton } from "./BottomNavigationFilterButton";
import { useAuth } from "../../contexts/AuthContext";

export function FloatNavigation(props: any) {
  const { currentPath } = props;

  switch (currentPath) {
    case PATHS.MATCHES:
      return <BottomNavigationFilterButton />;
      break;
    case PATHS.PROFILE:
      return <BottomNavigationFilterButton />;
      break;
    default:
      return null;
      break;
  }
}

export function BottomNavigation() {
  const location = useLocation();
  const navigate = useNavigate();
  const auth = useAuth();

  if (!auth?.uniqueID && !isLocalhost) return null;

  return (
    <React.Fragment>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar
          position="fixed"
          color="primary"
          sx={{ top: "auto", bottom: 0 }}
        >
          <Toolbar className="mx-3 flex justify-around">
            <Link to={PATHS.MATCHES} onClick={() => navigate(PATHS.MATCHES)}>
              <IconButton color="inherit" aria-label="Matches">
                <Typography>
                  <Groups2Icon />
                  <br /> Matches
                </Typography>
              </IconButton>
            </Link>
            <FloatNavigation currentPath={location.pathname} />
            <Link to={PATHS.PROFILE} onClick={() => navigate(PATHS.PROFILE)}>
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
    </React.Fragment>
  );
}
