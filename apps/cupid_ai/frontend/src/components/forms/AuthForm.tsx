import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import * as Yup from "yup";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";

import { PATHS } from "../../utils";
import { useAuth } from "../../utils/contexts/AuthContext";
import useYupValidationResolver from "../../utils/hooks/useYupValidationResolver";
import { AttractivenessModal } from "../AttractivenessModal";

const formValidationSchema = Yup.object({
  email: Yup.string()
    .email("Enter a valid email")
    .required("Email is required"),
  password: Yup.string()
    .min(6, "Password should be of minimum 6 characters length")
    .required("Password is required"),
});

interface AuthFormProps {
  type?: "register" | "login";
}

export function AuthForm({ type = "login" }: AuthFormProps) {
  const [showUploadMedia, setShowUploadMedia] = useState(true);

  const auth = useAuth();
  const onSubmit = async (values) => {
    if (auth?.loginAction) {
      await auth?.loginAction(values, () => {
        setShowUploadMedia(true);
      });
    }
  };

  const isRegister = useMemo(() => {
    return type === "register";
  }, [type]);

  const resolver = useYupValidationResolver(formValidationSchema);
  const { register, handleSubmit, formState } = useForm({
    resolver,
    defaultValues: {
      email: "",
      password: "",
    },
  });

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Typography variant="h4">
          {isRegister ? "Register" : "Login"}
        </Typography>
        <TextField
          fullWidth
          className="mt-2"
          id="email"
          label="Email"
          {...register("email", { required: true })}
          sx={{
            marginTop: 2,
          }}
        />

        <TextField
          fullWidth
          id="password"
          label="Password"
          type="password"
          {...register("password")}
          sx={{
            marginTop: 2,
          }}
        />

        <Box
          display="flex"
          alignItems="center"
          justifyContent="space-between"
          marginTop={5}
        >
          <Button
            size="large"
            color="primary"
            variant="contained"
            type="submit"
            disabled={formState.isSubmitting}
          >
            {isRegister ? "Register" : "Login"}
            {formState.isSubmitting && (
              <CircularProgress style={{ marginLeft: "20px" }} size="20px" />
            )}
          </Button>
          <Button>
            <Link to={isRegister ? PATHS.LOGIN : PATHS.REGISTER}>
              {isRegister ? "Login" : "Register"}
            </Link>
          </Button>
        </Box>
      </form>
      <AttractivenessModal
        open={showUploadMedia}
        setOpen={setShowUploadMedia}
        onClose={() => setShowUploadMedia(false)}
      />
    </>
  );
}
