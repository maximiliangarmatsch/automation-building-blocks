import * as React from "react";
import { useState } from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import {
  IconButton,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import Grid from "@mui/material/Grid2";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import { UserDataPoints } from "../data/UserDataPoints";

const generateListItem = ({ dataPoint, value, editMode }) => {
  const secondaryAction = editMode ? (
    <>
      <IconButton edge="end" aria-label="dislike">
        <ThumbDownIcon />
      </IconButton>
      <IconButton edge="end" aria-label="like">
        <ThumbUpIcon />
      </IconButton>
    </>
  ) : null;

  return (
    <ListItem key={dataPoint.name} secondaryAction={secondaryAction}>
      <ListItemText primary={dataPoint.label} secondary={value} />
    </ListItem>
  );
};

const YourFilters = ({ editMode }) => {
  return (
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
          W, 23-34, German/English, &lt;50km, Relationship/Family,
          Kids-Maybe/Kids-Soon/Kids-Never
        </Typography>
      </AccordionDetails>
    </Accordion>
  );
};

const BasicInformation = ({ editMode }) => {
  return (
    <Accordion>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel1-content"
        id="panel1-header"
      >
        Basic Information
      </AccordionSummary>
      <AccordionDetails>
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

        <List>
          {UserDataPoints.filter((dataPoint) =>
            [
              "gender",
              "age",
              "languages",
              "location",
              "occupation",
              "living_situation",
              "living_mates",
              "kids_wanted",
              "smoking",
              "drinking",
            ].includes(dataPoint.name)
          ).map((dataPoint) =>
            generateListItem({ dataPoint, value: "Sample Value", editMode })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

const Physique = ({ editMode }) => {
  return (
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
          {UserDataPoints.filter((dataPoint) =>
            [
              "height",
              "weight",
              "hair_length",
              "hair_color",
              "hair_style",
              "eye_color",
            ].includes(dataPoint.name)
          ).map((dataPoint) =>
            generateListItem({ dataPoint, value: "Sample Value", editMode })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

export const QuestionsForYourPartner = ({ editMode }) => {
  return (
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
              secondary={<Typography>[Text Area, 1-1000 words]</Typography>}
            />
          </ListItem>
        </List>
        <List>
          <ListItem>
            <ListItemText
              primary="Do you have Dept?"
              secondary={<Typography>[Text Area, 1-1000 words]</Typography>}
            />
          </ListItem>
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

const FacialFeatures = ({ editMode }) => {
  return (
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
  );
};

const Wealth = ({ editMode }) => {
  return (
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
  );
};

const PartnershipGoals = ({ editMode }) => {
  return (
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
  );
};

export const Profile = () => {
  const [editMode, setEditMode] = useState(true);

  return (
    <>
      <Typography variant="h3">Your Profile</Typography>
      <Grid container spacing={2} sx={{ padding: 2 }}>
        <Grid size={12}>
          <YourFilters editMode={editMode} />
          <BasicInformation editMode={editMode} />
          <Physique editMode={editMode} />
          <QuestionsForYourPartner editMode={editMode} />
          <FacialFeatures editMode={editMode} />
          <Wealth editMode={editMode} />
          <PartnershipGoals editMode={editMode} />
        </Grid>
      </Grid>
    </>
  );
};
