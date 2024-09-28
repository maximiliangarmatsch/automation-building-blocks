import * as React from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { List, ListItem, ListItemText, Typography } from "@mui/material";
import Grid from "@mui/material/Grid2";

export const Profile = () => {
  return (
    <>
      <Typography variant="h3">Your Profile</Typography>
      <Grid container spacing={2} style={{ padding: 16 }}>
        <Grid size={12}>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              Your Filters
            </AccordionSummary>
            <AccordionDetails>
              <Typography>
                W, 23-34, German/English, &lt;50km,
                <br />
                Relationship/Family, Kids-Maybe/Kids-Soon/Kids-Never
              </Typography>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              Basic Information
            </AccordionSummary>
            <AccordionDetails>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Your Headline"
                    secondary={
                      <Typography>
                        M38, German/English, Budapest
                        <br />
                        We're looking for the same!
                      </Typography>
                    }
                  />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Gender" secondary="Male" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Age" secondary="38" />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Languages"
                    secondary="German/English"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Location"
                    secondary="District 7, 1077, Budapest, Hungary"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Occupation"
                    secondary="Entrepreneur, Software Developer"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Living Situation"
                    secondary="Personal Apartment"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Living Mates" secondary="None" />
                </ListItem>

                <ListItem>
                  <ListItemText primary="Smoking" secondary="Yes" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Drinking" secondary="Daily" />
                </ListItem>
              </List>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              Physique
            </AccordionSummary>
            <AccordionDetails>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Ai Attractiveness-Score"
                    secondary={<Typography>[Coming soon]</Typography>}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Height" secondary="188cm" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Weight" secondary="80cm" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Hair Length" secondary="Short" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Hair Color" secondary="Brown" />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Hair Style"
                    secondary="10% Hairloss Corners"
                  />
                </ListItem>
              </List>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel3-content"
              id="panel3-header"
            >
              Questions for your Partner
            </AccordionSummary>
            <AccordionDetails>
              <List>
                <ListItem>
                  <ListItemText
                    primary="How many Partners have you had?"
                    secondary={
                      <Typography>[Text Area, 1-1000 words]</Typography>
                    }
                  />
                </ListItem>
              </List>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Do you have Dept?"
                    secondary={
                      <Typography>[Text Area, 1-1000 words]</Typography>
                    }
                  />
                </ListItem>
              </List>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
            >
              [Coming soon] Facial Form Featurs
            </AccordionSummary>
            <AccordionDetails>[Pending]</AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel3-content"
              id="panel3-header"
            >
              [Coming soon] Wealth
            </AccordionSummary>
            <AccordionDetails>[Pending]</AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel3-content"
              id="panel3-header"
            >
              [Coming soon] Partnership Goals (long-term)
            </AccordionSummary>
            <AccordionDetails>[Pending]</AccordionDetails>
          </Accordion>
        </Grid>
      </Grid>
    </>
  );
};
