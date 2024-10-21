import Box from "@mui/material/Box";
import Modal, { ModalProps } from "@mui/material/Modal";

interface CustomModalProps extends ModalProps {}

export const CustomModal = (props: CustomModalProps) => {
  const { children, ...rest } = props;

  const style = {
    position: "absolute" as "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: {
      xs: "calc(100% - 20px)",
      sm: 600,
    },
    height: {
      xs: "calc(100% - 20px)",
      sm: "auto",
    },
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
  };

  return (
    <Modal {...rest}>
      <Box sx={style}>{children}</Box>
    </Modal>
  );
};
