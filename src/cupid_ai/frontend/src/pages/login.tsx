import { AuthForm } from "../components/forms/AuthForm";

export const Login = () => {
  return (
    <div className="flex items-center justify-center h-[85vh]">
      <div className="w-full flex flex-col items-center mx-auto md:px-8 lg:px-16 xl:px-[92px]">
        <div className="w-full h-full">
          <AuthForm />
        </div>
      </div>
    </div>
  );
};
