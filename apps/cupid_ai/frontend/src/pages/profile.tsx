import { useState } from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Grid from "@mui/material/Grid2";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import { UserDataPoints } from "../data/UserDataPoints";
import ProfileHeader from "../components/ProfileHeader";
import { useAuth } from "../utils/contexts/AuthContext";

export const Profile = () => {
  const [editMode, setEditMode] = useState(false);
  const auth = useAuth();
  const user = auth?.user;

  if (!user) {
    return null;
  }

  return (
    <>
      <ProfileHeader user={user} />
      <Grid container spacing={2} sx={{ padding: 2 }}>
        <Grid size={12}>
          <BasicInformation user={user} editMode={editMode} />
          <GeneralQuestions user={user} editMode={editMode} />
          <PartnershipPreferences user={user} editMode={editMode} />
        </Grid>
      </Grid>
    </>
  );
};

const generateListItem = ({ dataPoint, value, editMode }) => {
  const secondaryAction = !editMode ? (
    <>
      <IconButton edge="end" aria-label="dislike">
        <ThumbDownIcon />
      </IconButton>
      <IconButton edge="end" aria-label="like">
        <ThumbUpIcon />
      </IconButton>
    </>
  ) : null;

  if (dataPoint.question) {
    return (
      <ListItem key={dataPoint.id} secondaryAction={secondaryAction}>
        <ListItemText
          primary={dataPoint.question}
          secondary={dataPoint.answer}
        />
      </ListItem>
    );
  }

  return (
    <ListItem key={dataPoint.name} secondaryAction={secondaryAction}>
      <ListItemText primary={dataPoint.label} secondary={dataPoint.value} />
    </ListItem>
  );
};

const BasicInformation = ({ user, editMode }) => {
  if (!user) {
    return null;
  }

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
        <List>
          {UserDataPoints.filter((dataPoint) =>
            [
              "languages",
              "city",
              "occupation",
              "living_space",
              "living_mates",
              "smoking",
              "drinking",
            ].includes(dataPoint.name)
          ).map((dataPoint) =>
            generateListItem({
              dataPoint,
              value: user[dataPoint.name] || "Not specified",
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

export const GeneralQuestions = ({ user, editMode }) => {
  const questions = user?.user_general_questions || [];

  return (
    <Accordion>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel3-content"
        id="panel3-header"
      >
        General Questions
      </AccordionSummary>
      <AccordionDetails>
        <List>
          {questions.map((question, index) =>
            generateListItem({
              dataPoint: {
                id: index,
                question: "Personal Trait",
                answer: question,
              },
              value: question,
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

export const SpecificQuestions = ({ user, editMode }) => {
  return null;
};

export const TheirQuestions = ({ user, editMode }) => {
  return null;
};

const PartnershipPreferences = ({ user, editMode }) => {
  if (!user) {
    return null;
  }

  return (
    <Accordion>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel3-content"
        id="panel3-header"
      >
        Partnership Experience & Goals
      </AccordionSummary>
      <AccordionDetails>
        <List>
          {UserDataPoints.filter((dataPoint) =>
            [
              "family_planning",
              "kids",
              "pets",
              "living_space",
              "wealth_splitting",
              "effort_splitting",
              "religion",
              "politics",
              "existing_family_structure",
              "retirement",
              "working_hours",
              "other_commitments",
            ].includes(dataPoint.name)
          ).map((dataPoint) =>
            generateListItem({
              dataPoint,
              value: user[dataPoint.name] || "Not specified",
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};
