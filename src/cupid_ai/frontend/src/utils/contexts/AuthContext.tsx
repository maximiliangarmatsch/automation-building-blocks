import { useContext, createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../utils";
import api, { API_ENDPOINTS, BASE_API } from "../../services/api";

const AuthContext = createContext<{
  user: any;
  uniqueID: string;
  loginAction: (data: any) => void;
  logOut: () => void;
} | null>(null);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [uniqueID, setUniqueID] = useState(
    localStorage.getItem("unique_id") || ""
  );
  const navigate = useNavigate();
  const loginAction = async (data) => {
    try {
      const authResponse = await api.post(API_ENDPOINTS.AUTH, data);

      if (authResponse.data) {
        localStorage.setItem("unique_id", authResponse.data?.unique_id);
        setUniqueID(authResponse.data?.unique_id ?? "");

        // get user profile and store in state
        if (authResponse.data.unique_id) {
          console.log("running");

          // TODO - fetch profile then set profile with setUser()
        }

        navigate(PATHS.PROFILE);
        return;
      }
      throw new Error(authResponse.data?.message);
    } catch (err) {
      console.error(err);
    }
  };

  const logOut = () => {
    setUser(null);
    setUniqueID("");
    localStorage.removeItem("unique_id");
    navigate(PATHS.LOGIN);
  };

  return (
    <AuthContext.Provider value={{ uniqueID, user, loginAction, logOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};
