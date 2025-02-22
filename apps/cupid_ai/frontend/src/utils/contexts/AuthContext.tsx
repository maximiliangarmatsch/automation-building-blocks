import React, {
  useContext,
  createContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../utils";
import api, { API_ENDPOINTS } from "../../services/api";

type User = Record<string, any>;

interface AuthContextType {
  user: User | null;
  uniqueID: string;
  loginAction: (data: LoginData, callback: () => void) => Promise<void>;
  logOut: () => void;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

interface LoginData {
  email: string;
  password: string;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [uniqueID, setUniqueID] = useState(
    localStorage.getItem("unique_id") || ""
  );
  const navigate = useNavigate();

  const loginAction = useCallback(
    async (data: LoginData, callback: () => void) => {
      try {
        const authResponse = await api.post(API_ENDPOINTS.AUTH, data);

        if (authResponse.data) {
          localStorage.setItem("unique_id", authResponse.data.unique_id);
          setUniqueID(authResponse.data.unique_id ?? "");

          if (authResponse.data.unique_id) {
            const response = await api.post(API_ENDPOINTS.GET_PROFILE, {
              unique_id: authResponse.data.unique_id,
            });

            if (response.data) {
              setUser(response.data);
              navigate(PATHS.MATCHES);
            }
          }
        } else {
          throw new Error(
            authResponse.data?.message || "Authentication failed"
          );
        }
      } catch (err) {
        console.error(err);
        callback();
      }
    },
    [navigate]
  );

  useEffect(() => {
    // fetch the user when uniqueid is present and user
    const fetchUser = async () => {
      const _uniqueID = localStorage.getItem("unique_id");
      if (!user && _uniqueID) {
        try {
          const response = await api.post(API_ENDPOINTS.GET_PROFILE, {
            unique_id: _uniqueID,
          });

          if (response.data) {
            setUser(response.data);
            navigate(PATHS.MATCHES);
          }
        } catch (err) {
          // do nothing
        }
      }
    };

    fetchUser();
  }, []);

  const logOut = useCallback(() => {
    setUser(null);
    setUniqueID("");
    localStorage.removeItem("unique_id");
    navigate(PATHS.LOGIN);
  }, [navigate]);

  const value = {
    uniqueID,
    user,
    loginAction,
    logOut,
    setUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
