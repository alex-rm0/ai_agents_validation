import React, { useState } from 'react';

interface Props {
  password: string;
}

const PasswordToggle: React.FC<Props> = ({ password }) => {
  const [showPassword, setShowPassword] = useState(false);

  const handleClick = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div>
      <input
        type={showPassword ? 'text' : 'password'}
        value={password}
        readOnly
      />
      <button onClick={handleClick}>
        {showPassword ? 'Esconder' : 'Mostrar'}
      </button>
    </div>
  );
};

export default PasswordToggle;