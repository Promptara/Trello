import { useState } from 'react';

const Btn = ({
  children,
  onClick,
  variant = 'primary',
  small,
  danger,
  disabled,
  type = 'button',
  style: s,
}) => {
  const [hov, setHov] = useState(false);

  const sizeClass = small
    ? 'text-xs px-3 py-[6px]'
    : 'text-sm px-[18px] py-[9px]';

  const variants = {
    primary: { background: hov ? '#2AA0A0' : '#3EB8B8', color: '#fff' },
    secondary: { background: hov ? '#EDECF4' : '#F0EFF8', color: '#17172E' },
    ghost: { background: hov ? '#F0EFF8' : 'transparent', color: '#5C5C7A' },
    danger: { background: hov ? '#dc2626' : '#EF4444', color: '#fff' },
  };
  const v = danger ? variants.danger : variants[variant] || variants.primary;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-1.5 border-none rounded-[10px] font-semibold transition-all select-none ${sizeClass} ${
        disabled ? 'opacity-55 cursor-default' : 'cursor-pointer'
      }`}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{ fontFamily: 'inherit', ...v, ...(s || {}) }}
    >
      {children}
    </button>
  );
};

export default Btn;
