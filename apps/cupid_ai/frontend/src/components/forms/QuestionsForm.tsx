import { useForm } from "react-hook-form";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import TextField from "@mui/material/TextField";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import LinearProgress from "@mui/material/LinearProgress";
import Checkbox from "@mui/material/Checkbox";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import api, { API_ENDPOINTS } from "../../services/api";
import { useAuth } from "../../utils/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../utils";
import { useState } from "react";
import questions from "../../data/questions.json";

export const QuestionForm = ({ data }) => {
  const { handleSubmit, formState, register, setValue, getValues } = useForm({
    defaultValues: data,
  });

  const [currentStep, setCurrentStep] = useState(0);
  const auth = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (payload) => {
    const createProfileResponse = await api.post(
      API_ENDPOINTS.CREATE_PROFILE,
      payload
    );

    if (createProfileResponse.data?.profile_id) {
      auth?.setUser && auth.setUser(data);
      navigate(PATHS.PROFILE);
    }
  };

  const handleNext = () => {
    setCurrentStep((prev) => Math.min(prev + 1, questions.length - 1));
  };

  const handleBack = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0));
  };

  const progress = (currentStep / (questions.length - 1)) * 100;

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <LinearProgress
        variant="determinate"
        value={progress}
        sx={{ marginBottom: 2 }}
      />

      {questions[currentStep].fields.map((field) => {
        switch (field.type) {
          case "text":
            return (
              <TextField
                key={field.id}
                fullWidth
                className="mt-2"
                id={field.id}
                label={field.label}
                {...register(field.id, { required: field.required })}
                sx={{ marginTop: 2 }}
              />
            );

          case "radio":
            return (
              <div key={field.id}>
                <label>{field.label}</label>
                <RadioGroup
                  {...register(field.id, { required: field.required })}
                >
                  {field.options?.map((option) => (
                    <FormControlLabel
                      key={option.value}
                      value={option.value}
                      control={<Radio />}
                      label={option.label}
                    />
                  ))}
                </RadioGroup>
              </div>
            );

          case "checkbox":
            return (
              <div key={field.id}>
                <label>{field.label}</label>
                {field.options?.map((option) => (
                  <FormControlLabel
                    key={option.value}
                    control={
                      <Checkbox
                        {...register(field.id)}
                        value={option.value}
                        onChange={({ target }) => {
                          const selectedValues = getValues(field.id) || [];
                          if (target.checked) {
                            setValue(field.id, [
                              ...selectedValues,
                              option.value,
                            ]);
                          } else {
                            setValue(
                              field.id,
                              selectedValues.filter(
                                (val) => val !== option.value
                              )
                            );
                          }
                        }}
                      />
                    }
                    label={option.label}
                  />
                ))}
              </div>
            );

          case "select":
            return (
              <Select
                key={field.id}
                fullWidth
                className="mt-2"
                id={field.id}
                label={field.label}
                {...register(field.id, { required: field.required })}
                sx={{ marginTop: 2 }}
              >
                {field.options?.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            );

          default:
            return null;
        }
      })}

      <div>
        {currentStep > 0 && (
          <Button
            onClick={handleBack}
            variant="outlined"
            style={{ marginTop: "20px", marginRight: "20px" }}
          >
            Back
          </Button>
        )}
        {currentStep < questions.length - 1 ? (
          <Button
            type="button"
            onClick={handleNext}
            variant="contained"
            style={{ marginTop: "20px" }}
          >
            Next
          </Button>
        ) : (
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
        )}
      </div>
    </form>
  );
};
