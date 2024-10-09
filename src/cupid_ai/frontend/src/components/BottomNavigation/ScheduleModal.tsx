import Box from "@mui/material/Box";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import ScheduledDatePicker from "../ScheduleDatePicker";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 600,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export function ScheduleModal(props: any) {
  const { onClose, onOpen, open } = props;

  const onSubmit = async () => {};

  const availableDates = [
    { date: "2024-12-04", startTime: "10:00", endTime: "16:00" },
    { date: "2024-12-05", startTime: "16:00", endTime: "21:00" },
  ];

  return (
    <>
      <Modal
        open={open}
        onClose={onClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography
            id="modal-modal-title"
            variant="h6"
            component="h1"
            sx={{ mb: 2 }}
          >
            Schedule a Date
          </Typography>
          <Box marginBottom={2}>
            <Typography>Her Dating Availability</Typography>
            <List>
              {availableDates?.map((availableDate) => (
                <Typography>
                  {availableDate.date}: {availableDate.startTime} -{" "}
                  {availableDate.endTime}
                </Typography>
              ))}
            </List>
          </Box>

          <ScheduledDatePicker availableDates={availableDates} />
        </Box>
      </Modal>
    </>
  );
}
