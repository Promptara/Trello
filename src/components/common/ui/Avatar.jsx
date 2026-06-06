import { useContext } from 'react';
import { AppContext } from '../../../context/AppContext';

const Avatar = ({ userId, size = 28, showRing = false }) => {
  const { data } = useContext(AppContext);
  const user = (data.users || []).find((u) => u.id === userId);
  if (!user) return null;
  return (
    <div
      className="rounded-full flex items-center justify-center font-bold select-none shrink-0"
      style={{
        width: size,
        height: size,
        background: user.color,
        color: '#fff',
        fontSize: Math.round(size * 0.36),
        border: showRing ? '2.5px solid white' : 'none',
        letterSpacing: '-0.3px',
      }}
      title={user.name}
    >
      {user.initials}
    </div>
  );
};

export default Avatar;
