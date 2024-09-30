import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../utils/contexts/AuthContext";
import { isLocalhost } from "../utils";

const PrivateRoute = () => {
  const auth = useAuth();

  if (!auth?.uniqueID && !isLocalhost) return <Navigate to="/login" />;
  return <Outlet />;
};

export default PrivateRoute;
