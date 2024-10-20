import { useForm } from "react-hook-form";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import AddIcon from "@mui/icons-material/Add";
import { useState } from "react";
import api, { API_ENDPOINTS } from "../../services/api";
import { useAuth } from "../../utils/contexts/AuthContext";
import { useNavigate } from "react-router-dom";

interface AttractivenessFormProps {
  setData: React.Dispatch<React.SetStateAction<any>>;
  setStep: React.Dispatch<React.SetStateAction<number>>;
}

export const AttractivenessForm = (props: AttractivenessFormProps) => {
  const { setData, setStep } = props;

  const { handleSubmit, setValue, formState } = useForm();
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const auth = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const createProfilePayload = {
      unique_id: auth?.uniqueID,
      attractiveness: 0,
      relationship_type: "",
      family_planning: "",
      living_address: "",
      apartment_style: "",
      roommates: 0,
      working_hours: "",
      other_commitments: "",
      dating_availability: "",
      height: 0,
      weight: 0,
      age: 0,
      gender: "",
      eye_color: "",
      eye_type: "",
      hair_color: "",
      hair_length: "",
      hair_style: "",
      nose: "",
      facial_form: "",
      cheekbones: "",
      eyebrows: "",
      dept: "",
      assets: "",
      income_this_year: 0,
      income_next_year: 0,
      income_over_next_year: 0,
      wealth_goals: "",
      kids: 0,
      pets: "",
      living: "",
      wealth_splitting: "",
      effort_splitting: "",
      religion: "",
      politics: "",
      existing_family_structure: "",
      retirement: "",
      q1: "",
      q2: "",
      q3: "",
      q4: "",
      q5: "",
      q6: "",
      q7: "",
      q8: "",
      q9: "",
      q10: "",
    };

    const formData = new FormData();
    formData.append("file", data.file);

    const response = await api.post(API_ENDPOINTS.ATTRACTIVENESS, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (response.data.attractiveness_score) {
      createProfilePayload.attractiveness = response.data.attractiveness_score;
    }

    const extraFeatureReponse = await api.post(
      API_ENDPOINTS.EXTRACT_FEATURES,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    if (extraFeatureReponse?.data) {
      createProfilePayload.cheekbones = extraFeatureReponse?.data?.Cheekbones;
      createProfilePayload.eye_color = extraFeatureReponse?.data?.EyeColor;
      createProfilePayload.eye_type = extraFeatureReponse?.data?.EyeType;
      createProfilePayload.eyebrows = extraFeatureReponse?.data?.Eyebrows;
      createProfilePayload.facial_form = extraFeatureReponse?.data?.FacialForm;
      createProfilePayload.gender = extraFeatureReponse?.data?.Gender;
      createProfilePayload.hair_color = extraFeatureReponse?.data?.HairColor;
      createProfilePayload.hair_length = extraFeatureReponse?.data?.HairLength;
      createProfilePayload.hair_style = extraFeatureReponse?.data?.HairStyle;
      createProfilePayload.nose = extraFeatureReponse?.data?.Nose;
    }

    setData(createProfilePayload);
    setStep(2);
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      setSelectedFile(URL.createObjectURL(file)); // Set the file URL
      setValue("file", file);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Typography variant="h6">Upload your picture</Typography>

      <input
        type="file"
        onChange={handleFileChange}
        style={{ display: "none" }}
      />
      <label>
        <Box
          onClick={() => {
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput instanceof HTMLInputElement) {
              fileInput.click();
            }
          }}
          sx={{
            width: "100%",
            height: 400,
            margin: "auto",
            border: "0.5px dashed gray",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            position: "relative",
            background: selectedFile ? `url(${selectedFile})` : "#f0f0f0",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          {!selectedFile ? (
            <AddIcon fontSize="large" />
          ) : (
            <Typography color="primary">Change Image</Typography>
          )}
        </Box>
      </label>

      <Button
        type="submit"
        variant="contained"
        style={{ marginTop: "20px" }}
        disabled={formState.isSubmitting}
      >
        Submit
        {formState.isSubmitting && (
          <CircularProgress style={{ marginLeft: "20px" }} size="20px" />
        )}
      </Button>
    </form>
  );
};
