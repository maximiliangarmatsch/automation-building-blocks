import Box from "@mui/material/Box";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import ScheduledDatePicker from "../ScheduleDatePicker";
import { CustomModal } from "../CustomModal";

interface ScheduleModalProps {
  onClose: () => void;
  open: boolean;
}

export function ScheduleModal({ onClose, open }: ScheduleModalProps) {
  const availableDates = [
    { date: "2024-12-04", startTime: "10:00", endTime: "16:00" },
    { date: "2024-12-05", startTime: "16:00", endTime: "21:00" },
  ];

  return (
    <CustomModal
      open={open}
      onClose={onClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <>
        <Typography
          id="modal-modal-title"
          variant="h6"
          component="h1"
          sx={{ mb: 2 }}
        >
          Schedule a Date
        </Typography>
        <Box marginBottom={2}>
          <Typography variant="subtitle1" component="h2">
            Her Dating Availability
          </Typography>
          <List>
            {availableDates?.map((availableDate) => (
              <Typography key={availableDate.date}>
                {availableDate.date}: {availableDate.startTime} -{" "}
                {availableDate.endTime}
              </Typography>
            ))}
          </List>
        </Box>

        <ScheduledDatePicker availableDates={availableDates} />
      </>
    </CustomModal>
  );
}
