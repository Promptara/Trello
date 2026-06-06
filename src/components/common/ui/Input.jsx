const Input = ({
  label,
  value,
  onChange,
  placeholder,
  type = 'text',
  multiline,
  rows = 3,
  required,
  style: s,
}) => (
  <div className="flex flex-col gap-[5px]">
    {label && (
      <label className="text-xs font-semibold text-[#5C5C7A] tracking-[0.3px]">
        {label}
        {required && <span className="text-red-500"> *</span>}
      </label>
    )}
    {multiline ? (
      <textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        className="border border-line rounded-[10px] px-3 py-[10px] text-[13px] text-ink resize-y outline-none transition-colors bg-[#FAFAF8]"
        style={{ fontFamily: 'inherit', ...s }}
      />
    ) : (
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="border border-line rounded-[10px] px-3 py-[10px] text-[13px] text-ink outline-none transition-colors bg-[#FAFAF8]"
        style={{ fontFamily: 'inherit', ...s }}
      />
    )}
  </div>
);

export default Input;
