import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import FormControl from "@mui/material/FormControl";
import RadioGroup from "@mui/material/RadioGroup";
import Radio from "@mui/material/Radio";
import FormControlLabel from "@mui/material/FormControlLabel";
import Grid from "@mui/material/Grid2";
import FormGroup from "@mui/material/FormGroup";
import { CustomModal } from "../CustomModal";

interface FilterModalProps {
  onClose: () => void;
  open: boolean;
}

export function FilterModal(props: FilterModalProps) {
  const { onClose, open } = props;

  return (
    <CustomModal
      open={open}
      onClose={onClose}
      aria-labelledby="filter-modal-title"
      aria-describedby="filter-modal-description"
    >
      <>
        <Typography
          id="filter-modal-title"
          variant="h6"
          component="h2"
          gutterBottom
        >
          Filter your Matches
        </Typography>

        <Grid container spacing={3}>
          <Grid size={12}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Gender
              </Typography>
              <FormControl component="fieldset">
                <RadioGroup row name="gender">
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
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Age
              </Typography>
              <FormGroup row>
                <FormControlLabel
                  control={<TextField size="small" sx={{ width: "80px" }} />}
                  label="From"
                  labelPlacement="start"
                />
                <FormControlLabel
                  control={<TextField size="small" sx={{ width: "80px" }} />}
                  label="To"
                  labelPlacement="start"
                />
              </FormGroup>
            </Paper>
          </Grid>

          <Grid size={12}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Distance (km)
              </Typography>
              <TextField size="small" sx={{ width: "120px" }} />
            </Paper>
          </Grid>
        </Grid>
      </>
    </CustomModal>
  );
}
