import React, {useState} from "react";
import { Fab, Typography} from "@mui/material";
import FilterListIcon from '@mui/icons-material/FilterList';

export function BottomNavigation_FabButton() {

  const handleFabClick = () => {
    // Add your logic for Fab button click here
    console.log("Fab button clicked");
  };

    return (
      <Fab color="primary" aria-label="add" 
      onClick={handleFabClick}
      sx={{
        position: 'absolute',
        zIndex: 9999,
        top: -40,
        left: 0,
        right: 0,
        margin: '0 auto',
      }} >
          <FilterListIcon />
        </Fab>
  );
}
