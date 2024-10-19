import Box from "@mui/material/Box";
import Modal, { ModalProps } from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { AttractivenessForm } from "./forms/AttractivenessForm";
import { useState } from "react";
import { QuestionForm } from "./forms/QuestionsForm";

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: {
    xs: "calc(100% - 20px)",
    sm: 400,
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

interface AttractivenessModalProps extends Omit<ModalProps, "children"> {
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

export const AttractivenessModal = (props: AttractivenessModalProps) => {
  const { onClose, open, setOpen } = props;

  const [step, setStep] = useState(1);
  const [data, setData] = useState<Record<string, any>>({});

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <div className="flex justify-between items-center mb-3">
          <Typography id="modal-modal-title" variant="h6" component="h1">
            Attractiveness
          </Typography>
          <IconButton onClick={() => setOpen(false)}>
            <CloseIcon />
          </IconButton>
        </div>

        {step === 1 ? (
          <AttractivenessForm setData={setData} setStep={setStep} />
        ) : (
          <QuestionForm data={data} />
        )}
      </Box>
    </Modal>
  );
};
