import { AuthForm } from "../components/AuthForm";

export const Register = () => {
  return (
    <div className="flex items-center justify-center h-[85vh]">
      <div className="w-full flex flex-col items-center mx-auto md:px-8 lg:px-16 xl:px-[92px]">
        <div className="w-full h-full">
          <AuthForm type="register" />
        </div>
      </div>
    </div>
  );
};
