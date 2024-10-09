import { useContext, createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../utils";
import api, { API_ENDPOINTS, BASE_API } from "../../services/api";

const AuthContext = createContext<{
  user: any;
  uniqueID: string;
  loginAction: (data: any, callback: () => void) => void;
  logOut: () => void;
  setUser: React.Dispatch<React.SetStateAction<any>>;
} | null>(null);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [uniqueID, setUniqueID] = useState(
    localStorage.getItem("unique_id") || ""
  );
  const navigate = useNavigate();
  const loginAction = async (data, callback) => {
    try {
      const authResponse = await api.post(API_ENDPOINTS.AUTH, data);

      if (authResponse.data) {
        localStorage.setItem("unique_id", authResponse.data?.unique_id);
        setUniqueID(authResponse.data?.unique_id ?? "");

        // get user profile and store in state
        if (authResponse.data.unique_id) {
          try {
            const response = await api.post(API_ENDPOINTS.GET_PROFILE, {
              unique_id: authResponse.data?.unique_id,
            });

            if (response.data) {
              setUser(response.data);
              navigate(PATHS.PROFILE);
            }
          } catch (err) {
            callback();
          }
        }
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
    <AuthContext.Provider
      value={{ uniqueID, user, loginAction, logOut, setUser }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};
