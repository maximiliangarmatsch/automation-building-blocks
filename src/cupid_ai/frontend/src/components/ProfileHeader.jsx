import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";

const styles = {
  header: {
    backgroundColor: "#e91e63",
    color: "white",
    padding: "16px",
    borderRadius: "0 0 16px 16px",
  },
  mainInfo: {
    fontWeight: "bold",
    marginBottom: "8px",
  },
  detailsContainer: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    alignItems: { xs: "flex-start", sm: "flex-end" },
  },
};

const ProfileHeader = ({ user }) => {
  const formatMainInfo = () => {
    return `${user.gender[0]}${user.age}, ${user.occupation}, ${user.languages}, ${user.distance}, ${user.relationship}`;
  };

  return (
    <Box sx={styles.header}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={7}>
          <Typography variant="h6" component="h1" sx={styles.mainInfo}>
            {formatMainInfo()}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={5}>
          <Box sx={styles.detailsContainer}>
            <Typography variant="body2">
              {`${user.attractiveness} - ${user.height} - ${user.weight}`}
            </Typography>
            <Typography variant="body2">
              {`${user.hairColor} (${user.hairLength}, ${user.hairStyle})`}
            </Typography>
            <Typography variant="body2">{`${user.eyeColor} eyes`}</Typography>
            <Typography variant="body2">{`Body-Shape: ${user.bodyShape}`}</Typography>
          </Box>
        </Grid>
      </Grid>
      <Typography variant="body2" sx={{ marginTop: "8px" }}>
        Chat-Date on {user.chatDate}
      </Typography>
    </Box>
  );
};

export default ProfileHeader;
