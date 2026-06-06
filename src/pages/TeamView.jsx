// PROMPTARA — Team View
import { useContext } from 'react';
import { AppContext } from '../context/AppContext';

const TeamView = () => {
  const { data } = useContext(AppContext);
  return (
    <div className="p-6 overflow-y-auto h-full">
      <h2 className="text-lg font-extrabold text-ink tracking-[-0.4px] mb-1.5">
        Tim
      </h2>
      <p className="text-xs mb-5" style={{ color: '#9090AA' }}>
        Member aktif di workspace PROMPTARA
      </p>
      <div
        className="grid gap-3.5"
        style={{
          gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
        }}
      >
        {(data.users || []).map((u) => {
          const assigned = (data.cards || []).filter((c) =>
            c.assignees?.includes(u.id)
          ).length;
          const active = (data.cards || []).filter(
            (c) =>
              c.assignees?.includes(u.id) && c.columnId !== 'col5'
          ).length;
          return (
            <div
              key={u.id}
              className="bg-white rounded-[14px] p-5 flex flex-col gap-3"
              style={{ border: '1.5px solid #E5E4EF' }}
            >
              <div className="flex gap-3 items-center">
                <div
                  className="w-[46px] h-[46px] rounded-full shrink-0 flex items-center justify-center text-base font-extrabold text-white"
                  style={{ background: u.color }}
                >
                  {u.initials}
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">
                    {u.name}
                  </div>
                  <div
                    className="text-[11px] font-medium"
                    style={{ color: '#9090AA' }}
                  >
                    {u.role}
                  </div>
                </div>
              </div>
              <div
                className="text-[11px] bg-surface rounded-lg py-2 px-2.5"
                style={{ color: '#9090AA' }}
              >
                {u.email}
              </div>
              <div className="flex gap-2">
                <div className="flex-1 rounded-[9px] py-2 px-2.5 text-center bg-brand-light">
                  <div className="text-base font-extrabold text-brand">
                    {assigned}
                  </div>
                  <div
                    className="text-[10px] font-semibold"
                    style={{ color: '#9090AA' }}
                  >
                    Total
                  </div>
                </div>
                <div
                  className="flex-1 rounded-[9px] py-2 px-2.5 text-center"
                  style={{ background: '#FFF7ED' }}
                >
                  <div
                    className="text-base font-extrabold"
                    style={{ color: '#F97316' }}
                  >
                    {active}
                  </div>
                  <div
                    className="text-[10px] font-semibold"
                    style={{ color: '#9090AA' }}
                  >
                    Aktif
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TeamView;
