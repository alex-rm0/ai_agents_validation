import React from 'react';

interface Props {
  children: React.ReactNode;
}

const LoginPage: React.FC<Props> = ({ children }) => {
  return (
    <div className="login-page">
      <header className="login-header">
        <h1>Login</h1>
      </header>
      <main className="login-main">
        {children}
      </main>
      <footer className="login-footer">
        <p>&copy; 2023</p>
      </footer>
    </div>
  );
};

export default LoginPage;