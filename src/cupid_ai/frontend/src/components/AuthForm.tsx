import { Box, Button, TextField, Typography } from "@mui/material";
import { Formik } from "formik";
import * as Yup from "yup";
import api, { API_ENDPOINTS } from "../services/api";
import { useMemo } from "react";
import { Link } from "react-router-dom";
import { PATHS } from "../utils";

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
  const onSubmit = async (values) => {
    const { data } = await api.post(API_ENDPOINTS.AUTH, values);

    console.log(data);
  };

  const isRegister = useMemo(() => {
    return type === "register";
  }, [type]);

  return (
    <Formik
      initialValues={{ email: "", password: "" }}
      validationSchema={formValidationSchema}
      onSubmit={onSubmit}
    >
      {({
        values,
        handleChange,
        handleBlur,
        touched,
        errors,
        handleSubmit,
      }) => (
        <form onSubmit={handleSubmit}>
          <Typography variant="h4">
            {isRegister ? "Register" : "Login"}
          </Typography>
          <TextField
            fullWidth
            className="mt-2"
            id="email"
            name="email"
            label="Email"
            value={values.email}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.email && Boolean(errors.email)}
            helperText={touched.email && errors.email}
            sx={{
              marginTop: 2,
            }}
          />

          <TextField
            fullWidth
            id="password"
            name="password"
            label="Password"
            type="password"
            value={values.password}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.password && Boolean(errors.password)}
            helperText={touched.password && errors.password}
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
            >
              {isRegister ? "Register" : "Login"}
            </Button>
            <Button>
              <Link to={isRegister ? PATHS.LOGIN : PATHS.REGISTER}>
                {isRegister ? "Login" : "Register"}
              </Link>
            </Button>
          </Box>
        </form>
      )}
    </Formik>
  );
}
