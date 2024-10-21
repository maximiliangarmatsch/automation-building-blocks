import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";
import Divider from "@mui/material/Divider";
import SettingsIcon from "@mui/icons-material/Settings";
import { useAuth } from "../utils/contexts/AuthContext";

export function TopNavigation() {
  const auth = useAuth();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <React.Fragment>
      <AppBar position="static" color="primary">
        <Toolbar
          className={`flex ${
            auth?.uniqueID ? "justify-between" : "justify-center"
          }`}
        >
          {auth?.uniqueID && (
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={() => {
                // window.history.back();
              }}
            >
              {/* <KeyboardBackspaceIcon /> */}
            </IconButton>
          )}

          <img src="/logo.svg" alt="Cupid AI Logo" />

          {auth?.uniqueID && (
            <>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <SettingsIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={auth.logOut}>
                  <p className="text-red-700">Logout</p>
                </MenuItem>
                <Divider />
                <MenuItem onClick={auth.deleteProfile}>
                  <p className="text-red-700">Delete Profile</p>
                </MenuItem>
              </Menu>
            </>
          )}
        </Toolbar>
      </AppBar>
    </React.Fragment>
  );
}
