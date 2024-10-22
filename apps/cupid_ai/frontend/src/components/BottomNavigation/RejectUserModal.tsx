import Typography from "@mui/material/Typography";
import { CustomModal } from "../CustomModal";

interface RejectUserModalProps {
  onClose: () => void;
  open: boolean;
}

export function RejectUserModal(props: RejectUserModalProps) {
  const { onClose, open } = props;

  return (
    <>
      <CustomModal
        open={open}
        onClose={onClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <>
          <Typography
            id="modal-modal-title"
            variant="h6"
            component="h1"
            sx={{ mb: 2 }}
          >
            Reject User
          </Typography>
        </>
      </CustomModal>
    </>
  );
}
