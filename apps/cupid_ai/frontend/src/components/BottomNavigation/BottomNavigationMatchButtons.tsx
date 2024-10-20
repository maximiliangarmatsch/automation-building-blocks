import { useState } from "react";
import Fab from "@mui/material/Fab";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import NotInterestedIcon from "@mui/icons-material/NotInterested";
import { ScheduleModal } from "./ScheduleModal";
import { RejectUserModal } from "./RejectUserModal";

export function BottomNavigationMatchButtons() {
  const [openSchedule, setOpenSchedule] = useState(false);
  const [openRejectUser, setOpenRejectUser] = useState(false);

  const onOpenSchedule = () => {
    setOpenSchedule(true);
  };

  const onCloseSchedule = () => {
    setOpenSchedule(false);
  };

  const onOpenRejectUser = () => {
    setOpenRejectUser(true);
  };

  const onCloseRejectUser = () => {
    setOpenRejectUser(false);
  };

  return (
    <>
      <Fab
        color="primary"
        aria-label="add"
        onClick={onOpenRejectUser}
        sx={{
          position: "absolute",
          zIndex: 9999,
          transform: "translateY(-50%)",
          left: 0,
          right: 85,
          margin: "0 auto",
        }}
      >
        <NotInterestedIcon />
      </Fab>
      <Fab
        color="primary"
        aria-label="add"
        onClick={onOpenSchedule}
        sx={{
          position: "absolute",
          zIndex: 9999,
          transform: "translateY(-50%)",
          left: 0,
          right: -85,
          margin: "0 auto",
        }}
      >
        <CalendarMonthIcon />
      </Fab>

      <RejectUserModal onClose={onCloseRejectUser} open={openRejectUser} />
      <ScheduleModal onClose={onCloseSchedule} open={openSchedule} />
    </>
  );
}
