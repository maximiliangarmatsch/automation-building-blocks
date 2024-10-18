import { useState } from "react";
import Fab from "@mui/material/Fab";
import FilterListIcon from "@mui/icons-material/FilterList";
import { FilterModal } from "./FilterModal";

export function BottomNavigationFilterButton() {
  const [open, setOpen] = useState(false);

  const onOpen = () => {
    setOpen(true);
  };

  const onClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Fab
        color="primary"
        aria-label="add"
        onClick={onOpen}
        sx={{
          position: "absolute",
          zIndex: 9999,
          transform: "translateY(-50%)",
          left: 0,
          right: 0,
          margin: "0 auto",
        }}
      >
        <FilterListIcon />
      </Fab>

      <FilterModal onClose={onClose} open={open} />
    </>
  );
}
