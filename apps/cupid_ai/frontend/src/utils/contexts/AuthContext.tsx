import React, { useContext, createContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { PATHS } from "../../utils";
import api, { API_ENDPOINTS } from "../../services/api";

type User = Record<string, any>;

interface AuthContextType {
  user: User | null;
  uniqueID: string;
  loginAction: (data: LoginData, callback: () => void) => Promise<void>;
  logOut: () => void;
  deleteProfile: () => Promise<void>;
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
              navigate(PATHS.PROFILE);
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

  const logOut = useCallback(() => {
    setUser(null);
    setUniqueID("");
    localStorage.removeItem("unique_id");
    navigate(PATHS.LOGIN);
  }, [navigate]);

  const deleteProfile = useCallback(async () => {
    if (user) {
      const response = await api.delete(API_ENDPOINTS.DELETE_PROFILE, {
        data: {
          email: user?.email,
        },
      });

      if (response.data) {
        setUniqueID("");
        localStorage.removeItem("unique_id");
        setUser(null);
      }
    }
  }, [user, logOut]);

  const value = {
    uniqueID,
    user,
    loginAction,
    logOut,
    deleteProfile,
    setUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
