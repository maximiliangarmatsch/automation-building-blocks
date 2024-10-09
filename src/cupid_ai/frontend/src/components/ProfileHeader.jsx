import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

const ProfileHeader = ({ user }) => {
  return (
    <Box
      sx={{
        backgroundColor: "#e91e63", // Pink background color
        color: "white",
        padding: "16px",
        borderRadius: "0 0 16px 16px", // Rounded bottom corners
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography
          variant="h6"
          component="h1"
          sx={{ fontWeight: "bold", marginBottom: "8px", width: "70%" }}
        >
          {user.gender[0]}
          {user.age}, {user.occupation}, {user.languages}, {user.distance},{" "}
          {user.relationship}
        </Typography>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            alignItems: "flex-end",
            width: "40%",
          }}
        >
          <Typography variant="body2">
            {user.attractiveness} - {user.height} - {user.weight}
          </Typography>
          <Typography variant="body2">
            {user.hairColor} ({user.hairLength}, {user.hairStyle})
          </Typography>
          <Typography variant="body2">{user.eyeColor} eyes</Typography>
          <Typography variant="body2">Body-Shape: {user.bodyShape}</Typography>
        </Box>
      </Box>
      <Typography variant="body2" sx={{ marginBottom: "4px" }}>
        Chat-Date on {user.chatDate}
      </Typography>
    </Box>
  );
};

export default ProfileHeader;
