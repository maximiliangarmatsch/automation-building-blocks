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
import { MockUser } from "../data/MockUser";
import { useAuth } from "../utils/contexts/AuthContext";

export const Profile = () => {
  // eslint-disable-next-line
  const [editMode, setEditMode] = useState(false);
  const user = MockUser;

  const auth = useAuth();
  const user1 = auth?.user;
  console.log(user1);

  return (
    <>
      <ProfileHeader user={user} />
      <Grid container spacing={2} sx={{ padding: 2 }}>
        <Grid size={12}>
          <BasicInformation user={user} editMode={editMode} />
          <GeneralQuestions user={user} editMode={editMode} />
          <SpecificQuestions user={user} editMode={editMode} />
          <TheirQuestions user={user} editMode={editMode} />
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

  // If the dataPoint is a question, we want to display the question and answer
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

  // If the dataPoint is a dataPoint, we want to display the label and value
  return (
    <ListItem key={dataPoint.name} secondaryAction={secondaryAction}>
      <ListItemText primary={dataPoint.label} secondary={dataPoint.value} />
    </ListItem>
  );
};

const BasicInformation = ({ user, editMode }) => {
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
              "location",
              "occupation",
              "living_situation",
              "living_mates",
              "smoking",
              "drinking",
            ].includes(dataPoint.name)
          ).map((dataPoint) =>
            generateListItem({
              dataPoint,
              value: user[dataPoint.name],
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

export const GeneralQuestions = ({ user, editMode }) => {
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
          {user.generalQuestions.map((question) =>
            generateListItem({
              dataPoint: question,
              value: question.answer,
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

export const SpecificQuestions = ({ user, editMode }) => {
  return (
    <Accordion>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel4-content"
        id="panel4-header"
      >
        Questions for {user.gender[0]}
        {user.age}-{user.occupation}
      </AccordionSummary>
      <AccordionDetails>
        <List>
          {user.specificQuestions.map((question) =>
            generateListItem({
              dataPoint: question,
              value: question.answer,
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

export const TheirQuestions = ({ user, editMode }) => {
  return (
    <Accordion>
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel5-content"
        id="panel5-header"
      >
        Questions for you
      </AccordionSummary>
      <AccordionDetails>
        <List>
          {user.theirQuestions.map((question) =>
            generateListItem({
              dataPoint: question,
              value: question.answer,
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};

const PartnershipPreferences = ({ user, editMode }) => {
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
              "familyPlanning",
              "kidsWanted",
              "pets",
              "livingPreference",
              "wealthSplitting",
              "effortSplitting",
              "religion",
              "politics",
              "existingFamilyStructure",
              "retirementPlans",
              "workingHours",
              "otherCommitments",
            ].includes(dataPoint.name)
          ).map((dataPoint) =>
            generateListItem({
              dataPoint: dataPoint,
              value: user[dataPoint.name],
              editMode,
            })
          )}
        </List>
      </AccordionDetails>
    </Accordion>
  );
};
