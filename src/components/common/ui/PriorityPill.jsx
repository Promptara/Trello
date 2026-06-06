import { PRIORITY } from '../../../constants';

const PriorityPill = ({ priority, small }) => {
  const p = PRIORITY[priority] || PRIORITY.low;
  return (
    <span
      className={`inline-flex items-center gap-1 font-semibold rounded-full whitespace-nowrap ${
        small
          ? 'text-[10px] px-[7px] py-[2px]'
          : 'text-[11px] px-[10px] py-[3px]'
      }`}
      style={{ background: p.bg, color: p.color }}
    >
      <span
        className="w-[5px] h-[5px] rounded-full shrink-0"
        style={{ background: p.color }}
      />
      {p.label}
    </span>
  );
};

export default PriorityPill;
