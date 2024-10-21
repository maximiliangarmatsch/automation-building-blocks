import { ModalProps } from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { AttractivenessForm } from "./forms/AttractivenessForm";
import { useState } from "react";
import { QuestionForm } from "./forms/QuestionsForm";
import { CustomModal } from "./CustomModal";

interface AttractivenessModalProps extends Omit<ModalProps, "children"> {
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

export const AttractivenessModal = (props: AttractivenessModalProps) => {
  const { onClose, open, setOpen } = props;

  const [step, setStep] = useState(1);
  const [data, setData] = useState<Record<string, any>>({});

  return (
    <CustomModal
      open={open}
      onClose={onClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <>
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
      </>
    </CustomModal>
  );
};
