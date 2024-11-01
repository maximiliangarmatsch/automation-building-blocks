import { List, ListItemButton, ListItemText } from "@mui/material";
import MatchesSort from "../components/MatchesSort";
import { PATHS } from "../utils";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import api, { API_ENDPOINTS } from "../services/api";
import { useAuth } from "../utils/contexts/AuthContext";

export const Matches = () => {
  const [profiles, setProfiles] = useState([]);
  const navigate = useNavigate();

  const handleNavigate = (userId) => {
    navigate(PATHS.PROFILE);
  };

  const auth = useAuth();

  useEffect(() => {
    const fetchMatches = async () => {};
    if (auth?.uniqueID) {
      const response = api.post(API_ENDPOINTS.GET_MATCHES, {
        unique_id: auth.uniqueID,
      });
      console.log(response);
    }
    fetchMatches();
  });

  const data = [
    { title: "welcome", id: "welcome", message: "this is the message" },
  ];

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
