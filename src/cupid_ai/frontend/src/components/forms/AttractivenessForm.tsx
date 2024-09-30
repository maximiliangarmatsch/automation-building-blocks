import { useForm } from "react-hook-form";
import { Button, TextField, Typography } from "@mui/material";
import api, { API_ENDPOINTS } from "../../services/api";

export const AttractivenessForm = () => {
  const { register, handleSubmit, setValue } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      setValue("file", files[0]);
    }

    api.post(API_ENDPOINTS.ATTRACTIVENESS, {
      file: files[0],
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Typography variant="h6">Upload Your File</Typography>

      <input
        type="file"
        {...register("file")}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />
      <label>
        <Button
          variant="contained"
          component="span"
          onClick={() => {
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput instanceof HTMLInputElement) {
              fileInput.click();
            }
          }}
        >
          Choose File
        </Button>
      </label>

      <Button type="submit" variant="contained" style={{ marginTop: "20px" }}>
        Submit
      </Button>
    </form>
  );
};
