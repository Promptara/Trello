import { useEffect } from 'react';

const Modal = ({ open, onClose, children, width = 560 }) => {
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-[1000] flex items-center justify-center p-5"
      style={{
        background: 'rgba(23,23,46,0.45)',
        backdropFilter: 'blur(3px)',
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        className="bg-white rounded-[18px] w-full overflow-y-auto relative"
        style={{
          maxWidth: width,
          maxHeight: '92vh',
          boxShadow: '0 24px 64px rgba(0,0,0,0.18)',
        }}
      >
        {children}
      </div>
    </div>
  );
};

export default Modal;
