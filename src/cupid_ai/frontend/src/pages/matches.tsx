import { List, ListItemButton, ListItemText } from "@mui/material";
import MatchesSort from "./matches_sort";

interface Match {
  title: string;
  message: string;
}

interface MatchesProps {
  data: Match[];
}

export const Matches = ({ data }: MatchesProps) => {
  return (
    <>
      <MatchesSort />
      <List
        sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
        component="nav"
        aria-labelledby="nested-list-subheader"
      >
        {data.map((match) => (
          <ListItemButton key={match.title}>
            <ListItemText primary={match.title} secondary={match.message} />
          </ListItemButton>
        ))}
      </List>
    </>
  );
};
