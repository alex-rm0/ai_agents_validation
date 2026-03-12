import React, { useState } from "react";

import LoginPage from "./generated/DesenvolverEstruturaPáginaLoginComponent";
import EmailInput from "./generated/ImplementarValidaçãoEmailComponent";
import PasswordToggle from "./generated/AdicionarBotãoMostrarPasswordComponent";
import ForgotPasswordLink from "./generated/IncluirLinkRecuperaçãoPasswordComponent";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    console.log("Login attempt:", { email, password });
    alert(`Login com ${email}`);
  };

  const handleForgotPassword = () => {
    alert("Fluxo de recuperação de password");
  };

  return (
    <LoginPage onLogin={() => handleLogin()}>
      <EmailInput value={email} onChange={setEmail} />

      <PasswordToggle password={password} setPassword={setPassword} />

      <br />

      <button onClick={handleLogin}>Login</button>

      <br />

      <ForgotPasswordLink onForgotPasswordClick={handleForgotPassword} />
    </LoginPage>
  );
}

export default App;