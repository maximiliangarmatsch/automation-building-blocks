import { Box, List, ListItemButton, ListItemText } from "@mui/material";
import MatchesSort from "../components/MatchesSort";
import { PATHS } from "../utils";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import api, { API_ENDPOINTS } from "../services/api";
import { useAuth } from "../utils/contexts/AuthContext";
import { Match } from "../components/Match";

export const Matches = () => {
  const [profiles, setProfiles] = useState<Array<Record<any, any>>>([]);
  const navigate = useNavigate();

  const handleNavigate = (profileId) => {
    navigate(`${PATHS.PROFILE}/${profileId}`);
  };

  const auth = useAuth();

  useEffect(() => {
    const fetchMatches = async () => {
      if (auth?.uniqueID) {
        const response = await api.post(API_ENDPOINTS.GET_MATCHES, {
          unique_id: auth.uniqueID,
        });

        if (response.data?.profiles && response.data.profiles?.length > 0) {
          setProfiles(response.data.profiles);
        }
      }
    };

    fetchMatches();
  }, []);

  console.log("proiles: ", profiles);

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
        {profiles.map((profile) => (
          <ListItemButton
            key={profile?.unique_id}
            onClick={() => {
              handleNavigate(profile.unique_id);
            }}
          >
            <Match profile={profile} />
          </ListItemButton>
        ))}
      </List>
    </>
  );
};
