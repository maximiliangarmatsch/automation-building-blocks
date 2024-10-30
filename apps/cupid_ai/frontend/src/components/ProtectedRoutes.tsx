import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../utils/contexts/AuthContext";
import { isLocalhost } from "../utils";

interface PrivateRouteInterface {
  withUserProfile?: boolean;
}

const PrivateRoute = ({ withUserProfile = true }: PrivateRouteInterface) => {
  const auth = useAuth();

  const protection = withUserProfile ? auth?.user : auth?.uniqueID;

  if (!protection && !isLocalhost) return <Navigate to="/login" />;
  return <Outlet />;
};

export default PrivateRoute;
