const Select = ({ label, value, onChange, options, required }) => (
  <div className="flex flex-col gap-[5px]">
    {label && (
      <label className="text-xs font-semibold text-[#5C5C7A] tracking-[0.3px]">
        {label}
        {required && <span className="text-red-500"> *</span>}
      </label>
    )}
    <select
      value={value}
      onChange={onChange}
      className="border border-line rounded-[10px] px-3 py-[10px] text-[13px] text-ink outline-none bg-[#FAFAF8] cursor-pointer"
      style={{ fontFamily: 'inherit' }}
    >
      {options.map((o) => (
        <option key={o.value} value={o.value}>
          {o.label}
        </option>
      ))}
    </select>
  </div>
);

export default Select;
