import { List, ListItemButton, ListItemText } from "@mui/material";
import MatchesSort from "../components/MatchesSort";
import { PATHS } from "../utils";
import { useNavigate } from "react-router-dom";

export const Matches = (props: any) => {
  const navigate = useNavigate();
  const { data } = props;

  const handleNavigate = (userId) => {
    navigate(PATHS.PROFILE);
  };

  return (
    <>
      <MatchesSort />
      <List
        sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
        component="nav"
        aria-labelledby="nested-list-subheader"
      >
        {data.map((match) => (
          <ListItemButton
            key={match.title}
            onClick={() => {
              handleNavigate(match.id);
            }}
          >
            <ListItemText primary={match.title} secondary={match.message} />
          </ListItemButton>
        ))}
      </List>
    </>
  );
};
