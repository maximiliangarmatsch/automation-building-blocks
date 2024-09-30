import {
  Box,
  TextField,
  Typography,
  Paper,
  FormControl,
  RadioGroup,
  Radio,
  FormControlLabel,
} from "@mui/material";
import Modal from "@mui/material/Modal";
import Grid from "@mui/material/Grid2";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export function RejectUserModal(props: any) {
  const { onClose, onOpen, open } = props;

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
            Reject User
          </Typography>

          {/* Just old trash */}
          {/* <Grid container spacing={2}>
            <Grid size={12}>
              <Paper elevation={2}>
                <Typography variant="h6">Gender</Typography>
                <FormControl>
                  <RadioGroup
                    row
                    aria-labelledby="demo-row-radio-buttons-group-label"
                    name="row-radio-buttons-group"
                  >
                    <FormControlLabel
                      value="female"
                      control={<Radio />}
                      label="Female"
                    />
                    <FormControlLabel
                      value="male"
                      control={<Radio />}
                      label="Male"
                    />
                  </RadioGroup>
                </FormControl>
              </Paper>
            </Grid>

            <Grid size={12}>
              <Paper elevation={2}>
                <Typography variant="h6">Age</Typography>
                <Box display="flex" flexDirection="row" gap={0}>
                  <FormControlLabel
                    control={<TextField size="small" sx={{ width: "60px" }} />}
                    label=" To"
                  />
                  <FormControlLabel
                    control={<TextField size="small" sx={{ width: "60px" }} />}
                    label=""
                  />
                </Box>
              </Paper>
            </Grid>

            <Grid size={12}>
              <Paper elevation={2}>
                <Typography variant="h6">Distance (km)</Typography>
                <Box display="flex" flexDirection="row" gap={0}>
                  <FormControlLabel
                    control={<TextField size="small" sx={{ width: "80px" }} />}
                    label=""
                  />
                </Box>
              </Paper>
            </Grid>
          </Grid> */}
        </Box>
      </Modal>
    </>
  );
}
