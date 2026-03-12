// EmailValidator.tsx
import React, { useState } from 'react';

interface Props {
  email: string;
  onValid: (isValid: boolean) => void;
  onError: (error: string) => void;
}

const EmailValidator: React.FC<Props> = ({ email, onValid, onError }) => {
  const [isValid, setIsValid] = useState(false);
  const [error, setError] = useState('');

  const validateEmail = () => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (emailRegex.test(email)) {
      setIsValid(true);
      setError('');
      onValid(true);
    } else {
      setIsValid(false);
      setError('Email inválido. Por favor, insira um email válido.');
      onValid(false);
    }
  };

  return (
    <div>
      <input
        type="email"
        value={email}
        onChange={(e) => {
          setError('');
          setIsValid(false);
          onValid(false);
        }}
      />
      <button onClick={validateEmail}>Validar Email</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
};

export default EmailValidator;