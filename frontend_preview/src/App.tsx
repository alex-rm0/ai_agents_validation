import React from "react";
import LoginForm from "./generated/ImplementarFormulárioLoginCamposEmailPasswordComponent";
import EmailValidator from "./generated/ImplementarValidaçãoEmailComponent";
import PasswordToggle from "./generated/ImplementarBotãoMostrarPasswordComponent";
import PasswordResetLink from "./generated/ImplementarLinkRecuperaçãoPasswordComponent";

function App() {
  const handlePasswordReset = (password: string) => {
    console.log("Password reset:", password);
    alert("Password reset solicitado");
  };

  return (
    <div style={{ maxWidth: 400, margin: "60px auto", fontFamily: "sans-serif" }}>
      <h1>PM Agent - Frontend Preview</h1>
      <h2>Login</h2>
      <LoginForm />
      <hr />
      <h3>Validação de Email</h3>
      <EmailValidator
        email=""
        onValid={(v) => console.log("valid", v)}
        onError={(e) => console.log("error", e)}
      />
      <hr />
      <h3>Mostrar/Esconder Password</h3>
      <PasswordToggle password="exemplo123" />
      <hr />
      <h3>Recuperar Password</h3>
      <PasswordResetLink onPasswordReset={handlePasswordReset} />
    </div>
  );
}

export default App;
