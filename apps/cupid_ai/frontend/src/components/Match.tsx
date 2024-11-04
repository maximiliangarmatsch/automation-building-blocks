import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

interface MatchProps {
  profile: any;
}

export const Match = ({ profile }: MatchProps) => {
  return (
    <Box>
      <Typography>Height: {profile.height}</Typography>
      <Typography>Age: {profile.age}</Typography>
    </Box>
  );
};
