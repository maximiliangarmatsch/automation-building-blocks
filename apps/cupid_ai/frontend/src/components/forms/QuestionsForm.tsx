import { useForm, FieldValues } from "react-hook-form";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import LinearProgress from "@mui/material/LinearProgress";
import Checkbox from "@mui/material/Checkbox";
import MenuItem from "@mui/material/MenuItem";
import api, { API_ENDPOINTS } from "../../services/api";
import { useAuth } from "../../utils/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../utils";
import { useState, useEffect } from "react";
import questions from "../../data/questions.json";
import FormLabel from "@mui/material/FormControl";
import FormHelperText from "@mui/material/FormHelperText";

export const QuestionForm = ({ data }) => {
  const [formData, setFormData] = useState(data);

  const {
    handleSubmit,
    formState,
    formState: { errors },
    register,
    setValue,
    getValues,
    trigger,
  } = useForm({
    defaultValues: formData,
  });

  const [currentStep, setCurrentStep] = useState(0);
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Update react-hook-form values when formData changes
    Object.entries(formData).forEach(([key, value]) => {
      setValue(key, value);
    });
  }, [formData, setValue]);

  const handleFieldChange = (fieldId, value) => {
    setFormData((prevData) => ({
      ...prevData,
      [fieldId]: value,
    }));
    setValue(fieldId, value); // Add this line to update react-hook-form
    trigger(fieldId);
  };

  const onSubmit = async (payload) => {
    const formattedPayload = {
      ...payload,
      height: Number(payload.height),
      weight: Number(payload.weight),
      age: Number(payload.age),
      kids: Number(payload.kids),
    };

    const createProfileResponse = await api.post(
      API_ENDPOINTS.CREATE_PROFILE,
      formattedPayload
    );

    if (createProfileResponse.data?.profile_id) {
      auth?.setUser && auth.setUser(data);
      navigate(PATHS.PROFILE);
    }
  };

  const handleNext = async () => {
    const currentFields = questions[currentStep].fields;
    const isStepValid = await trigger(currentFields.map((field) => field.id));

    if (isStepValid) {
      setCurrentStep((prev) => Math.min(prev + 1, questions.length - 1));
    }
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
              <Box key={field.id} sx={{ marginBottom: 2 }}>
                <TextField
                  fullWidth
                  id={field.id}
                  label={field.label}
                  value={formData[field.id] || ""}
                  {...register(field.id, {
                    required: field.required,
                    onChange: (e) => {
                      handleFieldChange(field.id, e.target.value);
                    },
                  })}
                  error={!!errors[field.id]}
                />
                {errors[field.id] && (
                  <FormHelperText error>
                    {field.label} is required
                  </FormHelperText>
                )}
              </Box>
            );

          case "radio":
            return (
              <Box key={field.id} sx={{ marginBottom: 2 }}>
                <FormLabel sx={{ marginBottom: 1 }}>{field.label}</FormLabel>
                <RadioGroup
                  value={formData[field.id] || ""}
                  onChange={(e) => handleFieldChange(field.id, e.target.value)}
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
                <input
                  type="hidden"
                  {...register(field.id, {
                    required: field.required
                      ? `${field.label} is required`
                      : false,
                  })}
                />
                {errors[field.id] && (
                  <FormHelperText error>
                    {errors[field.id]?.message as string}
                  </FormHelperText>
                )}
              </Box>
            );

          case "checkbox":
            return (
              <Box key={field.id} sx={{ marginBottom: 2 }}>
                <FormLabel sx={{ marginBottom: 1 }}>{field.label}</FormLabel>
                {field.options?.map((option) => (
                  <FormControlLabel
                    key={option.value}
                    control={
                      <Checkbox
                        checked={(formData[field.id] || []).includes(
                          option.value
                        )}
                        {...register(field.id, {
                          validate: (value) =>
                            !field.required ||
                            value.length > 0 ||
                            `${field.label} is required`,
                          onChange: ({ target }) => {
                            const selectedValues = formData[field.id] || [];
                            const newValues = target.checked
                              ? [...selectedValues, option.value]
                              : selectedValues.filter(
                                  (val) => val !== option.value
                                );
                            handleFieldChange(field.id, newValues);
                          },
                        })}
                        value={option.value}
                      />
                    }
                    label={option.label}
                  />
                ))}
                {errors[field.id] && (
                  <FormHelperText error>
                    {errors[field.id]?.message as string}
                  </FormHelperText>
                )}
              </Box>
            );

          case "select":
            return (
              <Box key={field.id} sx={{ marginBottom: 2 }}>
                <TextField
                  select
                  fullWidth
                  id={field.id}
                  label={field.label}
                  value={formData[field.id] || ""}
                  {...register(field.id, {
                    validate: (value) =>
                      !field.required ||
                      value !== "" ||
                      `${field.label} is required`,
                    onChange: (e) => {
                      handleFieldChange(field.id, e.target.value);
                    },
                  })}
                  error={!!errors[field.id]}
                >
                  {field.options?.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
                {errors[field.id] && (
                  <FormHelperText error>
                    {errors[field.id]?.message as string}
                  </FormHelperText>
                )}
              </Box>
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
            disabled={formState.isSubmitting}
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
