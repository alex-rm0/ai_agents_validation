import React, { useState } from 'react';

interface Props {
  onPasswordReset: (password: string) => void;
}

const PasswordResetLink: React.FC<Props> = ({ onPasswordReset }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password)) {
      setError('Password must contain at least one uppercase letter, one lowercase letter, one number and one special character');
      return;
    }
    onPasswordReset(password);
  };

  return (
    <div>
      <h2>Recuperar Senha</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Nova Senha:
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
        </label>
        <button type="submit">Enviar</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default PasswordResetLink;