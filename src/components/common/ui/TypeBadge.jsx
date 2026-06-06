import { PROJECT_TYPES } from '../../../constants';

const TypeBadge = ({ type, small }) => {
  const t = PROJECT_TYPES[type] || PROJECT_TYPES.other;
  return (
    <span
      className={`font-semibold rounded-full whitespace-nowrap ${
        small
          ? 'text-[10px] px-[7px] py-[2px]'
          : 'text-[11px] px-[10px] py-[3px]'
      }`}
      style={{ background: t.bg, color: t.color }}
    >
      {t.label}
    </span>
  );
};

export default TypeBadge;
