import { ICON_PATHS } from '../../../constants';

const Icon = ({ name, size = 18, color = 'currentColor', strokeWidth = 1.8 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={strokeWidth}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {(ICON_PATHS[name] || '').split(' M').map((p, i) => (
      <path key={i} d={i === 0 ? p : 'M' + p} />
    ))}
  </svg>
);

export default Icon;
