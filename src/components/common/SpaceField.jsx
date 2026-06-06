import { useMemo } from 'react';
import Icon from './ui/Icon';

const SpaceField = () => {
  const stars = useMemo(() => {
    let s = 0x9e3779b9 | 0;
    const r = () => {
      s ^= s << 13;
      s ^= s >> 17;
      s ^= s << 5;
      return (s >>> 0) / 0xffffffff;
    };
    return Array.from({ length: 180 }, () => ({
      x: r() * 100,
      y: r() * 100,
      size: 0.5 + r() * 1.6,
      o: 0.1 + r() * 0.75,
      twinkle: r() > 0.82,
      drift: r() > 0.94,
      dur: 2.5 + r() * 6,
      driftDur: 8 + r() * 14,
      delay: r() * 5,
    }));
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      <div
        className="absolute"
        style={{
          top: '-25%',
          right: '-20%',
          width: '65%',
          height: '65%',
          borderRadius: '50%',
          background:
            'radial-gradient(circle, rgba(62,184,184,0.09) 0%, transparent 62%)',
        }}
      />
      <div
        className="absolute"
        style={{
          bottom: '-10%',
          left: '-15%',
          width: '55%',
          height: '55%',
          borderRadius: '50%',
          background:
            'radial-gradient(circle, rgba(99,102,241,0.06) 0%, transparent 62%)',
        }}
      />
      <div
        className="absolute"
        style={{
          top: '20%',
          left: '-10%',
          right: '-10%',
          height: '35%',
          background:
            'linear-gradient(160deg, transparent 0%, rgba(255,255,255,0.012) 35%, rgba(200,220,255,0.018) 55%, transparent 100%)',
          transform: 'rotate(-12deg)',
          transformOrigin: 'center',
        }}
      />
      {stars.map((st, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${st.x}%`,
            top: `${st.y}%`,
            width: `${st.size}px`,
            height: `${st.size}px`,
            borderRadius: '50%',
            background: '#fff',
            opacity: st.o,
            '--so': st.o,
            animation: [
              st.twinkle
                ? `twinkle ${st.dur}s ${st.delay}s ease-in-out infinite`
                : '',
              st.drift
                ? `slowdrift ${st.driftDur}s ${st.delay}s ease-in-out infinite`
                : '',
            ]
              .filter(Boolean)
              .join(', ') || 'none',
            boxShadow:
              st.size > 1.5
                ? `0 0 ${st.size * 2}px rgba(255,255,255,0.4)`
                : 'none',
          }}
        />
      ))}
    </div>
  );
};

export default SpaceField;
