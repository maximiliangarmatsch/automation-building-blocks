import { useState, useEffect } from "react";
import { debounce } from "@mui/material";

export const useMobile = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const updateSize = () => {
      setIsMobile(window.innerWidth < 1024);
    };
    window.addEventListener("resize", debounce(updateSize, 250));
    updateSize();
    return () => window.removeEventListener("resize", updateSize);
  }, []);

  return isMobile;
};
