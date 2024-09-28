import {List, ListItemButton,ListItemText}  from "@mui/material";
import MatchesSort from "./matches_sort";

export const Matches = (props: any) => {
  const {data} = props;
  return (
    <>
      <MatchesSort />
      <List
        sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
        component="nav"
        aria-labelledby="nested-list-subheader"
      >
        {data.map(match => 
          <ListItemButton key={match.title}>
            <ListItemText primary={match.title} secondary={match.message} />
          </ListItemButton>
        )}
      </List>
    </>
  );
};
